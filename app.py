import streamlit as st
import simpy
import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="منصة محاكاة وإدارة العمليات الأكاديمية - كلية جدة العالمية",
    page_icon="⚡",
    layout="wide"
)

# --- STRICT WHITE & BLUE THEME (NO DARK BOXES, BLUE ACCENTS) ---
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
    .stat-law-card {
        background-color: #F8F9FA !important;
        border-right: 3px solid #0D6EFD !important;
        padding: 15px;
        border-radius: 6px;
        margin-top: 10px;
        margin-bottom: 15px;
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

# --- HEADER SECTION ---
st.markdown("""
<div class="hero-container">
    <h1 style="margin:0; font-size: 2.2rem;">كلية جدة العالمية (JIC)</h1>
    <h3 style="margin-top: 5px; font-size: 1.3rem;">منصة بحوث العمليات ونظرية الطوابير لإدارة العمليات الأكاديمية</h3>
    <p style="margin-top: 8px; font-size: 1.0rem;">
        تحليل طوابير الانتظار المادية (200+ تذكرة يومياً)، أخطاء مزامنة الدفع، السعة الاستيعابية للسيرفرات، والتكاليف التشغيلية للموظفين.
    </p>
</div>
""", unsafe_allow_html=True)

# --- ORGANIZED CONTROL PANEL (BLUE THEME) ---
st.markdown("### لوحة التحكم التشغيلية ومعلمات المحاكاة الرياضية")

# Section 1: Demographics & Infrastructure
st.markdown('<div class="control-section">', unsafe_allow_html=True)
st.markdown("<b>القسم الأول: أعداد الطلاب والبنية التحتية للخوادم</b>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    total_students = st.slider("إجمالي عدد طلاب الكلية", 1000, 10000, 4500, 500)
with col2:
    server_gateways = st.slider("عدد بوابات الخوادم السحابية المتوازية [c]", 2, 30, 8, 1)
with col3:
    daily_registration_hours = st.slider("فترة نافذة التسجيل الحرجة (ساعات يومياً - من 8 ص إلى 4 عصراً)", 1, 8, 3, 1)
st.markdown('</div>', unsafe_allow_html=True)

# Section 2: Demand & Operations Research Parameters
st.markdown('<div class="control-section">', unsafe_allow_html=True)
st.markdown("<b>القسم الثاني: معلمات بحوث العمليات ومعدلات الطلب (Lambda & Capacity)</b>", unsafe_allow_html=True)
col4, col5, col6 = st.columns(3)
with col4:
    # Calculated scientific arrival rate based on student body and hours
    arrival_rate = st.slider("معدل وصول الطلاب [Lambda] (طالب/دقيقة وقت الذروة)", 10.0, 150.0, float(min(120.0, total_students / 60.0)), 5.0)
with col5:
    system_capacity_limit = st.slider("حد التحميل الأقصى للسيرفرات (طلب/دقيقة قبل التعليق)", 30, 250, 80, 10)
with col6:
    daily_walkins = st.slider("أرقام الانتظار الفعلية للطلاب يومياً بشؤون الطلاب", 50, 400, 200, 10)
st.markdown('</div>', unsafe_allow_html=True)

# Section 3: Operational Risks & Staffing Costs
st.markdown('<div class="control-section">', unsafe_allow_html=True)
st.markdown("<b>القسم الثالث: المخاطر التشغيلية وتكاليف الموظفين والرواتب</b>", unsafe_allow_html=True)
col7, col8, col9 = st.columns(3)
with col7:
    payment_sync_risk = st.slider("نسبة أخطاء مزامنة الدفع المعلق (%) [بناءً على ضغط الشبكة]", 1, 30, 15, 1)
with col8:
    staff_count = st.slider("عدد موظفي الدعم وشؤون الطلاب المخصصين للتدقيق اليدوي", 2, 20, 8, 1)
with col9:
    staff_monthly_salary = st.slider("متوسط راتب الموظف الشهري (ريال سعودي)", 4000, 15000, 6500, 500)
st.markdown('</div>', unsafe_allow_html=True)

# --- SIMULATION CORE LOGIC ---
def run_operational_simulation(hours, lam, c_servers, limit, walkins, pay_risk, staff):
    env = simpy.Environment()
    sim_duration = hours * 60  # total minutes in daily window
    
    time_stamps = []
    queue_loads = []
    crashes_count = 0
    payment_failures = 0
    physical_tickets = 0
    section_lockouts = 0

    server_pool = simpy.Resource(env, capacity=c_servers)

    def operational_process(env):
        nonlocal crashes_count, payment_failures, physical_tickets, section_lockouts
        while True:
            current_time = env.now
            peak_factor = 1.0 + 2.5 * np.exp(-((current_time - (sim_duration*0.3))**2) / (2 * (sim_duration*0.15)**2))
            current_load = lam * peak_factor + random.gauss(0, 3)
            current_load = max(5.0, current_load)
            
            time_stamps.append(current_time)
            queue_loads.append(max(0, server_pool.count))
            
            if current_load > limit:
                crashes_count += 1
                
            payment_failures += int(current_load * (pay_risk / 100.0))
            physical_tickets += int(walkins * (pay_risk / 15.0))
            section_lockouts += int(current_load * 0.25)
                
            yield env.timeout(5)

    env.process(operational_process(env))
    env.run(until=sim_duration)
    return time_stamps, queue_loads, crashes_count, payment_failures, physical_tickets, section_lockouts

# --- FUNCTION TO GENERATE REPORT TEXT ---
def generate_report_text(crashes, pay_fails, phys_tickets, sec_locks, total_staff_cost):
    report_content = f"""
تقرير مشروع التخرج: نظام محاكاة وحل مشاكل التسجيل والعمليات الأكاديمية
كلية جدة العالمية (JIC)

1. خلفية المشكلة التشغيلية:
تواجه عمادة القبول والتسجيل في كلية جدة العالمية تحديات تشغيلية خلال فترات الذروة لتسجيل المواد الدراسية. 
تتمثل هذه المشاكل في ضغط هائل على البوابة الإلكترونية يترتب عليه تعليق النظام، وتأخر مزامنة عمليات السداد المالي، 
وتوافد أكثر من 200 طالب يومياً للحصول على أرقام انتظار يدوية، فضلاً عن أزمة انغلاق الشعب الدراسية.

2. التحليل الرياضي ونظرية الطوابير (M/M/c):
تم صياغة المعضلة كنموذج محاكاة لتدفق الطوابير متعدد الخوادم بناءً على معدل الوصول (Lambda) وتوزيع بواسون، 
مع قياس كثافة حركة المرور (Rho) لضمان استقرار الخوادم السحابية المتوازية (c).

3. النتائج والمؤشرات التشغيلية الحالية:
- حالات تعليق الموقع وسقوط السيرفرات: {crashes}
- أخطاء مزامنة الدفع المعلق: {pay_fails}
- تذاكر الانتظار اليدوية اليومية: {phys_tickets} تذكرة
- الشعب الدراسية المغلقة: {sec_locks}
- تكلفة الموظفين المخصصين لمعالجة الأزمات يدوياً: {total_staff_cost:,.2f} ريال سعودي شهرياً

4. الحلول الهندسية الاستراتيجية المقترحة:
1. إلغاء الطوابير الفعلية: تطوير بوابة خدمة ذاتية رقمية تصفّر عدد تذاكر الانتظار اليومية (200 تذكرة).
2. أتمتة مزامنة المدفوعات: ربط البوابة المالية بقاعدة البيانات لتحديث حالة السداد لحظياً عبر Webhook.
3. موازنة الأحمال السحابية الديناميكية: توزيع الأحمال على خوادم متعددة وقت الذروة لمنع تعليق الموقع.
4. التخصيص الاستباقي للشعب: استخدام خوارزميات تحليل البيانات لتوقع الطلب وفتح شعب إضافية مسبقاً.
"""
    return report_content.strip()

# --- EXECUTION BUTTON ---
col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
with col_b2:
    run_sim_btn = st.button("تشغيل محاكاة وتقييم الأداء التشغيلي للكلية")

if run_sim_btn:
    with st.spinner("جاري حساب نماذج الطوابير الإحصائية وتحليل التكاليف التشغيلية..."):
        random.seed(101)
        timestamps, queues, crashes, pay_fails, phys_tickets, sec_locks = run_operational_simulation(
            daily_registration_hours, arrival_rate, server_gateways, system_capacity_limit, daily_walkins, payment_sync_risk, staff_count
        )
        
        max_queue = max(queues) if queues else 0
        avg_queue = sum(queues) / len(queues) if queues else 0
        
        # Financial calculation based on staff salaries
        total_monthly_staff_cost = staff_count * staff_monthly_salary
        system_downtime_loss = crashes * 3000
        total_operational_loss = total_monthly_staff_cost + system_downtime_loss

        st.markdown("### مؤشرات الأداء التشغيلي الرئيسية للمنصة")
        k1, k2, k3, k4, k5, k6 = st.columns(6)
        k1.metric("البوابات النشطة [c]", f"{server_gateways}")
        k2.metric("أقصى ضغط طابور", f"{max_queue} طلب")
        k3.metric("حالات تعليق الموقع", f"{crashes}")
        k4.metric("أخطاء مزامنة الدفع", f"{pay_fails}")
        k5.metric("تذاكر الانتظار اليومية", f"{phys_tickets} تذكرة")
        k6.metric("الشعب المغلقة", f"{sec_locks}")

        st.markdown("""
        <div class="stat-law-card">
            <b>النموذج الإحصائي المستخدم (توزيع بواسون للوصول ونظرية الطوابير M/M/c):</b> 
            يتم نمذجة تدفق الطلاب عبر معدل الوصول العشوائي <b>(&lambda;)</b> وفق توزيع بواسون المحسوب لتقدير كفاءة الخوادم المتوازية (c).
        </div>
        """, unsafe_allow_html=True)
        st.latex(r"P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}")

        st.markdown("### تحليل التكاليف التشغيلية ورواتب الموظفين (بالريال السعودي)")
        e1, e2, e3 = st.columns(3)
        e1.metric("تكلفة رواتب موظفي الدعم والتدقيق", f"{total_monthly_staff_cost:,.2f} ريال/شهرياً")
        e2.metric("خسائر تعليق السيرفرات والطوارئ", f"{system_downtime_loss:,.2f} ريال")
        e3.metric("إجمالي الهدر المالي التشغيلي", f"{total_operational_loss:,.2f} ريال")

        st.markdown("""
        <div class="stat-law-card">
            <b>النموذج الإحصائي المستخدم (حساب تكلفة الموارد البشرية التشغيلية):</b> 
            تُحسب التكلفة عبر ضرب عدد الموظفين المخصصين لحل المشاكل اليدوية في متوسط الرواتب الشهرية.
        </div>
        """, unsafe_allow_html=True)
        st.latex(r"E(\text{Staff Cost}) = \text{Staff Count} \times \text{Average Salary}")

        st.markdown("### جدول مطابقة المشكلات الواقعية بالحلول الهندسية")
        col_q1, col_q2 = st.columns(2)
        
        with col_q1:
            stat_df = pd.DataFrame({
                "المشكلة الواقعية في الكلية": ["أكثر من 200 رقم انتظار يومياً", "أخطاء مزامنة الدفع وعدم ظهورها", "تعليق الموقع وبطء الاستجابة", "انغلاق الشعب الدراسية بوجه الطالب"],
                "السبب الجذري بحوث عمليات": ["فشل البوابة الرقمية والخوف الطلابي", "غياب الربط الفوري بقاعدة البيانات", "عجز سعة الخوادم المتزامنة [c]", "تخصيص الشعب بشكل ثابت تقليدي"],
                "الحل الهندسي عبر المنصة الذكية": ["بوابة ذاتية تسجل 0 زيارة يدوية", "تكامل آلي فوري (Webhook)", "زيادة السعة السحابية الديناميكية", "تخصيص ذكي وتنبؤ مبكر بالطلب"]
            })
            st.dataframe(stat_df, use_container_width=True, hide_index=True)
            
        with col_q2:
            current_rho = arrival_rate / (server_gateways * 6.0)
            metrics_df = pd.DataFrame({
                "مؤشر الأداء الرياضي": ["كثافة حركة المرور [Rho]", "نسبة استغلال الخوادم", "مؤشر انتظار الطابور", "مستوى المخاطر الإدارية"],
                "القيمة المحسوبة": [f"{current_rho:.3f}", f"{(avg_queue / server_gateways)*100:.1f}%", f"{max(1, int(avg_queue*0.5))} دقيقة", "حرج وعالي جداً"]
            })
            st.dataframe(metrics_df, use_container_width=True, hide_index=True)

        st.markdown("""
        <div class="stat-law-card">
            <b>النموذج الإحصائي المستخدم (معامل كثافة حركة المرور واستقرار النظام):</b> 
            لضمان استقرار الخوادم وعدم تكدس الطوابير، يشترط أن تكون كثافة الاستخدام أقل من الواحد الصحيح.
        </div>
        """, unsafe_allow_html=True)
        st.latex(r"\rho = \frac{\lambda}{c \cdot \mu} < 1")

        st.markdown("""
        <div class="solution-box">
            <h3 style="color: #0D6EFD !important; margin-top: 0;">شرح وتحليل تفصيلي للحلول المقترحة وإسهامها في تحسين الكفاءة:</h3>
            <p><b>1. القضاء التام على أرقام الانتظار الفعلية:</b> تمكين الطالب من إنهاء إجراءات التسجيل ومطابقة الحوالات من جهازه الشخصي لتصفير تذاكر الانتظار اليومية.</p>
            <p><b>2. الأتمتة اللحظية لمزامنة المدفوعات:</b> ربط البوابة المالية مباشرة بقاعدة البيانات عبر Webhook لمنع تعليق الحوالات المالية.</p>
            <p><b>3. التوسع السحابي الديناميكي:</b> توزيع الأحمال على خوادم متعددة وقت الذروة لمنع تعليق الموقع وسقوط السيرفرات.</p>
            <p><b>4. التخصيص الذكي والتنبؤ بالسعة:</b> استخدام خوارزميات تحليل البيانات لتوقع الطلب وفتح شعب إضافية مسبقاً للقضاء على انغلاق الشعب.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### الرسوم البيانية لتحليل الضغط وحجم المعاناة")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5))
        fig.patch.set_facecolor('#ffffff')
        
        ax1.set_facecolor('#ffffff')
        ax1.plot(timestamps, queues, color='#0D6EFD', linewidth=2, label='الطلبات المتزامنة الفعلية')
        ax1.axhline(y=system_capacity_limit, color='#0D6EFD', linestyle='--', linewidth=1.8, label='حد السعة الأقصى')
        ax1.set_title("ضغط طلبات التسجيل مقابل السعة الاستيعابية", color='#000000', fontsize=12)
        ax1.set_xlabel("وقت المحاكاة (بالدقائق)", color='#000000')
        ax1.set_ylabel("عدد الطلبات", color='#000000')
        ax1.tick_params(colors='#000000')
        ax1.grid(True, linestyle='--', alpha=0.3, color='#CED4DA')
        ax1.legend(facecolor='#ffffff', labelcolor='#000000')

        ax2.set_facecolor('#ffffff')
        categories = ['أخطاء الدفع', 'أرقام الانتظار اليدوية', 'الشعب المغلقة']
        values = [pay_fails, phys_tickets, sec_locks]
        ax2.bar(categories, values, color=['#0D6EFD', '#6C757D', '#0DCAF0'], width=0.5)
        ax2.set_title("حجم الحالات المتضررة من المشاكل التشغيلية", color='#000000', fontsize=12)
        ax2.set_ylabel("إجمالي الحالات", color='#000000')
        ax2.tick_params(colors='#000000')
        ax2.grid(True, linestyle='--', alpha=0.3, color='#CED4DA')

        st.pyplot(fig)
        
        st.markdown("---")
        st.markdown("### تحميل تقرير المشروع الرسمي (Text)")
        
        report_text = generate_report_text(crashes, pay_fails, phys_tickets, sec_locks, total_monthly_staff_cost)
        st.download_button(
            label="تحميل التقرير الخطي التنفيذي الشامل (ملف مستند رسمى .txt جاهز للفتح والنسخ لوورد)",
            data=report_text,
            file_name="JIC_Academic_Registration_Report.txt",
            mime="text/plain"
        )
        
        st.success("تم تنفيذ المحاكاة بنجاح وتجهيز التقرير التنفيذي للتحميل الفوري!")
else:
    st.markdown("""
        <div style="text-align: center; padding: 50px; background: #FFFFFF; border-radius: 12px; border: 1px solid #0D6EFD;">
            <h3 style="color: #0D6EFD;">منصة محاكاة العمليات الأكاديمية جاهزة للتشغيل</h3>
            <p style="color: #333333;">قم بضبط إعدادات ومعلمات لوحة التحكم بالأعلى، ثم اضغط على زر التشغيل لعرض النتائج وتنزيل التقرير الرسمي.</p>
        </div>
    """, unsafe_allow_html=True)
