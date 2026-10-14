import streamlit as st
import simpy
import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="JIC Smart Campus Registration & Operations Platform",
    page_icon="⚡",
    layout="wide"
)

# --- FORCED BRIGHT WHITE, LIGHT BLUE & BLACK CSS THEME ---
st.markdown("""
    <style>
    .stApp {
        background-color: #FFFFFF !important;
    }
    .main {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    .hero-container {
        background: #F8F9FA !important;
        border: 2px solid #0D6EFD !important;
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(13, 110, 253, 0.1);
    }
    .control-box {
        background: #F8F9FA !important;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #CED4DA !important;
        margin-bottom: 25px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
    }
    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: #212529 !important;
    }
    .hero-container h1 {
        color: #0D6EFD !important;
    }
    .hero-container h3, .hero-container p {
        color: #495057 !important;
    }
    .stMetric {
        background: #FFFFFF !important;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #0D6EFD !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .stMetric label {
        color: #495057 !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #0D6EFD !important;
    }
    .stButton button {
        background-color: #0D6EFD !important;
        color: #FFFFFF !important;
        border-radius: 6px;
        font-weight: 700;
        border: none;
        padding: 12px 24px;
        width: 100%;
    }
    .stButton button:hover {
        background-color: #0B5ED7 !important;
        color: #FFFFFF !important;
    }
    .stSlider label {
        color: #212529 !important;
        font-weight: 600 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown("""
<div class="hero-container">
    <h1 style="margin:0; font-size: 2.2rem;">Jeddah International College (JIC)</h1>
    <h3 style="margin-top: 5px; font-size: 1.3rem;">Smart Campus Course Registration & Operational Risk Platform</h3>
    <p style="margin-top: 8px; font-size: 1.0rem;">
        Eliminating Physical Walk-in Queues (200+ Daily Tickets), Payment Sync Failures, System Freezes & Section Lockouts
    </p>
</div>
""", unsafe_allow_html=True)

# --- TOP HORIZONTAL CONTROLS CONTAINER ---
st.markdown("### Operational Parameters & Physical Queue Controls")
st.markdown('<div class="control-box">', unsafe_allow_html=True)

col_c1, col_c2, col_c3, col_c4 = st.columns(4)

with col_c1:
    total_students = st.slider("Total Student Body Size", 500, 5000, 2500, 250)
    server_gateways = st.slider("Active Cloud Servers / Gateways [c]", 2, 50, 12, 2)
    registration_window = st.slider("Peak Registration Window (Hours)", 12, 72, 24, 6)
    
with col_c2:
    arrival_rate = st.slider("Student Arrival Rate [lambda] (Req/Min)", 10.0, 200.0, 45.0, 5.0)
    system_capacity_limit = st.slider("Server Overload Threshold (Req/Min)", 50, 300, 100, 10)
    daily_walkins = st.slider("Daily Physical Walk-in Tickets", 50, 400, 200, 10)
    
with col_c3:
    payment_sync_risk = st.slider("Payment Sync Failure Rate (%)", 1, 25, 12, 1)
    manual_review_cost = st.slider("Cost per Walk-in Visit (SAR)", 50, 500, 150, 25)
    section_lockout_rate = st.slider("Section Capacity Lockout Risk (%)", 5, 50, 22, 2)
    
with col_c4:
    st.markdown("<b>Platform Solution Mode</b>", unsafe_allow_html=True)
    platform_upgrade = st.checkbox("Enable JIC Automated Smart Platform", value=True)
    automation_efficiency = st.slider("Digital Automation & Resolution (%)", 70, 99, 95, 1)

st.markdown('</div>', unsafe_allow_html=True)

# --- SIMULATION CORE LOGIC ---
def run_operational_simulation(window_hours, lam, c_servers, limit, walkins, pay_risk, lockout_risk, is_upgraded, efficiency):
    env = simpy.Environment()
    sim_duration = window_hours * 60  # minutes
    
    time_stamps = []
    queue_loads = []
    crashes_count = 0
    payment_failures = 0
    physical_tickets = 0
    section_lockouts = 0

    effective_servers = int(c_servers * 1.8) if is_upgraded else c_servers
    server_pool = simpy.Resource(env, capacity=effective_servers)

    def operational_process(env):
        nonlocal crashes_count, payment_failures, physical_tickets, section_lockouts
        while True:
            current_time = env.now
            peak_factor = 1.0 + 2.0 * np.exp(-((current_time - (sim_duration*0.2))**2) / (2 * (sim_duration*0.12)**2))
            current_load = lam * peak_factor + random.gauss(0, 4)
            current_load = max(5.0, current_load)
            
            time_stamps.append(current_time)
            queue_loads.append(max(0, server_pool.count))
            
            if current_load > limit:
                crashes_count += 1
                
            eff_factor = (1.0 - (efficiency / 100.0)) if is_upgraded else 1.0
            payment_failures += int(current_load * (pay_risk / 100.0) * eff_factor)
            physical_tickets += int(walkins * (pay_risk / 12.0) * eff_factor)
            section_lockouts += int(current_load * (lockout_risk / 100.0) * eff_factor)
                
            yield env.timeout(5)

    env.process(operational_process(env))
    env.run(until=sim_duration)
    return time_stamps, queue_loads, crashes_count, payment_failures, physical_tickets, section_lockouts, effective_servers

# --- EXECUTION BUTTON ---
col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
with col_b2:
    run_sim_btn = st.button("Run JIC Operational Solutions Simulation")

if run_sim_btn:
    with st.spinner("Analyzing physical queues, digital bottlenecks, and financial losses..."):
        random.seed(101)
        timestamps, queues, crashes, pay_fails, phys_tickets, sec_locks, active_c = run_operational_simulation(
            registration_window, arrival_rate, server_gateways, system_capacity_limit, daily_walkins, payment_sync_risk, section_lockout_rate, platform_upgrade, automation_efficiency
        )
        
        max_queue = max(queues) if queues else 0
        avg_queue = sum(queues) / len(queues) if queues else 0
        
        # Financial Impact of Pain Points (SAR)
        total_walkin_cost = phys_tickets * manual_review_cost
        system_downtime_loss = crashes * 5000
        total_operational_loss = total_walkin_cost + system_downtime_loss

        # --- SECTION 1: PAIN-POINT EXECUTIVE KPIs ---
        st.markdown("### Operational Pain-Points & Physical Queue KPIs")
        
        k1, k2, k3, k4, k5, k6 = st.columns(6)
        k1.metric("Active Gateways [c]", f"{active_c}")
        k2.metric("Peak Request Queue", f"{max_queue} Req")
        k3.metric("System Freezes", f"{crashes}")
        k4.metric("Payment Sync Errors", f"{pay_fails}")
        k5.metric("Daily Physical Walk-ins", f"{phys_tickets} Tickets")
        k6.metric("Section Lockouts", f"{sec_locks}")

        # --- SECTION 2: FINANCIAL & ADMINISTRATIVE COST ANALYSIS ---
        st.markdown("### Administrative Cost & Physical Queue Losses (SAR)")
        
        e1, e2, e3 = st.columns(3)
        e1.metric("Physical Walk-in & Support Cost", f"{total_walkin_cost:,.2f} SAR")
        e2.metric("System Downtime & Crash Losses", f"{system_downtime_loss:,.2f} SAR")
        e3.metric("Total Operational Inefficiency Loss", f"{total_operational_loss:,.2f} SAR")

        # --- SECTION 3: OPERATIONS RESEARCH MAPPING ---
        st.markdown("### Operations Research Solutions & System Validation")
        col_q1, col_q2 = st.columns(2)
        
        with col_q1:
            stat_df = pd.DataFrame({
                "Operational Problem": ["200+ Daily Physical Walk-ins", "Payment Synchronization", "Website Freezing & Latency", "Section Capacity Lockouts"],
                "Root Cause [Operations Research]": ["Digital Transaction Failure & Fear", "Lack of Real-time DB Handshake", "Server Capacity Deficit [c]", "Static Course Allocation"],
                "Proposed Platform Solution": ["Self-Service Digital Portal (0 Walk-ins)", "Automated Webhook & Gateway Sync", "Dynamic Cloud Scalability", "Dynamic Queue Allocation"]
            })
            st.dataframe(stat_df, use_container_width=True, hide_index=True)
            
        with col_q2:
            metrics_df = pd.DataFrame({
                "Performance Parameter": ["Traffic Intensity [rho]", "Server Utilization", "Queue Wait Time Index", "Administrative Risk Rating"],
                "Evaluated Result": [f"{arrival_rate / (active_c * service_rate if 'service_rate' in locals() else 6.0):.3f}", f"{(avg_queue / active_c)*100:.1f}%", f"{max(1, int(avg_queue*0.5))} Min", "Optimized" if platform_upgrade else "High Exposure"]
            })
            st.dataframe(metrics_df, use_container_width=True, hide_index=True)

        # --- SECTION 4: CHARTS ---
        st.markdown("---")
        st.markdown("### Registration Traffic Congestion & Physical Queue Dynamics")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5))
        fig.patch.set_facecolor('#ffffff')
        
        # Plot 1: Queue pressure
        ax1.set_facecolor('#f8f9fa')
        ax1.plot(timestamps, queues, color='#0D6EFD', linewidth=2, label='Active Concurrent Requests')
        ax1.axhline(y=system_capacity_limit, color='#DC3545', linestyle='--', linewidth=1.8, label='Overload Limit')
        ax1.set_title("Registration Portal Load vs Capacity Limit", color='#212529', fontsize=12)
        ax1.set_xlabel("Simulation Time (Minutes)", color='#212529')
        ax1.set_ylabel("Concurrent Requests", color='#212529')
        ax1.tick_params(colors='#495057')
        ax1.grid(True, linestyle='--', alpha=0.3, color='#ced4da')
        ax1.legend(facecolor='#ffffff', labelcolor='#212529')
        for spine in ax1.spines.values(): spine.set_color('#ced4da')

        # Plot 2: Pain points comparison
        ax2.set_facecolor('#f8f9fa')
        categories = ['Payment Errors', 'Physical Walk-ins', 'Section Lockouts']
        values = [pay_fails, phys_tickets, sec_locks]
        ax2.bar(categories, values, color=['#fd7e14', '#dc3545', '#0dcaf0'], width=0.5)
        ax2.set_title("Operational Pain-Points Volume", color='#212529', fontsize=12)
        ax2.set_ylabel("Total Affected Incidents", color='#212529')
        ax2.tick_params(colors='#495057')
        ax2.grid(True, linestyle='--', alpha=0.3, color='#ced4da')
        for spine in ax2.spines.values(): spine.set_color('#ced4da')

        st.pyplot(fig)
        
        # --- SECTION 5: EXPORT ---
        st.markdown("---")
        st.markdown("### Operational Solution Report Export")
        export_df = pd.DataFrame({
            "Time_Min": timestamps,
            "Queue_Load": queues,
            "Payment_Failures": pay_fails,
            "Physical_Walkins": phys_tickets
        })
        csv_data = export_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download JIC Operational Solutions & Cost Report (CSV)",
            data=csv_data,
            file_name="JIC_Operational_Solutions_Report.csv",
            mime="text/csv"
        )
        
        st.success("Operational simulation executed successfully. Physical queues and financial losses are fully mapped.")
else:
    st.markdown("""
        <div style="text-align: center; padding: 50px; background: #f8f9fa; border-radius: 12px; border: 1px solid #ced4da;">
            <h3 style="color: #495057;">JIC Course Registration Operations Platform Ready</h3>
            <p style="color: #6c757d;">Configure student traffic and physical queue parameters above, then click the simulation button to generate the operational resolution report.</p>
        </div>
    """, unsafe_allow_html=True)
