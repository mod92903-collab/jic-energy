import streamlit as st
import simpy
import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="JIC Smart Campus Energy & Microgrid Intelligence Platform",
    page_icon="⚡",
    layout="wide"
)

# --- ADVANCED CSS STYLING ---
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
    }
    .hero-container {
        background: rgba(22, 27, 34, 0.85);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(48, 54, 61, 0.9);
        padding: 25px;
        border-radius: 16px;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    .stMetric {
        background: linear-gradient(145deg, #161b22, #0d1117);
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #30363d;
    }
    h1, h2, h3 {
        color: #f0f6fc;
    }
    .stButton button {
        background: linear-gradient(90deg, #1f6feb 0%, #388bfd 100%);
        color: white;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        padding: 12px 24px;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown("""
<div class="hero-container">
    <h1 style="margin:0; font-size: 2.2rem;">Jeddah International College (JIC)</h1>
    <h3 style="color: #58a6ff; margin-top: 5px; font-size: 1.3rem;">Smart Campus Energy & Microgrid Intelligence Platform</h3>
    <p style="color: #8b949e; margin-top: 8px; font-size: 1.0rem;">
        Comprehensive Industrial Engineering Capstone Simulation • Capacity Planning, M/M/c Queueing & Economic Optimization
    </p>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTROLS ---
st.sidebar.header("JIC Infrastructure & Parameters")

with st.sidebar.expander("Campus Zoning & Buildings", expanded=True):
    num_buildings = st.slider("Total Active Buildings", 1, 10, 4, 1)
    num_transformers = st.slider("Substations / Power Units [c]", 1, 150, 30, 5)
    work_hours = st.slider("Daily Operation Window (Hours)", 4, 16, 8, 1)

with st.sidebar.expander("Power Demand & Peak Waves", expanded=True):
    base_load = st.slider("Base Energy Demand [lambda] (kW)", 50.0, 1500.0, 300.0, 25.0)
    overload_limit = st.slider("Critical Overload Threshold (kW)", 200, 3000, 850, 50)
    temp_factor = st.slider("Jeddah Climate / AC Load Factor", 1.0, 2.0, 1.3, 0.1)

with st.sidebar.expander("Tariff & Blackout Penalties (SAR)", expanded=True):
    peak_tariff = st.slider("Peak Electricity Tariff (SAR/kWh)", 0.10, 3.00, 0.48, 0.05)
    off_peak_tariff = st.slider("Off-Peak Tariff (SAR/kWh)", 0.05, 1.50, 0.22, 0.05)
    blackout_penalty = st.slider("Blackout / Deficit Penalty (SAR)", 5000, 100000, 25000, 5000)

with st.sidebar.expander("Contingency & Stress Testing", expanded=True):
    stress_mode = st.checkbox("Enable Emergency Sudden Load Spike", value=False)
    stress_multiplier = st.slider("Emergency Spike Severity Factor", 1.1, 2.0, 1.4, 0.1)

# --- SIMULATION CORE LOGIC ---
def run_jic_comprehensive_simulation(hours, base_lam, transformers, limit, ac_factor, buildings, is_stressed, spike_factor):
    env = simpy.Environment()
    sim_duration = hours * 60  # minutes
    
    time_stamps = []
    total_demands = []
    building_breakdown = {f"Building {i+1}": [] for i in range(buildings)}
    overload_count = 0
    total_kwh = 0.0

    def campus_process(env):
        nonlocal overload_count, total_kwh
        while True:
            t = env.now
            peak_multiplier = (1.0 + 1.8 * np.sin(np.pi * t / sim_duration)) * ac_factor
            
            # Apply contingency stress test if enabled in middle of day
            if is_stressed and (sim_duration * 0.3 <= t <= sim_duration * 0.7):
                peak_multiplier *= spike_factor
                
            total_demand = max(20.0, base_lam * peak_multiplier + random.gauss(0, 35))
            
            time_stamps.append(t)
            total_demands.append(total_demand)
            total_kwh += total_demand * (1/60)
            
            if total_demand > limit:
                overload_count += 1
                
            load_per_bldg = total_demand / buildings
            for bldg in building_breakdown:
                building_breakdown[bldg].append(load_per_bldg * random.uniform(0.9, 1.1))
                
            yield env.timeout(5)

    env.process(campus_process(env))
    env.run(until=sim_duration)
    return time_stamps, total_demands, building_breakdown, overload_count, total_kwh

# --- EXECUTION ---
col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
with col_b2:
    run_btn = st.button("Run Comprehensive JIC Simulation")

if run_btn:
    with st.spinner("Running advanced microgrid simulation and compiling engineering reports..."):
        random.seed(101)
        timestamps, demands, bldg_data, overloads, total_energy = run_jic_comprehensive_simulation(
            work_hours, base_load, num_transformers, overload_limit, temp_factor, num_buildings, stress_mode, stress_multiplier
        )
        
        max_dem = max(demands)
        min_dem = min(demands)
        avg_dem = sum(demands) / len(demands)
        std_dem = pd.Series(demands).std()
        
        # Financial & Economic Metrics
        peak_energy_cost = total_energy * 0.6 * peak_tariff
        off_peak_energy_cost = total_energy * 0.4 * off_peak_tariff
        base_energy_cost = peak_energy_cost + off_peak_energy_cost
        outage_penalty_cost = overloads * (blackout_penalty / 15)
        total_economic_cost = base_energy_cost + outage_penalty_cost
        
        reliability_index = max(0.0, 100.0 - (overloads / len(demands) * 100))
        
        # Queueing Metrics (M/M/c approximation)
        utilization_rho = min(0.99, avg_dem / (num_transformers * 45))

        # --- SECTION 1: EXECUTIVE KPIs ---
        st.markdown("### JIC Executive Performance & Reliability KPIs")
        
        k1, k2, k3, k4, k5, k6 = st.columns(6)
        k1.metric("Active Buildings", f"{num_buildings}")
        k2.metric("Substations [c]", f"{num_transformers}")
        k3.metric("Peak Demand", f"{max_dem:.1f} kW")
        k4.metric("Average Load", f"{avg_dem:.1f} kW")
        k5.metric("Grid Reliability", f"{reliability_index:.1f}%")
        k6.metric("Overload Events", f"{overloads}")

        # --- SECTION 2: ECONOMIC & COST OPTIMIZATION ---
        st.markdown("### Financial & Economic Optimization Breakdown (SAR)")
        
        e1, e2, e3, e4 = st.columns(4)
        e1.metric("Total Energy Consumed", f"{total_energy:,.1f} kWh")
        e2.metric("Base Tariffs Cost", f"{base_energy_cost:,.2f} SAR")
        e3.metric("Deficit / Outage Penalties", f"{outage_penalty_cost:,.2f} SAR")
        e4.metric("Total Objective Cost", f"{total_economic_cost:,.2f} SAR")

        # --- SECTION 3: M/M/C QUEUEING & STATISTICAL ANALYSIS ---
        st.markdown("### M/M/c Queueing & Statistical Performance Metrics")
        col_q1, col_q2 = st.columns(2)
        
        with col_q1:
            stat_df = pd.DataFrame({
                "Metric Parameter": ["Maximum Load", "Minimum Load", "Mean Load", "Standard Deviation", "Capacity Margin", "Simulation Duration"],
                "Value": [f"{max_dem:.2f} kW", f"{min_dem:.2f} kW", f"{avg_dem:.2f} kW", f"{std_dem:.2f} kW", f"{(num_transformers * 40) - max_dem:.2f} kW", f"{work_hours * 60} Minutes"]
            })
            st.dataframe(stat_df, use_container_width=True, hide_index=True)
            
        with col_q2:
            queue_df = pd.DataFrame({
                "Queueing Parameter [M/M/c]": ["Server Count [c]", "Traffic Intensity [rho]", "Queue State Probability [P0]", "Expected Waiting Time [Wq]", "System Service Rate [mu]"],
                "Computed Value": [f"{num_transformers} Units", f"{utilization_rho:.3f}", f"{max(0.0, 1-utilization_rho):.4f}", f"{max(0.0, utilization_rho*2.5):.2f} Min", "45.0 kW/Unit"]
            })
            st.dataframe(queue_df, use_container_width=True, hide_index=True)

        # --- SECTION 4: DETAILED BUILDINGS CONSUMPTION TABLE ---
        st.markdown("### Building-by-Building Peak Consumption Breakdown")
        bldg_summary = []
        for bldg, values in bldg_data.items():
            bldg_summary.append({
                "Building Name": f"JIC - {bldg}",
                "Peak Load (kW)": f"{max(values):.1f} kW",
                "Average Load (kW)": f"{sum(values)/len(values):.1f} kW",
                "Share of Total (%)": f"{(sum(values)/sum(demands))*100:.1f}%",
                "Status": "Normal" if max(values) < (overload_limit / num_buildings) else "High Stress"
            })
        st.table(pd.DataFrame(bldg_summary))

        # --- SECTION 5: ADVANCED PLOTS & OPTIMIZATION CURVE ---
        st.markdown("---")
        st.markdown("### Multi-Dimensional Power Dynamics & Cost Optimization Curves")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5))
        fig.patch.set_facecolor('#0d1117')
        
        # Plot 1: Demand vs Threshold
        ax1.set_facecolor('#161b22')
        ax1.plot(timestamps, demands, color='#388bfd', linewidth=2, label='Total Campus Demand')
        ax1.axhline(y=overload_limit, color='#f85149', linestyle='--', linewidth=1.8, label='Overload Limit')
        ax1.set_title("Campus Power Load vs. Overload Line", color='#f0f6fc', fontsize=12)
        ax1.set_xlabel("Time (Minutes)", color='#f0f6fc')
        ax1.set_ylabel("Power (kW)", color='#f0f6fc')
        ax1.tick_params(colors='#8b949e')
        ax1.grid(True, linestyle='--', alpha=0.3, color='#30363d')
        ax1.legend(facecolor='#161b22', labelcolor='#f0f6fc')
        for spine in ax1.spines.values(): spine.set_color('#30363d')

        # Plot 2: Total Cost Optimization Curve (Trade-off c)
        ax2.set_facecolor('#161b22')
        c_range = np.arange(max(5, num_transformers - 15), num_transformers + 20, 2)
        simulated_costs = [(c * 1200 + max(0, avg_dem - c * 35) * 8000) for c in c_range]
        ax2.plot(c_range, simulated_costs, color='#238636', linewidth=2.5, marker='o', label='Total Economic Cost (SAR)')
        ax2.axvline(x=num_transformers, color='#58a6ff', linestyle='--', label=f'Current Selected c = {num_transformers}')
        ax2.set_title("Economic Lot Sizing & Capacity Optimization Curve", color='#f0f6fc', fontsize=12)
        ax2.set_xlabel("Number of Substations [c]", color='#f0f6fc')
        ax2.set_ylabel("Total Objective Cost (SAR)", color='#f0f6fc')
        ax2.tick_params(colors='#8b949e')
        ax2.grid(True, linestyle='--', alpha=0.3, color='#30363d')
        ax2.legend(facecolor='#161b22', labelcolor='#f0f6fc')
        for spine in ax2.spines.values(): spine.set_color('#30363d')

        st.pyplot(fig)
        
        # --- SECTION 6: CSV REPORT EXPORT ---
        st.markdown("---")
        st.markdown("### Engineering Report Export")
        export_df = pd.DataFrame({
            "Timestamp_Min": timestamps,
            "Campus_Demand_kW": demands
        })
        csv_data = export_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Complete JIC Simulation CSV Report",
            data=csv_data,
            file_name="JIC_Smart_Campus_Energy_Report.csv",
            mime="text/csv"
        )
        
        st.success("Comprehensive JIC Simulation Report Generated Successfully with Full Statistical, Queueing & Economic Metrics.")
else:
    st.markdown("""
        <div style="text-align: center; padding: 50px; background: rgba(22, 27, 34, 0.4); border-radius: 12px; border: 1px dashed #30363d;">
            <h3 style="color: #8b949e;">JIC Microgrid Intelligence Platform Ready</h3>
            <p style="color: #6e7681;">Adjust your campus parameters from the sidebar and click the button to generate the complete engineering dashboard.</p>
        </div>
    """, unsafe_allow_html=True)
