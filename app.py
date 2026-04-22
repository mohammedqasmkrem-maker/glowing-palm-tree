import streamlit as st
import json
import os
from datetime import datetime
import time

# --- 1. إعدادات الصفحة والأساس ---
st.set_page_config(page_title="مملكة محمد قاسم", page_icon="🔱", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

# --- 2. نظام حفظ البيانات ---
def load_data():
    if os.path.exists("mohammed_king_final.json"):
        with open("mohammed_king_final.json", "r", encoding="utf-8") as f: return json.load(f)
    return {"tasks": [], "journal": []}

def save_data(data):
    with open("mohammed_king_final.json", "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False)

data = load_data()

# --- 3. الواجهة الرئيسية (الترحيب) ---
if st.session_state.page == 'welcome':
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Changa:wght@700&display=swap');
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                        url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1350&q=80');
            background-size: cover; background-attachment: fixed; font-family: 'Changa', sans-serif;
        }
        .room-card {
            background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(15px);
            border: 2px solid rgba(255, 255, 255, 0.2); border-radius: 25px;
            padding: 30px; text-align: center; color: white; transition: 0.3s;
        }
        .room-card:hover { border-color: #00ffff; transform: translateY(-5px); }
        .stButton>button { width: 100%; border-radius: 15px !important; font-weight: bold; }
        </style>
        """, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align:center; color:white; font-size:55px; text-shadow: 2px 2px 10px #000;'>🔱 مملكة محمد قاسم 🔱</h1>", unsafe_allow_html=True)
    
    cols = st.columns(4)
    rooms = [
        {"id": "دراسة", "icon": "📚", "title": "الدراسة"},
        {"id": "رياضة", "icon": "💪", "title": "الرياضة"},
        {"id": "مذكرات", "icon": "📖", "title": "المذكرات"},
        {"id": "مطالعة", "icon": "☕", "title": "المطالعة"}
    ]
    
    for i, r in enumerate(rooms):
        with cols[i]:
            st.markdown(f"<div class='room-card'><h1>{r['icon']}</h1><h3>{r['title']}</h3></div>", unsafe_allow_html=True)
            if st.button(f"دخول {r['title']}", key=f"btn_{r['id']}"):
                st.session_state.page = r['id']
                st.rerun()

# --- 4. الغرف التخصصية ---
else:
    room = st.session_state.page
    
    # اختيار الخلفية واللون حسب الغرفة
    styles = {
        "دراسة": ("https://images.unsplash.com/photo-1497633762265-9d179a990aa6", "#4caf50"),
        "رياضة": ("https://images.unsplash.com/photo-1534438327276-14e5300c3a48", "#f44336"),
        "مذكرات": ("https://images.unsplash.com/photo-1517842645767-c639042777db", "#795548"),
        "مطالعة": ("https://images.unsplash.com/photo-1524995997946-a1c2e315a42f", "#2196f3")
    }
    bg_url, m_color = styles[room]

    st.markdown(f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('{bg_url}');
            background-size: cover;
        }}
        .journal-paper {{
            background: #fffcf0; padding: 25px; border-radius: 10px; border-left: 8px solid {m_color};
            color: #333; margin-bottom: 15px; box-shadow: 2px 2px 10px rgba(0,0,0,0.2); text-align: right;
        }}
        </style>
        """, unsafe_allow_html=True)

    if st.button("🔙 العودة للرئيسية"):
        st.session_state.page = 'welcome'
        st.rerun()

    st.markdown(f"<h1 style='text-align:center; color:{m_color};'>{room} محمد قاسم</h1>", unsafe_allow_html=True)

    # --- أدوات الرياضة ---
    if room == "رياضة":
        col1, col2 = st.columns([1, 1])
        with col1:
            st.write("### ⏱️ ساعة التمرين")
            if st.button("تشغيل العداد"): st.session_state.t_start = time.time()
            if 't_start' in st.session_state and st.session_state.t_start:
                el = int(time.time() - st.session_state.t_start)
                st.subheader(f"⏱️ {el//60:02d}:{el%60:02d}")
                if st.button("إيقاف"): st.session_state.t_start = None
        with col2:
            st.write("### 🏃 قائمة التمارين")
            ex_name = st.text_input("التمرين (مثلاً: شناو، ركض)")
            if st.button("إضافة تمرين"):
                if ex_name:
                    data["tasks"].append({"cat": room, "name": ex_name, "done": False})
                    save_data(data)
                    st.rerun()

    # --- أدوات المذكرات ---
    elif room == "مذكرات":
        note = st.text_area("🖋️ اكتب مذكراتك هنا...", height=150)
        if st.button("حفظ في السجل الخشبي"):
            if note:
                data["journal"].append({"date": datetime.now().strftime("%Y-%m-%d"), "text": note})
                save_data(data)
                st.success("تم الحفظ!")
                st.rerun()
        st.write("---")
        for j in reversed(data["journal"]):
            st.markdown(f"<div class='journal-paper'><small>{j['date']}</small><br>{j['text']}</div>", unsafe_allow_html=True)

    # --- الدراسة والمطالعة ---
    else:
        t_in = st.text_input("أضف مهمة جديدة:")
        if st.button("حفظ المهمة"):
            if t_in:
                data["tasks"].append({"cat": room, "name": t_in, "done": False})
                save_data(data)
                st.rerun()

    # عرض المهام العامة لكل غرفة
    if room != "مذكرات":
        for i, t in enumerate(data["tasks"]):
            if t["cat"] == room and not t["done"]:
                st.info(f"📍 {t['name']}")
                if st.button("تم ✅", key=f"d_{i}"):
                    t["done"] = True
                    save_data(data)
                    st.rerun()
    
