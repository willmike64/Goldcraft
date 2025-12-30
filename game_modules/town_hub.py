import streamlit as st

FACTIONS = {
    "Old Miners Guild": {
        "description": "Tradition-bound, slow-moving, but deeply influential.",
    },
    "Industrial Syndicate": {
        "description": "Capital-rich, efficient, and ruthless.",
    },
    "Frontier Independents": {
        "description": "High risk, high reward, little protection.",
    },
}

def render_town_hub():
    st.markdown("## 🏘️ Town Hub")
    st.caption("Commerce, Diplomacy, and Preparation")

    st.divider()

    if "reputation" not in st.session_state:
        st.session_state.reputation = {}

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown("### 🤝 Factions")

        faction = st.selectbox(
            "Choose a faction to engage",
            list(FACTIONS.keys())
        )

        st.markdown(f"**{faction}**")
        st.markdown(FACTIONS[faction]["description"])

        rep = st.session_state.reputation.get(faction, 0)
        st.metric("Reputation", rep)

        col_a, col_b = st.columns(2)

        with col_a:
            if st.button("📜 Negotiate Access"):
                st.session_state.reputation[faction] = rep + 1
                st.success("Negotiation improved relations.")

        with col_b:
            if st.button("💰 Offer Capital"):
                st.session_state.gold = max(0, st.session_state.gold - 10)
                st.session_state.reputation[faction] = rep + 2
                st.info("Capital greased the wheels.")

    with col_right:
        st.markdown("### 🧰 Preparation")

        if st.button("🔧 Upgrade Equipment"):
            st.info("Upgrades coming soon.")

        if st.button("📦 Secure Supplies"):
            st.info("Supply logistics coming soon.")

    st.divider()

    if st.button("⬅️ Return to Map"):
        st.session_state.current_view = "map"
