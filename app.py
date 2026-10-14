import streamlit as st
import simpy
import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="JIC Smart Campus Energy Platform",
    page_icon="⚡",
    layout="wide"
)

# --- ADVANCED CSS STYLING (ENTERPRISE GRADE) ---
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
    }
    .hero-container {
        background: rgba(22, 27, 34, 0.8);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(48, 54, 61, 0.9);
        padding: 25px;
        border-radius: 16px;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    .stMetric {
        background: linear-gradient(145deg, #161b22, #0d1117);
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #30363d;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .stMetric label {
        color: #8b949e !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #58a6ff !important;
        font-weight: 700 !important;
    }
    h1, h2, h3 {
        color: #f0f6fc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .stButton button {
        background: linear-gradient(90deg, #1f6feb 0%, #388bfd 100%);
        color: white;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        padding: 12px 24px;
        transition: 0.3s ease;
    }
    .stButton button:hover {
        background: linear-gradient(90deg, #388bfd 0%, #1f6feb 100%);
        box-shadow: 0 0 15px rgba(56, 139, 253, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown("""
<div class="hero-container">
    <h1 style="margin:0; font-size: 2.2rem;">🏛️ Jeddah International College (JIC)</h1>
    <h3 style="color: #58a6ff; margin-top: 5px; font-size: 1.3rem;">Smart Campus Energy & Microgrid Intelligence Platform</h3>
    <p style="color: #8b949e; margin-top: 8px; font-size: 1.0rem;">
        Industrial Engineering Capstone Project • <b>Capacity Planning & M/M/c Queueing Models</b> • 
        Peak-Load Electricity Management & Economic Optimization (SAR)
    </p>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTROLS ---
st.sidebar.header("🎛️ JIC Campus Infrastructure & Controls")

with st.sidebar.expander("🏢 Buildings & Operating Hours", expanded=True):
    num_buildings = st.slider("Active Campus Buildings", 1, 10, 4, 1)
    num_transformers = st.slider("Substations / Power Units [c]", 1, 100, 25, 5)
    work_hours = st.slider("Daily Operation Window (Hours)", 4, 16, 8, 1)

with st.sidebar.expander("⚡ Power Demand & Peak Waves", expanded=True):
    base_load = st.slider("Base Energy Demand [λ] (kW)", 50.0, 1000.0, 250.0, 25.0)
    overload_limit = st.slider("Critical Overload Threshold (kW)", 200, 2000, 800, 50)

with st.sidebar.expander("💰 Tariff & Blackout Penalties (SAR)", expanded=True):
    peak_tariff = st.slider("Peak Electricity Tariff (SAR/kWh)", 0.10, 2.00, 0.45, 0.05)
    blackout_penalty = st.slider("Blackout / Deficit Penalty (SAR)", 1000, 50000, 15000, 1000)

# --- SIMULATION CORE LOGIC ---
def run_jic_energy_simulation(hours, base_lam, transformers, limit):
    env = simpy.Environment()
    power_units = simpy.Resource(env, capacity=transformers)
    
    sim_duration = hours * 60  # convert to minutes
    demand_history = []
    time_stamps = []
    overload_events = 0
    total_energy_consumed = 0.0

    def campus_load_generator(env, base_lam):
        nonlocal overload_events, total_energy_consumed
        t = 0
        while True:
            current_time = env.now
            # Sinusoidal peak wave during middle of academic day
            peak_multiplier = 1.0 + 1.6 * np.sin(np.pi * current_time / sim_duration)
            current_demand = max(10.0, base_lam * peak_multiplier + random.gauss(0, 20))
            
            demand_history.append(current_demand)
            time_stamps.append(current_time)
            total_energy_consumed += current_demand * (1/60) # kWh approx
            
            if current_demand > limit:
                overload_events += 1
                
            yield env.timeout(5) # sample every 5 minutes

    env.process(campus_load_generator(env, base_load))
    env.run(until=sim_duration)
    
    return demand_history, time_stamps, overload_events, total_energy_consumed

# --- EXECUTION BUTTON ---
col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
with col_b2:
    run_sim_btn = st.button("🚀 Run JIC Campus Energy Simulation", use_container_width=True)

if run_sim_btn:
    with st.spinner("🔄 Simulating JIC microgrid power loads and computing economic impact..."):
        random.seed(42)
        demands, timestamps, overloads, total_energy = run_jic_energy_simulation(
            work_hours, base_load, num_transformers, overload_limit
        )
        
        max_demand = max(demands) if demands else 0
        avg_demand = sum(demands) / len(demands) if demands else 0
        
        # Financial calculations
        energy_cost = total_energy * peak_tariff
        penalty_cost = overloads * (blackout_penalty / 10) # weighted penalty distribution
        total_economic_impact = energy_cost + penalty_cost
        
        reliability_pct = max(0.0, 100.0 - (overloads / len(demands) * 100)) if len(demands) > 0 else 100.0

        # --- SECTION 1: EXECUTIVE KPIs ---
        st.markdown("### 📊 JIC Campus Executive Performance Dashboard")
        
        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("Active Buildings", f"{num_buildings}")
        k2.metric("Peak Demand Recorded", f"{max_demand:.1f} kW")
        k3.metric("Grid Reliability", f"{reliability_pct:.1f}%")
        k4.metric("Overload Incidents", f"{overloads}")
        k5.metric("Total Energy (kWh)", f"{total_energy:,.0f}")

        # --- SECTION 2: ECONOMIC IMPACT ---
        st.markdown("### 💵 Microgrid Economic & Penalty Analysis")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Base Energy Consumption Cost", f"{energy_cost:,.2f} SAR")
        c2.metric("Deficit & Outage Penalty", f"{penalty_cost:,.2f} SAR")
        c3.metric("Total Objective Economic Function", f"{total_economic_impact:,.2f} SAR")

        # --- SECTION 3: CHARTS ---
        st.markdown("---")
        st.markdown("### 📈 Campus Power Load vs. Critical Overload Threshold")
        
        fig, ax = plt.subplots(figsize=(11, 4.5))
        fig.patch.set_facecolor('#0d1117')
        ax.set_facecolor('#161b22')
        
        ax.plot(timestamps, demands, color='#388bfd', linewidth=2, label='Campus Power Demand [kW]')
        ax.axhline(y=overload_limit, color='#f85149', linestyle='--', linewidth=1.8, label=f'Critical Overload Limit ({overload_limit} kW)')
        
        ax.set_xlabel("Simulation Time (Minutes from Opening)", color='#f0f6fc', fontsize=11)
        ax.set_ylabel("Power Demand (kW)", color='#f0f6fc', fontsize=11)
        ax.tick_params(colors='#8b949e', labelsize=10)
        ax.grid(True, linestyle='--', alpha=0.3, color='#30363d')
        ax.legend(facecolor='#161b22', edgecolor='#30363d', labelcolor='#f0f6fc')
        for spine in ax.spines.values():
            spine.set_color('#30363d')
            
        st.pyplot(fig)
        
        st.success("✨ JIC Campus simulation completed successfully. Ready for your custom adjustments!")
else:
    st.markdown("""
        <div style="text-align: center; padding: 40px; background: rgba(22, 27, 34, 0.4); border-radius: 12px; border: 1px dashed #30363d;">
            <h3 style="color: #8b949e;">Platform Ready</h3>
            <p style="color: #6e7681;">Configure your JIC campus parameters on the sidebar and click the button above to generate the live simulation.</p>
        </div>
    """, unsafe_allow_html=True)
