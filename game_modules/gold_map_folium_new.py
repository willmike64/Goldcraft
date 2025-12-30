# gold_map_folium_new.py

import streamlit as st
import random

STRATA_LAYERS = {
    "Surface": {
        "risk_modifier": 0.1,
        "claims": [
            "Creekside Claim",
            "Abandoned Shaft",
            "Prospector’s Folly",
        ],
    },
    "Industrial Veins": {
        "risk_modifier": 0.3,
        "claims": [
            "Iron Vein 12",
            "Coal Spine",
            "Deep Rail Cut",
        ],
    },
    "Ancient Caverns": {
        "risk_modifier": 0.5,
        "claims": [
            "Echo Chamber",
            "Forgotten Vault",
            "Crystal Hollow",
        ],
    },
}

def advance_turn():
    st.session_state.turn += 1

def resolve_claim(claim_name, layer_data):
    base_risk = layer_data["risk_modifier"]
    roll = random.random()

    gold_found = random.randint(5, 25)

    if roll < base_risk:
        return {
            "event": "hazard",
            "message": f"⚠️ Hazard encountered at {claim_name}. Extraction disrupted."
        }

    st.session_state.gold += gold_found
    return {
        "event": "success",
        "message": f"⛏️ Extracted {gold_found} gold from {claim_name}."
    }

def render_gold_map_folium():
    st.markdown("## 🗺️ Strata Map")
    st.caption("Descend through Earth’s layers")

    st.divider()

    # Layer selection
    layer = st.selectbox(
        "Select Strata Layer",
        list(STRATA_LAYERS.keys()),
        index=list(STRATA_LAYERS.keys()).index(st.session_state.depth_layer)
    )

    st.session_state.depth_layer = layer
    layer_data = STRATA_LAYERS[layer]

    st.markdown(
        f"**Risk Level:** {int(layer_data['risk_modifier'] * 100)}%"
    )

    st.divider()

    # Initialize visited sites
    if "visited_sites" not in st.session_state:
        st.session_state.visited_sites = set()

    st.markdown("### ⛏️ Available Claims")

    for claim in layer_data["claims"]:
        visited = claim in st.session_state.visited_sites

        cols = st.columns([3, 1, 2])
        cols[0].markdown(f"**{claim}**")
        cols[1].markdown("✅ Visited" if visited else "🆕 New")

        if cols[2].button(
            "Enter",
            key=f"{layer}-{claim}",
            disabled=visited
        ):
            advance_turn()
            result = resolve_claim(claim, layer_data)
            st.session_state.visited_sites.add(claim)

            if result["event"] == "success":
                st.success(result["message"])
            else:
                st.warning(result["message"])

    st.divider()

    if st.button("⬅️ Return to Town Hub"):
        st.session_state.current_view = "town"
