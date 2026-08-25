import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="صانع السير الذاتية الذكي", page_icon="📄", layout="centered")

# عنوان الموقع
st.markdown("<h1 style='text-align: center; color: #2e6c80;'>📄 صانع السير الذاتية المتوافق مع ATS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>أدخل بياناتك لإنشاء سيرة ذاتية احترافية تتخطى أنظمة الفرز الآلي</p>", unsafe_allow_html=True)
st.write("---")

# قسم المعلومات الشخصية
st.subheader("👤 المعلومات الشخصية")
col1, col2 = st.columns(2)

with col1:
    full_name = st.text_input("الاسم الكامل (بالإنجليزي)")
    email = st.text_input("البريد الإلكتروني")

with col2:
    phone = st.text_input("رقم الهاتف")
    linkedin = st.text_input("رابط لينكد إن (اختياري)")

# قسم النبذة المهنية
st.subheader("🎯 النبذة المهنية (Summary)")
summary = st.text_area("اكتب نبذة قصيرة عنك وعن أهدافك المهنية:", height=100)

# زر توليد السيرة (حالياً بس بيعطي رسالة نجاح)
st.write("---")
if st.button("🚀 إنشاء السيرة الذاتية (PDF)"):
    if full_name and email:
        st.success(f"عاش يا {full_name}! رح نبرمج تحويل هاي البيانات لـ PDF بخطوتنا الجاية.")
    else:
        st.error("الرجاء إدخال الاسم والبريد الإلكتروني على الأقل.")
