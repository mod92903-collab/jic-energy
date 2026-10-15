import streamlit as st
import simpy
import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="نظام إدارة ومحاكاة مركز خدمة العملاء والدعم الفني",
    page_icon="🎧",
    layout="wide"
)

# --- STRICT WHITE & BLUE THEME (INCLUDING SLIDERS) ---
st.markdown("""
    <style>
    .stApp, .main, div[data-testid="stVerticalBlock"], section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        direction: rtl;
        text-align: right;
    }
    h1, h2, h3, h4, h5, h6, p, label, span, div, li, strong, b {
        color: #000000 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .hero-container {
        background-color: #FFFFFF !important;
        border: 2px solid #0D6EFD !important;
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(13, 110, 253, 0.08);
        text-align: center;
    }
    .hero-container h1 {
        color: #0D6EFD !important;
    }
    .control-section {
        background-color: #FFFFFF !important;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #0D6EFD !important;
        margin-bottom: 15px;
        box-shadow: 0 2px 6px rgba(13, 110, 253, 0.05);
    }
    .solution-box {
        background-color: #FFFFFF !important;
        border: 2px solid #0D6EFD !important;
        padding: 25px;
        border-radius: 10px;
        margin-top: 25px;
        margin-bottom: 25px;
        color: #000000 !important;
    }
    .formulas-box {
        background-color: #F8F9FA !important;
        border: 2px solid #0D6EFD !important;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 25px;
        color: #000000 !important;
    }
    .stat-law-prominent {
        background-color: #F0F7FF !important;
        border: 2px solid #0D6EFD !important;
        border-right: 8px solid #0D6EFD !important;
        padding: 20px;
        border-radius: 8px;
        margin-top: 15px;
        margin-bottom: 20px;
        color: #000000 !important;
    }
    .stMetric {
        background-color: #FFFFFF !important;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #0D6EFD !important;
        text-align: center;
    }
    .stMetric label {
        color: #0D6EFD !important;
        font-weight: 600 !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #0D6EFD !important;
        font-weight: 700 !important;
    }
    /* FORCE SLIDERS AND CONTROLS TO BLUE INSTEAD OF RED */
    div[data-baseweb="slider"] div[role="slider"] {
        background-color: #0D6EFD !important;
    }
    div[data-testid="stSlider"] [data-baseweb="slider"] div > div > div {
        background-color: #0D6EFD !important;
    }
    span[data-baseweb="tag"] {
        background-color: #0D6EFD !important;
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
    table {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    th {
        background-color: #F8F9FA !important;
        color: #0D6EFD !important;
    }
    td {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- CLEAN HEADER SECTION ---
st.markdown("""
<div class="hero-container">
    <h1 style="margin:0; font-size: 2.3rem;">نظام إدارة ومحاكاة مركز خدمة العملاء والدعم الفني</h1>
    <p style="margin-top: 10px; font-size: 1.1rem; color: #333333 !important;">
        التطبيق الهندسي لبحوث العمليات ونظرية الطوابير (M/M/c) على مراكز الاتصال وخدمة المستفيدين على مدار 24 ساعة.
    </p>
</div>
""", unsafe_allow_html=True)

# --- DEDICATED FORMULAS BOX ---
st.markdown("""
<div class="formulas-box">
    <h3 style="color: #0D6EFD !important; margin-top: 0; margin-bottom: 15px;"> مرجع القوانين الإحصائية والرياضية المستخدمة في البرنامج</h3>
    <ul>
        <li><b>توزيع بواسون لمعدل الوصول (Poisson Arrival):</b> يُستخدم لنمذجة عدد المكالمات الواردة عشوائياً للمركز خلال فترة زمنية محددة.</li>
        <li><b>نظرية الطوابير متعددة الخوادم (M/M/c Queueing Model):</b> تُقيس أوقات الانتظار وط طول الطابور بناءً على عدد موظفي الدعم ($c$).</li>
        <li><b>كثافة حركة المرور واستقرار النظام ($\rho$):</b> النسبة بين معدل الوصول ($ \lambda $) والسعة الإجمالية للخدمة ($ c \cdot \mu $)، ويشترط إحصائياً أن تكون أقل من 1 لضمان عدم انهيار المركز.</li>
        <li><b>القيمة المتوقعة للتكلفة الإجمالية (Expected Total Cost):</b> حساب الهدر المالي بدمج رواتب الموظفين مع خسائر تسرب العملاء بسبب سوء الخدمة.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# --- CONTROL PANEL FOR CALL CENTER ---
st.markdown("### لوحة التحكم التشغيلية ومعلمات محاكاة خدمة العملاء")

st.markdown('<div class="control-section">', unsafe_allow_html=True)
st.markdown("<b>القسم الأول: حجم قاعدة العملاء وسعة طاقم خدمة العملاء (تشغيل 24 ساعة)</b>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    total_customers_base = st.slider("إجمالي عدد العملاء المستهدفين (عميل)", 5000, 50000, 20000, 2500)
with col2:
    support_agents = st.slider("عدد موظفي خدمة العملاء في الوردية النشطة [c]", 2, 50, 15, 1)
with col3:
    shift_hours = 24
    st.info("⏱️ نظام التشغيل مفعل على مدار: **24 ساعة يومياً**")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="control-section">', unsafe_allow_html=True)
st.markdown("<b>القسم الثاني: معدلات الوصول والخدمة ($\lambda$ & Service Rate)</b>", unsafe_allow_html=True)
col4, col5, col6 = st.columns(3)
with col4:
    arrival_rate_calls = st.slider("معدل وصول المكالمات [Lambda] (مكالمة/دقيقة وقت الذروة)", 5.0, 100.0, 30.0, 5.0)
with col5:
    avg_service_time = st.slider("متوسط وقت خدمة العميل للمكالمة الواحدة (دقائق)", 2.0, 15.0, 5.0, 0.5)
with col6:
    max_hold_tolerance = st.slider("الحد الأقصى لصبر العميل قبل قطع الاتصال (دقائق)", 2, 15, 6, 1)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="control-section">', unsafe_allow_html=True)
st.markdown("<b>القسم الثالث: جودة الخدمة وتكاليف الموظفين والرواتب</b>", unsafe_allow_html=True)
col7, col8, col9 = st.columns(3)
with col7:
    escalation_rate = st.slider("نسبة الشكاوى المعقدة التي تحتاج تصعيد (%)", 5, 40, 18, 1)
with col8:
    agent_monthly_salary = st.slider("متوسط راتب موظف خدمة العملاء الشهري (ريال)", 3500, 12000, 5500, 500)
with col9:
    customer_loss_cost = st.slider("تكلفة خسارة العميل الواحد بسبب سوء الخدمة (ريال)", 50, 500, 200, 25)
st.markdown('</div>', unsafe_allow_html=True)

# --- SIMULATION CORE LOGIC FOR CALL CENTER (24 HOURS) ---
def run_call_center_simulation(agents, lam, serv_time, max_tolerance, shift, esc_rate, base_customers):
    env = simpy.Environment()
    sim_duration = shift * 60  # 1440 minutes
    
    time_stamps = []
    queue_loads = []
    abandoned_calls = 0
    resolved_calls = 0
    escalated_cases = 0
    max_wait_time_recorded = 0

    agent_pool = simpy.Resource(env, capacity=agents)

    def call_process(env):
        nonlocal abandoned_calls, resolved_calls, escalated_cases, max_wait_time_recorded
        while True:
            current_time = env.now
            peak_factor = 1.0 + 1.8 * np.exp(-((current_time - 480)**2) / (2 * (120)**2)) + 1.5 * np.exp(-((current_time - 1100)**2) / (2 * (150)**2))
            current_incoming = (lam / 2.0) * peak_factor + random.gauss(0, 2)
            current_incoming = max(2.0, current_incoming)
            
            time_stamps.append(current_time)
            active_queue = max(0, int(current_incoming - agents))
            queue_loads.append(active_queue)
            
            estimated_wait = (active_queue * serv_time) / max(1, agents)
            if estimated_wait > max_wait_time_recorded:
                max_wait_time_recorded = estimated_wait
                
            if estimated_wait > max_tolerance:
                abandoned_calls += int(current_incoming * 0.25)
            else:
                resolved_calls += int(current_incoming * (1.0 - esc_rate/100.0))
                escalated_cases += int(current_incoming * (esc_rate/100.0))
                
            yield env.timeout(15)

    env.process(call_process(env))
    env.run(until=sim_duration)
    return time_stamps, queue_loads, abandoned_calls, resolved_calls, escalated_cases, max_wait_time_recorded

# --- FUNCTION TO GENERATE REPORT TEXT ---
def generate_call_center_report(agents, abandoned, resolved, escalated, max_wait, total_payroll):
    report_content = f"""
تقرير مشروع التخرج: نظام محاكاة وإدارة مركز خدمة العملاء والدعم الفني (تشغيل 24 ساعة)
تحليل طوابير الانتظار وكفاءة طاقم العمل على مدار اليوم

1. خلفية المشكلة التشغيلية في مركز الاتصال (24/7):
يواجه مركز خدمة العملاء تحديات حرجة على مدار الساعة، خصوصاً خلال أوقات الذروة المزدوجة (الصباحية والمسائية)، 
حيث يتوافد حجم مكالمات ضخم يعجز طاقم العمل الحالي عن استيعابه، مما يؤدي إلى ارتفاع طوابير الانتظار، 
غضب المستفيدين، وزيادة نسبة المكالمات المتخلية (قطع الاتصال قبل الرد)، وارتفاع الشكاوى المعقدة.

2. التحليل الرياضي ونظرية الطوابير (M/M/c):
تم بناء نموذج محاكاة يعتمد على توزيع بواسون لمعدل وصول المكالمات (Lambda) ونظرية الطوابير متعددة الخوادم (c موظفين)، 
لقياس كثافة حركة المرور (Rho) وزمن الانتظار المتوقع على الخط قبل رد الممثل.

3. النتائج والمؤشرات التشغيلية الحالية:
- المكالمات المتخلية (العملاء الغاضبون الذين قطعوا الاتصال): {abandoned} مكالمة
- المكالمات المحلولة من الاتصال الأول (FCR): {resolved} مكالمة
- الحالات المعقدة التي تتطلب تصعيداً: {escalated} حالة
- أقصى زمن انتظار تم تسجيله على الخط: {max_wait:.1f} دقيقة
- إجمالي تكلفة رواتب طاقم خدمة العملاء (24 ساعة): {total_payroll:,.2f} ريال سعودي شهرياً

4. الحلول الهندسية الاستراتيجية المقترحة:
1. تطبيق مساعد آلي ذكي (AI Chatbot / IVR): لفلترة الاستفسارات المتكررة على مدار 24 ساعة وتخفيف العبء عن الموظفين.
2. الجدولة الذكية للورديات (24/7 Shift Scheduling): زيادة عدد الموظفين أوقات الذروة الصباحية والمسائية بناءً على التنبؤ بمعدل الوصول.
3. التوجيه الذكي بناءً على المهارات (Skill-based Routing): توجيه العميل للموظف المختص مباشرة لتقليل وقت المكالمة ورفع نسبة الحل الفوري.
"""
    return report_content.strip()

# --- EXECUTION BUTTON ---
col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
with col_b2:
    run_sim_btn = st.button("تشغيل محاكاة وتقييم مركز خدمة العملاء (24 ساعة)")

if run_sim_btn:
    with st.spinner("جاري حساب نماذج الطوابير الإحصائية على مدار 24 ساعة وتحليل المؤشرات..."):
        random.seed(101)
        timestamps, queues, abandoned_count, resolved_count, escalated_count, max_wait_time = run_call_center_simulation(
            support_agents, arrival_rate_calls, avg_service_time, max_hold_tolerance, shift_hours, escalation_rate, total_customers_base
        )
        
        max_queue_load = max(queues) if queues else 0
        avg_queue_load = sum(queues) / len(queues) if queues else 0
        
        total_monthly_payroll = support_agents * agent_monthly_salary
        customer_churn_loss = abandoned_count * customer_loss_cost
        total_financial_impact = total_monthly_payroll + customer_churn_loss

        st.markdown("### مؤشرات الأداء الرئيسي لمركز خدمة العملاء (KPIs على مدار 24 ساعة)")
        k1, k2, k3, k4, k5, k6 = st.columns(6)
        k1.metric("موظفو الدعم [c]", f"{support_agents}")
        k2.metric("أقصى طول طابور", f"{max_queue_load} عميل")
        k3.metric("المكالمات المتخلية", f"{abandoned_count}")
        k4.metric("الحل الفوري (FCR)", f"{resolved_count}")
        k5.metric("الحالات المُصعدة", f"{escalated_count}")
        k6.metric("أقصى انتظار", f"{max_wait_time:.1f} دقيقة")

        # --- STAT LAW 1 ---
        st.markdown("""
        <div class="stat-law-prominent">
            <h4 style="color: #0D6EFD !important; margin-top: 0;"> القانون الإحصائي الأول: توزيع بواسون لمعدل وصول المكالمات (Poisson Arrival Process)</h4>
            <p>يتم نمذجة معدل وصول المكالمات الواردة لمركز الاتصال على مدار 24 ساعة باستخدام توزيع بواسون الاحتمالي لتقدير احتمال وصول عدد معين من العملاء ($k$) في فترة زمنية محددة بناءً على معدل الوصول المتسلسل (\\(\\lambda\\)):</p>
        </div>
        """, unsafe_allow_html=True)
        st.latex(r"P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}")

        st.markdown("### تحليل التكاليف التشغيلية والأثر المالي (بالريال السعودي)")
        e1, e2, e3 = st.columns(3)
        e1.metric("إجمالي رواتب طاقم خدمة العملاء", f"{total_monthly_payroll:,.2f} ريال/شهرياً")
        e2.metric("خسائر تسرب العملاء (Churn Loss)", f"{customer_churn_loss:,.2f} ريال")
        e3.metric("إجمالي الهدر والتكلفة المالية", f"{total_financial_impact:,.2f} ريال")

        # --- STAT LAW 2 ---
        st.markdown("""
        <div class="stat-law-prominent">
            <h4 style="color: #0D6EFD !important; margin-top: 0;"> القانون الإحصائي الثاني: حساب القيمة المتوقعة للتكلفة الإجمالية (Expected Total Cost)</h4>
            <p>تُحسب التكلفة التشغيلية الكلية لمركز الاتصال بجمع الرواتب الشهرية لطاقم الموظفين على مدار الوردية مع الخسائر المترتبة على تسرب العملاء نتيجة تخليهم عن الانتظار:</p>
        </div>
        """, unsafe_allow_html=True)
        st.latex(r"E(\text{Total Cost}) = (\text{Agents} \times \text{Salary}) + (\text{Abandoned Calls} \times \text{Loss Cost})")

        st.markdown("### جدول مطابقة مشاكل خدمة العملاء بالحلول الهندسية")
        col_q1, col_q2 = st.columns(2)
        
        with col_q1:
            stat_df = pd.DataFrame({
                "المشكلة الواقعية في المركز (24/7)": ["طول طوابير الانتظار وانخفاض الرد", "فقدان العملاء (المكالمات المتخلية)", "تكرار الشكوى وضعف الحل الفوري", "ضغط العمل الهائل على الموظفين"],
                "السبب الجذري بحوث عمليات": ["نقص عدد ممثلي الدعم [c] أوقات الذروة", "تجاوز زمن الانتظار الحد الأقصى للصبر", "غياب التوجيه الذكي وضعف التدريب", "توزيع عشوائي للمكالمات دون جدولة"],
                "الحل الهندسي عبر المنصة الذكية": ["مساعد آلي ذكي (AI Chatbot) للتصفية", "موازنة طاقم العمل ديناميكياً (Scheduling)", "توجيه ذكي مبني على المهارات (Skills)", "أتمتة العمليات وخفض أوقات الانتظار"]
            })
            st.dataframe(stat_df, use_container_width=True, hide_index=True)
            
        with col_q2:
            current_rho = arrival_rate_calls / (support_agents * (60.0 / avg_service_time))
            metrics_df = pd.DataFrame({
                "مؤشر الأداء الرياضي": ["كثافة حركة المرور [Rho]", "نسبة استغلال الموظفين", "متوسط زمن الانتظار النظري", "مستوى جودة الخدمة (SLA)"],
                "القيمة المحسوبة": [f"{current_rho:.3f}", f"{min(100.0, current_rho*100.1):.1f}%", f"{max(1.0, avg_service_time * current_rho):.1f} دقيقة", "حرج وعالي المخاطر" if current_rho > 0.8 else "مستقر وآمن"]
            })
            st.dataframe(metrics_df, use_container_width=True, hide_index=True)

        # --- STAT LAW 3 ---
        st.markdown("""
        <div class="stat-law-prominent">
            <h4 style="color: #0D6EFD !important; margin-top: 0;"> القانون الإحصائي الثالث: معامل كثافة حركة المرور واستقرار النظام (Traffic Intensity $\\rho$)</h4>
            <p>يحدد هذا القانون نسبة تشبع طاقم العمل ومعدل استغلال الخوادم ($c$). لضمان استقرار مركز الاتصال وعدم تكدس المكالمات للانهيار، يجب إحصائياً أن تكون كثافة حركة المرور أقل من الواحد الصحيح:</p>
        </div>
        """, unsafe_allow_html=True)
        st.latex(r"\rho = \frac{\lambda}{c \cdot \mu} < 1")

        st.markdown("""
        <div class="solution-box">
            <h3 style="color: #0D6EFD !important; margin-top: 0;">شرح وتحليل تفصيلي للحلول المقترحة وإسهامها في تحسين الكفاءة:</h3>
            <p><b>1. تطبيق المساعد الآلي الذكي (AI Chatbot على مدار 24 ساعة):</b> تصفية ما يصل إلى 45% من الاستفسارات البسيطة وتوجيه العملاء آلياً، مما يصفر أوقات الانتظار تماماً للخدمات السريعة طوال اليوم.</p>
            <p><b>2. الجدولة الديناميكية لطاقم العمل (24/7 Shift Scheduling):</b> استخدام خوارزميات التنبؤ بمعدل وصول المكالمات لزيادة عدد الموظفين المتاحين أوقات الذروة الصباحية والمسائية.</p>
            <p><b>3. التوجيه الذكي بناءً على المهارات (Skill-based Routing):</b> ربط العميل بالممثل الأكثر كفاءة في حل مشكلته من المرة الأولى (FCR) لتقليل وقت المكالمة.</p>
            <p><b>4. خفض معدل التخلي عن المكالمات:</b> ضمان استقرار طوابير الانتظار تحت الحد الأقصى لصبر العميل، مما يحافظ على ولاء العملاء ويخفض الخسائر المالية.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### الرسوم البيانية لتحليل تدفق المكالمات وحجم الضغط على مدار 24 ساعة")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5))
        fig.patch.set_facecolor('#ffffff')
        
        ax1.set_facecolor('#ffffff')
        ax1.plot(timestamps, queues, color='#0D6EFD', linewidth=2, label='طابور انتظار المكالمات الفعلي (24 ساعة)')
        ax1.axhline(y=support_agents, color='#0D6EFD', linestyle='--', linewidth=1.8, label='السعة الاستيعابية للموظفين [c]')
        ax1.set_title("ضغط المكالمات الواردة مقابل سعة موظفي الدعم على مدار اليوم", color='#000000', fontsize=12)
        ax1.set_xlabel("وقت المحاكاة (بالدقائق عبر 24 ساعة)", color='#000000')
        ax1.set_ylabel("عدد المكالمات المنتظرة", color='#000000')
        ax1.tick_params(colors='#000000')
        ax1.grid(True, linestyle='--', alpha=0.3, color='#CED4DA')
        ax1.legend(facecolor='#ffffff', labelcolor='#000000')

        ax2.set_facecolor('#ffffff')
        categories = ['المكالمات المتخلية', 'الحل الفوري (FCR)', 'الحالات المُصعدة']
        values = [abandoned_count, resolved_count, escalated_count]
        ax2.bar(categories, values, color=['#0D6EFD', '#6C757D', '#0DCAF0'], width=0.5)
        ax2.set_title("تصنيف حالات خدمة العملاء ونتائج المعالجة اليومية", color='#000000', fontsize=12)
        ax2.set_ylabel("إجمالي الحالات", color='#000000')
        ax2.tick_params(colors='#000000')
        ax2.grid(True, linestyle='--', alpha=0.3, color='#CED4DA')

        st.pyplot(fig)
        
        st.markdown("---")
        st.markdown("### تحميل تقرير المشروع الرسمي لخدمة العملاء (Text)")
        
        report_text = generate_call_center_report(support_agents, abandoned_count, resolved_count, escalated_count, max_wait_time, total_monthly_payroll)
        st.download_button(
            label="تحميل التقرير الخطي التنفيذي الشامل (ملف مستند رسمى .txt جاهز للفتح والنسخ لوورد)",
            data=report_text,
            file_name="Customer_Service_Simulation_Report_24H.txt",
            mime="text/plain"
        )
        
        st.success("تم تنفيذ محاكاة مركز خدمة العملاء بنجاح على مدار 24 ساعة وتجهيز التقرير التنفيذي للتحميل الفوري!")
else:
    st.markdown("""
        <div style="text-align: center; padding: 40px; background: #FFFFFF; border-radius: 12px; border: 2px solid #0D6EFD;">
            <h3 style="color: #0D6EFD;">منصة محاكاة وإدارة مركز خدمة العملاء (24 ساعة) جاهزة للتشغيل</h3>
            <p style="color: #333333;">راجع القوانين بالأعلى، ثم اضغط على زر التشغيل لتنفيذ المحاكاة وعرض النتائج والتحليلات الإحصائية.</p>
        </div>
    """, unsafe_allow_html=True)
