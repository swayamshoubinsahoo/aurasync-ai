import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="AuraSync | Green Infrastructure",
    page_icon="🌿",
    layout="wide"
)

st.title("🌿 AuraSync: Green Infrastructure")
st.caption("Edge-Vision & IoT-Driven Dynamic Commercial Energy & HVAC Management System")
st.markdown("---")

st.sidebar.header("🕹️ Zone Environment Controls")
selected_zone = st.sidebar.selectbox("Select Building Zone", ["Zone 1: Tech Hub", "Zone 2: Conference Suite", "Zone 3: Cafeteria & Lounge"])
occupancy_count = st.sidebar.slider("Simulated Occupancy (People)", min_value=0, max_value=80, value=28)
ambient_temp = st.sidebar.slider("External Ambient Temperature (°C)", min_value=15, max_value=42, value=33)
solar_irradiance = st.sidebar.slider("Ambient Solar Exposure (Lux)", min_value=100, max_value=2000, value=1100)

if occupancy_count == 0:
    hvac_status = "Eco / Standby"
    hvac_target_temp = 28.0
    fan_speed = "Off"
    lighting_level = 10
    energy_draw = 0.8
elif occupancy_count < 15:
    hvac_status = "Active - Low"
    hvac_target_temp = 24.5
    fan_speed = "Low"
    lighting_level = max(20, 100 - int(solar_irradiance / 20))
    energy_draw = 3.2
else:
    hvac_status = "Active - Dynamic"
    hvac_target_temp = round(23.0 - (occupancy_count * 0.05), 1)
    fan_speed = "Adaptive High"
    lighting_level = max(35, 100 - int(solar_irradiance / 22))
    energy_draw = round(4.5 + (occupancy_count * 0.12), 2)

legacy_energy_draw = 14.5
savings_pct = round(((legacy_energy_draw - energy_draw) / legacy_energy_draw) * 100, 1)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Zone Occupancy", f"{occupancy_count} Persons")
col2.metric("Dynamic HVAC Target", f"{hvac_target_temp} °C", delta=hvac_status)
col3.metric("Current Power Draw", f"{energy_draw} kW", delta=f"-{savings_pct}% vs Legacy", delta_color="inverse")
col4.metric("Smart Lighting Level", f"{lighting_level}%", delta="Solar Offset Active")

st.markdown("---")

tab1, tab2 = st.tabs(["📊 Real-Time Energy Optimization", "🏢 Multi-Zone Microclimate Analytics"])

with tab1:
    col_chart1, col_chart2 = st.columns(2)
    hours = [f"{h:02d}:00" for h in range(24)]
    legacy_profile = [5.0 if (h < 7 or h > 20) else 14.5 for h in range(24)]
    aurasync_profile = [1.0 if (h < 7 or h > 21) else (5.2 + np.sin(h) * 1.5 if 9 <= h <= 17 else 3.1) for h in range(24)]

    chart_df = pd.DataFrame({
        "Hour": hours,
        "Legacy Static Baseline (kW)": legacy_profile,
        "AuraSync AI Dynamic (kW)": aurasync_profile
    })
    
    with col_chart1:
        st.subheader("24-Hour Energy Profile (Legacy vs AuraSync)")
        fig = px.line(chart_df, x="Hour", y=["Legacy Static Baseline (kW)", "AuraSync AI Dynamic (kW)"],
                      color_discrete_map={"Legacy Static Baseline (kW)": "#FF4B4B", "AuraSync AI Dynamic (kW)": "#00CC96"})
        st.plotly_chart(fig, use_container_width=True)

    with col_chart2:
        st.subheader("Autonomous Actuator Status")
        st.info(f"**Zone Operational Status:** {hvac_status}")
        st.write(f"- **Fan Circulation:** `{fan_speed}`")
        st.write(f"- **External Thermal Load:** `{ambient_temp} °C`")
        st.write(f"- **Luminance Harvested:** `{solar_irradiance} Lux`")
        st.progress(lighting_level / 100, text=f"Dimming Level: {lighting_level}%")
        st.success(f"Est. Daily CO2 Avoidance: **{round(savings_pct * 0.42, 2)} kg CO2e/day**")

with tab2:
    st.subheader("Zone Occupancy vs Energy Correlation")
    zone_data = pd.DataFrame({
        "Zone": ["Zone 1: Tech Hub", "Zone 2: Conference Suite", "Zone 3: Cafeteria & Lounge"],
        "Occupancy": [occupancy_count, 12, 4],
        "Energy Demand (kW)": [energy_draw, 2.8, 1.2],
        "Carbon Savings (%)": [savings_pct, 44.0, 68.5]
    })
    st.dataframe(zone_data, use_container_width=True)