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
    exp_desc = st.text_area("أبرز المهام أو الإنجازات (استخدم فاصلة منقوطة للبنود أو أسطر جديدة):", placeholder="Managed classrooms; Delivered interactive lectures...")

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

# دالة لتنظيف الرموز الخاصة في LaTeX لكي لا تسبب أخطاء بالترجمة
def escape_latex(text):
    if not text:
        return ""
    return (text.replace("&", "\\&")
                .replace("%", "\\%")
                .replace("$", "\\$")
                .replace("#", "\\#")
                .replace("_", "\\_"))

# دالة لتوليد ملف الـ PDF باستخدام محرك الـ LaTeX الحقيقي
def generate_latex_cv(name, mail, phone, link, loc, summ, e_title, e_comp, e_dur, e_desc, deg, univa, yr, t_skills, s_skills):
    
    # كتابة قالب LaTeX الأكاديمي النظيف والاحترافي
    latex_content = rf"""
    \documentclass[10pt,a4paper]{{article}}
    \usepackage[utf8]{{inputenc}}
    \usepackage[margin=1in]{{geometry}}
    \usepackage{{titlesec}}
    \usepackage{{enumitem}}
    \usepackage{{hyperref}}
    \usepackage{{parskip}}

    \pagestyle{{empty}}
    \titleformat{{\section}} {{\large\bfseries\color{{blue!40!black}}}}{{}}{{0em}}{{}}[{{\titlerule}}]
    \titlespacing{{\section}}{{0pt}}{{10pt}}{{5pt}}

    \begin{{document}}

    % رأس الصفحة (المعلومات الشخصية)
    \begin{{center}}
        {{\huge \textbf{{{escape_latex(name)}}}}} \\[4pt]
        \small {{{escape_latex(mail)} | {escape_latex(phone)} | {escape_latex(loc)} }}
        \ifx\{escape_latex(link)}\empty \else \\ \small \url{{{escape_latex(link)}}} \fi
    \end{{center}}

    % النبذة المهنية
    \ifx\{escape_latex(summ)}\empty \else
    \section{{Professional Summary}}
    {escape_latex(summ)}
    \fi

    % الخبرات العملية
    \if0{0 if not (has_experience and e_title) else 1}
    \section{{Work Experience}}
    \textbf{{{escape_latex(e_title)}}} \hfill {{{escape_latex(e_dur)}}} \\
    \textit{{{escape_latex(e_comp)}}}
    \begin{{itemize}[nosep, leftmargin=*]
        \item {escape_latex(e_desc)}
    \end{{itemize}}
    \fi

    % التعليم
    \ifx\{escape_latex(deg)}\empty \else
    \section{{Education}}
    \textbf{{{escape_latex(deg)}}} \hfill {{{escape_latex(yr)}}} \\
    \textit{{{escape_latex(univa)}}}
    \fi

    % المهارات
    \ifx\{escape_latex(t_skills)}\empty \ifx\{escape_latex(s_skills)}\empty \else
    \section{{Skills}}
    \begin{{itemize}[nosep, leftmargin=*]
        \ifx\{escape_latex(t_skills)}\empty \else \item \textbf{{Technical Skills:}} {escape_latex(t_skills)} \fi
        \ifx\{escape_latex(s_skills)}\empty \else \item \textbf{{Soft Skills:}} {escape_latex(s_skills)} \fi
    \end{{itemize}}
    \fi

    \end{{document}}
    """

    # إنشاء مجلد مؤقت للعمليات
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, "cv.tex")
        pdf_path = os.path.join(tmpdir, "cv.pdf")
        
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(latex_content)
            
        # تشغيل محرك pdflatex لتوليد الـ PDF
        try:
            subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "-output-directory", tmpdir, tex_path],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            if os.path.exists(pdf_path):
                # نسخ الملف لمكان دائم لكي يستطيع Streamlit قراءته
                permanent_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                with open(pdf_path, "rb") as src, open(permanent_pdf.name, "wb") as dst:
                    dst.write(src.read())
                return permanent_pdf.name
        except subprocess.CalledProcessError as e:
            st.error("حدث خطأ أثناء ترجمة ملف الـ LaTeX. تأكد من إدخال النصوص باللغة الإنجليزية بشكل صحيح.")
            return None
    return None

# زر التوليد والتحميل
if st.button("🚀 توليد السيرة الذاتية عبر LaTeX (ATS PDF)"):
    if full_name and email:
        with st.spinner("جاري بناء السيرة الذاتية بتنسيق LaTeX الفخم... استنتج ثوانٍ معدودة! ⏳"):
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
