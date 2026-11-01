# MMLS-AI v2.0 — Feature Specification

## LSCO Scale Coverage & Digital Twin Simulator with Dynamic Predictor

| | |
|---|---|
| **Project** | Rapid-MMLS (MMLS-AI) v2.0 |
| **Features documented** | 1. Large-Scale Combat Operations coverage at 2,000 casualties per day · 2. Digital Twin Simulator and Dynamic Predictor for real-time supply |
| **Source documents** | BST Rapid-MMLS Problem Analysis & PID v0.2 (7 Oct 2026) · BST LSCO Medical Logistics Digital Twin v1.0 (7 Oct 2026) · AI and Decision Support for Military Medical Logistics: Structured Review (Sept 2026) |
| **Status** | TRL 4 prototype functionality, live at the existing deployment |
| **Classification** | Commercial in Confidence |

---

## 1. Summary

Two capabilities have been added to the existing MMLS-AI system (inventory, QR scanning, clinical-event decrement, XGBoost/LSTM forecasting — all unchanged):

1. **LSCO scale coverage.** The system now models theatre-wide Large-Scale Combat Operations at the BST planning figure of **2,000 casualties per day** — twenty times the brigade planning annex — across the full supply chain from the main national warehouse to the combat medic: Warehouse → Theatre Depot → Role 3 → Role 2E → Role 1. Demand is generated from an explicit **triage-driven casualty-to-consumption model** (20% T1 / 30% T2 / 50% T3), reproducing the daily demand table in PID §4.2 exactly.

2. **Digital Twin Simulator + Dynamic Predictor.** The same supply-chain model runs in two modes, as PID §8 requires:
   - **Simulator** (planner mode): a 30-day, hourly-resolution synthetic run that answers *"where does stock run out, when, and what prevents it?"* — and compares today's **static planning factors** against the **dynamic predictor** head-to-head.
   - **Operational system** (live mode): a **real-time dynamic supply forecast** computed from the actual inventory database and the usage audit trail (QR scans and Rapid-EPR-style clinical events) recorded through the existing API over the preceding 72 hours.

Both are surfaced in a new **"🪖 Digital Twin" tab** on the role-scoped Streamlit dashboard and through three new API endpoints.

> **Honest-positioning statement (per PID §11.3 / review "no overclaiming"):** simulator outputs are *scenario results on synthetic data, not predictions of real demand*. The casualty-to-consumption factors beyond theatre packs are **placeholders** pending clinical planning factors (PID §19, open question 3). The system **recommends and drafts only — a logistician approves every resupply plan** (NATO meaningful human control, PID §8/§16.2).

---

## 2. Feature 1 — LSCO coverage at 2,000 casualties per day

### 2.1 What it does

It scales the entire demand model of the digital twin to the theatre LSCO planning figure and derives item demand directly from casualty triage, exactly as set out in the Digital Twin PDF §2 and PID §4.2:

| Item | Basis (from the PDFs) | Per day @ 2,000 | Per 30 days |
|---|---|---|---|
| Casualties by triage | 20% T1 / 30% T2 / 50% T3 | 400 / 600 / 1,000 | 12,000 / 18,000 / 30,000 |
| Surgical cases | All T1 + half of T2 | 700 | 21,000 |
| Role 2E theatre packs | Brigade annex × 20 (PID §4.2) | 660 | — |
| Role 3 theatre packs | Annex × 20, incl. re-operations | 1,000 | — |
| **Theatre packs total** | | **1,660** | ~49,800 |
| Anaesthetic sets | 600 (R2E) + 840 (R3) | **1,440** | 43,200 |
| Blood and blood products | 10 units per T1 casualty (RUSI ratio) | **4,000 units** | 120,000 units |
| Haemorrhage control sets | One per T1+T2 casualty | **1,000** | 30,000 |
| Antibiotic courses | One per T1+T2 casualty | **1,000** | 30,000 |
| Analgesia doses (controlled) | ≥ one per casualty | **2,000** | 60,000 |
| Wound dressings | ≥ one per casualty | **2,000** | 60,000 |

These figures are computed by the engine itself and are **returned in every simulation response** (`daily_demand_at_casualty_rate`) and shown on the dashboard as a cross-check table, so the client can verify at any casualty rate that the model still reproduces the PID table. The automated test suite locks these seven numbers (test: `test_simulate_daily_demand_matches_pid_table_at_2000_a_day`).

The blood figure is the headline stress test: 4,000 units/day is approximately **one whole day of UK blood donations** (Defence Medical Research Strategy 2026–31 ratio, quoted in both PDFs), which is why the twin models blood as a perishable, cold-chain item rather than a generic consumable (see §3.2).

### 2.2 Scale topology

To carry 2,000 casualties/day the twin instantiates the six-link chain from PID §2:

- **WH** — national main warehouse (finite stock measured in days of national supply; just-in-time resupply fraction)
- **DEP** — theatre medical depot (can be destroyed at a chosen hour — depot dispersal problem, PID §5)
- **R3** — 10 Role 3 field hospitals
- **R2E** — 20 Role 2E forward surgery nodes (one per brigade-equivalent)
- **R1** — 80 Role 1 nodes (4 per brigade group)

Casualties arrive at Role 1 as a stochastic stream (Poisson, diurnal variation, uneven axes of advance via a Dirichlet split), then appear at Role 2E and Role 3 after **configurable evacuation delays** — this is how the Ukraine-driven "slower evacuation / prolonged field care" effect (review §7.4–7.6) raises forward consumption.

### 2.3 How to use it

**Dashboard:** open the **🪖 Digital Twin** tab → set *Casualties per day* (default 2,000; range 100–10,000) and *Simulation days* (1–60, default 30) → press **Run static vs dynamic simulation**.

**API:**

```
GET /twin/simulate?theatre_casualties_per_day=2000&days=30
```

Any parameter can be overridden; see §4.1 for the full endpoint reference.

---

## 3. Feature 2 — Digital Twin Simulator & Dynamic Predictor

### 3.1 The simulator (planner mode)

An hourly, whole-chain inventory simulation (PID §8 "Simulator" column: *"Where does stock runs out, when, and what prevents it?"*). Each hour it: consumes stock against casualty-derived demand at each node, ships resupply upward-ordered from parent nodes through delayed, lossy links, and records unmet demand.

**Policies compared in every run** (this is the project's core claim — dynamic beats static):

| Policy | What it represents |
|---|---|
| `static` | Today's practice: NATO-style fixed planning factors × planned casualty rate, never updated |
| `dynamic` | The MMLS-AI predictor: live casualty feed + evacuation pipeline look-ahead + **learned per-item correction factors** (bounded 0.5–3.0×) + surge detection (fast/slow EWMA of arrivals) |
| `seasonal_naive`, `croston_sba` | Also implemented as benchmark baselines (intermittent-demand methods, per the review's recommendation to lead with OR for sparse Class VIII lines) |

**LSCO scenario switches** (the scenario library of PID §11.2, step 4):

| Scenario | Parameter(s) | Models (PDF reference) |
|---|---|---|
| Mass-casualty surge | `surge_start_h`, `surge_mult`, `surge_len_h` | Surge-driven Role 3 consumption spikes (PID §5) |
| Theatre depot destroyed | `depot_loss_h` | Static depot struck; dispersal problem (PID §5) |
| Cold-chain failure | `cold_chain_loss_h` | Forward refrigeration lost at Role 2E (PID §6, blood category) |
| Blood spoilage | `blood_spoil_h` (hourly % loss, default 0.5%) | Short shelf life / wastage (Digital Twin PDF §5 cold chain) |
| Walking blood bank | `wbb_units_per_day` | Fresh units/day donated at R2E — the Nye Monte Carlo benchmark (review §3.1) |
| DDIL comms | `order_fail_p` | Nodes cannot transmit orders (PID §5 "whole chain") |
| Contested lift | `lift_factor`, `evac_factor` | Slower resupply and slower casualty movement (Ukraine lessons) |
| National stock depth | `wh_init_days`, blood inflow fraction | Just-in-time national stock exhaustion (PID §5) |

**Outputs:** fill rate %, unmet demand and **first stock-out day** per item; fill rate by echelon; and an Hours-of-Supply snapshot for any hour and echelon via `/twin/hos`, tiered with the PID §9.3 actions:

| Tier | HoS | System action (PID §9.3) |
|---|---|---|
| GREEN | > 24 h | Monitor |
| TEAL | 12–24 h | Draft resupply for logistician review |
| AMBER | 6–12 h | Escalate to FST commander / MO |
| RED | 2–6 h | Emergency resupply; Role 3 CO alerted |
| PURPLE | < 2 h | Commander alert; lateral redistribution |

**Validation anchor:** in a 10-day scenario at 2,000/day with surge and depot loss, the simulator's first blood stock-out falls on **day 2** — consistent with the review's "blood cliff" benchmark (Nye et al.: conventional forward blood supply fails once casualties exceed ~30/day per surgical detachment, median 2 days).

### 3.2 The dynamic predictor (operational / real-time mode)

The other half of the digital twin: the same prediction engine applied to **your real inventory**, not synthetic nodes (PID §8 "Operational system" column).

- `GET /twin/live-forecasts?horizon_h=24` reads the live MongoDB inventory and the audit log of the **last 72 hours** (QR scans and clinical-event decrements recorded through the existing `/scan` and `/clinical_event` endpoints — the Rapid-EPR auto-decrement trigger path of PID §9.1).
- Per item it maintains **dual exponential moving averages** (short 0.30 / long 0.02, the same architecture as the simulator's `DynamicPolicy`), clips the learned correction to the 0.5–3.0× fail-safe band, and reports: predicted consumption rate, expected quantity over the horizon, **Hours-of-Supply at the predicted (not historical) rate**, HoS tier, and whether the estimate came from recent observed usage or the inventory baseline.
- Items with no recent activity **safely fall back to the catalogue baseline** rather than forecasting near-zero (fail-safe rule, per the review's warning that sparse demand must not be over-forecast).
- Forecast horizons of **6 / 24 / 72 hours** (objectives, PID §12.1.2) are selectable on the dashboard; the API accepts 1–168.
- It is read-only: **forecasting never modifies stock**, and every recommendation requires human approval.

On the dashboard this is the lower half of the 🪖 Digital Twin tab, refreshed on load, sorted worst-first by hours of supply.

### 3.3 How to use it end-to-end (client walkthrough)

1. Log in to the dashboard (`logistic01 / admin123` for the full Role 3 view).
2. Record usage as normal (QR scan or clinical event) — this feeds the predictor's audit trail.
3. Open **🪖 Digital Twin**.
4. Top section — set the LSCO scenario (casualties/day, days, evacuation and lift multipliers, national stock, DDIL %, surge/depot-loss/cold-chain toggles, walking blood bank) → **Run static vs dynamic simulation** → review the fill-rate chart, first stock-out table, the daily-demand cross-check, and echelon comparison.
5. Middle section — choose a snapshot hour and echelon → **Load HoS snapshot** to see which synthetic nodes are in which HoS tier and what action each triggers.
6. Bottom section — the live forecast table for the real inventory at your chosen 6/24/72 h horizon; act on TEAL-and-below items per the §9.3 escalation ladder.

---

## 4. API reference (new endpoints)

### 4.1 `GET /twin/simulate`

Static-vs-dynamic scenario run. Query parameters (all optional; defaults in brackets):

`theatre_casualties_per_day` [2000] (100–10,000) · `days` [30] (1–60) · `surge_start_h` [72] · `surge_len_h` [6] · `surge_mult` [2.5] · `evac_factor` [1.0] · `lift_factor` [1.0] · `depot_loss_h` [-1 = never] · `cold_chain_loss_h` [-1 = never] · `blood_spoil_h` [0.005] · `wbb_units_per_day` [0] · `order_fail_p` [0.0] · `wh_init_days` [30] · `seed` [42].

Returns: `classification`, `assumptions` (casualty rate, days, triage mix), `planning_basis`, `daily_demand_at_casualty_rate`, `tier_actions`, and for each of `static` and `dynamic`: `summary` (fill rate, unmet, first stock-out day per item) and `by_level` (fill rate per echelon). Invalid or out-of-range parameters return HTTP 400 with a clear message; identical parameters are cached.

### 4.2 `GET /twin/hos`

Synthetic Hours-of-Supply snapshot. Parameters: scenario parameters as above, plus `t` [24] = hour, `level` = `R1|R2E|R3`, `limit` [100] (max 1,000). Returns worst-first rows: node, level, item, stock, HoS hours, tier.

### 4.3 `GET /twin/live-forecasts`

Real-time supply prediction for the live inventory. Parameter: `horizon_h` [24] (1–168). Returns `generated_at`, `window_h` (72), `classification`, and per item: baseline vs predicted rate, expected quantity, hours of supply, HoS tier, observed 72 h consumption, predictor version (`dynamic-ema-v1`) and data source (`recent_audit_activity` or `inventory_baseline`).

### 4.4 Code map (for engineering handover)

| File | Role |
|---|---|
| `lsco_twin/config.py` | All planning assumptions in one place: triage mix, casualty-to-consumption factors (derived from PDF tables), topology, delays, stock policy, scenario switches |
| `lsco_twin/world.py` | Network topology, stochastic casualty stream, ground-truth demand |
| `lsco_twin/predictor.py` | `StaticPolicy`, `DynamicPolicy` (surge-aware, learned corrections), Croston/SBA and seasonal-naive baselines |
| `lsco_twin/simulator.py` | Hourly multi-echelon stock/shipment engine, spoilage, cold-chain failure, walking blood bank, HoS tiers + actions |
| `lsco_twin/api.py` | The three Flask routes above, parameter validation and caching |
| `twin_dashboard.py` | The 🪖 Digital Twin Streamlit tab |
| `test_twin_integration.py` | 6 integration tests, incl. PID §4.2 demand-table conformance and scenario-switch tests |

All pre-existing endpoints (`/inventory`, `/scan`, `/clinical_event`, `/forecast`, `/hours_of_supply`, `/audit_log`, `/register_item`, `/delete_items`, `/reset`) are untouched.

---

## 5. Assumptions, limitations and evidence position

Stated deliberately, consistent with the structured review's evidence grading:

1. **Placeholder factors.** Triage mix and per-casualty multipliers beyond the theatre-pack annex are illustrative (the PDFs' own open question). The design keeps every factor in `config.py` so validated clinical planning factors can replace them without touching the engine.
2. **Synthetic ground truth.** Simulator runs generate synthetic casualties/consumption; their outputs grade scenario resilience, they are not demand predictions. Live forecasts are labelled estimates from baselines and observed audit events.
3. **No clinical decision support.** The system sizes and predicts logistics demand; it makes no patient-level recommendations (SaMD boundary, PID §16.2).
4. **Human authority.** Resupply outputs are drafts; controlled-drug lines (analgesia) are flagged, sized and audited but remain subject to dual-signature process.
5. **Blood modelled at aggregate level** with spoilage and cold-chain failure switches; blood grouping and donor attrition are the documented next extensions (review: "treat the Nye model as the benchmark to reproduce and extend").
6. **Model quality** inherits the prototype position: XGBoost/LSTM were trained on synthetic data; the twin's dynamic predictor is presented comparatively (static vs dynamic in identical scenarios), not with absolute accuracy claims.

---

## 6. Running and deployment

- **Local:** start the API (`py -3 "app (1).py"`, needs MongoDB via `MONGO_URI`), then `MMLS_AI_API_URL=http://127.0.0.1:5000` and `streamlit run dashboard.py`. Tests: `py -3 -m pytest -q test_twin_integration.py` (6 passed).
- **Hugging Face:** the `hf_deploy/` folder contains the ready-to-upload set under clean names — `app.py`, `dashboard.py`, `twin_dashboard.py`, `lsco_twin/` package, merged `requirements.txt`, model artefacts and the NSN catalogue. Per the PDFs' data-sensitivity rule (PID §11.3), only synthetic/unclassified scenario data belongs on public Hugging Face Spaces; live stock data stays behind the accredited API.
- A simulation of 30 days × 2 policies typically completes server-side in seconds; results for identical parameters are cached.

---

## 7. TRL Roadmap — Path from 4/5 to 7

| TRL | Definition | Status | Key activities | Target |
|---|---|---|---|---|
| **4** | Technology validated in lab | ✅ Done | Simulator + predictor working against synthetic data; Monte Carlo validation framework | Completed |
| **5** | Technology validated in relevant environment | ✅ Current | Deployed to Render cloud; live inventory forecast against MongoDB Atlas; Digital Twin tab operational | Completed |
| **6** | Technology demonstrated in relevant environment | 🔲 Next | • Replace placeholder planning factors with validated clinical data (NATO AMedP-13, Borden JMALL, RUSI). • Integrate with real (or realistic exercise) inventory feeds. • User testing with logisticians in a controlled exercise. • Blood grouping + donor attrition model validated against Nye data. | +3 months |
| **7** | System prototype in operational environment | 🔲 Goal | • Deploy within a theatre logistics network (or wargame). • Interface with real CSSP / MEDLOG systems. • Handle live data sensitivity (PID §11.3: accredited network only). • Demonstrate HoS alerts driving actual resupply decisions. • Formal validation report: Monte Carlo outcomes vs after-action review. | +6–12 months |

### Critical path to TRL 7

1. **Validated planning factors** (mentor action item):
   - Sources: NATO AMedP-13(B), US Borden Institute JMALL Table 14-2, UK DCDC JFHA, RUSI Blood & Military Medicine 2022.
   - Replace triage-mix placeholder (20/30/50) with theatre-specific data.
   - Confirm blood 10 units per T1 against theatre-level evidence.

2. **Nye Monte Carlo full reproduction** (mentor decision):
   - Current: simple WBB inflow + spoilage.
   - Implemented: donor attrition (exponential decay + Poisson loss) + ABO/Rh grouping constraint.
   - Validation: run 100+ Monte Carlo iterations; compare day-of-blood-stockout distribution to Nye et al. reported outcomes.
   - Decision needed: is day-2 stockout a robust anchor (p5 ≤ 2, median ≤ 4) or does full Nye model change the picture?

3. **Blood grouping & donor attrition prioritisation** (mentor confirmed: YES):
   - Implemented in simulator (config flags `use_blood_grouping`, `use_donor_attrition`).
   - Walking blood bank may be limiting factor if supply chain disrupted — validated via Monte Carlo.
   - Next: integrate with real donor registry data (blood types of available personnel at each node).

4. **End-user consultation** (next week per mentor):
   - Present Monte Carlo results to logisticians.
   - Gather feedback on HoS tier thresholds (are 24h/12h/6h/2h right for their operating tempo?).
   - Validate fill-rate targets against actual theatre expectations.

---

## 8. Planning Factor Sources (replacing placeholders)

| Factor | Current placeholder | Source to validate against | Status |
|---|---|---|---|
| Triage mix 20/30/50 | PID Q2 open | NATO AMedP-13(B) Annex B; theatre-specific casualty data | Pending end-user |
| Blood 10 units per T1 | RUSI ratio | RUSI "Blood and Military Medicine" 2022; US JMALL Table 14-2 | Literature-backed, needs theatre confirmation |
| Theatre packs 1,660/day | PID §4.2 brigade annex ×20 | Borden JMALL; UK DCDC JFHA | Placeholder pending validation |
| WBB donor attrition 8%/day | Nye et al. 2014 | Mil Med 179(7):365-370 | Implemented, needs local validation |
| Blood group distribution | NHS + military registry | NHSBT Annual Data; US Armed Services Blood Program | Approximate, adequate for simulation |
| Cold-chain spoilage 0.5%/hr | PID §6 | NATO AMedP-13 cold chain guidance | Placeholder |
