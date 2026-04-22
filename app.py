import streamlit as st
import json
import os
from streamlit_fancier_animations import LottieAnimation

# --- إعدادات الصفحة وستايل RPG-Vintage ---
st.set_page_config(page_title="شجرة مهمات محمد", page_icon="🌳", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background: url('https://img.freepik.com/free-photo/old-paper-parchment-texture_1232-155.jpg');
        background-size: cover;
        font-family: 'Amiri', serif;
        color: #4a3121;
    }
    
    .stMetricValue { color: #b8860b !important; font-size: 50px !important; }
    
    /* ستايل ورقة المهمة المعلقة */
    .hanging-task {
        background: rgba(255, 255, 255, 0.7);
        border: 2px solid #8b4513;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: transform 0.3s ease-out;
        transform-origin: top center;
    }
    .hanging-task:hover { transform: rotate(3deg) scale(1.03); border-color: #ffd700; }

    .stButton>button {
        background: #8b4513; color: white; border: 2px solid #ffd700; border-radius: 5px; font-weight: bold;
        box-shadow: 0 4px 0 #5d3a1a; transition: 0.1s;
    }
    .stButton>button:active { transform: translateY(4px); box-shadow: 0 0 0 #5d3a1a; }
    </style>
    """, unsafe_allow_html=True)

# --- نظام البيانات ---
DB_FILE = "mohammed_quest.json"
def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f: return json.load(f)
    return {"level": 1, "xp": 0, "gold": 50, "tasks": []}

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False)

data = load_data()

# --- خوارزمية التطوير ---
def add_xp(amt):
    data["xp"] += amt
    data["gold"] += amt // 2
    if data["xp"] >= data["level"] * 100:
        data["level"] += 1
        data["xp"] = 0
        st.balloons()
    save_data(data)

# --- الواجهة ---
st.markdown("<h1 style='text-align: center; color: #5d3a1a; text-shadow: 2px 2px #d2b48c;'>🌳 شجرة المهام الأسطورية 🌳</h1>", unsafe_allow_html=True)

# الإحصائيات الفينتاج
c1, c2, c3 = st.columns(3)
with c1: st.metric("المستوى", data["level"])
with c2: st.metric("الذهب 💰", data["gold"])
with c3: 
    st.write(f"الخبرة (XP): {data['xp']}")
    st.progress(data["xp"] / (data["level"] * 100))

st.markdown("---")

# حاوية جانبية لإضافة المهمة (كتيب المهمات)
with st.sidebar:
    st.header("📜 سجل مهمة جديدة")
    task_name = st.text_input("اسم الوحش (المهمة)")
    task_type = st.selectbox("نوع المهمة", ["عادة (متكررة)", "هدد (لمرة واحدة)"])
    if st.button("تعليق على الشجرة 📌"):
        if task_name:
            xp = 40 if task_type == "عادة (متكررة)" else 100
            data["tasks"].append({"name": task_name, "type": task_type, "xp": xp, "done": False})
            save_data(data)
            st.rerun()

# --- عرض "الشجرة الحية" للمهام ---
st.subheader("⚔️ الوحوش المعلقة على الأغصان")
col1, col2 = st.columns([1, 2]) # كولوم للشجرة، وكولوم للمهام

# 1. صورة الشجرة بالأنيميشن
with col1:
    # انيميشن شجرة RPG بسيطة (للتجربة)
    LottieAnimation(url="https://assets2.lottiefiles.com/packages/lf20_w51pviLm.json", height=400, loop=True).show()

# 2. عرض المهام كأنها أوراق تسقط
with col2:
    if not any(not t["done"] for t in data["tasks"]):
        st.success("أشجارك مثمرة! لا وحوش حالياً.")
    else:
        for i, task in enumerate(data["tasks"]):
            if not task["done"]:
                # واجهة ورقة المهمة "المعلقة"
                st.markdown(f"""
                    <div class="hanging-task">
                        <div style='display: flex; justify-content: space-between;'>
                            <span style='color: #ffd700; font-weight: bold;'>+{task['xp']} XP</span>
                            <span style='color: #4a3121;'>{task['name']} 👾</span>
                        </div>
                        <p style='color: #8b4513; margin:0; text-align:right; font-size:0.8em;'>({task['type']})</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # زر هزيمة الوحش بانيميشن سقوط
                if st.button(f"سحق الوحش وجمعه 🗡️", key=f"fall_{i}"):
                    task["done"] = True
                    add_xp(task["xp"])
                    st.toast(f"سقط {task['name']}! حصلت على XP.")
                    st.rerun()
                    
