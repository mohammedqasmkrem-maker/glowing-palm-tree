import streamlit as st
import json
import os
from datetime import datetime

# --- 1. إعدادات الصفحة والجمالية ---
st.set_page_config(page_title="مملكة محمد", page_icon="🔱", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Changa:wght@700&display=swap');
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                    url('https://images.unsplash.com/photo-1505118380757-91f5f5632de0?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80');
        background-size: cover;
        background-attachment: fixed;
        font-family: 'Changa', sans-serif;
    }

    /* تصميم البطاقات الكبيرة للخانات */
    .category-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 30px;
        padding: 40px;
        text-align: center;
        transition: 0.4s;
        cursor: pointer;
        color: white;
    }
    .category-card:hover {
        background: rgba(0, 255, 255, 0.2);
        border-color: #00ffff;
        transform: translateY(-10px);
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 20px !important;
        height: 3em;
        font-size: 1.2em !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. نظام حفظ البيانات ---
def load_data():
    if os.path.exists("mohammed_king.json"):
        with open("mohammed_king.json", "r", encoding="utf-8") as f: return json.load(f)
    return {"tasks": []}

def save_data(data):
    with open("mohammed_king.json", "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False)

data = load_data()

# --- 3. نظام التنقل (Navigation) ---
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

# --- الصفحة الأولى: الترحيب والاختيار ---
if st.session_state.page == 'welcome':
    st.markdown("<h1 style='text-align:center; color:white; font-size:60px;'>🔱 أهلاً بك في مملكتك يا محمد 🔱</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#ddd; font-size:25px;'>اختر الوجهة التي تريد الذهاب إليها الآن:</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='category-card'><h2>📚 الدراسة</h2><p>وقت التركيز والنجاح</p></div>", unsafe_allow_html=True)
        if st.button("دخول الغرفة", key="study"):
            st.session_state.page = 'دراسة'
            st.rerun()

    with col2:
        st.markdown("<div class='category-card'><h2>💪 الرياضة</h2><p>بناء القوة والطاقة</p></div>", unsafe_allow_html=True)
        if st.button("دخول الغرفة", key="gym"):
            st.session_state.page = 'رياضة'
            st.rerun()

    with col3:
        st.markdown("<div class='category-card'><h2>📖 المذكرات</h2><p>تفريغ الأفكار والمشاعر</p></div>", unsafe_allow_html=True)
        if st.button("دخول الغرفة", key="journal"):
            st.session_state.page = 'مذكرات'
            st.rerun()

    st.write("<br>", unsafe_allow_html=True)
    col4, col5 = st.columns(2)
    with col4:
        st.markdown("<div class='category-card'><h2>☕ المطالعة</h2><p>غذاء الروح والعقل</p></div>", unsafe_allow_html=True)
        if st.button("دخول الغرفة", key="read"):
            st.session_state.page = 'مطالعة'
            st.rerun()
    with col5:
        st.markdown("<div class='category-card'><h2>🍎 الأكل</h2><p>تنظيم الوجبات الصحي</p></div>", unsafe_allow_html=True)
        if st.button("دخول الغرفة", key="food"):
            st.session_state.page = 'أكل'
            st.rerun()

# --- الصفحة الثانية: غرف المهام المتخصصة ---
else:
    room = st.session_state.page
    st.markdown(f"<h1 style='text-align:center; color:white;'>📍 غرفة {room}</h1>", unsafe_allow_html=True)
    
    if st.button("⬅️ العودة للرئيسية"):
        st.session_state.page = 'welcome'
        st.rerun()

    st.write("---")

    # إضافة مهمة داخل الغرفة
    with st.container():
        c_in1, c_in2 = st.columns([3, 1])
        with c_in1:
            t_text = st.text_input(f"ما هي مهمة {room} القادمة؟")
        with c_in2:
            t_time = st.time_input("توقيت المنبه")
        
        if st.button(f"تثبيت في جدول {room}"):
            if t_text:
                data["tasks"].append({"category": room, "name": t_text, "time": str(t_time), "done": False})
                save_data(data)
                st.rerun()

    # عرض المهام الخاصة بهذه الغرفة فقط
    st.subheader(f"✅ قائمة مهام {room} الحالية:")
    for i, t in enumerate(data["tasks"]):
        if t["category"] == room and not t["done"]:
            st.markdown(f"""
                <div style='background:rgba(255,255,255,0.1); padding:15px; border-radius:15px; border-left: 5px solid #00ffff; margin-bottom:10px;'>
                    <h3 style='margin:0; color:#00ffff;'>{t['name']}</h3>
                    <p style='margin:0; color:#eee;'>⏰ التوقيت: {t['time']}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("تم الإنجاز ✅", key=f"d_{i}"):
                t["done"] = True
                save_data(data)
                st.rerun()
        
