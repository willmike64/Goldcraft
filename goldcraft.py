import streamlit as st
import sys
import os

# --------------------------------------------------
# Path setup
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# --------------------------------------------------
# Imports
# --------------------------------------------------
from game_modules.gold_map_folium import render_gold_map_folium
from game_modules.town_hub import render_town_hub
from game_modules.statistics import render_statistics
from game_modules.menu import render_game_menu

# --------------------------------------------------
# Page Config (must be first Streamlit call)
# --------------------------------------------------
st.set_page_config(
    page_title="⛏️ GoldCraft | Dimensional Mining Expedition",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# Session State Initialization
# --------------------------------------------------
def init_session_state():
    defaults = {
        "current_view": "menu",
        "current_strata": "Surface",
        "depth_layer": "Surface",
        "gold": 50,
        "reputation": {},
        "visited_sites": set(),
        "turn": 1,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# --------------------------------------------------
# Sidebar Navigation (Game Control)
# --------------------------------------------------
def render_sidebar():
    st.sidebar.title("⛏️ GoldCraft")
    st.sidebar.caption("Dimensional Earth Mining")

    view = st.sidebar.radio(
        "Navigate",
        options=[
            "menu",
            "map",
            "town",
            "stats",
        ],
        format_func=lambda x: {
            "menu": "🏁 Main Menu",
            "map": "🗺️ Strata Map",
            "town": "🏘️ Town Hub",
            "stats": "📊 Expedition Stats",
        }[x],
        index=["menu", "map", "town", "stats"].index(st.session_state.current_view) if st.session_state.current_view in ["menu", "map", "town", "stats"] else 0,
    )

    st.session_state.current_view = view

    st.sidebar.divider()

    st.sidebar.markdown("### ⏳ Expedition Turn")
    st.sidebar.metric("Turn", st.session_state.turn)

    st.sidebar.markdown("### 💰 Gold Reserves")
    st.sidebar.metric("Gold", f"{st.session_state.gold:,}")

# --------------------------------------------------
# Main Router
# --------------------------------------------------
def main():
    init_session_state()
    render_sidebar()

    view = st.session_state.current_view

    if view == "menu":
        render_game_menu()

    elif view == "map":
        render_gold_map_folium()

    elif view == "town":
        render_town_hub()

    elif view == "stats":
        render_statistics()

    else:
        render_game_menu()


# --------------------------------------------------
# Entry Point
# --------------------------------------------------
if __name__ == "__main__":
    main()
