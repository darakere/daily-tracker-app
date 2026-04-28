import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta, time
import uuid
import matplotlib.pyplot as plt

st.set_page_config(page_title="Daily Tracker", layout="wide")

st.title("📋 Daily Tracker")

FILE = "sheet1.csv"

# ---- LOAD DATA ----
if os.path.exists(FILE):
    df = pd.read_csv(FILE)
else:
    df = pd.DataFrame(columns=[
        "ID", "Date", "Name", "Step Count", "Fine", "Reason",
        "Sleep From", "Sleep To", "Sleep Hours",
        "Water", "Screen Time", "Lunch", "Dinner",
        "Junk Eaten", "Gratitude"
    ])

# ---- INPUTS ----
col1, col2 = st.columns(2)

with col1:
    date = st.date_input("📅 Date", datetime.today())

with col2:
    name = st.selectbox("👤 User", ["D", "U"])

date_str = str(date)

# ---- GET TODAY DATA ----
today_entries = df[df["Date"] == date_str]

d_steps = None
u_steps = None

for _, row in today_entries.iterrows():
    if row["Name"] == "D":
        d_steps = row["Step Count"]
    elif row["Name"] == "U":
        u_steps = row["Step Count"]

# ---- STEP + REASON + FINE ----
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    steps = st.number_input("👣 Step Count", min_value=0, step=1000, value=0)

with col2:
    reason = st.text_area("⚠️ Reason", height=80)

# include current input
if name == "D":
    d_steps = steps
elif name == "U":
    u_steps = steps

# ---- LIVE FINE ----
fine = 0

if name == "D":
    cond1 = d_steps is not None and d_steps < 8500
    cond2 = u_steps is not None and u_steps >= 13000
    fine = (100 if cond1 else 0) + (100 if cond2 else 0)

elif name == "U":
    cond1 = d_steps is not None and d_steps > 11000
    cond2 = u_steps is not None and u_steps < 10000
    fine = (100 if cond1 else 0) + (100 if cond2 else 0)

with col3:
    st.metric("💰 Fine", f"₹{fine}")

# ---- SCREEN TIME ----
screen_time = st.number_input("📱 Screen Time (hrs)", min_value=0, step=1, value=0)

# ---- SLEEP ----
st.markdown("### 🛌 Sleep Tracker")

col1, col2 = st.columns(2)

with col1:
    sleep_from = st.time_input("🌙 Sleep From", value=time(23, 0))

with col2:
    sleep_to = st.time_input("🌅 Wake Up", value=time(7, 0))

sleep_start = datetime.combine(datetime.today(), sleep_from)
sleep_end = datetime.combine(datetime.today(), sleep_to)

if sleep_end < sleep_start:
    sleep_end += timedelta(days=1)

sleep_hours = round((sleep_end - sleep_start).seconds / 3600, 2)

st.info(f"🛌 Sleep Duration: {sleep_hours} hrs")

# ---- OTHER INPUTS ----
water = st.selectbox("💧 Water Intake", ["Less", "Mid", "Adequate"])
junk = st.radio("🍔 Junk Eaten?", ["No", "Yes"])
lunch = st.text_input("🍱 Lunch")
dinner = st.text_input("🍽 Dinner")
gratitude = st.text_area("🙏 Gratitude")

# ---- SUBMIT ----
if st.button("Submit"):

    errors = []

    if steps == 0:
        errors.append("Step Count required")
    if screen_time == 0:
        errors.append("Screen Time required")
    if not reason.strip():
        errors.append("Reason required")
    if not lunch:
        errors.append("Lunch required")
    if not dinner:
        errors.append("Dinner required")
    if not gratitude.strip():
        errors.append("Gratitude required")
    if sleep_from == sleep_to:
        errors.append("Sleep times cannot match")

    if errors:
        st.error("⚠️ Fix the following:")
        for e in errors:
            st.write(f"- {e}")
        st.stop()

    # ---- UPSERT (NO DUPLICATES) ----
    existing_index = df[
        (df["Date"] == date_str) & (df["Name"] == name)
    ].index

    if len(existing_index) > 0:
        idx = existing_index[0]

        df.at[idx, "Step Count"] = steps
        df.at[idx, "Reason"] = reason
        df.at[idx, "Sleep From"] = sleep_from
        df.at[idx, "Sleep To"] = sleep_to
        df.at[idx, "Sleep Hours"] = sleep_hours
        df.at[idx, "Water"] = water
        df.at[idx, "Screen Time"] = screen_time
        df.at[idx, "Lunch"] = lunch
        df.at[idx, "Dinner"] = dinner
        df.at[idx, "Junk Eaten"] = junk
        df.at[idx, "Gratitude"] = gratitude

    else:
        new_row = {
            "ID": str(uuid.uuid4()),
            "Date": date_str,
            "Name": name,
            "Step Count": steps,
            "Fine": 0,
            "Reason": reason,
            "Sleep From": sleep_from,
            "Sleep To": sleep_to,
            "Sleep Hours": sleep_hours,
            "Water": water,
            "Screen Time": screen_time,
            "Lunch": lunch,
            "Dinner": dinner,
            "Junk Eaten": junk,
            "Gratitude": gratitude
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # ---- SYNC BOTH USERS ----
    mask = df["Date"] == date_str
    today_df = df[mask]

    d_steps = None
    u_steps = None

    for _, row in today_df.iterrows():
        if row["Name"] == "D":
            d_steps = row["Step Count"]
        elif row["Name"] == "U":
            u_steps = row["Step Count"]

    d_fine = (100 if d_steps and d_steps < 8500 else 0) + \
             (100 if u_steps and u_steps >= 13000 else 0)

    u_fine = (100 if d_steps and d_steps > 11000 else 0) + \
             (100 if u_steps and u_steps < 10000 else 0)

    for idx in df[mask].index:
        if df.at[idx, "Name"] == "D":
            df.at[idx, "Fine"] = d_fine
        elif df.at[idx, "Name"] == "U":
            df.at[idx, "Fine"] = u_fine

    df.to_csv(FILE, index=False)

    st.success("✅ Saved successfully!")

# ---- TABLE ----
st.markdown("---")
st.subheader("📊 Records")
st.dataframe(df, use_container_width=True)

# ---- CHARTS ----
st.markdown("### 📈 Trends (Last 7 Days)")

if not df.empty:

    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')

    last_7_days = df[
        df["Date"] >= (pd.to_datetime("today") - pd.Timedelta(days=7))
    ].sort_values("Date")

    if not last_7_days.empty:

        st.subheader("👣 Steps")
        fig1 = plt.figure()
        plt.plot(last_7_days["Date"], last_7_days["Step Count"])
        st.pyplot(fig1)

        st.subheader("🛌 Sleep")
        fig2 = plt.figure()
        plt.plot(last_7_days["Date"], last_7_days["Sleep Hours"])
        st.pyplot(fig2)

        st.subheader("💰 Fine")
        fig3 = plt.figure()
        plt.plot(last_7_days["Date"], last_7_days["Fine"])
        st.pyplot(fig3)
