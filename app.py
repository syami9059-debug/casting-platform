import streamlit as st
import pandas as pd

# إعدادات الصفحة
st.set_page_config(
    page_title="منصة الكاستينغ", 
    page_icon="🎬", 
    layout="wide"
)

# ----------------- تصميم الخلفية السينمائية (CSS) -----------------
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1598899134739-24c46f58b8c0?q=80&w=2000&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background-color: rgba(15, 15, 25, 0.85);
    z-index: 0;
}
[data-testid="stAppViewBlockContainer"] {
    z-index: 1;
}
[data-testid="stSidebar"] {
    background-color: rgba(10, 10, 15, 0.95) !important;
    border-left: 2px solid #ff4d4d;
}
div[data-testid="stForm"] {
    background-color: rgba(30, 30, 45, 0.6);
    border-radius: 15px;
    padding: 20px;
    border: 1px solid #555;
    box-shadow: 0 4px 15px rgba(0,0,0,0.5);
}
h1, p, label, span {
    color: #ffffff !important;
    text-shadow: 1px 1px 2px black;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# ----------------- قاعدة البيانات المؤقتة لتخزين الطلبات -----------------
if 'actors_data' not in st.session_state:
    st.session_state.actors_data = pd.DataFrame(columns=[
        'الاسم', 'العمر', 'الجنس', 'المظهر', 'نوع الدور', 'اللهجات', 'رقم الهاتف', 'رابط الفيديو'
    ])

# القائمة الجانبية
st.sidebar.title("📌 القائمة الرئيسية")
choice = st.sidebar.radio("اختر القسم:", ["👤 تقديم طلب (للممثلين)", "🔐 لوحة تحكم المسؤولة"])

# ----------------- القسم الأول: صفحة الممثلين -----------------
if choice == "👤 تقديم طلب (للممثلين)":
    st.markdown("<h1 style='text-align: center; color: #ff4d4d !important;'>🎬 نموذج التسجيل للممثلين والكومبارس</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px;'>قم بتعبئة بياناتك لتصل إلى مسؤولة الكاستينغ مباشرة.</p>", unsafe_allow_html=True)
    st.write("---")
    
    with st.form("actor_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("الاسم الرباعي")
            age = st.number_input("العمر", min_value=1, max_value=95, value=25)
            gender = st.selectbox("الجنس", ["أنثى", "ذكر"])
            
        with col2:
            phone = st.text_input("رقم الهاتف (واتساب)")
            role_type = st.selectbox("نوع الدور", ["ممثل رئيسي", "ممثل ثانوي", "كومبارس"])
            
            appearance = "غير محدد"
            if gender == "أنثى":
                appearance = st.selectbox("المظهر / الحجاب", ["محجبة", "غير محجبة (مفرّعة)"])
            else:
                appearance = st.selectbox("المظهر العام", ["لحية / ذقن", "حليق تماماً", "عادي"])
                
        dialects = st.multiselect(
            "اللهجات التي تتقنها:",
            ["أردنية", "فلسطينية", "سورية", "مصرية", "خليجية"]
        )
        
        video_link = st.text_input("رابط الفيديو التعريفي (يوتيوب أو درايف)")
        
        submit_btn = st.form_submit_button("🚀 إرسال الطلب الآن")
        
        if submit_btn:
            if name.strip() != "":
                dialects_text = ", ".join(dialects) if dialects else "عادية"
                
                # حفظ الطلب مباشرة في جدول النظام الداخلي
                new_row = pd.DataFrame({
                    'الاسم': [name], 
                    'العمر': [age], 
                    'الجنس': [gender], 
                    'المظهر': [appearance], 
                    'نوع الدور': [role_type], 
                    'اللهجات': [dialects_text],
                    'رقم الهاتف': [phone],
                    'رابط الفيديو': [video_link]
                })
                st.session_state.actors_data = pd.concat([st.session_state.actors_data, new_row], ignore_index=True)
                st.success(f"تم إرسال طلبك بنجاح يا {name}!")
            else:
                st.error("الرجاء إدخال الاسم على الأقل.")

# ----------------- القسم الثاني: لوحة تحكم المسؤولة -----------------
elif choice == "🔐 لوحة تحكم المسؤولة":
    st.markdown("<h1 style='color: #ff4d4d !important;'>🔐 لوحة تحكم مسؤولة الكاستينغ</h1>", unsafe_allow_html=True)
    
    ADMIN_PASSWORD = "1234"
    password = st.text_input("أدخل كلمة المرور الخاصة بالمسؤولة:", type="password")
    
    if password == ADMIN_PASSWORD:
        st.success("أهلاً بك يا مديرة الإنتاج!")
        st.write("---")
        
        st.subheader("🔍 أدوات الفرز وعرض الطلبات الواردة")
        f_role = st.selectbox("فلتر حسب الدور:", ["الكل", "ممثل رئيسي", "ممثل ثانوي", "كومبارس"])
        
        df = st.session_state.actors_data
        if f_role != "الكل":
            df = df[df['نوع الدور'] == f_role]
            
        st.markdown(f"**عدد النتائج المطابقة:** {len(df)}")
        
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("لا توجد طلبات مسجلة حتى الآن. عبي طلب من صفحة الممثلين عشان تشوفه هون فوراً!")
            
    elif password != "":
        st.error("كلمة المرور غير صحيحة!")
    else:
        st.info("الرجاء إدخال كلمة المرور لعرض لوحة التحكم.")
