import streamlit as st
import json
import os
from datetime import datetime
import time

# --- 1. إعدادات الصفحة والستايل الخورافي ---
st.set_page_config(page_title="مغاص محمد الأسطوري", page_icon="🔱", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Changa:wght@700&display=swap');
    
    /* خلفية فيديو أو صورة بحر حية */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), 
                    url('https://wallpaperaccess.com/full/1510461.jpg');
        background-size: cover;
        background-attachment: fixed;
        font-family: 'Changa', sans-serif;
        color: white;
    }

    /* كارت المهمة "رسالة في زجاجة" */
    .quest-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(0, 255, 255, 0.3);
        border-radius: 25px;
        padding: 20px;
        margin-bottom: 20px;
        transition: 0.3s;
    }
    .quest-card:hover { border-color: #00ffff; transform: scale(1.02); }

    /* عدادات الـ RPG */
    .stat-badge {
        background: linear-gradient(45deg, #004d40, #00bcd4);
        padding: 10px 20px;
        border-radius: 15px;
        border: 2px solid #fff;
        text-align: center;
    }

    /* زر السحق القوي */
    .stButton>button {
        background: linear-gradient(to right, #00d2ff, #3a7bd5) !important;
        color: white !important;
        border-radius: 50px !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(0,210,255,0.4) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. نظام البيانات والذكاء ---
DB = "ocean_adventure.json"
def load_game():
    if os.path.exists(DB):
        with open(DB, "r", encoding="utf-8") as f: return json.load(f)
    return {"level": 1, "xp": 0, "gold": 50, "depth": 0, "tasks": []}

def save_game(data):
    with open(DB, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False)

data = load_game()

# --- 3. موسيقى البحر (اختياري) ---
st.sidebar.markdown("### 🔊 ركن الاسترخاء")
if st.sidebar.checkbox("تشغيل صوت الأمواج 🌊"):
    st.sidebar.audio("https://www.soundjay.com/nature/ocean-wave-1.mp3")

# --- 4. واجهة البطل والقائمة العلوية ---
st.markdown("<h1 style='text-align:center;'>🧜‍♂️ مملكة الغواص محمد قاسم 🔱</h1>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f"<div class='stat-badge'>🔥 المستوى<br>{data['level']}</div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='stat-badge'>💰 الذهب<br>{data['gold']}</div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='stat-badge'>⚓ العمق<br>{data['depth']} متر</div>", unsafe_allow_html=True)
with c4: st.markdown(f"<div class='stat-badge'>⭐ الخبرة<br>{data['xp']}/100</div>", unsafe_allow_html=True)

# شريط العمق (Progress)
st.write(f"التقدم نحو الكنز القادم:")
st.progress(data['xp'] / 100)

# --- 5. إضافة مهمة جديدة بستايل "رسالة في زجاجة" ---
with st.expander("📝 أضف مهمة جديدة (رسالة في زجاجة)"):
    col_in1, col_in2 = st.columns([2, 1])
    with col_in1:
        t_name = st.text_input("ما هي مهمتك القادمة؟")
    with col_in2:
        t_time = st.time_input("وقت المنبه ⏰")
    
    if st.button("إلقاء الزجاجة في البحر 🍾"):
        if t_name:
            data["tasks"].append({
                "name": t_name, 
                "time": str(t_time), 
                "done": False,
                "created_at": str(datetime.now())
            })
            save_game(data)
            st.rerun()

# --- 6. ساحة المهام (ساحة المعركة المائية) ---
st.markdown("### 🐚 المهام العالقة في الشعاب المرجانية")

current_t = datetime.now().strftime("%H:%M")

for i, task in enumerate(data["tasks"]):
    if not task["done"]:
        # حساب الوقت المتبقي (Countdown فكرة 5)
        # (تبسيطاً سنعرض الوقت المحدد)
        
        st.markdown(f"""
            <div class="quest-card">
                <div style="display: flex; justify-content: space-between; flex-direction: row-reverse;">
                    <div>
                        <h3 style="margin:0; color:#00ffff;">📜 {task['name']}</h3>
                        <p style="margin:0; font-size:14px; color:#eee;">حان وقت الإنجاز في: {task['time']}</p>
                    </div>
                    <div style="text-align:center;">
                        <span style="font-size:30px;">🎁</span><br>
                        <small>+30 XP</small>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # فكرة المنبه (فكرة 7)
        if task['time'][:5] == current_t:
            st.warning(f"⚠️ تنبيه من الأعماق: موعد {task['name']}!")

        if st.button(f"سحق المهمة والوصول للكنز 🗡️", key=f"win_{i}"):
            task["done"] = True
            data["xp"] += 34
            data["gold"] += 20
            data["depth"] += 10 # الغواص ينزل أعمق (فكرة 1)
            
            if data["xp"] >= 100:
                data["level"] += 1
                data["xp"] = 0
                st.balloons() # احتفالية (فكرة 9)
            
            save_game(data)
            st.toast(f"عاش يا بطل! حصلت على كنز جديد 💎")
            time.sleep(0.5)
            st.rerun()

# --- 7. فكرة 10: وضع الاسترخاء (Zen Mode) ---
if st.sidebar.button("💎 وضع الاسترخاء (Zen Mode)"):
    st.empty()
    st.markdown("<h2 style='text-align:center; margin-top:200px;'>استرخِ مع أمواج البحر... اترك ضجيج المهام قليلاً</h2>", unsafe_allow_html=True)
    st.stop()

if st.sidebar.button("إعادة ضبط كل شيء"):
    if os.path.exists(DB): os.remove(DB)
    st.rerun()
                            
