import streamlit as st
import json
import os
from datetime import datetime

# --- إعدادات الصفحة ---
st.set_page_config(page_title="مهام محمد البحرية", page_icon="🌊", layout="wide")

# --- CSS لتصميم البحر والخانات ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Changa:wght@700&display=swap');
    
    /* خلفية البحر */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), 
                    url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80');
        background-size: cover;
        background-attachment: fixed;
        font-family: 'Changa', sans-serif;
    }

    /* خانة المهمة الشفافة */
    .task-box {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
        color: white;
        text-align: right;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }

    .stTimeInput label, .stTextInput label { color: white !important; font-size: 18px !important; }
    
    h1 { color: white; text-shadow: 2px 2px 10px #000; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- نظام الحفظ ---
DB = "sea_tasks.json"
def load_data():
    if os.path.exists(DB):
        with open(DB, "r", encoding="utf-8") as f: return json.load(f)
    return []

def save_data(tasks):
    with open(DB, "w", encoding="utf-8") as f: json.dump(tasks, f, ensure_ascii=False)

tasks = load_data()

# --- الواجهة ---
st.markdown("<h1>🌊 غواص المهام: ساحة محمد 🌊</h1>", unsafe_allow_html=True)

# إضافة مهمة جديدة مع وقت
with st.container():
    st.markdown("<div style='background:rgba(0,0,0,0.5); padding:20px; border-radius:15px;'>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        task_text = st.text_input("شنو المهمة اللي ببالك؟")
    with col2:
        task_time = st.time_input("وقت التنبيه")
    
    if st.button("تثبيت المهمة وتشغيل المنبه 🔔"):
        if task_text:
            new_task = {
                "id": len(tasks),
                "name": task_text,
                "time": str(task_time),
                "done": False
            }
            tasks.append(new_task)
            save_data(tasks)
            st.success(f"تم ضبط المنبه لـ {task_text} الساعة {task_time}")
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.write("---")

# عرض المهام كخانات مرتبة
st.markdown("<h3 style='color:white;'>📋 جدول مهامك اليومية:</h3>", unsafe_allow_html=True)

for i, t in enumerate(tasks):
    if not t["done"]:
        with st.container():
            st.markdown(f"""
                <div class="task-box">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-direction: row-reverse;">
                        <div style="font-size: 22px; font-weight: bold;">📍 {t['name']}</div>
                        <div style="background: #00bcd4; padding: 5px 15px; border-radius: 10px; font-size: 16px;">⏰ {t['time']}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"تم الإنجاز ✅", key=f"done_{i}"):
                t["done"] = True
                save_data(tasks)
                st.balloons()
                st.rerun()

# تنبيه المنبه (بسيط)
current_time = datetime.now().strftime("%H:%M")
for t in tasks:
    if not t["done"] and t["time"][:5] == current_time:
        st.warning(f"🔔 حان الآن موعد مهمة: {t['name']}!")
        st.toast(f"انتبه! موعد {t['name']}")

if st.sidebar.button("مسح كل المهام"):
    save_data([])
    st.rerun()
    
