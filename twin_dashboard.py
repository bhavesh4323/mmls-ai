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
    evac = evac_col.slider("Evacuation delay multiplier", 0.0, 5.0, 1.0, 0.5)
    lift = lift_col.slider("Resupply delay multiplier", 0.0, 5.0, 1.0, 0.5)
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

    if st.button("Run static vs dynamic simulation", key="run_twin_simulation"):
        params = {
            "theatre_casualties_per_day": int(casualties),
            "days": int(days),
            "evac_factor": evac,
            "lift_factor": lift,
            "wh_init_days": wh_days,
            "order_fail_p": order_loss / 100,
            "wbb_units_per_day": wbb,
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
