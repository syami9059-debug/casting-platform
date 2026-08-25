import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="صانع السير الذاتية الذكي - ATS", page_icon="📄", layout="centered")

# عنوان الموقع
st.markdown("<h1 style='text-align: center; color: #2e6c80;'>📄 صانع السير الذاتية المتوافق مع ATS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>أدخل بياناتك بدقة لضمان تجاوز أنظمة الفرز الآلي للشركات</p>", unsafe_allow_html=True)
st.write("---")

# 1. قسم المعلومات الشخصية
st.subheader("👤 1. المعلومات الشخصية")
col1, col2 = st.columns(2)

with col1:
    full_name = st.text_input("الاسم الكامل (بالإنجليزية يفضل)", placeholder="e.g. Ibrahim Siyam")
    email = st.text_input("البريد الإلكتروني المهني", placeholder="name@example.com")

with col2:
    st.text("رقم الهاتف")
    phone_col1, phone_col2 = st.columns([1, 25])
    with phone_col1:
        st.markdown("<p style='padding-top: 5px; font-weight: bold;'>+962</p>", unsafe_allow_html=True)
   with col2:
    phone_number = st.text_input("رقم الهاتف", placeholder="7xxxxxxxx", value="+962 ")
    linkedin = st.text_input("رابط لينكد إن (LinkedIn)", placeholder="linkedin.com/in/username")

location = st.text_input("مكان الإقامة الحالي (المدينة، الدولة)", placeholder="Amman, Jordan")
st.info("💡 **تنويه:** استخدم بريداً إلكترونياً احترافياً (اسمك الصريح)، وتأكد من كتابة اسمك بوضوح تام لكي يقرأه روبوت الـ ATS بسهولة.")

st.write("---")

# 2. النبذة المهنية
st.subheader("🎯 2. النبذة المهنية (Professional Summary)")
summary = st.text_area("اكتب ملخصاً قصيراً (3-4 أسطر) يعكس هويتك المهنية:", 
                       placeholder="مثال: خريج ماجستير رياضيات بخبرة في التحليل والبرمجة، أبحث عن فرصة لتطبيق مهاراتي التقنية...")
st.info("💡 **تنويه:** اجعل النبذة مركزة وتحتوي على الكلمات المفتاحية الخاصة بمجالك (مثل: Python, Data Analysis, Teaching) لكي يلتقطها النظام الآلي فوراً.")

st.write("---")

# 3. الخبرات العملية
st.subheader("💼 3. الخبرات العملية (Work Experience)")
has_experience = st.checkbox("هل تمتلك خبرات عملية سابقة؟")
exp_details = ""
if has_experience:
    exp_title = st.text_input("المسمى الوظيفي", placeholder="e.g. Mathematics Teacher")
    exp_company = st.text_input("اسم الشركة أو الجهة", placeholder="e.g. Al-Abbas School")
    exp_duration = st.text_input("فترة العمل (من - إلى)", placeholder="e.g. Mar 2025 - Jul 2025")
    exp_desc = st.text_area("أبرز الإنجازات أو المهام التي قمتم بها:", placeholder="- شرح المناهج بأساليب تفاعلية...\n- إدارة وتنظيم الفصول...")
    exp_details = f"{exp_title} at {exp_company} ({exp_duration}):\n{exp_desc}"
    st.info("💡 **تنويه:** رتب خبراتك من الأحدث للأقدم، واستخدم أفعال إنجاز واضحة (أدرت، طورت، درّست) بدلاً من الجمل الإنشائية الطويلة.")

st.write("---")

# 4. التعليم والأكاديميات
st.subheader("🎓 4. التعليم والأكاديميات (Education)")
edu_degree = st.text_input("الدرجة العلمية والتخصص", placeholder="e.g. Master of Science in Mathematics")
edu_university = st.text_input("اسم الجامعة والمؤسسة التعليمية", placeholder="e.g. Yarmouk University")
edu_year = st.text_input("سنة التخرج (أو المتوقعة)", placeholder="e.g. 2027")
st.info("💡 **تنويه:** اكتب اسم الشهادة والجامعة بدقة رسمية (مثلاً: Bachelor's degree بدلاً من اختصارات قد لا يفهمها الروبوت).")

st.write("---")

# 5. المهارات التقنية والشخصية
st.subheader("🛠️ 5. المهارات (Skills)")
tech_skills = st.text_input("المهارات التقنية (مفصولة بفواصل)", placeholder="e.g. Python, LaTeX, Excel, Data Analysis, Git")
soft_skills = st.text_input("المهارات الشخصية (مفصولة بفواصل)", placeholder="e.g. Problem Solving, Teamwork, Communication")
st.info("💡 **تنويه:** قسم مهاراتك بوضوح لتسهيل قراءتها على مسؤولي التوظيف وأنظمة الفرز الآلي (ATS).")

# زر التوليد النهائي
st.write("---")
if st.button("🚀 معالجة وتوليد السيرة الذاتية (ATS)"):
    if full_name and email:
        full_phone = f"+962{phone_number}" if phone_number else "غير مدخل"
        st.success(f"عاش يا {full_name}! تم جمع بياناتك بنجاح، والنظام جاهز الآن لتحويلها لملف PDF متوافق مع الـ ATS.")
        
        # معاينة سريعة للبيانات المدخلة للتأكد
        with st.expander("🔍 معاينة البيانات المدخلة"):
            st.write(f"**الاسم:** {full_name}")
            st.write(f"**الإيميل:** {email} | **الهاتف:** {full_phone}")
            st.write(f"**النبذة:** {summary}")
            if has_experience:
                st.write(f"**الخبرة:** {exp_details}")
            st.write(f"**التعليم:** {edu_degree} - {edu_university} ({edu_year})")
            st.write(f"**المهارات التقنية:** {tech_skills}")
    else:
        st.error("الرجاء إدخال الاسم الكامل والبريد الإلكتروني على الأقل للمتابعة.")
