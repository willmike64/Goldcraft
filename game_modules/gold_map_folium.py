# gold_map_folium.py
import streamlit as st # type: ignore
import pandas as pd # type: ignore
from streamlit_folium import st_folium # type: ignore
import folium # type: ignore
from folium import plugins # type: ignore
from branca.element import Element  # type: ignore # public/safe

STRATA_LAYERS = {
    "Surface": {
        "description": "Shallow claims, low risk, limited yield",
        "allowed_statuses": ["active", "depleting"],
        "risk_modifier": 0,
    },
    "Industrial Veins": {
        "description": "Deep commercial mining zones",
        "allowed_statuses": ["active", "depleting", "unexplored"],
        "risk_modifier": 1,
    },
    "Ancient Caverns": {
        "description": "Old-world shafts and forgotten tunnels",
        "allowed_statuses": ["unexplored", "abandoned"],
        "risk_modifier": 2,
    },
    "Ghost Layers": {
        "description": "Legends, collapses, and things best left alone",
        "allowed_statuses": ["abandoned"],
        "risk_modifier": 3,
    },
}

st.subheader("🧭 Strata Depth")

if "current_strata" not in st.session_state:
    st.session_state.current_strata = "Surface"

selected_strata = st.selectbox(
    "Current Layer",
    list(STRATA_LAYERS.keys()),
    index=list(STRATA_LAYERS.keys()).index(st.session_state.current_strata) if st.session_state.current_strata in STRATA_LAYERS.keys() else 0,
)

st.session_state.current_strata = selected_strata
st.caption(STRATA_LAYERS[selected_strata]["description"])


def _gold_sites_df():
    """Mining expedition sites with StarCraft-style resource mechanics."""
    import random
    import math
    
    # Gold Creek coordinates for distance calculations
    gold_creek_lat, gold_creek_lon = 38.92, -120.75
    
    def calculate_distance(lat, lon):
        """Calculate distance from Gold Creek in miles (simplified)."""
        return round(math.sqrt((lat - gold_creek_lat)**2 + (lon - gold_creek_lon)**2) * 69, 1)
    
    def calculate_costs(distance, difficulty):
        """Calculate expedition costs based on distance and terrain difficulty."""
        base_travel = distance * 2  # Round trip cost
        security_cost = max(10, distance * 1.5 * difficulty)  # Anti-bandit protection
        equipment_cost = 5 + (difficulty * 3)  # Mining equipment transport
        return {
            'travel': round(base_travel),
            'security': round(security_cost), 
            'equipment': round(equipment_cost),
            'total': round(base_travel + security_cost + equipment_cost)
        }
    
    # Enhanced mining site data: name, lat, lon, type, current_gold, max_gold, difficulty, status, special_notes
    sites_data = [
        # HOME BASE MINE (Gold Creek Main Vein)
        ("Gold Creek Main Vein", 38.92, -120.75, "vein", 52000, 55000, 1, "active", "Town's main claim - safely operated and well-defended"),
        
        # Rich active sites (high reward, high risk)
        ("Feather Fork #3", 38.94, -120.78, "river", 8200, 9200, 2, "active", "Rich gravels, moderate bandit activity"),
        ("Grass Valley Lode", 38.89, -120.77, "vein", 35000, 38000, 4, "active", "Legendary deep lodes, heavy bandit presence"),
        ("Angels Reef", 38.95, -120.77, "vein", 19500, 21000, 3, "active", "Wide quartz ribbon, organized bandit gangs"),
        ("Nevada City Drift", 38.93, -120.73, "vein", 16800, 17600, 3, "active", "Ancient channels, moderate security risk"),
        
        # Moderate sites (balanced risk/reward)
        ("Downie Ridge Vein", 38.95, -120.76, "vein", 12400, 14800, 2, "active", "Visible gold in quartz, occasional bandits"),
        ("Placerville Reef", 38.94, -120.74, "vein", 11000, 13200, 2, "active", "High grade but narrow, light security needed"),
        ("Coloma Bar", 38.88, -120.76, "river", 7200, 8500, 1, "active", "Prime panning location, well-patrolled route"),
        ("Yuba Bend", 38.90, -120.72, "river", 5100, 6100, 1, "active", "North Yuba bar, safe but lower yields"),
        
        # Partially depleted sites (lower risk, lower reward)
        ("Auburn Ravine", 38.90, -120.78, "river", 2800, 5200, 1, "depleting", "Pockets still rich but fewer, minimal bandit interest"),
        ("Mokelumne Cut", 38.89, -120.73, "river", 1900, 4400, 1, "depleting", "Bank diggings mostly worked, very safe"),
        ("Jamestown Flats", 38.88, -120.74, "river", 3100, 6600, 1, "depleting", "Shallow placers, easy pickings mostly gone"),
        
        # Mystery/unexplored sites (high risk, unknown reward)
        ("Columbia Pocket", 38.91, -120.72, "vein", None, None, 3, "unexplored", "Rumors of spectacular nuggets, unconfirmed"),
        ("Tuolumne Quartz", 38.93, -120.76, "vein", None, None, 4, "unexplored", "High-sulfide ore, needs expert assessment"),
        ("Merced Shine", 38.90, -120.77, "river", None, None, 2, "unexplored", "Fine gold reported, requires proper equipment"),
        
        # Abandoned/dangerous sites (very high risk, potentially very high reward)
        ("Dead Man's Gulch", 38.87, -120.79, "vein", None, None, 5, "abandoned", "Rich strike abandoned after bandit massacre"),
        ("Widow's Peak Mine", 38.96, -120.74, "vein", None, None, 4, "abandoned", "Collapsed tunnels, treasure hunters' tales"),
    ]
    
    processed_data = []
    for site in sites_data:
        name, lat, lon, mine_type, current_gold, max_gold, difficulty, status, notes = site
        distance = calculate_distance(lat, lon)
        costs = calculate_costs(distance, difficulty)
        
        processed_data.append([
            name, lat, lon, mine_type, current_gold, max_gold, difficulty, status, notes, 
            distance, costs['travel'], costs['security'], costs['equipment'], costs['total']
        ])
    
    return pd.DataFrame(processed_data, columns=[
        "name", "lat", "lon", "type", "current_gold", "max_gold", "difficulty", 
        "status", "notes", "distance_miles", "travel_cost", "security_cost", 
        "equipment_cost", "total_cost"
    ])

# CSS: Enhanced pulse animations for different mine statuses
PULSE_CSS = """
<style>
.leaflet-marker-icon.pulse-dot, .leaflet-marker-shadow.pulse-dot { background: none; border: none; }
.leaflet-marker-icon.pulse-dot { z-index: 10000 !important; }

@keyframes pulse-dot {
  0%   { transform: scale(0.9); opacity: 0.95; }
  50%  { transform: scale(1.15); opacity: 1.0; }
  100% { transform: scale(0.9); opacity: 0.95; }
}
@keyframes pulse-ring {
  0%   { box-shadow: 0 0 0 0 rgba(0,0,0,0.35); }
  70%  { box-shadow: 0 0 0 14px rgba(0,0,0,0); }
  100% { box-shadow: 0 0 0 0 rgba(0,0,0,0); }
}
@keyframes slow-pulse {
  0%   { transform: scale(1.0); opacity: 0.7; }
  50%  { transform: scale(1.05); opacity: 0.9; }
  100% { transform: scale(1.0); opacity: 0.7; }
}
@keyframes danger-pulse {
  0%   { transform: scale(0.8); opacity: 0.8; box-shadow: 0 0 5px red; }
  50%  { transform: scale(1.2); opacity: 1.0; box-shadow: 0 0 15px red; }
  100% { transform: scale(0.8); opacity: 0.8; box-shadow: 0 0 5px red; }
}

.pulse {
  position: relative;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  animation: pulse-dot 1.8s ease-in-out infinite;
  will-change: transform, opacity;
}

/* Mine status-based styling */
.pulse.vein.active  { background: rgba(218,165,32,0.95); box-shadow: 0 0 6px rgba(218,165,32,0.9); }
.pulse.river.active { background: rgba(30,136,229,0.95); box-shadow: 0 0 6px rgba(30,136,229,0.9); }

.pulse.vein.depleting  { background: rgba(139,69,19,0.8); animation: slow-pulse 3s ease-in-out infinite; }
.pulse.river.depleting { background: rgba(70,130,180,0.8); animation: slow-pulse 3s ease-in-out infinite; }

.pulse.vein.unexplored  { background: rgba(128,0,128,0.9); box-shadow: 0 0 8px rgba(128,0,128,0.7); }
.pulse.river.unexplored { background: rgba(25,25,112,0.9); box-shadow: 0 0 8px rgba(25,25,112,0.7); }

.pulse.vein.abandoned  { background: rgba(220,20,60,0.9); animation: danger-pulse 2s ease-in-out infinite; }
.pulse.river.abandoned { background: rgba(178,34,34,0.9); animation: danger-pulse 2s ease-in-out infinite; }

.pulse::after {
  content: "";
  position: absolute; left: -2px; top: -2px; right: -2px; bottom: -2px;
  border-radius: 50%;
  animation: pulse-ring 1.8s ease-out infinite;
}

.gc-label {
  background: rgba(255,255,255,0.9);
  padding: 4px 8px;
  border-radius: 10px;
  border: 2px solid #222;
  font-weight: 700;
  font-size: 14px;
}

.expedition-popup {
  max-width: 350px !important;
  font-family: 'Courier New', monospace;
}
</style>
"""

def _pulse_marker_html(marker_class: str, status: str, delay_ms: int = 0) -> str:
    """Generate HTML for pulsing markers based on mine type and status."""
    return f'<div class="pulse {marker_class} {status}" style="animation-delay:{delay_ms}ms;"></div>'

def render_gold_map_folium():
    st.title("🗺️ Mining Expedition Command Center")
    st.caption("📡 Select mining sites for resource extraction missions • 💰 Plan expeditions carefully - costs and risks vary!")

    df = _gold_sites_df()

    # Initialize expedition state
    if 'expedition_unlocked_sites' not in st.session_state:
        st.session_state.expedition_unlocked_sites = []
    if 'expedition_history' not in st.session_state:
        st.session_state.expedition_history = []

    # Sidebar - Mission Control Panel
    with st.sidebar:
        st.subheader("🎮 Mission Control")
        
        # Current resources
        player_gold = st.session_state.get('gold', 0)
        st.metric("Available Gold", f"{player_gold:.1f} oz")
        
        # Filter controls
        st.subheader("🔍 Site Filters")
        show_active = st.checkbox("Active Sites", True)
        show_depleting = st.checkbox("Depleting Sites", True) 
        show_unexplored = st.checkbox("Unexplored Sites", True)
        show_abandoned = st.checkbox("Abandoned Sites", False)
        
        show_veins = st.checkbox("Vein Mines", True)
        show_rivers = st.checkbox("River Sites", True)
        
        # Legend
        st.subheader("📋 Site Status Legend")
        st.markdown("""
        **🟡 Active** - Rich, operational sites  
        **🟤 Depleting** - Partially worked, safer  
        **🟣 Unexplored** - Unknown potential, risky  
        **🔴 Abandoned** - Dangerous, high reward potential  
        
        **Site Types:**  
        <span style="color: #DAA520;">●</span> Vein Mines  
        <span style="color: #1E88E5;">●</span> River Claims
        """, unsafe_allow_html=True)
        
        st.subheader("📊 Mission Statistics")
        st.markdown(f"**Missions Completed:** {len(st.session_state.expedition_history)}")
        st.markdown(f"**Sites Unlocked:** {len(st.session_state.expedition_unlocked_sites)}")

    # Apply filters
    status_filter = []
    if show_active: status_filter.append("active")
    if show_depleting: status_filter.append("depleting") 
    if show_unexplored: status_filter.append("unexplored")
    if show_abandoned: status_filter.append("abandoned")
    
    type_filter = []
    if show_veins: type_filter.append("vein")
    if show_rivers: type_filter.append("river")

    strata = STRATA_LAYERS[st.session_state.current_strata]
    allowed_statuses = strata["allowed_statuses"]


    filtered = df[
    (df["status"].isin(status_filter)) &
    (df["type"].isin(type_filter)) &
    (df["status"].isin(allowed_statuses))
    ].copy()

    # Main map display
    m = folium.Map(
        location=[38.92, -120.75],  # Gold Creek coordinates
        zoom_start=13,  # Closer zoom for better initial view
        tiles="CartoDB Positron",
        control_scale=True
    )

    st.caption(f"📡 Scanning {len(filtered)} mining sites for expedition opportunities...")

    # Inject CSS
    m.get_root().add_child(Element(PULSE_CSS))

    # Map controls
    plugins.MiniMap(toggle_display=True, minimized=True).add_to(m)
    plugins.Fullscreen().add_to(m)

    # Mining sites
    fg = folium.FeatureGroup(name="Mining Expedition Sites", show=True).add_to(m)

    for idx, rec in enumerate(filtered.to_dict("records")):
        marker_class = "vein" if rec["type"] == "vein" else "river"
        status = rec["status"]
        delay = (idx * 120) % 1800
        html = _pulse_marker_html(marker_class, status, delay_ms=delay)

        # Base circle marker (always visible)
        color_map = {
            "active": "#DAA520" if marker_class == "vein" else "#1E88E5",
            "depleting": "#8B4513" if marker_class == "vein" else "#4682B4", 
            "unexplored": "#800080" if marker_class == "vein" else "#191970",
            "abandoned": "#DC143C" if marker_class == "vein" else "#B22222"
        }
        
        folium.CircleMarker(
            location=[rec["lat"], rec["lon"]],
            radius=8,
            color="#000000",
            weight=2,
            fill=True,
            fill_color=color_map[status],
            fill_opacity=0.9,
            tooltip=f"{rec['name']} ({rec['status'].title()})",
        ).add_to(fg)

        # Pulsing overlay
        icon = folium.DivIcon(
            html=html,
            class_name="pulse-dot",
            icon_size=(16, 16),
            icon_anchor=(8, 8),
        )

        # Enhanced popup with expedition details
        popup_html = create_expedition_popup(rec)

        folium.Marker(
            location=[rec["lat"], rec["lon"]],
            icon=icon,
            popup=folium.Popup(popup_html, max_width=400, class_name="expedition-popup"),
            z_index_offset=1000,
        ).add_to(fg)

    # Gold Creek base marker
    folium.Marker(
        location=[38.92, -120.75],
        icon=folium.DivIcon(html='<div class="gc-label">� Gold Creek Base</div>', class_name=""),
        tooltip="Gold Creek Mining Operations Base",
    ).add_to(m)

    folium.LayerControl(collapsed=True).add_to(m)

    # Render map
    map_state = st_folium(m, width=None, height=700)

    # Handle expedition selection
    if map_state and map_state.get("last_object_clicked_popup"):
        handle_expedition_selection(map_state, df)

    # Expedition history
    if st.session_state.expedition_history:
        with st.expander("📜 Recent Expedition History"):
            for expedition in st.session_state.expedition_history[-10:]:  # Last 10
                st.markdown(f"• **{expedition['site']}**: {expedition['result']} (Day {expedition.get('day', '?')})")

    st.markdown("---")
    if st.button("🏠 Return to Gold Creek Base", width='stretch'):
        st.session_state.current_view = "main_game"
        st.rerun()

def create_expedition_popup(site_data):
    """Create detailed expedition popup with StarCraft-style information."""
    name = site_data['name']
    site_type = site_data['type'].title()
    status = site_data['status'].title()
    distance = site_data['distance_miles']
    
    # Resource information
    if site_data['current_gold'] is not None:
        current_gold = f"{site_data['current_gold']:,} oz"
        max_gold = f"{site_data['max_gold']:,} oz"
        depletion = round((site_data['current_gold'] / site_data['max_gold']) * 100, 1)
        resource_info = f"""
        <strong>📊 Resource Analysis:</strong><br/>
        Current Reserves: <span style="color: #DAA520;">{current_gold}</span><br/>
        Original Deposit: {max_gold}<br/>
        Remaining: <span style="color: {'green' if depletion > 70 else 'orange' if depletion > 30 else 'red'};">{depletion}%</span>
        """
    else:
        resource_info = """
        <strong>📊 Resource Analysis:</strong><br/>
        <span style="color: purple;">⚠️ UNKNOWN RESERVES</span><br/>
        Reconnaissance mission required
        """
    
    # Cost breakdown
    costs = f"""
    <strong>💰 Expedition Costs:</strong><br/>
    Travel ({distance} mi): <span style="color: #B8860B;">{site_data['travel_cost']} oz</span><br/>
    Security: <span style="color: #B8860B;">{site_data['security_cost']} oz</span><br/>
    Equipment: <span style="color: #B8860B;">{site_data['equipment_cost']} oz</span><br/>
    <strong>Total: <span style="color: red;">{site_data['total_cost']} oz</span></strong>
    """
    
    # Risk assessment
    difficulty = site_data['difficulty']
    risk_levels = ["Minimal", "Low", "Moderate", "High", "Extreme"]
    risk_colors = ["green", "lightgreen", "orange", "red", "darkred"]
    risk_level = risk_levels[min(difficulty-1, 4)]
    risk_color = risk_colors[min(difficulty-1, 4)]
    
    risk_info = f"""
    <strong>⚠️ Risk Assessment:</strong><br/>
    Difficulty Level: <span style="color: {risk_color};">{difficulty}/5 ({risk_level})</span><br/>
    Bandit Activity: {'High' if difficulty >= 4 else 'Moderate' if difficulty >= 3 else 'Low'}<br/>
    Terrain: {'Treacherous' if difficulty >= 4 else 'Challenging' if difficulty >= 2 else 'Manageable'}
    """
    
    # Status indicator
    status_colors = {
        "Active": "green",
        "Depleting": "orange", 
        "Unexplored": "purple",
        "Abandoned": "red"
    }
    
    return f"""
    <div style="font-family: 'Courier New', monospace; background: #1a1a1a; color: #00ff00; padding: 10px; border-radius: 5px;">
        <h3 style="color: #00ffff; margin: 0 0 10px 0; text-align: center;">
            🎯 {name}
        </h3>
        
        <div style="background: #2a2a2a; padding: 8px; margin: 5px 0; border-left: 3px solid {status_colors.get(status, 'gray')};">
            <strong>📍 Site Classification:</strong><br/>
            Type: {site_type} Mine<br/>
            Status: <span style="color: {status_colors.get(status, 'white')};">{status}</span><br/>
            Distance: {distance} miles from base
        </div>
        
        <div style="background: #2a2a2a; padding: 8px; margin: 5px 0;">
            {resource_info}
        </div>
        
        <div style="background: #2a2a2a; padding: 8px; margin: 5px 0;">
            {costs}
        </div>
        
        <div style="background: #2a2a2a; padding: 8px; margin: 5px 0;">
            {risk_info}
        </div>
        
        <div style="background: #2a2a2a; padding: 8px; margin: 5px 0;">
            <strong>📝 Intelligence Report:</strong><br/>
            <em>{site_data['notes']}</em>
        </div>
        
        <div style="text-align: center; margin-top: 10px;">
            <small style="color: #888;">Click site to launch expedition</small>
        </div>
    </div>
    """

def handle_expedition_selection(map_state, df):
    """Handle when a player clicks on a mining site to start an expedition."""
    if map_state.get("last_object_clicked_popup"):
        # Parse the clicked site from the popup content
        popup_content = map_state["last_object_clicked_popup"]
        
        # Extract site name from popup (this is a simplified approach)
        # In a real implementation, you'd want a more robust site selection system
        
        with st.expander("🚀 Launch Mining Expedition", expanded=True):
            render_expedition_interface(df)

def render_expedition_interface(df):
    """Render the expedition planning and execution interface."""
    
    # Site selection
    site_names = df['name'].tolist()
    selected_site = st.selectbox("Select Mining Site:", site_names)
    
    if selected_site:
        site_data = df[df['name'] == selected_site].iloc[0]
        
        # Display site summary
        st.markdown(f"### 🎯 {selected_site}")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Distance", f"{site_data['distance_miles']} mi")
        with col2:
            st.metric("Total Cost", f"{site_data['total_cost']} oz")
        with col3:
            risk_level = ["Minimal", "Low", "Moderate", "High", "Extreme"][min(site_data['difficulty']-1, 4)]
            st.metric("Risk Level", f"{site_data['difficulty']}/5 ({risk_level})")
        
        # Equipment selection
        st.markdown("### ⚙️ Expedition Equipment")
        equipment_choice = st.radio(
            "Choose your equipment loadout:",
            [
                "Basic Kit (No bonus, standard cost)",
                "Advanced Kit (+20% yield, +15 oz cost)", 
                "Premium Kit (+40% yield, +30 oz cost, -1 risk level)"
            ]
        )
        
        equipment_bonus = 0
        equipment_cost = 0
        risk_reduction = 0
        
        if "Advanced" in equipment_choice:
            equipment_bonus = 0.2
            equipment_cost = 15
        elif "Premium" in equipment_choice:
            equipment_bonus = 0.4
            equipment_cost = 30
            risk_reduction = 1
        
        # Security selection
        st.markdown("### 🛡️ Security Detail")
        security_choice = st.radio(
            "Choose your security level:",
            [
                "Solo (No extra cost, high risk)",
                "Small Guard (15 oz, -1 risk level)",
                "Armed Escort (35 oz, -2 risk levels, bandit insurance)"
            ]
        )
        
        security_cost = 0
        security_reduction = 0
        bandit_insurance = False
        
        if "Small" in security_choice:
            security_cost = 15
            security_reduction = 1
        elif "Armed" in security_choice:
            security_cost = 35
            security_reduction = 2
            bandit_insurance = True
        
        # Calculate total mission cost
        total_cost = site_data['total_cost'] + equipment_cost + security_cost
        effective_risk = max(1, site_data['difficulty'] - risk_reduction - security_reduction)
        
        st.markdown("### 💰 Mission Summary")
        st.info(f"""
        **Total Expedition Cost**: {total_cost} oz gold  
        **Effective Risk Level**: {effective_risk}/5  
        **Potential Yield Bonus**: +{equipment_bonus*100:.0f}%  
        **Bandit Insurance**: {'Yes' if bandit_insurance else 'No'}
        """)
        
        # Check if player can afford it
        player_gold = st.session_state.get('gold', 0)
        
        if player_gold >= total_cost:
            if st.button("🚀 Launch Expedition!", type="primary"):
                launch_expedition(site_data, equipment_bonus, effective_risk, total_cost, bandit_insurance)
        else:
            st.error(f"Insufficient funds! Need {total_cost} oz gold, have {player_gold:.1f} oz")
        
        # Show active expeditions
        show_active_expeditions()

def launch_expedition(site_data, equipment_bonus, risk_level, cost, bandit_insurance):
    """Launch an expedition with event-driven gameplay."""

    strata_risk = STRATA_LAYERS[st.session_state.current_strata]["risk_modifier"]
    effective_risk = max(1, risk_level + strata_risk)

 # Initialize expedition state
    if 'current_expedition' not in st.session_state:
        st.session_state.current_expedition = None
    
    # Deduct cost
    st.session_state.gold = st.session_state.get('gold', 0) - cost
    
    # Create expedition
    expedition = {
        'site': site_data['name'],
        'site_data': site_data.to_dict(),
        'equipment_bonus': equipment_bonus,
        'risk_level': risk_level,
        'cost': cost,
        'bandit_insurance': bandit_insurance,
        'phase': 'travel_out',
        'events': [],
        'resources_gathered': 0,
        'supplies_remaining': 100,
        'team_morale': 75,
        'day_started': st.session_state.get('day', 1),
        'completed': False
    }
    
    st.session_state.current_expedition = expedition
    st.success(f"🚀 Expedition to {site_data['name']} launched!")
    st.rerun()

def show_active_expeditions():
    """Display and manage active expeditions."""
    
    if st.session_state.get('current_expedition'):
        expedition = st.session_state.current_expedition
        
        if not expedition['completed']:
            st.markdown("### 🎮 Active Expedition")
            render_expedition_progress(expedition)
        else:
            st.markdown("### ✅ Recently Completed")
            render_expedition_results(expedition)
            
            if st.button("📋 Archive Expedition"):
                # Move to history and clear active
                if 'expedition_history' not in st.session_state:
                    st.session_state.expedition_history = []
                
                st.session_state.expedition_history.append({
                    'site': expedition['site'],
                    'result': f"Gathered {expedition['resources_gathered']:.1f} oz gold",
                    'day': expedition['day_started']
                })
                
                st.session_state.current_expedition = None
                st.rerun()

def render_expedition_progress(expedition):
    """Render the active expedition with game show excitement and choices."""
    
    site_name = expedition['site']
    phase = expedition['phase']
    
    # Game show introduction
    if 'game_show_intro' not in expedition:
        expedition['game_show_intro'] = True
        st.balloons()
        st.markdown(f"""
        ## 🎪 **WELCOME TO "GOLD RUSH ROULETTE!"** 🎪
        
        *The audience roars as the spotlight hits you!*
        
        **🎙️ Host:** "Ladies and gentlemen, we have a brave prospector ready to risk it all at 
        **{site_name}**! Will they strike it rich or go home empty-handed? Let's find out!"
        
        *Dramatic music swells...*
        """)
    
    # Progress indicator with game show flair
    phases = ['travel_out', 'mining', 'events', 'travel_back']
    current_phase_idx = phases.index(phase) if phase in phases else 0
    progress = (current_phase_idx + 1) / len(phases)
    
    phase_names = ['🗺️ The Journey', '⛏️ The Challenge', '🎲 Wild Card', '🏠 Victory Lap']
    current_phase_name = phase_names[current_phase_idx] if current_phase_idx < len(phase_names) else "Unknown"
    
    st.markdown(f"### 🎭 **ROUND {current_phase_idx + 1}: {current_phase_name}**")
    st.progress(progress, text=f"Game Show Progress: {current_phase_name}")
    
    # Audience excitement meter
    excitement_level = min(100, 50 + (expedition['resources_gathered'] * 2) + expedition['team_morale'] // 2)
    st.markdown(f"🎉 **Audience Excitement**: {excitement_level}% {'🔥' if excitement_level > 80 else '👏' if excitement_level > 60 else '😐'}")
    
    # Show expedition status with game show styling
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 Gold Jackpot", f"{expedition['resources_gathered']:.1f} oz", 
                 delta=f"+{expedition['resources_gathered']:.1f}" if expedition['resources_gathered'] > 0 else None)
    with col2:
        supplies_color = "🟢" if expedition['supplies_remaining'] > 70 else "🟡" if expedition['supplies_remaining'] > 30 else "🔴"
        st.metric(f"{supplies_color} Supplies", f"{expedition['supplies_remaining']}%")
    with col3:
        morale_emoji = "😄" if expedition['team_morale'] > 70 else "😐" if expedition['team_morale'] > 40 else "😰"
        st.metric(f"{morale_emoji} Team Spirit", f"{expedition['team_morale']}%")
    
    # Phase-specific content with game show themes
    if phase == 'travel_out':
        render_travel_game_show(expedition)
    elif phase == 'mining':
        render_mining_game_show(expedition)
    elif phase == 'events':
        render_events_game_show(expedition)
    elif phase == 'travel_back':
        render_finale_game_show(expedition)

def render_travel_game_show(expedition):
    """Handle the journey with game show drama."""
    
    site_name = expedition['site']
    
    st.markdown(f"### 🎪 **ROUND 1: THE JOURNEY TO {site_name.upper()}!**")
    st.markdown("*🎙️ Host: 'Our contestant is about to face their first challenge on the road to fortune!'*")
    
    # Generate or get travel event
    if 'travel_event' not in expedition:
        expedition['travel_event'] = generate_site_specific_travel_event(expedition)
    
    event = expedition['travel_event']
    
    # Dramatic presentation
    st.markdown(f"### 🎭 **{event['title']}**")
    
    with st.container():
        st.markdown(f"""
        <div style="background: linear-gradient(45deg, #FF6B6B, #4ECDC4); padding: 20px; border-radius: 15px; color: white; text-align: center;">
        <h3>🎪 SITUATION ALERT! 🎪</h3>
        <p style="font-size: 18px; font-weight: bold;">{event['description']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Audience reaction
    st.markdown(f"*🎭 Audience: {event.get('audience_reaction', 'The crowd holds its breath...')}*")
    
    # Present choices with game show flair
    if event['choices'] and 'travel_choice' not in expedition:
        st.markdown("### 🎯 **CHOOSE YOUR STRATEGY!**")
        st.markdown("*🎙️ Host: 'What's it going to be? The audience is on the edge of their seats!'*")
        
        choice_options = []
        for i, choice in enumerate(event['choices']):
            risk_indicator = get_choice_risk_indicator(choice)
            choice_options.append(f"{chr(65+i)}) {choice['text']} {risk_indicator}")
        
        selected = st.radio("**Make your choice:**", choice_options)
        
        if st.button("🎬 LOCK IN YOUR DECISION!", type="primary"):
            if selected:  # Safety check
                choice_index = ord(selected[0]) - ord('A')
                selected_choice = event['choices'][choice_index]
                expedition['travel_choice'] = selected_choice
                
                # Dramatic reveal
                apply_choice_consequences(expedition, selected_choice)
                expedition['phase'] = 'mining'
                
                st.success(f"🎉 **CHOICE LOCKED!** {selected_choice['text']}")
                st.markdown(f"**🎭 Outcome:** {selected_choice['result']}")
                st.rerun()
    
    elif 'travel_choice' in expedition:
        choice = expedition['travel_choice']
        st.success(f"✅ **DECISION MADE**: {choice['text']}")
        st.markdown(f"**🎭 Result**: {choice['result']}")
        st.markdown("*🎙️ Host: 'Brilliant! Our contestant is ready for the main event!'*")
        
        if st.button("🎪 ADVANCE TO THE MINING CHALLENGE!", type="primary"):
            expedition['phase'] = 'mining'
            st.rerun()

def render_mining_game_show(expedition):
    """Handle mining with unique challenges per site."""
    
    site_name = expedition['site']
    
    st.markdown(f"### ⛏️ **ROUND 2: THE {site_name.upper()} CHALLENGE!**")
    
    if 'mining_sessions' not in expedition:
        expedition['mining_sessions'] = 0
        expedition['max_sessions'] = 3
        
        # Site-specific introduction
        intro = get_site_mining_introduction(site_name)
        st.markdown(f"*🎙️ Host: '{intro}'*")
    
    current_session = expedition['mining_sessions']
    max_sessions = expedition['max_sessions']
    
    st.markdown(f"### 🎯 **MINING ROUND {current_session + 1} OF {max_sessions}**")
    st.markdown("*🎭 Audience chanting: 'DIG! DIG! DIG!'*")
    
    if current_session < max_sessions:
        if 'current_mining_event' not in expedition:
            expedition['current_mining_event'] = generate_site_specific_mining_event(expedition)
        
        event = expedition['current_mining_event']
        
        # Dramatic mining challenge presentation
        st.markdown(f"### 🎪 **{event['title']}**")
        
        with st.container():
            st.markdown(f"""
            <div style="background: linear-gradient(45deg, #FFD700, #FF8C00); padding: 20px; border-radius: 15px; color: black; text-align: center;">
            <h3>⛏️ MINING CHALLENGE! ⛏️</h3>
            <p style="font-size: 18px; font-weight: bold;">{event['description']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Present mining choices with potential rewards shown
        if 'mining_choice' not in expedition:
            st.markdown("### 💎 **CHOOSE YOUR MINING STRATEGY!**")
            
            choice_options = []
            for i, choice in enumerate(event['choices']):
                potential_gold = choice.get('gold', 0)
                bonus_gold = potential_gold * expedition['equipment_bonus']
                total_potential = potential_gold + bonus_gold
                
                risk_level = "🔥 HIGH RISK" if choice.get('supplies', 0) < -15 else "⚠️ MODERATE" if choice.get('supplies', 0) < -5 else "✅ SAFE"
                choice_options.append(f"{chr(65+i)}) {choice['text']} (Potential: {total_potential:.1f} oz) {risk_level}")
            
            selected = st.radio("**Choose wisely:**", choice_options)
            
            # Add suspense
            if st.button("⛏️ START MINING!", type="primary"):
                if selected:  # Safety check
                    choice_index = ord(selected[0]) - ord('A')
                    selected_choice = event['choices'][choice_index]
                    expedition['mining_choice'] = selected_choice
                    
                    # Apply results with drama
                    result = apply_mining_results_with_drama(expedition, selected_choice)
                    expedition['mining_sessions'] += 1
                    
                    # Clear for next session
                    del expedition['current_mining_event']
                    if 'mining_choice' in expedition:
                        del expedition['mining_choice']
                    
                    st.balloons()
                    st.success(f"🎉 **MINING COMPLETE!** {result}")
                    st.rerun()
        
        else:
            choice = expedition['mining_choice']
            st.success(f"✅ **Strategy Executed**: {choice['text']}")
            st.markdown(f"**⛏️ Result**: {choice['result']}")
    
    else:
        st.markdown("### 🎊 **MINING PHASE COMPLETE!**")
        st.markdown("*🎙️ Host: 'Incredible performance! But wait... there's more!'*")
        
        if st.button("🎪 PROCEED TO WILD CARD ROUND!", type="primary"):
            expedition['phase'] = 'events'
            st.rerun()

def render_events_game_show(expedition):
    """Handle dramatic final events."""
    
    st.markdown("### 🎲 **ROUND 3: WILD CARD CHALLENGE!**")
    st.markdown("*🎙️ Host: 'Time for our signature Wild Card round! Anything can happen!'*")
    
    if 'final_event' not in expedition:
        expedition['final_event'] = generate_site_specific_final_event(expedition)
    
    event = expedition['final_event']
    
    # Ultra-dramatic presentation
    st.markdown(f"### 🎪 **{event['title']}**")
    
    with st.container():
        st.markdown(f"""
        <div style="background: linear-gradient(45deg, #8B00FF, #FF1493); padding: 20px; border-radius: 15px; color: white; text-align: center;">
        <h3>🎲 WILD CARD EVENT! 🎲</h3>
        <p style="font-size: 18px; font-weight: bold;">{event['description']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("*🎭 Audience: The crowd is going WILD!*")
    
    if event['choices'] and 'final_choice' not in expedition:
        st.markdown("### 🏆 **FINAL DECISION!**")
        st.markdown("*🎙️ Host: 'This choice could make or break everything! What will it be?'*")
        
        choice_options = []
        for i, choice in enumerate(event['choices']):
            drama_level = get_choice_drama_level(choice)
            choice_options.append(f"{chr(65+i)}) {choice['text']} {drama_level}")
        
        selected = st.radio("**Your final choice:**", choice_options)
        
        if st.button("🎬 MAKE THE FINAL CALL!", type="primary"):
            if selected:  # Safety check
                choice_index = ord(selected[0]) - ord('A')
                selected_choice = event['choices'][choice_index]
                expedition['final_choice'] = selected_choice
                
                apply_choice_consequences(expedition, selected_choice)
                expedition['phase'] = 'travel_back'
                
                st.success(f"🎉 **FINAL CHOICE MADE!** {selected_choice['text']}")
                st.rerun()
    
    elif 'final_choice' in expedition:
        choice = expedition['final_choice']
        st.success(f"✅ **Final Decision**: {choice['text']}")
        st.markdown(f"**🎭 Outcome**: {choice['result']}")
        
        if st.button("🏁 BEGIN THE VICTORY LAP!", type="primary"):
            expedition['phase'] = 'travel_back'
            st.rerun()

def render_finale_game_show(expedition):
    """Handle the triumphant return with game show finale."""
    
    st.markdown("### 🏁 **ROUND 4: VICTORY LAP!**")
    st.markdown("*🎙️ Host: 'Here comes our contestant, returning from their epic adventure!'*")
    
    if 'return_event' not in expedition:
        expedition['return_event'] = generate_triumphant_return_event(expedition)
    
    event = expedition['return_event']
    
    # Victory presentation
    st.markdown(f"### 🏆 **{event['title']}**")
    
    total_gold = expedition['resources_gathered']
    success_level = "LEGENDARY" if total_gold > 40 else "SPECTACULAR" if total_gold > 25 else "EXCELLENT" if total_gold > 15 else "RESPECTABLE"
    
    with st.container():
        st.markdown(f"""
        <div style="background: linear-gradient(45deg, #32CD32, #FFD700); padding: 20px; border-radius: 15px; color: black; text-align: center;">
        <h3>🏆 {success_level} PERFORMANCE! 🏆</h3>
        <p style="font-size: 18px; font-weight: bold;">{event['description']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    if event['choices'] and 'return_choice' not in expedition:
        st.markdown("### 🎊 **VICTORY CELEBRATION CHOICE!**")
        
        choice_options = [f"{chr(65+i)}) {choice['text']}" for i, choice in enumerate(event['choices'])]
        selected = st.radio("**How do you celebrate?**", choice_options)
        
        if st.button("🎉 COMPLETE THE SHOW!", type="primary"):
            choice_index = ord(selected[0]) - ord('A')
            selected_choice = event['choices'][choice_index]
            expedition['return_choice'] = selected_choice
            
            apply_choice_consequences(expedition, selected_choice)
            expedition['completed'] = True
            
            # Grand finale
            final_gold = expedition['resources_gathered']
            st.session_state.gold = st.session_state.get('gold', 0) + final_gold
            
            st.balloons()
            st.success(f"🎊 **SHOW COMPLETE!** You've won {final_gold:.1f} oz gold!")
            st.markdown("*🎙️ Host: 'What an incredible performance! Give them a hand, folks!'*")
            st.rerun()
    
    elif 'return_choice' in expedition:
        choice = expedition['return_choice']
        st.success(f"✅ **Victory Style**: {choice['text']}")
        st.markdown(f"**🎊 Celebration**: {choice['result']}")
        
        if st.button("🏆 CLAIM YOUR PRIZE!", type="primary"):
            expedition['completed'] = True
            final_gold = expedition['resources_gathered']
            st.session_state.gold = st.session_state.get('gold', 0) + final_gold
            
            st.balloons()
            st.success(f"🎊 **CONGRATULATIONS!** You've won {final_gold:.1f} oz gold!")
            st.rerun()

# Site-specific event generators for unique experiences
def generate_site_specific_travel_event(expedition):
    """Generate travel events based on specific mining sites."""
    site_name = expedition['site']
    risk_level = expedition['risk_level']
    
    site_events = {
        'Gold Creek Main Vein': {
            'title': '🏠 Hometown Hero Journey',
            'description': 'The whole town is watching as you head to the main vein! Kids are following you down the street cheering!',
            'audience_reaction': '"Go get \'em, champ!" shouts the crowd!',
            'choices': [
                {'text': 'Wave to the crowd and take the scenic route', 'result': 'You arrive feeling confident and beloved!', 'morale': 15, 'supplies': -5},
                {'text': 'Stay focused and head straight there', 'result': 'You arrive with full concentration.', 'morale': 5, 'supplies': 0}
            ]
        },
        'Grass Valley Lode': {
            'title': '💀 The Legendary Death Valley Approach',
            'description': 'You\'re approaching the most dangerous site in the territory! Vultures circle overhead as you see abandoned wagons along the trail.',
            'audience_reaction': 'The audience gasps in terror!',
            'choices': [
                {'text': 'Hire extra guards immediately', 'result': 'You feel safer but your wallet feels lighter.', 'morale': 10, 'supplies': -20},
                {'text': 'Trust in your skills and push forward', 'result': 'You steel yourself for the challenge ahead.', 'morale': -5, 'supplies': 5},
                {'text': 'Scout ahead carefully first', 'result': 'You gather valuable intelligence.', 'morale': 0, 'supplies': -10}
            ]
        },
        'Angels Reef': {
            'title': '👼 The Heavenly Ascent',
            'description': 'You\'re climbing toward the legendary Angels Reef! The path winds up through clouds as locals whisper about divine fortune.',
            'audience_reaction': 'The crowd chants: "Angels! Angels! Angels!"',
            'choices': [
                {'text': 'Stop at the shrine for a blessing', 'result': 'You feel spiritually prepared for the challenge.', 'morale': 20, 'supplies': -5},
                {'text': 'Power through with determination', 'result': 'You arrive quickly but breathless.', 'morale': 0, 'supplies': -15}
            ]
        }
    }
    
    # Default event for unmapped sites
    default_event = {
        'title': f'🗺️ Journey to {site_name}',
        'description': f'You\'re heading toward the mysterious {site_name}! The path ahead is uncertain but adventure awaits!',
        'audience_reaction': 'The crowd cheers with anticipation!',
        'choices': [
            {'text': 'Take the safe, well-traveled route', 'result': 'You arrive safely but predictably.', 'morale': 5, 'supplies': 0},
            {'text': 'Risk the shortcut through unknown territory', 'result': 'You save time but face unexpected challenges.', 'morale': -5, 'supplies': 10}
        ]
    }
    
    return site_events.get(site_name, default_event)

def get_site_mining_introduction(site_name):
    """Get site-specific mining introductions."""
    intros = {
        'Gold Creek Main Vein': "This is it, folks! Our contestant is about to mine the town's pride and joy! This vein has never let anyone down!",
        'Grass Valley Lode': "Ladies and gentlemen, we have a DAREDEVIL in the house! They're about to tackle the most dangerous mine in California!",
        'Angels Reef': "Heavenly riches await! Our brave soul is about to mine where angels fear to tread!",
        'Feather Fork #3': "Time for some river action! Will our contestant strike gold in these rushing waters?",
        'Dead Man\'s Gulch': "Are you ready for a HORROR STORY? This site is literally named after the miners who never returned!",
        'Widow\'s Peak Mine': "Spooky times ahead! Legend says the widow's ghost still guards the treasure within!"
    }
    
    return intros.get(site_name, f"Here we go! Time to see what {site_name} has in store for our brave contestant!")

def generate_site_specific_mining_event(expedition):
    """Generate unique mining events for each site."""
    site_name = expedition['site']
    
    site_events = {
        'Gold Creek Main Vein': {
            'title': '🏠 Hometown Advantage',
            'description': 'You know these tunnels like the back of your hand! Plus, your neighbors are cheering you on from above!',
            'choices': [
                {'text': 'Use your local knowledge for precision mining', 'result': 'Your expertise pays off beautifully!', 'gold': 20, 'supplies': -5},
                {'text': 'Show off for the hometown crowd', 'result': 'Spectacular display but risky moves!', 'gold': 15, 'supplies': -15, 'morale': 20},
                {'text': 'Play it safe and steady', 'result': 'Reliable hometown mining at its finest.', 'gold': 12, 'supplies': -3}
            ]
        },
        'Grass Valley Lode': {
            'title': '💀 Survival Mining',
            'description': 'The walls are unstable, your team is nervous, but the gold is EVERYWHERE! This is the challenge of a lifetime!',
            'choices': [
                {'text': 'Go all-in despite the danger', 'result': 'MASSIVE RISK, MASSIVE REWARD!', 'gold': 35, 'supplies': -25, 'morale': -20},
                {'text': 'Extract carefully with maximum safety', 'result': 'Slow but steady in dangerous territory.', 'gold': 18, 'supplies': -8},
                {'text': 'Grab what you can and get out', 'result': 'Quick escape with modest gains.', 'gold': 12, 'supplies': -5, 'morale': 10}
            ]
        },
        'Angels Reef': {
            'title': '👼 Divine Intervention',
            'description': 'A shaft of heavenly light illuminates a vein of pure gold! Is this a miracle or just incredible luck?',
            'choices': [
                {'text': 'Mine reverently, thanking the heavens', 'result': 'The angels smile upon your respectful approach!', 'gold': 25, 'supplies': -5, 'morale': 25},
                {'text': 'Mine aggressively while the light lasts', 'result': 'You rush to capitalize on the divine moment!', 'gold': 22, 'supplies': -15},
                {'text': 'Study the phenomenon first', 'result': 'You learn something amazing about the site!', 'gold': 15, 'supplies': -3, 'morale': 15}
            ]
        }
    }
    
    # Default mining event
    default_event = {
        'title': f'⛏️ The {site_name} Challenge',
        'description': f'You\'ve reached the heart of {site_name}! The gold is here, but so are the challenges!',
        'choices': [
            {'text': 'Mine with maximum efficiency', 'result': 'Professional mining technique pays off!', 'gold': 18, 'supplies': -10},
            {'text': 'Take risks for bigger rewards', 'result': 'High risk, high reward strategy!', 'gold': 25, 'supplies': -20, 'morale': -10},
            {'text': 'Focus on safety and conservation', 'result': 'Steady and reliable approach.', 'gold': 12, 'supplies': -5, 'morale': 10}
        ]
    }
    
    return site_events.get(site_name, default_event)

def generate_site_specific_final_event(expedition):
    """Generate dramatic final events based on site."""
    site_name = expedition['site']
    total_gold = expedition['resources_gathered']
    
    site_events = {
        'Dead Man\'s Gulch': {
            'title': '👻 THE GHOST OF DEAD MAN\'S GULCH',
            'description': 'A spectral figure appears! "Turn back!" it wails, "This gold is cursed!" The temperature drops 20 degrees!',
            'choices': [
                {'text': 'Stand your ground and demand passage', 'result': 'The ghost respects your courage and vanishes!', 'gold': 5, 'morale': 15},
                {'text': 'Offer to share the gold with the spirit', 'result': 'The ghost is moved by your generosity!', 'gold': -3, 'morale': 25},
                {'text': 'Run away screaming', 'result': 'You escape but drop some gold in panic!', 'gold': -8, 'morale': -15, 'supplies': 20}
            ]
        },
        'Grass Valley Lode': {
            'title': '💥 CAVE-IN CATASTROPHE',
            'description': 'RUMBLE! The mountain is collapsing! You have seconds to choose: save your team, save the gold, or save yourself!',
            'choices': [
                {'text': 'Hero move: Save everyone first', 'result': 'You\'re a hero! The town will remember this forever!', 'gold': -5, 'morale': 50},
                {'text': 'Grab the gold and run', 'result': 'You escaped with treasure but at what cost?', 'gold': 10, 'morale': -25},
                {'text': 'Coordinate a careful evacuation', 'result': 'Leadership under pressure pays off!', 'gold': 2, 'morale': 20}
            ]
        },
        'Angels Reef': {
            'title': '🌟 MIRACLE AT ANGELS REEF',
            'description': 'The ground glows with ethereal light and reveals a hidden chamber filled with the purest gold ever seen!',
            'choices': [
                {'text': 'Take only what you need', 'result': 'Your restraint is rewarded by the heavens!', 'gold': 8, 'morale': 30},
                {'text': 'Fill every bag you have', 'result': 'Greed clouds your judgment but fills your pockets!', 'gold': 20, 'morale': -10},
                {'text': 'Share the discovery with other miners', 'result': 'Your generosity creates lifelong allies!', 'gold': 5, 'morale': 35}
            ]
        }
    }
    
    # High gold discovery event
    if total_gold > 30:
        return {
            'title': '🏆 LEGENDARY DISCOVERY',
            'description': f'Word of your incredible {total_gold:.1f} oz haul has spread! Reporters, bandits, and admirers are all heading your way!',
            'choices': [
                {'text': 'Hold a press conference', 'result': 'You become a mining celebrity!', 'gold': 0, 'morale': 25},
                {'text': 'Sneak out the back way', 'result': 'You avoid attention but miss opportunities.', 'gold': 0, 'morale': 0},
                {'text': 'Hire bodyguards immediately', 'result': 'Safety first with your newfound wealth!', 'gold': -5, 'morale': 10}
            ]
        }
    
    return site_events.get(site_name, {
        'title': f'🎲 The {site_name} Finale',
        'description': f'Your adventure at {site_name} reaches its climax! What final challenge awaits?',
        'choices': [
            {'text': 'Face the challenge head-on', 'result': 'Courage pays off in the final moments!', 'gold': 5, 'morale': 15},
            {'text': 'Use cunning over courage', 'result': 'Smart thinking saves the day!', 'gold': 3, 'morale': 10}
        ]
    })

def generate_triumphant_return_event(expedition):
    """Generate celebratory return events."""
    total_gold = expedition['resources_gathered']
    site_name = expedition['site']
    
    if total_gold > 35:
        return {
            'title': '🏆 TRIUMPHANT HERO\'S RETURN',
            'description': f'The whole town turns out to celebrate your LEGENDARY {total_gold:.1f} oz haul from {site_name}! There\'s a parade in your honor!',
            'choices': [
                {'text': 'Grand parade down Main Street', 'result': 'You bask in the adoration of Gold Creek!', 'morale': 30},
                {'text': 'Humble victory lap', 'result': 'Your modesty impresses everyone.', 'morale': 20},
                {'text': 'Donate some gold to the town', 'result': 'Your generosity makes you a living legend!', 'gold': -10, 'morale': 50}
            ]
        }
    elif total_gold > 20:
        return {
            'title': '🎉 SUCCESSFUL EXPEDITION RETURN',
            'description': f'You return to Gold Creek with an impressive {total_gold:.1f} oz! The townsfolk gather to hear your tales!',
            'choices': [
                {'text': 'Tell exciting stories at the saloon', 'result': 'You become the talk of the town!', 'morale': 20},
                {'text': 'Quietly bank your earnings', 'result': 'Discretion is the better part of valor.', 'morale': 10}
            ]
        }
    else:
        return {
            'title': '🏠 Respectable Return',
            'description': f'You return from {site_name} with {total_gold:.1f} oz of honest gold! Not spectacular, but respectable work!',
            'choices': [
                {'text': 'Share lessons learned with others', 'result': 'Your wisdom helps future miners!', 'morale': 15}
            ]
        }

def get_choice_risk_indicator(choice):
    """Get visual risk indicators for choices."""
    supplies_cost = choice.get('supplies', 0)
    morale_impact = choice.get('morale', 0)
    
    if supplies_cost < -15 or morale_impact < -15:
        return "🔥 EXTREME"
    elif supplies_cost < -10 or morale_impact < -10:
        return "⚠️ HIGH RISK"
    elif supplies_cost < -5 or morale_impact < -5:
        return "🟡 MODERATE"
    else:
        return "✅ SAFE"

def get_choice_drama_level(choice):
    """Get drama level indicators."""
    gold_impact = abs(choice.get('gold', 0))
    morale_impact = abs(choice.get('morale', 0))
    
    if gold_impact > 15 or morale_impact > 25:
        return "🎭 EPIC DRAMA"
    elif gold_impact > 8 or morale_impact > 15:
        return "🎪 HIGH DRAMA"
    else:
        return "📺 DRAMATIC"

def apply_mining_results_with_drama(expedition, choice):
    """Apply mining results with dramatic flair."""
    base_gold = choice.get('gold', 0)
    
    # Apply equipment bonus
    bonus_gold = base_gold * expedition['equipment_bonus']
    total_gold = base_gold + bonus_gold
    
    expedition['resources_gathered'] += total_gold
    
    # Apply other consequences
    apply_choice_consequences(expedition, choice)
    
    # Create dramatic result message
    if total_gold > 20:
        return f"INCREDIBLE! You struck {total_gold:.1f} oz of gold! The audience goes WILD!"
    elif total_gold > 10:
        return f"Excellent work! {total_gold:.1f} oz added to your collection!"
    elif total_gold > 5:
        return f"Solid results! {total_gold:.1f} oz of honest gold!"
    else:
        return f"Every ounce counts! {total_gold:.1f} oz secured!"

def render_travel_out_phase(expedition):
    """Handle the journey to the mining site."""
    
    st.markdown(f"### 🗺️ Journey to {expedition['site']}")
    
    # Generate travel event based on risk level
    if 'travel_event' not in expedition:
        expedition['travel_event'] = generate_travel_event(expedition['risk_level'])
    
    event = expedition['travel_event']
    st.markdown(f"**{event['title']}**")
    st.markdown(event['description'])
    
    # Present choices
    if event['choices'] and 'travel_choice' not in expedition:
        choice = st.radio("What do you do?", [c['text'] for c in event['choices']])
        
        if st.button("Confirm Decision"):
            # Find selected choice
            selected_choice = next(c for c in event['choices'] if c['text'] == choice)
            expedition['travel_choice'] = selected_choice
            
            # Apply consequences
            apply_choice_consequences(expedition, selected_choice)
            expedition['phase'] = 'mining'
            st.rerun()
    
    elif 'travel_choice' in expedition:
        choice = expedition['travel_choice']
        st.success(f"✅ **Decision Made**: {choice['text']}")
        st.markdown(f"**Result**: {choice['result']}")
        
        if st.button("Continue to Mining Site"):
            expedition['phase'] = 'mining'
            st.rerun()

def render_mining_phase(expedition):
    """Handle the actual mining operations."""
    
    st.markdown(f"### ⛏️ Mining Operations at {expedition['site']}")
    
    if 'mining_sessions' not in expedition:
        expedition['mining_sessions'] = 0
        expedition['max_sessions'] = 3  # Can do 3 mining sessions per expedition
    
    current_session = expedition['mining_sessions']
    max_sessions = expedition['max_sessions']
    
    st.markdown(f"**Mining Session {current_session + 1} of {max_sessions}**")
    
    if current_session < max_sessions:
        if 'current_mining_event' not in expedition:
            expedition['current_mining_event'] = generate_mining_event(expedition)
        
        event = expedition['current_mining_event']
        st.markdown(f"**{event['title']}**")
        st.markdown(event['description'])
        
        # Present mining choices
        if 'mining_choice' not in expedition:
            choice = st.radio("Choose your mining approach:", [c['text'] for c in event['choices']])
            
            if st.button("Execute Mining Plan"):
                selected_choice = next(c for c in event['choices'] if c['text'] == choice)
                expedition['mining_choice'] = selected_choice
                
                # Apply mining results
                apply_mining_results(expedition, selected_choice)
                expedition['mining_sessions'] += 1
                
                # Clear current event for next session
                del expedition['current_mining_event']
                if 'mining_choice' in expedition:
                    del expedition['mining_choice']
                
                st.rerun()
        else:
            choice = expedition['mining_choice']
            st.success(f"✅ **Action Taken**: {choice['text']}")
            st.markdown(f"**Result**: {choice['result']}")
    
    else:
        st.info("Mining operations complete!")
        if st.button("Proceed to Final Events"):
            expedition['phase'] = 'events'
            st.rerun()

def render_events_phase(expedition):
    """Handle random events and final challenges."""
    
    st.markdown("### 🎲 Unexpected Events")
    
    if 'final_event' not in expedition:
        expedition['final_event'] = generate_final_event(expedition)
    
    event = expedition['final_event']
    st.markdown(f"**{event['title']}**")
    st.markdown(event['description'])
    
    if event['choices'] and 'final_choice' not in expedition:
        choice = st.radio("How do you respond?", [c['text'] for c in event['choices']])
        
        if st.button("Make Decision"):
            selected_choice = next(c for c in event['choices'] if c['text'] == choice)
            expedition['final_choice'] = selected_choice
            
            apply_choice_consequences(expedition, selected_choice)
            expedition['phase'] = 'travel_back'
            st.rerun()
    
    elif 'final_choice' in expedition:
        choice = expedition['final_choice']
        st.success(f"✅ **Decision Made**: {choice['text']}")
        st.markdown(f"**Result**: {choice['result']}")
        
        if st.button("Begin Journey Home"):
            expedition['phase'] = 'travel_back'
            st.rerun()

def render_travel_back_phase(expedition):
    """Handle the return journey with potential complications."""
    
    st.markdown("### 🏠 Return Journey")
    
    if 'return_event' not in expedition:
        expedition['return_event'] = generate_return_event(expedition)
    
    event = expedition['return_event']
    st.markdown(f"**{event['title']}**")
    st.markdown(event['description'])
    
    if event['choices'] and 'return_choice' not in expedition:
        choice = st.radio("Final decision:", [c['text'] for c in event['choices']])
        
        if st.button("Complete Expedition"):
            selected_choice = next(c for c in event['choices'] if c['text'] == choice)
            expedition['return_choice'] = selected_choice
            
            apply_choice_consequences(expedition, selected_choice)
            expedition['completed'] = True
            
            # Award final gold
            final_gold = expedition['resources_gathered']
            st.session_state.gold = st.session_state.get('gold', 0) + final_gold
            
            st.success(f"🎉 Expedition complete! Gained {final_gold:.1f} oz gold!")
            st.rerun()
    
    elif 'return_choice' in expedition:
        choice = expedition['return_choice']
        st.success(f"✅ **Final Decision**: {choice['text']}")
        st.markdown(f"**Result**: {choice['result']}")
        
        if st.button("Complete Expedition"):
            expedition['completed'] = True
            final_gold = expedition['resources_gathered']
            st.session_state.gold = st.session_state.get('gold', 0) + final_gold
            st.success(f"🎉 Expedition complete! Gained {final_gold:.1f} oz gold!")
            st.rerun()

def render_expedition_results(expedition):
    """Show final expedition results."""
    
    st.markdown(f"### 📊 Expedition to {expedition['site']} - Complete!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Gold Gathered", f"{expedition['resources_gathered']:.1f} oz")
        st.metric("Total Cost", f"{expedition['cost']} oz")
    
    with col2:
        profit = expedition['resources_gathered'] - expedition['cost']
        st.metric("Net Profit", f"{profit:.1f} oz", delta=f"{profit:.1f}")
        st.metric("Final Morale", f"{expedition['team_morale']}%")
    
    # Show event summary
    with st.expander("📜 Expedition Log"):
        for event in expedition.get('events', []):
            st.markdown(f"• {event}")

# Event Generation Functions
def generate_travel_event(risk_level):
    """Generate random travel events based on risk level."""
    import random
    
    if risk_level <= 2:
        events = [
            {
                'title': '🌤️ Clear Weather',
                'description': 'The journey is proceeding smoothly with clear skies and good visibility.',
                'choices': [
                    {'text': 'Make good time', 'result': 'You arrive early and well-rested.', 'morale': 5, 'supplies': 0},
                    {'text': 'Take it slow and careful', 'result': 'You conserve energy for the mining ahead.', 'morale': 0, 'supplies': 5}
                ]
            }
        ]
    else:
        events = [
            {
                'title': '⚠️ Bandit Signs',
                'description': 'Your scout reports signs of bandit activity ahead - fresh horse tracks and abandoned campsites.',
                'choices': [
                    {'text': 'Take the direct route anyway', 'result': 'You push through but stay alert.', 'morale': -10, 'supplies': 0},
                    {'text': 'Take a longer, safer detour', 'result': 'You avoid trouble but use extra supplies.', 'morale': 0, 'supplies': -15},
                    {'text': 'Wait and observe', 'result': 'You gather intelligence and proceed safely.', 'morale': 5, 'supplies': -5}
                ]
            }
        ]
    
    return random.choice(events)

def generate_mining_event(expedition):
    """Generate mining events based on site characteristics."""
    import random
    
    site_data = expedition['site_data']
    
    if site_data['status'] == 'active':
        events = [
            {
                'title': '💎 Rich Vein Discovered',
                'description': 'Your team has found a particularly rich section of ore!',
                'choices': [
                    {'text': 'Extract carefully for maximum yield', 'result': 'You gather high-quality gold slowly.', 'gold': 15, 'supplies': -10},
                    {'text': 'Mine aggressively for speed', 'result': 'You gather decent gold quickly.', 'gold': 10, 'supplies': -5},
                    {'text': 'Study the formation first', 'result': 'You learn about the site for future expeditions.', 'gold': 8, 'supplies': -3}
                ]
            }
        ]
    else:
        events = [
            {
                'title': '🔍 Hidden Cache',
                'description': 'You discover an old miner\'s hidden stash!',
                'choices': [
                    {'text': 'Take everything you can carry', 'result': 'You find valuable items but anger local spirits.', 'gold': 12, 'morale': -15},
                    {'text': 'Take only what you need', 'result': 'You find some gold and useful supplies.', 'gold': 8, 'supplies': 10},
                    {'text': 'Leave it for the next person', 'result': 'Your team respects your honor.', 'gold': 2, 'morale': 20}
                ]
            }
        ]
    
    return random.choice(events)

def generate_final_event(expedition):
    """Generate final events based on expedition progress."""
    import random
    
    events = [
        {
            'title': '🌊 Flash Flood Warning',
            'description': 'Storm clouds are gathering and the creek is rising fast!',
            'choices': [
                {'text': 'Evacuate immediately', 'result': 'You escape safely but lose some equipment.', 'gold': 0, 'supplies': -20},
                {'text': 'Secure the gold first', 'result': 'You save your gold but risk everything.', 'gold': 5, 'morale': -10},
                {'text': 'Help other miners evacuate', 'result': 'You earn respect but lose time.', 'gold': -2, 'morale': 15}
            ]
        }
    ]
    
    return random.choice(events)

def generate_return_event(expedition):
    """Generate return journey events."""
    import random
    
    if expedition['resources_gathered'] > 20:
        events = [
            {
                'title': '👁️ You\'re Being Watched',
                'description': 'With your heavy gold pouches, you\'ve attracted unwanted attention.',
                'choices': [
                    {'text': 'Travel at night', 'result': 'You avoid bandits but face other dangers.', 'gold': 0, 'supplies': -10},
                    {'text': 'Hire additional guards', 'result': 'You spend gold for safety.', 'gold': -5, 'morale': 10},
                    {'text': 'Trust in your preparations', 'result': 'You arrive safely with everything intact.', 'gold': 0, 'morale': 0}
                ]
            }
        ]
    else:
        events = [
            {
                'title': '🏠 Peaceful Return',
                'description': 'The journey home is uneventful and your team is in good spirits.',
                'choices': [
                    {'text': 'Share stories at camp', 'result': 'Everyone enjoys the camaraderie.', 'gold': 0, 'morale': 10}
                ]
            }
        ]
    
    return random.choice(events)

def apply_choice_consequences(expedition, choice):
    """Apply the consequences of player choices."""
    
    if 'gold' in choice:
        expedition['resources_gathered'] += choice['gold']
    
    if 'morale' in choice:
        expedition['team_morale'] = max(0, min(100, expedition['team_morale'] + choice['morale']))
    
    if 'supplies' in choice:
        expedition['supplies_remaining'] = max(0, min(100, expedition['supplies_remaining'] + choice['supplies']))
    
    # Log the event
    if 'events' not in expedition:
        expedition['events'] = []
    
    expedition['events'].append(f"{choice['text']}: {choice['result']}")

def apply_mining_results(expedition, choice):
    """Apply mining session results."""
    
    base_gold = choice.get('gold', 0)
    
    # Apply equipment bonus
    bonus_gold = base_gold * expedition['equipment_bonus']
    total_gold = base_gold + bonus_gold
    
    expedition['resources_gathered'] += total_gold
    
    # Apply other consequences
    apply_choice_consequences(expedition, choice)
    
    # Add to event log
    if bonus_gold > 0:
        expedition['events'].append(f"Equipment bonus: +{bonus_gold:.1f} oz gold")

if __name__ == "__main__":
    render_gold_map_folium()
