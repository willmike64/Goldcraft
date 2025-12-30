import streamlit as st

def render_game_menu():
    st.markdown("## ⛏️ GoldCraft")
    st.markdown("### Dimensional Earth Mining Expedition")

    st.divider()

    st.markdown(
        """
        It is **1848**.

        You stand on ground already spoken for —  
        layered with claims, capital, risk, and reputation.

        Descent is not exploration.  
        It is participation.

        Every decision leaves a trace.
        """
    )


    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🚀 Begin Expedition", use_container_width=True):
            st.session_state.current_view = "map"

    with col2:
        if st.button("🏘️ Visit Town Hub", use_container_width=True):
            st.session_state.current_view = "town"

    st.divider()

    st.markdown(
        """
        **Game Structure**
        - 🗺️ Explore strata layers
        - ⛏️ Extract finite resources
        - 🤝 Negotiate with factions
        - 📉 Shape gold markets
        """
    )
