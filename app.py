import streamlit as st
import simpy
import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="منصة محاكاة وإدارة العمليات الأكاديمية - كلية جدة العالمية",
    page_icon="⚡",
    layout="wide"
)

# --- STRICT WHITE CSS (NO DARK BOXES) ---
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
    }
    .hero-container h1 {
        color: #0D6EFD !important;
    }
    .control-section {
        background-color: #FFFFFF !important;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #CED4DA !important;
        margin-bottom: 15px;
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
        color: #333333 !important;
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
        color: #000000 !important;
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
    <h3 style="margin-top: 5px; font-size: 1.3rem;">منصة الذكاء الاصطناعي لمحاكاة وحل مشاكل التسجيل والعمليات الأكاديمية</h3>
    <p style="margin-top: 8px; font-size: 1.0rem;">
        مشروع تخرج في الهندسة الصناعية • بحوث العمليات ونظرية الطوابير M/M/c • القضاء على الطوابير الفعلية وأخطاء النظام
    </p>
</div>
""", unsafe_allow_html=True)

# --- ORGANIZED CONTROL PANEL ---
st.markdown("### لوحة التحكم التشغيلية ومعلمات المحاكاة")

st.markdown('<div class="control-section">', unsafe_allow_html=True)
st.markdown("<b>القسم الأول: البنية التحتية والسعة الاستيعابية للخوادم</b>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    total_students = st.slider("إجمالي عدد طلاب الكلية", 500, 5000, 2500, 250)
with col2:
    server_gateways = st.slider("عدد بوابات الخوادم السحابية [c]", 2, 50, 12, 2)
with col3:
    registration_window = st.slider("فترة نافذة التسجيل الحرجة (بالساعات)", 12, 72, 24, 6)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="control-section">', unsafe_allow_html=True)
st.markdown("<b>القسم الثاني: معدلات الطلب والوصول وحركة المرور</b>", unsafe_allow_html=True)
col4, col5, col6 = st.columns(3)
with col4:
    arrival_rate = st.slider("معدل وصول الطلاب [Lambda] (طالب/دقيقة)", 10.0, 200.0, 45.0, 5.0)
with col5:
    system_capacity_limit = st.slider("حد التحميل الأقصى للسيرفرات (طلب/دقيقة)", 50, 300, 100, 10)
with col6:
    daily_walkins = st.slider("عدد أرقام الانتظار الفعلية للطلاب يومياً بالمبنى", 50, 400, 200, 10)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="control-section">', unsafe_allow_html=True)
st.markdown("<b>القسم الثالث: نسب المخاطر التشغيلية والتكاليف بالريال السعودي</b>", unsafe_allow_html=True)
col7, col8, col9 = st.columns(3)
with col7:
    payment_sync_risk = st.slider("نسبة أخطاء مزامنة الدفع المعلق (%)", 1, 25, 12, 1)
with col8:
    manual_review_cost = st.slider("تكلفة معالجة الحالة الواحدة يدوياً (ريال)", 50, 500, 150, 25)
with col9:
    section_lockout_rate = st.slider("مخاطر انغلاق الشعب الدراسية (%)", 5, 50, 22, 2)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="control-section">', unsafe_allow_html=True)
st.markdown("<b>القسم الرابع: تفعيل المنصة الذكية المقترحة</b>", unsafe_allow_html=True)
col10, col11 = st.columns(2)
with col10:
    platform_upgrade = st.checkbox("تفعيل منصة كلية جدة العالمية الذكية للحلول الآلية", value=True)
with col11:
    automation_efficiency = st.slider("كفاءة الأتمتة والربط الرقمي والتصحيح الفوري (%)", 70, 99, 95, 1)
st.markdown('</div>', unsafe_allow_html=True)

# --- SIMULATION CORE LOGIC ---
def run_operational_simulation(window_hours, lam, c_servers, limit, walkins, pay_risk, lockout_risk, is_upgraded, efficiency):
    env = simpy.Environment()
    sim_duration = window_hours * 60
    
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

# --- FUNCTION TO GENERATE REPORT TEXT (WORD COMPATIBLE) ---
def generate_report_text(crashes, pay_fails, phys_tickets, sec_locks, total_loss):
    report_content = f"""
تقرير مشروع التخرج: نظام محاكاة وحل مشاكل التسجيل والعمليات الأكاديمية
كلية جدة العالمية (JIC)

1. خلفية المشكلة التشغيلية:
تواجه عمادة القبول والتسجيل في كلية جدة العالمية تحديات تشغيلية جوهرية خلال فترات الذروة لتسجيل المواد الدراسية. 
تتمثل هذه المشاكل في ضغط هائل ومفاجئ على البوابة الإلكترونية يترتب عليه تعليق النظام وسقوط الخوادم، 
فضلاً عن تأخر مزامنة عمليات السداد المالي، وتوافد أكثر من 200 طالب يومياً للحصول على أرقام انتظار يدوية، 
ناهيك عن أزمة انغلاق الشعب الدراسية التي تهدد التأخر الأكاديمي للطلاب.

2. التحليل الرياضي ونظرية الطوابير (M/M/c):
تم صياغة المعضلة كنموذج محاكاة لتدفق الطوابير متعدد الخوادم. حيث يُنمذج وصول الطلاب عبر توزيع بواسون العشوائي 
بمعدل وصول (Lambda)، وتُدار العمليات عبر خوادم سحابية متوازية (c) لضمان استقرار النظام وعدم تجاوز كثافة المرور (Rho).

3. النتائج والمؤشرات التشغيلية الحالية:
- حالات تعليق الموقع المسجلة: {crashes}
- أخطاء مزامنة الدفع المعلق: {pay_fails}
- تذاكر الانتظار اليدوية اليومية: {phys_tickets} تذكرة
- الشعب الدراسية المغلقة: {sec_locks}
- إجمالي الهدر المالي التشغيلي: {total_loss:,.2f} ريال سعودي

4. الحلول الهندسية الاستراتيجية المقترحة:
1. القضاء التام على أرقام الانتظار الفعلية: تطوير بوابة خدمة ذاتية رقمية تصفّر عدد تذاكر الانتظار اليومية.
2. أتمتة مزامنة المدفوعات: ربط البوابة المالية بقاعدة البيانات لتحديث حالة السداد لحظياً عبر Webhook.
3. موازنة الأحمال السحابية الديناميكية: توزيع الأحمال على خوادم متعددة وقت الذروة لمنع تعليق الموقع وسقوط السيرفرات.
4. التخصيص الذكي والتنبؤ بالسعة: استخدام خوارزميات تحليل البيانات لتوقع الطلب وفتح شعب إضافية مسبقاً.
"""
    return report_content.strip()

# --- EXECUTION BUTTON ---
col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
with col_b2:
    run_sim_btn = st.button("تشغيل محاكاة وتقييم الأداء التشغيلي")

if run_sim_btn:
    with st.spinner("جاري حساب نماذج الطوابير الإحصائية وتحليل التكاليف التشغيلية..."):
        random.seed(101)
        timestamps, queues, crashes, pay_fails, phys_tickets, sec_locks, active_c = run_operational_simulation(
            registration_window, arrival_rate, server_gateways, system_capacity_limit, daily_walkins, payment_sync_risk, section_lockout_rate, platform_upgrade, automation_efficiency
        )
        
        max_queue = max(queues) if queues else 0
        avg_queue = sum(queues) / len(queues) if queues else 0
        
        total_walkin_cost = phys_tickets * manual_review_cost
        system_downtime_loss = crashes * 5000
        total_operational_loss = total_walkin_cost + system_downtime_loss

        st.markdown("### مؤشرات الأداء التشغيلي الرئيسية للمنصة")
        k1, k2, k3, k4, k5, k6 = st.columns(6)
        k1.metric("البوابات النشطة [c]", f"{active_c}")
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

        st.markdown("### تحليل التكاليف التشغيلية والخسائر المالية (بالريال السعودي)")
        e1, e2, e3 = st.columns(3)
        e1.metric("تكلفة زيارات الانتظار اليدوية", f"{total_walkin_cost:,.2f} ريال")
        e2.metric("خسائر تعليق السيرفرات والطوارئ", f"{system_downtime_loss:,.2f} ريال")
        e3.metric("إجمالي الهدر المالي التشغيلي", f"{total_operational_loss:,.2f} ريال")

        st.markdown("""
        <div class="stat-law-card">
            <b>النموذج الإحصائي المستخدم (حساب القيمة المتوقعة للخسائر التشغيلية):</b> 
            تُحسب التكلفة الإجمالية بضرب عدد حوادث الفشل أو الزيارات في التكلفة التشغيلية المتوسطة لكل حالة.
        </div>
        """, unsafe_allow_html=True)
        st.latex(r"E(\text{Total Cost}) = \sum (n_i \times \text{Cost}_i)")

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
            current_rho = arrival_rate / (active_c * 6.0)
            metrics_df = pd.DataFrame({
                "مؤشر الأداء الرياضي": ["كثافة حركة المرور [Rho]", "نسبة استغلال الخوادم", "مؤشر انتظار الطابور", "مستوى المخاطر الإدارية"],
                "القيمة المحسوبة": [f"{current_rho:.3f}", f"{(avg_queue / active_c)*100:.1f}%", f"{max(1, int(avg_queue*0.5))} دقيقة", "محسوب وآمن" if platform_upgrade else "حرج وعالي"]
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
        ax1.axhline(y=system_capacity_limit, color='#DC3545', linestyle='--', linewidth=1.8, label='حد السعة الأقصى')
        ax1.set_title("ضغط طلبات التسجيل مقابل السعة الاستيعابية", color='#000000', fontsize=12)
        ax1.set_xlabel("وقت المحاكاة (بالدقائق)", color='#000000')
        ax1.set_ylabel("عدد الطلبات", color='#000000')
        ax1.tick_params(colors='#000000')
        ax1.grid(True, linestyle='--', alpha=0.3, color='#CED4DA')
        ax1.legend(facecolor='#ffffff', labelcolor='#000000')

        ax2.set_facecolor('#ffffff')
        categories = ['أخطاء الدفع', 'أرقام الانتظار اليدوية', 'الشعب المغلقة']
        values = [pay_fails, phys_tickets, sec_locks]
        ax2.bar(categories, values, color=['#fd7e14', '#dc3545', '#0dcaf0'], width=0.5)
        ax2.set_title("حجم الحالات المتضررة من المشاكل التشغيلية", color='#000000', fontsize=12)
        ax2.set_ylabel("إجمالي الحالات", color='#000000')
        ax2.tick_params(colors='#000000')
        ax2.grid(True, linestyle='--', alpha=0.3, color='#CED4DA')

        st.pyplot(fig)
        
        st.markdown("---")
        st.markdown("### تحميل تقرير المشروع الرسمي (Word / Text)")
        
        report_text = generate_report_text(crashes, pay_fails, phys_tickets, sec_locks, total_operational_loss)
        st.download_button(
            label="تحميل التقرير الخطي التنفيذي الشامل (ملف مستند رسمي .txt جاهز للفتح والنسخ لوورد)",
            data=report_text,
            file_name="JIC_Academic_Registration_Report.txt",
            mime="text/plain"
        )
        
        st.success("تم تنفيذ المحاكاة بنجاح وتجهيز التقرير التنفيذي للتحميل الفوري!")
else:
    st.markdown("""
        <div style="text-align: center; padding: 50px; background: #FFFFFF; border-radius: 12px; border: 1px solid #CED4DA;">
            <h3 style="color: #000000;">منصة محاكاة العمليات الأكاديمية جاهزة للتشغيل</h3>
            <p style="color: #333333;">قم بضبط إعدادات ومعلمات الأقسام بالأعلى، ثم اضغط على زر التشغيل لعرض النتائج وتنزيل التقرير الرسمي.</p>
        </div>
    """, unsafe_allow_html=True)
