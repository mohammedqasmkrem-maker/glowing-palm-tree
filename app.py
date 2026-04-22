import streamlit as st
import json
import os

# --- إعدادات الصفحة ---
st.set_page_config(page_title="شجرة مهام محمد", page_icon="🌳")

# --- CSS مستقر جداً وبسيط ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Changa:wght@400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #e0f2f1; /* لون أخضر فاتح مريح */
        font-family: 'Changa', sans-serif;
        direction: rtl;
    }
    
    /* ستايل الورقة */
    .leaf-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border-right: 8px solid #2e7d32;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 10px;
        text-align: right;
    }
    
    .stMetric { background: white; padding: 10px; border-radius: 10px; box-shadow: 1px 1px 5px rgba(0,0,0,0.1); }
    h1, h2, h3 { color: #2e7d32; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- نظام البيانات ---
DB_FILE = "data.json"
def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except: return {"level": 1, "xp": 0, "gold": 50, "tasks": []}
    return {"level": 1, "xp": 0, "gold": 50, "tasks": []}

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False)

data = load_data()

# --- واجهة التطبيق ---
st.write(f"<h1 style='font-size: 30px;'>🌳 شجرة مهام محمد الأسطورية</h1>", unsafe_allow_html=True)

# عرض الإحصائيات بشكل مبسط
c1, c2 = st.columns(2)
with c1: st.metric("المستوى 🔥", data["level"])
with c2: st.metric("الذهب 💰", data["gold"])

st.progress(min(data["xp"] / (data["level"] * 100), 1.0))
st.write(f"<p style='text-align:center;'>الخبرة الحالية: {data['xp']}</p>", unsafe_allow_html=True)

st.write("---")

# إضافة المهمة
with st.expander("➕ أضف مهمة جديدة (وحش)"):
    t_input = st.text_input("ماذا ستنجز اليوم؟")
    if st.button("إضافة إلى الشجرة"):
        if t_input:
            data["tasks"].append({"id": len(data["tasks"]), "name": t_input, "done": False})
            save_data(data)
            st.rerun()

# عرض المهام (الوحوش)
st.subheader("🍃 المهام المعلقة")
for task in data["tasks"]:
    if not task["done"]:
        st.markdown(f"""
            <div class='leaf-card'>
                <h4 style='margin:0;'>🍂 {task['name']}</h4>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"هزيمة الوحش 🗡️", key=f"btn_{task['id']}"):
            task["done"] = True
            data["xp"] += 35
            data["gold"] += 15
            if data["xp"] >= data["level"] * 100:
                data["level"] += 1
                data["xp"] = 0
                st.balloons()
            save_data(data)
            st.rerun()

if st.sidebar.button("حذف كل البيانات"):
    if os.path.exists(DB_FILE): os.remove(DB_FILE)
    st.rerun()
    
