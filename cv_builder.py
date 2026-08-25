import streamlit as st
import subprocess
import tempfile
import os

# إعدادات الصفحة
st.set_page_config(page_title="صانع السير الذاتية بالـ LaTeX - ATS", page_icon="📄", layout="centered")

# عنوان الموقع
st.markdown("<h1 style='text-align: center; color: #2e6c80;'>📄 صانع السير الذاتية الأكاديمي (LaTeX & ATS)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>أدخل بياناتك باللغة الإنجليزية لتوليد سيرة ذاتية احترافية عبر محرك LaTeX</p>", unsafe_allow_html=True)
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
st.info("💡 **تنويه:** يُفضل كتابة البيانات باللغة الإنجليزية لتتوافق مع معايير الـ LaTeX والـ ATS.")

st.write("---")

# 2. النبذة المهنية
st.subheader("🎯 2. النبذة المهنية (Professional Summary)")
summary = st.text_area("ملخص قصير (3-4 أسطر):", placeholder="e.g. Dedicated mathematics graduate with strong analytical and programming skills...")

st.write("---")

# 3. الخبرات العملية
st.subheader("💼 3. الخبرات العملية (Work Experience)")
has_experience = st.checkbox("هل تمتلك خبرات عملية سابقة؟")
exp_title, exp_company, exp_duration, exp_desc = "", "", "", ""
if has_experience:
    exp_title = st.text_input("المسمى الوظيفي", placeholder="e.g. Mathematics Teacher")
    exp_company = st.text_input("اسم الشركة أو الجهة", placeholder="e.g. Al-Abbas School")
    exp_duration = st.text_input("فترة العمل", placeholder="e.g. Mar 2025 - Jul 2025")
    exp_desc = st.text_area("أبرز المهام أو الإنجازات:", placeholder="Managed classrooms and delivered interactive lessons.")

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
soft_skills = st.text_input("المهارات الشخصية (مفصولة بفواصل)", placeholder="e.g. Problem Solving, Teamwork, Communication")

st.write("---")

# دالة لتنظيف الرموز الخاصة في LaTeX
def escape_latex(text):
    if not text:
        return ""
    return (text.replace("&", "\\&")
                .replace("%", "\\%")
                .replace("$", "\\$")
                .replace("#", "\\#")
                .replace("_", "\\_"))

# دالة لتوليد ملف الـ PDF باستخدام قالب LaTeX مع تقارير أخطاء واضحة
def generate_latex_cv(name, mail, phone, link, loc, summ, e_title, e_comp, e_dur, e_desc, deg, univa, yr, t_skills, s_skills):
    
    latex_code = r"""
\documentclass[10pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[margin=1in]{geometry}
\usepackage{titlesec}
\usepackage{enumitem}
\usepackage{hyperref}
\usepackage{parskip}
\usepackage{xcolor}

\pagestyle{empty}
\titleformat{\section} {\large\bfseries\color{blue!40!black}}{}{0em}{}[]
\titlespacing{\section}{0pt}{10pt}{5pt}

\begin{document}

\begin{center}
    {\huge \textbf{NAME_PLACEHOLDER}} \\[4pt]
    \small {MAIL_PLACEHOLDER | PHONE_PLACEHOLDER | LOC_PLACEHOLDER}
    LINK_PLACEHOLDER
\end{center}

SUMMARY_PLACEHOLDER

EXPERIENCE_PLACEHOLDER

EDUCATION_PLACEHOLDER

SKILLS_PLACEHOLDER

\end{document}
"""

    latex_code = latex_code.replace("NAME_PLACEHOLDER", escape_latex(name))
    latex_code = latex_code.replace("MAIL_PLACEHOLDER", escape_latex(mail))
    latex_code = latex_code.replace("PHONE_PLACEHOLDER", escape_latex(phone))
    latex_code = latex_code.replace("LOC_PLACEHOLDER", escape_latex(loc))
    
    if link:
        link_str = r"\\ \small \url{" + escape_latex(link) + "}"
        latex_code = latex_code.replace("LINK_PLACEHOLDER", link_str)
    else:
        latex_code = latex_code.replace("LINK_PLACEHOLDER", "")
        
    if summ:
        summary_str = r"""
\section{Professional Summary}
SUMMARY_TEXT
""".replace("SUMMARY_TEXT", escape_latex(summ))
        latex_code = latex_code.replace("SUMMARY_PLACEHOLDER", summary_str)
    else:
        latex_code = latex_code.replace("SUMMARY_PLACEHOLDER", "")
        
    if has_experience and e_title:
        exp_str = r"""
\section{Work Experience}
\textbf{EXP_TITLE} \hfill {EXP_DUR} \\
\textit{EXP_COMP}
\begin{itemize}[nosep, leftmargin=*]
    \item EXP_DESC
\end{itemize}
"""
        exp_str = (exp_str.replace("EXP_TITLE", escape_latex(e_title))
                           .replace("EXP_DUR", escape_latex(e_dur))
                           .replace("EXP_COMP", escape_latex(e_comp))
                           .replace("EXP_DESC", escape_latex(e_desc)))
        latex_code = latex_code.replace("EXPERIENCE_PLACEHOLDER", exp_str)
    else:
        latex_code = latex_code.replace("EXPERIENCE_PLACEHOLDER", "")
        
    if deg:
        edu_str = r"""
\section{Education}
\textbf{DEGREE} \hfill {YEAR} \\
\textit{UNIV}
"""
        edu_str = (edu_str.replace("DEGREE", escape_latex(deg))
                          .replace("YEAR", escape_latex(yr))
                          .replace("UNIV", escape_latex(univa)))
        latex_code = latex_code.replace("EDUCATION_PLACEHOLDER", edu_str)
    else:
        latex_code = latex_code.replace("EDUCATION_PLACEHOLDER", "")
        
    if t_skills or s_skills:
        skills_lines = []
        if t_skills:
            skills_lines.append(r"\item \textbf{Technical Skills:} " + escape_latex(t_skills))
        if s_skills:
            skills_lines.append(r"\item \textbf{Soft Skills:} " + escape_latex(s_skills))
            
        skills_str = r"""
\section{Skills}
\begin{itemize}[nosep, leftmargin=*]
    SKILLS_ITEMS
\end{itemize}
"""
        skills_str = skills_str.replace("SKILLS_ITEMS", "\n    ".join(skills_lines))
        latex_code = latex_code.replace("SKILLS_PLACEHOLDER", skills_str)
    else:
        latex_code = latex_code.replace("SKILLS_PLACEHOLDER", "")

    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, "cv.tex")
        pdf_path = os.path.join(tmpdir, "cv.pdf")
        
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(latex_code)
            
        try:
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "-output-directory", tmpdir, tex_path],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            if os.path.exists(pdf_path):
                permanent_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                with open(pdf_path, "rb") as src, open(permanent_pdf.name, "wb") as dst:
                    dst.write(src.read())
                return permanent_pdf.name
        except subprocess.CalledProcessError as e:
            error_output = e.stderr.decode("utf-8", errors="ignore") if e.stderr else "Unknown LaTeX error"
            st.error(f"خطأ في محرك LaTeX: {error_output[:300]}")
            return None
    return None

# زر التوليد والتحميل
if st.button("🚀 توليد السيرة الذاتية عبر LaTeX (ATS PDF)"):
    if full_name and email:
        with st.spinner("جاري ترجمة السيرة الذاتية عبر محرك LaTeX الأكاديمي... انتظر ثوانٍ معدودة! ⏳"):
            pdf_path = generate_latex_cv(
                full_name, email, phone_number, linkedin, location,
                summary, exp_title, exp_company, exp_duration, exp_desc,
                edu_degree, edu_university, edu_year, tech_skills, soft_skills
            )
            
            if pdf_path and os.path.exists(pdf_path):
                with open(pdf_path, "rb") as pdf_file:
                    st.success("🎉 تم توليد سيرتك الذاتية بنجاح عبر محرك LaTeX الاحترافي!")
                    st.download_button(
                        label="📥 اضغط هنا لتحميل ملف الـ PDF الفخم",
                        data=pdf_file,
                        file_name=f"{full_name.replace(' ', '_')}_LaTeX_CV.pdf",
                        mime="application/pdf"
                    )
    else:
        st.error("الرجاء إدخال الاسم الكامل والبريد الإلكتروني على الأقل لمتابعة التوليد.")
