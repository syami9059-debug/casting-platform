import streamlit as st
from fpdf import FPDF
import tempfile
import os

# إعدادات الصفحة
st.set_page_config(page_title="صانع السير الذاتية الذكي - ATS", page_icon="📄", layout="centered")

# عنوان الموقع
st.markdown("<h1 style='text-align: center; color: #2e6c80;'>📄 صانع السير الذاتية المتوافق مع ATS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>أدخل بياناتك باللغة الإنجليزية لضمان تجاوز أنظمة الفرز الآلي للشركات</p>", unsafe_allow_html=True)
st.write("---")

# 1. المعلومات الشخصية
st.subheader("👤 1. المعلومات الشخصية")
col1, col2 = st.columns(2)

with col1:
    full_name = st.text_input("الاسم الكامل (بالإنجليزي)", placeholder="e.g. Ibrahim Siyam")
    email = st.text_input("البريد الإلكتروني المهني", placeholder="name@example.com")

with col2:
    phone_number = st.text_input("رقم الهاتف", value="+962 ")
    linkedin = st.text_input("رابط لينكد إن (LinkedIn)", placeholder="linkedin.com/in/username")

location = st.text_input("مكان الإقامة الحالي (المدينة، الدولة)", placeholder="Amman, Jordan")
st.info("💡 **تنويه:** يُفضل كتابة البيانات باللغة الإنجليزية بالكامل لتتطابق مع معايير أنظمة الـ ATS العالمية.")

st.write("---")

# 2. النبذة المهنية
st.subheader("🎯 2. النبذة المهنية (Professional Summary)")
summary = st.text_area("ملخص قصير (3-4 أسطر):", placeholder="e.g. Dedicated mathematics graduate with strong analytical skills...")

st.write("---")

# 3. الخبرات العملية
st.subheader("💼 3. الخبرات العملية (Work Experience)")
has_experience = st.checkbox("هل تمتلك خبرات عملية سابقة؟")
exp_title, exp_company, exp_duration, exp_desc = "", "", "", ""
if has_experience:
    exp_title = st.text_input("المسمى الوظيفي", placeholder="e.g. Mathematics Teacher")
    exp_company = st.text_input("اسم الشركة أو الجهة", placeholder="e.g. Al-Abbas School")
    exp_duration = st.text_input("فترة العمل", placeholder="e.g. Mar 2025 - Jul 2025")
    exp_desc = st.text_area("أبرز المهام أو الإنجازات:", placeholder="- Managed classrooms...\n- Delivered lectures...")

st.write("---")

# 4. التعليم
st.subheader("🎓 4. التعليم والأكاديميات (Education)")
edu_degree = st.text_input("الدرجة العلمية والتخصص", placeholder="e.g. Master of Science in Mathematics")
edu_university = st.text_input("اسم الجامعة", placeholder="e.g. Yarmouk University")
edu_year = st.text_input("سنة التخرج", placeholder="e.g. 2027")

st.write("---")

# 5. المهارات
st.subheader("🛠️ 5. المهارات (Skills)")
tech_skills = st.text_input("المهارات التقنية (مفصولة بفواصل)", placeholder="e.g. Python, LaTeX, Excel, Data Analysis")
soft_skills = st.text_input("المهارات الشخصية (مفصولة بفواصل)", placeholder="e.g. Problem Solving, Teamwork")

st.write("---")

# دالة لتنظيف النصوص من أي أحرف قد تسبب مشاكل برمجية
def clean_text(text):
    if not text:
        return ""
    return text.encode("latin-1", "ignore").decode("latin-1")

# دالة لتوليد ملف الـ PDF بمواصفات الـ ATS مع الحماية
def create_ats_pdf(name, mail, phone, link, loc, summ, e_title, e_comp, e_dur, e_desc, deg, univa, yr, t_skills, s_skills):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # استخدام خط افتراضي نظيف (Helvetica)
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, clean_text(name), ln=True, align="C")
    
    pdf.set_font("Helvetica", "", 10)
    contact_info = f"{mail} | {phone} | {loc}"
    if link:
        contact_info += f" | {link}"
    pdf.cell(0, 6, clean_text(contact_info), ln=True, align="C")
    pdf.ln(5)
    
    # دالة فرعية لتنسيق العناوين الرئيسية
    def add_section_header(title):
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(46, 108, 128)
        pdf.cell(0, 8, clean_text(title.upper()), ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", "", 10)
    
    # Summary
    if summ:
        add_section_header("Professional Summary")
        pdf.multi_cell(0, 5, clean_text(summ))
        pdf.ln(3)
        
    # Experience
    if has_experience and e_title:
        add_section_header("Work Experience")
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 5, clean_text(f"{e_title} - {e_comp}"), ln=True)
        pdf.set_font("Helvetica", "I", 9)
        pdf.cell(0, 5, clean_text(e_dur), ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 5, clean_text(e_desc))
        pdf.ln(3)
        
    # Education
    if deg:
        add_section_header("Education")
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 5, clean_text(deg), ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 5, clean_text(f"{univa} | Expected {yr}"), ln=True)
        pdf.ln(3)
        
    # Skills
    if t_skills or s_skills:
        add_section_header("Skills")
        if t_skills:
            pdf.multi_cell(0, 5, clean_text(f"Technical Skills: {t_skills}"))
        if s_skills:
            pdf.multi_cell(0, 5, clean_text(f"Soft Skills: {s_skills}"))
            
    # حفظ الملف مؤقتاً
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name

# زر التوليد والتحميل
if st.button("🚀 توليد وتحميل السيرة الذاتية (ATS PDF)"):
    if full_name and email:
        pdf_path = create_ats_pdf(
            full_name, email, phone_number, linkedin, location,
            summary, exp_title, exp_company, exp_duration, exp_desc,
            edu_degree, edu_university, edu_year, tech_skills, soft_skills
        )
        
        with open(pdf_path, "rb") as pdf_file:
            st.success("🎉 تم إنشاء سيرتك الذاتية بنجاح ومتوافقة تماماً مع نظام الـ ATS!")
            st.download_button(
                label="📥 اضغط هنا لتحميل ملف الـ PDF",
                data=pdf_file,
                file_name=f"{full_name.replace(' ', '_')}_CV.pdf",
                mime="application/pdf"
            )
    else:
        st.error("الرجاء إدخال الاسم الكامل والبريد الإلكتروني على الأقل لمتابعة التوليد.")
