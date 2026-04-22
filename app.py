import streamlit as st
import json
import os

# --- إعدادات الصفحة ---
st.set_page_config(page_title="مغامرة محمد الأسطورية", page_icon="⚔️", layout="wide")

# --- CSS لتصميم حيوي ورهيب ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Changa:wght@400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear_gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                    url('https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=2000&auto=format&fit=crop');
        background-size: cover;
        font-family: 'Changa', sans-serif;
        color: #fff;
    }
    
    .stMetric { background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 15px; border: 1px solid #ffd700; }
    
    .task-card {
        background: rgba(0, 0, 0, 0.7);
        padding: 20px;
        border-right: 5px solid #ffd700;
        border-radius: 10px;
        margin-bottom: 15px;
        transition: 0.3s;
    }
    .task-card:hover { transform: scale(1.02); background: rgba(50, 50, 50, 0.8); }
    
    h1, h2, h3 { color: #ffd700 !important; text-shadow: 2px 2px #000; text-align: center; }
    
    .stButton>button {
        background: linear-gradient(45deg, #8b4513, #d2691e);
        color: white; border: none; font-weight: bold; width: 100%;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# --- نظام البيانات ---
DB_FILE = "save_game.json"
def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f: return json.load(f)
    return {"level": 1, "xp": 0, "gold": 100, "tasks": []}

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False)

data = load_data()

# --- المنطق البرمجي ---
def add_xp(amt):
    data["xp"] += amt
    data["gold"] += amt // 2
    if data["xp"] >= data["level"] * 100:
        data["level"] += 1
        data["xp"] = 0
        st.balloons()
    save_data(data)

# --- الواجهة الرئيسية ---
st.markdown("<h1>⚔️ مغامرة محمد: صائد الوحوش ⚔️</h1>", unsafe_allow_html=True)

# عرض الإحصائيات بشكل "حيوي"
c1, c2, c3 = st.columns(3)
with c1: st.metric("المستوى 🔥", data["level"])
with c2: st.metric("الذهب 💰", data["gold"])
with c3: 
    prog = data["xp"] / (data["level"] * 100)
    st.write(f"الخبرة (XP): {data['xp']}")
    st.progress(prog)

st.markdown("---")

# إضافة مهمة جديدة بستايل الوحوش
with st.expander("➕ استدعاء وحش جديد (إضافة مهمة)"):
    t_name = st.text_input("اسم المهمة (الوحش)")
    t_diff = st.select_slider("قوة الوحش", options=["ضعيف", "عادي", "زعيم"])
    if st.button("تأكيد الاستدعاء 📜"):
        xp_map = {"ضعيف": 30, "عادي": 60, "زعيم": 150}
        data["tasks"].append({"name": t_name, "xp": xp_map[t_diff], "done": False})
        save_data(data)
        st.rerun()

# ساحة المعركة
st.subheader("🗡️ وحوش بانتظارك في الساحة")
for i, task in enumerate(data["tasks"]):
    if not task["done"]:
        st.markdown(f"""
            <div class="task-card">
                <h3 style='text-align:right; margin:0;'>👾 {task['name']}</h3>
                <p style='text-align:right; color:#ddd;'>الجائزة: {task['xp']} نقطة خبرة</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button(f"القضاء على الوحش {i} ⚔️", key=f"t_{i}"):
            task["done"] = True
            add_xp(task["xp"])
            st.toast(f"تم سحق {task['name']}! +{task['xp']} XP")
            st.rerun()

if st.sidebar.button("تصفير المغامرة 🔄"):
    if os.path.exists(DB_FILE): os.remove(DB_FILE)
    st.rerun()
    
