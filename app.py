import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta, time
import uuid
import random

st.set_page_config(page_title="Daily Tracker", layout="centered")




# ---- HIDE STREAMLIT BRANDING ----
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

footer:after {
    content:'';
    display:none;
}
</style>
""", unsafe_allow_html=True)



# ---- SESSION STATE ----
for key in [
    "expand_activity","expand_sleep","expand_lifestyle",
    "expand_food","expand_reflection",
    "show_data","submitted"
]:
    if key not in st.session_state:
        st.session_state[key] = False

# ---- THEME ----

st.markdown("""
<style>

/* ===== LIGHT MODE ===== */
.stApp {
    background-color: #F9FBFD;
    color: #111;
}

/* Section cards (light) */
.activity { background:#EAF4FF; }
.sleep { background:#F3E8FF; }
.lifestyle { background:#E8F8F1; }
.nutrition { background:#FFF4E6; }
.reflection { background:#FFF9DB; }

/* ===== DARK MODE (Streamlit specific) ===== */
[data-theme="dark"] .stApp {
    background-color: #0E1117;
    color: #E6EDF3;
}

[data-theme="dark"] .activity { background:#1E2A38; }
[data-theme="dark"] .sleep { background:#2A1E38; }
[data-theme="dark"] .lifestyle { background:#1E3830; }
[data-theme="dark"] .nutrition { background:#3A2E1E; }
[data-theme="dark"] .reflection { background:#3A381E; }

/* ===== COMMON ===== */
.section-card {
    border-radius:14px;
    padding:14px;
    margin-bottom:12px;
    border:1px solid rgba(255,255,255,0.05);
}

/* Inputs */
input, textarea {
    color: inherit !important;
}

/* Labels */
label {
    color: inherit !important;
}

/* Metrics */
[data-testid="stMetricValue"] {
    color: inherit !important;
}

/* Clean UI */



/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}






</style>
""", unsafe_allow_html=True)

st.title("📋 DU Tracker")

# ---- TABS ----
tab1, tab2 = st.tabs(["📋 Habit Tracker", "🎟️ Experiences Tracker"])

# =========================================================
# ================= HABIT TRACKER ==========================
# =========================================================
with tab1:

    FILE = "sheet1.csv"

    if os.path.exists(FILE):
        df = pd.read_csv(FILE)
    else:
        df = pd.DataFrame(columns=[
            "ID","Date","Name","Step Count","Date Fund","Motivation",
            "Sleep From","Sleep To","Sleep Hours",
            "Water","Screen Time","Care",
            "Lunch","Dinner","Junk","Gratitude"
        ])

    date = st.date_input("📅 Date", datetime.today())
    date_str = str(date)

    # ---- CHILD ----
    with st.expander("👤 God's Favvv Child"):
        name = st.selectbox("Select Child", ["D","U"])

    # ================= ACTIVITY =================
    st.markdown('<div class="section-card activity">', unsafe_allow_html=True)
    with st.expander("👣 Stepsssss"):

        col1, col2, col3 = st.columns([2,2,1])

        steps = col1.slider("Step Count", 0, 20000, step=500)
        motivation = col2.text_area("🔥 What drove you today?")

        # ---- STEP FEEDBACK ----
        if steps == 0:
            msg = "🛋️ idle mode | 💭 shoes abandoned"
        elif steps < 3000:
            msg = "🚶 barely moving | 📉 warm-up missing"
        elif steps < 5000:
            msg = "🚶 low activity | 😬 stopped early"
        elif steps < 8500:
            msg = "👣 getting there | ⏳ push more"
        elif steps < 10000:
            msg = "👍 almost there | 🎯 close"
        elif steps < 13000:
            msg = "💪 solid movement | 🌟 healthy"
        elif steps < 16000:
            msg = "🔥 high activity | 🚀 strong"
        else:
            msg = "🏆 beast mode | 👑 elite"

        if steps < 5000:
            st.error(f"👣 {steps} steps | {msg}")
        elif steps < 8500:
            st.warning(f"👣 {steps} steps | {msg}")
        elif steps < 12000:
            st.info(f"👣 {steps} steps | {msg}")
        else:
            st.success(f"👣 {steps} steps | {msg}")

        # ---- DATE FUND ----
        if name == "D":
            fine = 100 if steps < 8500 else 0
        else:
            fine = 100 if steps < 10000 else 0

        col3.metric("🍿 Date Fund", f"₹{fine}")

    st.markdown('</div>', unsafe_allow_html=True)

    # ================= SLEEP =================
    st.markdown('<div class="section-card sleep">', unsafe_allow_html=True)
    with st.expander("🛌 Niddhe"):

        c1, c2 = st.columns(2)

        sleep_from = c1.time_input("Sleep From", value=time(0,0))
        sleep_to = c2.time_input("Wake Up", value=time(0,0))

        if sleep_from != time(0,0) or sleep_to != time(0,0):

            s1 = datetime.combine(datetime.today(), sleep_from)
            s2 = datetime.combine(datetime.today(), sleep_to)

            if s2 < s1:
                s2 += timedelta(days=1)

            sleep_hours = round((s2 - s1).seconds / 3600, 2)

            message = f"🛌 {sleep_hours} hrs"

            if time(0,30) <= sleep_from <= time(5,0):
                message += " | 🌙 night owl"
            elif sleep_from >= time(23,0):
                message += " | 😴 decent bedtime"
            else:
                message += " | ⏰ early sleeper"

            if sleep_to > time(10,0):
                message += " | 🌅 woke late"
            elif sleep_to < time(6,0):
                message += " | 🐓 early bird"
            else:
                message += " | ☀️ normal wake"

            if sleep_hours < 6:
                message += " | 💀 survival"
            elif sleep_hours < 8:
                message += " | ☕ low battery"
            elif sleep_hours <= 9:
                message += " | 🌟 elite recovery"
            else:
                message += " | 🐻 hibernation"

            st.info(message)
        else:
            sleep_hours = 0

    st.markdown('</div>', unsafe_allow_html=True)

    # ================= LIFESTYLE =================
    st.markdown('<div class="section-card lifestyle">', unsafe_allow_html=True)
    with st.expander("⚖️ ಇಂದಿನ ದಿನ"):

        screen_time = st.number_input("📱 Screen Time (hrs)", min_value=0.0, step=0.5)

        if screen_time > 6:
            st.error("💀 phone owns your soul")
        elif screen_time > 3.5:
            st.warning("📱 scrolling got clingy")

        water = st.selectbox("💧 Water", ["Less","Mid","Adequate"])
        care = st.radio("🌿 Skin & Hair Care", ["No","Yes"])

    st.markdown('</div>', unsafe_allow_html=True)

    # ================= NUTRITION =================
    st.markdown('<div class="section-card nutrition">', unsafe_allow_html=True)
    with st.expander("🥦 ತಿಂಡಿ/ ತಿನಿಸು"):

        lunch = st.text_input("🥗 Lunch")
        dinner = st.text_input("🍽 Dinner")
        junk = st.radio("🍔 Junk?", ["No","Yes"])

    st.markdown('</div>', unsafe_allow_html=True)

    # ================= REFLECTION =================
    st.markdown('<div class="section-card reflection">', unsafe_allow_html=True)
    with st.expander("🌻 Reflection"):

        gratitude = st.text_area("What are you grateful for today?")

    st.markdown('</div>', unsafe_allow_html=True)

    # ================= SUBMIT =================
    if st.button("🎯 Complete Today"):

        if steps == 0 or not motivation.strip():
            st.error("⚠️ Please fill required fields")
            st.stop()

        # ✅ SAFE SAVE (DICT → no mismatch error)
        df.loc[len(df)] = {
            "ID": str(uuid.uuid4()),
            "Date": date_str,
            "Name": name,
            "Step Count": steps,
            "Date Fund": fine,
            "Motivation": motivation,
            "Sleep From": sleep_from,
            "Sleep To": sleep_to,
            "Sleep Hours": sleep_hours,
            "Water": water,
            "Screen Time": screen_time,
            "Care": care,
            "Lunch": lunch,
            "Dinner": dinner,
            "Junk": junk,
            "Gratitude": gratitude
        }

        df.to_csv(FILE, index=False)

        st.success("🎉 Today completed!")
        st.balloons()

        # ---- INSIGHT ----
        st.markdown("### 💡 Daily Insight")

        parts = []
        parts.append("💪 beast mode" if steps >= 10000 else "🚶 lazy mode")
        parts.append("🛌 slept well" if sleep_hours >= 8 else "😴 low sleep")
        parts.append("📱 balanced screen" if screen_time <= 3.5 else "💀 phone overload")

        st.info("✨ " + " | ".join(parts))

# =========================================================
# ================= EXPERIENCE TAB =========================
# =========================================================
with tab2:

    st.header("🎟️ Experiences Tracker")

    st.info("🚧 Coming soon... exciting things are on the way!")
    st.caption("✨ You'll soon be able to track and revisit your experiences here.")
