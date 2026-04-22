import streamlit as st
import json
import os

# --- إعدادات الصفحة ---
st.set_page_config(page_title="مغامرة محمد الأسطورية", page_icon="🌳", layout="wide")

# --- CSS جبار للألوان والجمالية ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Changa:wght@700&display=swap');
    
    /* خلفية الغابة الحيوية */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                    url('https://img.freepik.com/free-vector/jungle-forest-with-river-background_1308-54522.jpg');
        background-size: cover;
        background-position: center;
    }

    /* كروت المهام - ستايل الخشب والذهب */
    .quest-card {
        background: linear-gradient(135deg, #5d4037 0%, #3e2723 100%);
        border: 3px solid #ffd700;
        border-radius: 20px;
        padding: 20px;
        margin: 15px 0px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
        text-align: right;
        color: white;
    }

    .xp-badge {
        background: #ffd700;
        color: #000;
        padding: 5px 15px;
        border-radius: 50px;
        font-weight: bold;
        float: left;
    }

    /* العدادات العلوية */
    .stat-box {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border: 2px solid #ffd700;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        color: #ffd700;
        font-family: 'Changa', sans-serif;
    }

    .stButton>button {
        background: #ffd700 !important;
        color: #000 !important;
        font-weight: bolder !important;
        border-radius: 30px !important;
        border: 2px solid #fff !important;
        height: 3em !important;
        font-size: 1.1em !important;
    }
    
    h1, h2, h3 { font-family: 'Changa', sans-serif; color: #ffd700 !important; text-shadow: 2px 2px 10px #000; }
    </style>
    """, unsafe_allow_html=True)

# --- نظام البيانات ---
DB = "save_data.json"
def load():
    if os.path.exists(DB):
        with open(DB, "r", encoding="utf-8") as f: return json.load(f)
    return {"level": 1, "xp": 0, "gold": 100, "tasks": []}

def save(data):
    with open(DB, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False)

data = load()

# --- واجهة البطل ---
st.markdown("<h1 style='text-align:center;'>🛡️ مملكة البطل محمد قاسم 🛡️</h1>", unsafe_allow_html=True)

# العدادات (Stats)
c1, c2, c3 = st.columns(3)
with c1: st.markdown(f"<div class='stat-box'>🔥 المستوى<br><span style='font-size:30px;'>{data['level']}</span></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='stat-box'>💰 الذهب<br><span style='font-size:30px;'>{data['gold']}</span></div>", unsafe_allow_html=True)
with c3:
    xp_prog = (data['xp'] / (data['level'] * 100)) * 100
    st.markdown(f"<div class='stat-box'>⭐ الخبرة<br><span style='font-size:30px;'>{int(xp_prog)}%</span></div>", unsafe_allow_html=True)

st.write("")
st.progress(data['xp'] / (data['level'] * 100))

# منطقة إضافة المهام
with st.expander("📜 استدعاء وحش جديد (إضافة مهمة)"):
    name = st.text_input("شنو اسم الوحش؟")
    if st.button("تثبيت المهمة بالخريطة ⚔️"):
        if name:
            data["tasks"].append({"name": name, "done": False, "xp": 45})
            save(data)
            st.rerun()

# عرض "وحوش الغابة" (المهام)
st.markdown("### 🌲 وحوش بانتظار سيفك")
for i, t in enumerate(data["tasks"]):
    if not t["done"]:
        st.markdown(f"""
            <div class="quest-card">
                <span class="xp-badge">+{t['xp']} XP</span>
                <h2 style='margin:0;'>👾 {t['name']}</h2>
                <p style='color:#ccc; margin:0;'>الخطر: متوسط | المكافأة: ذهب و خبرة</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"سحق الوحش {t['name']} 🗡️", key=f"btn_{i}"):
            t["done"] = True
            data["xp"] += t["xp"]
            data["gold"] += 20
            if data["xp"] >= data["level"] * 100:
                data["level"] += 1
                data["xp"] = 0
                st.balloons()
            save(data)
            st.rerun()

if st.sidebar.button("حذف السجل وابدأ مغامرة جديدة"):
    if os.path.exists(DB): os.remove(DB)
    st.rerun()
    
