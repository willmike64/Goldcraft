import streamlit as st

def render_statistics():
    st.markdown("## 📊 Expedition Statistics")
    st.caption("Your impact on the world below")

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric("⏳ Turn", st.session_state.turn)
    col2.metric("💰 Gold", f"{st.session_state.gold:,}")
    col3.metric("🧭 Depth Layer", st.session_state.depth_layer)

    st.divider()

    st.markdown("### 🤝 Reputation by Faction")

    if not st.session_state.reputation:
        st.info("No faction interactions yet.")
    else:
        for faction, value in st.session_state.reputation.items():
            st.progress(min(max(value, 0), 10) / 10, text=f"{faction}: {value}")

    st.divider()

    st.markdown("### 🗺️ Exploration")

    visited = len(st.session_state.visited_sites)
    st.metric("Sites Visited", visited)

    st.divider()

    if st.button("⬅️ Return to Menu"):
        st.session_state.current_view = "menu"
