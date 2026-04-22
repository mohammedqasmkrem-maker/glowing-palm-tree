import streamlit as st
import json
import os

# --- إعدادات الصفحة ---
st.set_page_config(page_title="شجرة مهام محمد", page_icon="🌳", layout="wide")

# --- ستايل الشجرة والألوان الحيوية (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Changa:wght@400;700&display=swap');
    
    /* خلفية كرتونية حيوية تشبه الصورة اللي ردتها */
    [data-testid="stAppViewContainer"] {
        background-image: url('https://img.freepik.com/free-vector/nature-forest-landscape-background_1308-72431.jpg');
        background-size: cover;
        font-family: 'Changa', sans-serif;
    }

    .stMetric {
        background: rgba(255, 255, 255, 0.9);
        padding: 10px;
        border-radius: 15px;
        border: 2px solid #5d3a1a;
    }

    /* ستايل ورقة المهمة (معلقة على الغصن) */
    .task-leaf {
        background: #fdf5e6;
        border-left: 10px solid #8b4513;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.2);
        color: #4a3121;
        text-align: right;
    }

    .stButton>button {
        background: linear-gradient(to bottom, #ffeb3b, #fbc02d);
        color: #000 !important;
        border-radius: 20px !important;
        font-weight: bold !important;
        border: 2px solid #8b4513 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- نظام حفظ البيانات ---
DB_FILE = "quest_data.json"
def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f: return json.load(f)
    return {"level": 1, "xp": 0, "gold": 50, "tasks": []}

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False)

data = load_data()

# --- واجهة التطبيق ---
st.markdown("<h1 style='text-align:center; color:#fff; text-shadow: 3px 3px 5px #000;'>🌳 مملكة المهام: شجرة محمد 🌳</h1>", unsafe_allow_html=True)

# الإحصائيات (اللفل والذهب)
col_stat1, col_stat2, col_stat3 = st.columns(3)
with col_stat1: st.metric("المستوى 🔥", data["level"])
with col_stat2: st.metric("الذهب 💰", data["gold"])
with col_stat3: 
    prog = min(data["xp"] / (data["level"] * 100), 1.0)
    st.write(f"الخبرة: {data['xp']}")
    st.progress(prog)

st.write("---")

# إضافة مهمة جديدة
with st.expander("➕ أضف ثمرة جديدة للشجرة (مهمة)"):
    new_t = st.text_input("ما هي المهمة؟")
    if st.button("تعليق المهمة 📌"):
        if new_t:
            data["tasks"].append({"name": new_t, "done": False})
            save_data(data)
            st.rerun()

# عرض المهام بستايل "الأوراق"
st.subheader("⚔️ الوحوش المعلقة على الأغصان")
for i, task in enumerate(data["tasks"]):
    if not task["done"]:
        st.markdown(f"""
            <div class="task-leaf">
                <h3 style='margin:0;'>🍂 {task['name']}</h3>
                <small>بانتظار الإنجاز...</small>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"هزيمة الوحش {i} 🗡️", key=f"bt_{i}"):
            task["done"] = True
            data["xp"] += 30
            data["gold"] += 10
            if data["xp"] >= data["level"] * 100:
                data["level"] += 1
                data["xp"] = 0
                st.balloons()
            save_data(data)
            st.rerun()
