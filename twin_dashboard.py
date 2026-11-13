"""Dashboard views for the LSCO simulator and live inventory forecasts.

Scenario parameters follow BST PID v0.2 s4.2/s8/s11.2 and
BST_LSCO_Medical_Logistics_Digital_Twin.pdf s2/s8: triage-driven demand at
2,000 casualties a day, surge, depot loss, cold-chain failure, walking blood
bank, DDIL order loss and lift competition. Outputs are synthetic planning
estimates only; a logistician approves every resupply plan (PID s8).
"""

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

# Base delays from lsco_twin/config.py. The twin's delay inputs are HOURS; the
# two multipliers on the dashboard scale these, so the effective hours/days are
# shown next to each slider (mentor review item 9).
BASE_EVAC_H = {"R1 → R2E": 4, "R1 → R3": 16}
BASE_LINK_H = {"R1 resupply": 4, "R2E resupply": 8, "R3 resupply": 12, "Depot → theatre": 48}
FACTOR_MAX = 30.0


def _fmt_delay(hours):
    return f"{hours:.0f}h" if hours < 48 else f"{hours:.0f}h ({hours / 24:.1f} days)"


def _delay_caption(base, factor):
    parts = " · ".join(f"{label} {_fmt_delay(h * factor)}" for label, h in base.items())
    return f"Multiplier applies to **hours**. At {factor:.1f}×: {parts}"


def render_twin_dashboard(api_url):
    st.subheader("Large-Scale Combat Operations Digital Twin")
    st.caption(
        "The simulator defaults to 2,000 casualties per day (triage mix 20% T1 / 30% T2 / "
        "50% T3). Casualty-to-consumption factors are BST PID v0.2 s4.2 placeholders, not "
        "validated clinical planning factors. The twin recommends and drafts; a logistician "
        "approves every resupply plan."
    )

    # ── Scenario controls (PID s11.2 scenario library) ──
    casualties_col, days_col, evac_col, lift_col = st.columns(4)
    casualties = casualties_col.number_input(
        "Casualties per day", min_value=100, max_value=10000, value=2000, step=100
    )
    days = days_col.number_input("Simulation days", min_value=1, max_value=60, value=30)
    evac = evac_col.slider(
        "Evacuation delay multiplier", 0.0, FACTOR_MAX, 1.0, 0.5,
        help="Scales the evacuation legs (hours). 1.0× = doctrinal baseline, "
             "higher = Ukraine-type prolonged field care.",
    )
    lift = lift_col.slider(
        "Resupply delay multiplier", 0.0, FACTOR_MAX, 1.0, 0.5,
        help="Scales every resupply leg (hours). 1.0× = doctrinal baseline, "
             "higher = contested lift / long lines of communication.",
    )
    evac_col.caption(_delay_caption(BASE_EVAC_H, evac))
    lift_col.caption(_delay_caption(BASE_LINK_H, lift))
    if max(lift * max(BASE_LINK_H.values()), evac * max(BASE_EVAC_H.values())) > days * 24:
        st.warning(
            f"At these multipliers the longest delay ({_fmt_delay(max(lift * max(BASE_LINK_H.values()), evac * max(BASE_EVAC_H.values())))}) "
            f"is longer than the {days}-day simulation window, so those resupply/evacuation "
            "movements never complete inside the run. Increase Simulation days to see their effect."
        )
    stock_days, ddil, national_stock = st.columns(3)
    wh_days = national_stock.slider("National stock (days)", 0, 365, 30)
    order_loss = ddil.slider("Orders lost % (DDIL)", 0, 100, 0, 5)
    surge_hours = stock_days.selectbox(
        "Mass-casualty surge", options=["None", "At hour 72", "At hour 240"], index=1
    )

    cold_col, wbb_col, depot_col = st.columns(3)
    cold_chain = cold_col.checkbox("Cold-chain failure at Role 2E (hour 120)", value=False)
    wbb = wbb_col.slider("Walking blood bank (units/day per R2E)", 0, 120, 0, 10)
    depot_loss = depot_col.checkbox("Theatre depot struck (hour 168)", value=False)

    # ── Walking blood bank model inputs (mentor review item 10) ──
    with st.expander("🩸 Walking blood bank — ABO/Rh and donor-attrition inputs (Nye et al. 2014)"):
        st.caption(
            "The two switches are on/off only — their **magnitudes** are set here: how many "
            "pre-typed donors each Role 2E starts with, and what fraction of that pool is lost "
            "per day. Accepted ranges: donor pool **10–1000**, attrition **0–50 %/day**, "
            "flat WBB inflow **0–200 units/day per R2E**."
        )
        grp_col, attr_col = st.columns(2)
        use_grouping = grp_col.checkbox(
            "Enable ABO/Rh blood group constraints", value=False,
            help="Scales every collected unit by the usable fraction (0.97 with the default "
                 "UK/NATO group mix: AB- 1% and B- 2% cannot be covered by the pool).")
        use_attrition = attr_col.checkbox(
            "Enable donor pool attrition", value=False,
            help="Replaces the flat WBB inflow with a decaying donor pool: "
                 "pool(t) = donor_pool_init × (1 − attrition)^days, plus a stochastic "
                 "casualty loss each collection round.")
        pool_col, rate_col = st.columns(2)
        donor_pool = pool_col.number_input(
            "Donor pool per Role 2E (10–1000)", min_value=10, max_value=1000,
            value=120, step=10, disabled=not use_attrition,
            help="Nye et al. 2014 used ~120 pre-typed donors at a deployed Role 2.")
        attrition_pct = rate_col.slider(
            "Donor attrition (% of pool lost per day, 0–50%)", 0.0, 50.0, 8.0, 0.5,
            disabled=not use_attrition,
            help="8%/day is the Nye 2014 Afghanistan figure (casualties, rotation, illness).")
        if use_attrition and wbb == 0:
            st.info(
                "The 'Walking blood bank' slider above is at 0, but with attrition enabled the "
                f"inflow is driven by the donor pool ({donor_pool} donors) instead, so the "
                "model still runs."
            )
        if st.button("Show ABO/Rh mix and donor-pool projection", key="show_blood_model"):
            try:
                bm = requests.get(
                    f"{api_url}/twin/blood-model",
                    params={
                        "days": int(days),
                        "use_blood_grouping": "true" if use_grouping else "false",
                        "use_donor_attrition": "true" if use_attrition else "false",
                        "wbb_units_per_day": wbb,
                        "donor_pool_init": int(donor_pool),
                        "donor_attrition_rate": attrition_pct / 100,
                    },
                    timeout=30,
                )
                bm.raise_for_status()
                bm_data = bm.json()
            except (requests.RequestException, ValueError) as exc:
                st.error(f"Unable to load the blood model: {exc}")
                bm_data = None
            if bm_data:
                dist_c, proj_c = st.columns([1, 2])
                with dist_c:
                    st.markdown("**ABO/Rh distribution used**")
                    st.dataframe(
                        pd.DataFrame(
                            [{"Group": g, "Share of donors": f"{share * 100:.0f}%"}
                             for g, share in bm_data["blood_group_distribution"].items()]
                        ),
                        use_container_width=True, hide_index=True,
                    )
                    st.metric("Usable fraction after grouping",
                              f"{bm_data['usable_fraction'] * 100:.0f}%")
                with proj_c:
                    st.markdown("**Donor pool and units per Role 2E, day by day**")
                    proj = pd.DataFrame(bm_data["projection"])
                    st.dataframe(proj, use_container_width=True, hide_index=True)
                    st.plotly_chart(
                        px.line(proj, x="day", y=["active_donors", "units_usable"],
                                title="Donor pool decay vs usable units collected per Role 2E"),
                        use_container_width=True, config={'displayModeBar': False},
                    )
                st.caption(
                    f"Collection model: {bm_data['collection']['units_per_donor']} unit per donor "
                    f"every {bm_data['collection']['interval_h']}h. Inputs sent: "
                    f"pool {bm_data['inputs']['donor_pool_init']}, attrition "
                    f"{bm_data['inputs']['donor_attrition_rate'] * 100:.1f}%/day, "
                    f"flat inflow {bm_data['inputs']['wbb_units_per_day']} units/day."
                )

    if st.button("Run static vs dynamic simulation", key="run_twin_simulation"):
        params = {
            "theatre_casualties_per_day": int(casualties),
            "days": int(days),
            "evac_factor": evac,
            "lift_factor": lift,
            "wh_init_days": wh_days,
            "order_fail_p": order_loss / 100,
            "wbb_units_per_day": wbb,
            "use_blood_grouping": "true" if use_grouping else "false",
            "use_donor_attrition": "true" if use_attrition else "false",
            "donor_pool_init": int(donor_pool),
            "donor_attrition_rate": attrition_pct / 100,
        }
        if surge_hours == "At hour 72":
            params.update(surge_start_h=72, surge_mult=2.5)
        elif surge_hours == "At hour 240":
            params.update(surge_start_h=240, surge_mult=2.5)
        else:
            params.update(surge_mult=1.0)
        if cold_chain:
            params["cold_chain_loss_h"] = 120
        if depot_loss:
            params["depot_loss_h"] = 168
        try:
            response = requests.get(
                f"{api_url}/twin/simulate", params=params, timeout=120
            )
            response.raise_for_status()
            result = response.json()
        except (requests.RequestException, ValueError) as exc:
            st.error(f"Unable to run the digital-twin simulation: {exc}")
            return

        st.caption(result["classification"])
        assumptions = result["assumptions"]
        mix = " / ".join(f"{int(share * 100)}% {tier}" for tier, share in assumptions["triage_mix"].items())
        st.caption(
            f"Scenario: {assumptions['theatre_casualties_per_day']:,} casualties/day "
            f"({mix}) for {assumptions['days']} days. Planning basis: {result['planning_basis']}"
        )

        # Daily demand cross-check against the PID s4.2 table.
        demand = result.get("daily_demand_at_casualty_rate", {})
        if demand:
            st.markdown("**Planned daily consumption at this casualty rate** (PID §4.2: 1,660 packs, 1,440 anaesthetic sets, 4,000 blood units, 1,000 haemorrhage/antibiotic, 2,000+ analgesia/dressings at 2,000 a day)")
            st.dataframe(
                pd.DataFrame(
                    [{"Item": item, "Units per day": qty} for item, qty in demand.items()]
                ),
                use_container_width=True,
                hide_index=True,
            )

        rows = [
            {**item, "policy": policy}
            for policy in ("static", "dynamic")
            for item in result[policy]["summary"]
        ]
        if rows:
            frame = pd.DataFrame(rows)
            st.plotly_chart(
                px.bar(
                    frame,
                    x="item",
                    y="fill_rate_pct",
                    color="policy",
                    barmode="group",
                    title="Demand fill rate by item (static planning factors vs dynamic predictor)",
                ),
                use_container_width=True,
                config={'displayModeBar': False},
            )
            stockouts = frame.pivot(
                index="item", columns="policy", values="first_stockout_day"
            ).rename_axis(None)
            st.markdown("**First stock-out day by item**")
            st.dataframe(stockouts, use_container_width=True)

        by_level = pd.DataFrame(result.get("dynamic", {}).get("by_level", []))
        if not by_level.empty:
            st.plotly_chart(
                px.bar(
                    by_level,
                    x="level",
                    y="fill_rate_pct",
                    title="Dynamic-policy fill rate by echelon",
                ),
                use_container_width=True,
                config={'displayModeBar': False},
            )

    # ── Hours-of-Supply snapshot across the theatre (simulator output) ──
    st.divider()
    st.subheader("Synthetic Hours-of-Supply by node (simulator)")
    hos_col1, hos_col2 = st.columns([1, 2])
    hos_hour = hos_col1.slider("Snapshot hour", 0, 719, 96, step=1)
    hos_level = hos_col2.selectbox(
        "Echelon", ["All", "R1", "R2E", "R3"], index=0
    )
    if st.button("Load HoS snapshot", key="load_twin_hos"):
        params = {"t": hos_hour, "limit": 300}
        if hos_level != "All":
            params["level"] = hos_level
        try:
            response = requests.get(f"{api_url}/twin/hos", params=params, timeout=120)
            response.raise_for_status()
            snapshot = response.json()
        except (requests.RequestException, ValueError) as exc:
            st.error(f"Unable to load the HoS snapshot: {exc}")
            return
        if snapshot:
            frame = pd.DataFrame(snapshot)
            st.dataframe(frame, use_container_width=True, hide_index=True)
            tier_actions = {
                "GREEN": "Monitor",
                "TEAL": "Draft resupply for logistician review",
                "AMBER": "Escalate to FST commander / MO",
                "RED": "Emergency resupply; Role 3 CO alerted",
                "PURPLE": "Commander alert; lateral redistribution",
            }
            worst = frame["tier"].value_counts().to_dict()
            st.caption(
                "Tiers per PID §9.3 · "
                + " · ".join(
                    f"{tier}: {count} ({tier_actions.get(tier, '')})"
                    for tier, count in sorted(worst.items(), key=lambda kv: kv[1], reverse=True)
                )
            )
        else:
            st.info("No forward demand at this hour for the selected echelon.")

    # ── Live dynamic forecast for the real inventory (operational system) ──
    st.divider()
    st.subheader("Dynamic forecast for current inventory")
    st.caption(
        "The operational twin: forecasts 6/24/72-hour demand per item from inventory "
        "baseline rates and usage audit events in the last 72 hours (Rapid-EPR auto-decrement "
        "and scans). It does not modify stock and recommends only — resupply needs human approval."
    )
    horizon = st.select_slider(
        "Forecast horizon (hours)", options=[6, 12, 24, 48, 72, 168], value=24
    )
    try:
        response = requests.get(
            f"{api_url}/twin/live-forecasts",
            params={"horizon_h": horizon},
            timeout=30,
        )
        response.raise_for_status()
        live = response.json()
    except (requests.RequestException, ValueError) as exc:
        st.error(f"Unable to load the live inventory forecast: {exc}")
        return

    st.caption(f"Generated at {live['generated_at']} · {live['classification']}")
    predictions = live.get("predictions", [])
    if not predictions:
        st.info("No inventory items are available for forecasting.")
        return
    frame = pd.DataFrame(predictions)
    columns = [
        "item_id",
        "item_name",
        "current_stock",
        "predicted_rate",
        "expected_qty",
        "hours_of_supply",
        "hos_tier",
        "observed_consumption_72h",
        "source",
    ]
    st.dataframe(
        frame[columns].sort_values(["hours_of_supply", "item_id"]),
        use_container_width=True,
        hide_index=True,
    )
    tier = frame["hos_tier"].iloc[0] if not frame.empty else None
    st.caption(
        "HoS tiers (PID §9.3): GREEN >24h monitor · TEAL 12-24h draft resupply · "
        "AMBER 6-12h escalate to FST commander · RED 2-6h emergency resupply, Role 3 CO · "
        "PURPLE <2h commander alert and lateral redistribution. Lowest item: "
        f"{frame.sort_values('hours_of_supply').iloc[0]['item_name']} at {tier}."
    )

    # ── Monte Carlo Validation (Nye model benchmark) ──────────────────────────────
    st.divider()
    st.subheader("Monte Carlo Validation (Nye blood model benchmark)")
    st.caption(
        "Runs the simulation N times with different random seeds to produce a "
        "statistical distribution of outcomes. Validates whether the day-2 blood "
        "stock-out is a robust finding or seed-dependent. Sources: Nye et al. 2014, "
        "BST PID \u00a74.2."
    )
    mc_col1, mc_col2 = st.columns([1, 2])
    mc_runs = mc_col1.slider("Number of runs", 10, 200, 50, step=10)
    mc_policy = mc_col2.selectbox("Policy", ["dynamic", "static"], index=0)

    if st.button("Run Monte Carlo validation", key="run_monte_carlo"):
        mc_params = {
            "theatre_casualties_per_day": int(casualties),
            "days": int(days),
            "evac_factor": evac,
            "lift_factor": lift,
            "order_fail_p": order_loss / 100,
            "wbb_units_per_day": wbb,
            "use_blood_grouping": "true" if use_grouping else "false",
            "use_donor_attrition": "true" if use_attrition else "false",
            "donor_pool_init": int(donor_pool),
            "donor_attrition_rate": attrition_pct / 100,
            "mc_runs": mc_runs,
            "policy": mc_policy,
        }
        if surge_hours == "At hour 72":
            mc_params.update(surge_start_h=72, surge_mult=2.5)
        elif surge_hours == "At hour 240":
            mc_params.update(surge_start_h=240, surge_mult=2.5)
        if cold_chain:
            mc_params["cold_chain_loss_h"] = 120
        if depot_loss:
            mc_params["depot_loss_h"] = 168
        with st.spinner(f"Running {mc_runs} Monte Carlo iterations..."):
            try:
                resp = requests.get(
                    f"{api_url}/twin/monte-carlo", params=mc_params, timeout=300
                )
                resp.raise_for_status()
                mc_result = resp.json()
            except requests.RequestException as exc:
                detail = ""
                resp_obj = getattr(exc, "response", None)
                if resp_obj is not None:
                    try:
                        detail = resp_obj.json().get("error", "")
                    except ValueError:
                        pass
                st.error(f"Monte Carlo run failed: {detail or exc}")
                return

        st.caption(mc_result["classification"])
        if mc_result.get("note"):
            st.info(f"\u2139 {mc_result['note']}: requested {mc_result.get('requested_runs')} runs, "
                    f"completed {mc_result.get('n_runs')} to stay within free-hosting time limits.")
        summary = mc_result["summary"]
        results_df = pd.DataFrame(mc_result["results"])
        actual_runs = len(results_df)

        # Key metrics cards
        col_a, col_b, col_c = st.columns(3)
        fr = summary.get("fill_rate", {})
        col_a.metric("Median Fill Rate", f"{fr.get('median', 'N/A')}%",
                     f"p5: {fr.get('p5', '?')}% \u2013 p95: {fr.get('p95', '?')}%")
        bso = summary.get("blood_stockout_day", {})
        col_b.metric("Blood Stock-out Day (median)", f"{bso.get('median', 'None')}",
                     f"p5: {bso.get('p5', '?')} \u2013 p95: {bso.get('p95', '?')}")
        fso = summary.get("first_stockout_day", {})
        col_c.metric("First Stock-out Day (median)", f"{fso.get('median', 'None')}",
                     f"p5: {fso.get('p5', '?')} \u2013 p95: {fso.get('p95', '?')}")

        # Distribution histogram
        if not results_df.empty:
            fig_mc = px.histogram(
                results_df, x="overall_fill_rate_pct", nbins=20,
                title=f"Monte Carlo distribution of fill rate ({actual_runs} runs, {mc_policy} policy)",
                color_discrete_sequence=["#58a6ff"],
            )
            fig_mc.add_vline(x=fr.get("median", 0), line_dash="dash", line_color="#f85149",
                            annotation_text="Median")
            fig_mc.update_layout(
                plot_bgcolor="#0d1117", paper_bgcolor="#161b22",
                font_color="#c9d1d9", height=350,
                xaxis_title="Fill rate (%)", yaxis_title="Count",
            )
            st.plotly_chart(fig_mc, use_container_width=True, config={'displayModeBar': False})

        # Blood stock-out distribution
        blood_df = results_df.dropna(subset=["blood_stockout_day"])
        if not blood_df.empty:
            fig_b = px.histogram(
                blood_df, x="blood_stockout_day", nbins=15,
                title="Distribution of first blood stock-out day across runs",
                color_discrete_sequence=["#f85149"],
            )
            fig_b.update_layout(
                plot_bgcolor="#0d1117", paper_bgcolor="#161b22",
                font_color="#c9d1d9", height=300,
                xaxis_title="Day", yaxis_title="Count",
            )
            st.plotly_chart(fig_b, use_container_width=True, config={'displayModeBar': False})

        # Validation interpretation
        st.markdown("**Validation interpretation:**")
        if bso and bso.get("p5") is not None:
            if bso["p5"] <= 2 and bso["median"] <= 4:
                st.success(
                    f"\u2705 Day-{bso['median']} blood stock-out is a **robust finding**: "
                    f"95% of runs stock out by day {bso['p95']}. "
                    f"This validates the PID \u00a74.2 blood constraint."
                )
            else:
                st.warning(
                    f"\u26a0\u00a0 Blood stock-out timing is variable (p5={bso['p5']}, "
                    f"p95={bso['p95']}). Day-2 is not a sufficient validation anchor alone \u2014 "
                    f"consider reproducing the full Nye Monte Carlo model with donor attrition."
                )
        st.dataframe(results_df.head(20), use_container_width=True, hide_index=True)
