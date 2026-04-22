import streamlit as st
import json
import os

# --- إعدادات الصفحة وستايل الفينتاج ---
st.set_page_config(page_title="مغامرة محمد", page_icon="⚔️")

st.markdown("""
    <style>
    .main { background-color: #f5f5dc; } /* لون ورقي قديم */
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #8b4513; color: white; }
    h1, h2, h3 { color: #5d4037; font-family: 'Courier New', Courier, monospace; text-align: right; }
    .stWrite { text-align: right; }
    </style>
    """, unsafe_allow_html=True)

# --- نظام إدارة البيانات (قاعدة بيانات بسيطة) ---
DB_FILE = "user_data.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"level": 1, "xp": 0, "hp": 50, "gold": 0, "tasks": []}

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

data = load_data()

# --- خوارزمية التطور (Logic) ---
def add_xp(amount):
    data["xp"] += amount
    data["gold"] += amount // 2
    if data["xp"] >= data["level"] * 100:
        data["level"] += 1
        data["xp"] = 0
        st.balloons()
        st.sidebar.success(f"🎊 كفو! صعدت للمستوى {data['level']}")
    save_data(data)

# --- واجهة المستخدم ---
st.title("🛡️ نظام مغامرة المهام اليومية")

# الجانب (Sidebar) لعرض إحصائيات البطل
st.sidebar.header(f"البطل: محمد قاسم")
st.sidebar.metric("المستوى (Level)", data["level"])
st.sidebar.progress(data["xp"] / (data["level"] * 100), text=f"الخبرة: {data['xp']}")
st.sidebar.metric("الذهب (Gold) 💰", data["gold"])
st.sidebar.metric("الصحة (HP) ❤️", data["hp"])

# قسم إضافة "وحش" (مهمة) جديد
st.subheader("👾 إضافة وحش جديد (مهمة)")
col1, col2 = st.columns([3, 1])
with col1:
    new_task = st.text_input("شنو اسم الوحش؟ (مثلاً: وحش الإنجليزي)", placeholder="اكتب هنا...")
with col2:
    difficulty = st.selectbox("الصعوبة", ["سهل", "متوسط", "صعب"])

if st.button("إرسال الوحش إلى الساحة ⚔️"):
    if new_task:
        xp_reward = {"سهل": 20, "متوسط": 50, "صعب": 100}[difficulty]
        data["tasks"].append({"name": new_task, "xp": xp_reward, "done": False})
        save_data(data)
        st.rerun()

# عرض "ساحة المعركة" (المهام الحالية)
st.subheader("⚔️ ساحة المعركة (مهامك اليومية)")
for i, task in enumerate(data["tasks"]):
    if not task["done"]:
        col_t, col_b = st.columns([4, 1])
        col_t.write(f"**{task['name']}** (الجائزة: {task['xp']} XP)")
        if col_b.button("هزيمة 🗡️", key=f"btn_{i}"):
            task["done"] = True
            add_xp(task["xp"])
            st.rerun()

# نظام العقوبة البسيط (زر يدوي للتجربة)
if st.sidebar.button("نمت وما كملت المهام؟ 💀"):
    data["hp"] -= 10
    save_data(data)
    if data["hp"] <= 0:
        st.error("لقد هُزمت! ارتاح وابدأ من جديد.")
        data["hp"] = 50
    st.rerun()

st.info("نصيحة المبرمج: كلما تخلص مهمة، بطلك يجمع ذهب ويقوى!")
