import streamlit as st
import json
import os

# --- إعدادات الصفحة ---
st.set_page_config(page_title="ساحة مهام محمد", page_icon="🗡️", layout="wide")

# --- ستايل خانات المهام (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Changa:wght@700&display=swap');
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url('https://wallpaperaccess.com/full/1253733.jpg');
        background-size: cover;
        font-family: 'Changa', sans-serif;
    }

    /* تصميم خانة المهمة */
    .quest-slot {
        background: rgba(45, 20, 10, 0.85); /* لون خشبي محروق */
        border: 2px solid #ffd700;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.5);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-direction: row-reverse; /* للغة العربية */
    }

    .quest-info h3 { margin: 0; color: #ffd700 !important; font-size: 22px; }
    .quest-info p { margin: 0; color: #ddd; font-size: 14px; }

    .xp-amount {
        background: #b8860b;
        color: white;
        padding: 5px 12px;
        border-radius: 8px;
        font-weight: bold;
        border: 1px solid #ffd700;
    }

    /* ستايل زر السحق */
    .stButton>button {
        background: linear-gradient(to bottom, #d32f2f, #b71c1c) !important;
        color: white !important;
        border: 1px solid #fff !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- نظام الحفظ ---
DB = "rpg_quests.json"
def load():
    if os.path.exists(DB):
        with open(DB, "r", encoding="utf-8") as f: return json.load(f)
    return {"level": 1, "xp": 0, "gold": 100, "tasks": []}

def save(data):
    with open(DB, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False)

data = load()

# --- الهيدر ---
st.markdown("<h1 style='text-align:center; color:#ffd700;'>🛡️ لوحة مهام البطل محمد 🛡️</h1>", unsafe_allow_html=True)

# عدادات الحالة
c1, c2, c3 = st.columns(3)
with c1: st.metric("المستوى 🔥", data["level"])
with c2: st.metric("الذهب 💰", data["gold"])
with c3: st.metric("الخبرة ⭐", f"{data['xp']}/100")

st.write("---")

# خانة إضافة مهمة جديدة
with st.expander("➕ إضافة مهمة (وحش جديد) إلى الساحة"):
    q_name = st.text_input("اسم المهمة أو الوحش")
    q_diff = st.selectbox("صعوبة المهمة", ["سهلة (40 XP)", "متوسطة (80 XP)", "صعبة (150 XP)"])
    if st.button("تثبيت المهمة باللوحة 📜"):
        if q_name:
            xp_map = {"سهلة (40 XP)": 40, "متوسطة (80 XP)": 80, "صعبة (150 XP)": 150}
            data["tasks"].append({"name": q_name, "xp": xp_map[q_diff], "done": False})
            save(data)
            st.rerun()

# --- عرض الخانات (Quest Log) ---
st.markdown("### 🗡️ المهام المتاحة حالياً")

for i, task in enumerate(data["tasks"]):
    if not task["done"]:
        # إنشاء الخانة باستخدام HTML و Columns للزر
        col_txt, col_btn = st.columns([4, 1])
        
        with col_txt:
            st.markdown(f"""
                <div class="quest-slot">
                    <div class="quest-info">
                        <h3>👾 {task['name']}</h3>
                        <p>الحالة: نشط | الجائزة: <span class="xp-amount">+{task['xp']} XP</span></p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        with col_btn:
            st.write("<br>", unsafe_allow_html=True) # موازنة الزر مع الخانة
            if st.button(f"سحق ⚔️", key=f"kill_{i}"):
                task["done"] = True
                data["xp"] += task["xp"]
                data["gold"] += 25
                if data["xp"] >= 100:
                    data["level"] += 1
                    data["xp"] = 0
                    st.balloons()
                save(data)
                st.rerun()

if st.sidebar.button("تصفير المغامرة"):
    if os.path.exists(DB): os.remove(DB)
    st.rerun()
    
