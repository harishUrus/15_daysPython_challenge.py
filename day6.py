import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(page_title="Water Intake Tracker 💧", page_icon="💧", layout="centered")

# -------------------------------
# Initialize session state
# -------------------------------
if "water_data" not in st.session_state:
    st.session_state.water_data = {}

if "daily_goal" not in st.session_state:
    st.session_state.daily_goal = 3000  # 3L in ml

if "last_reminder" not in st.session_state:
    st.session_state.last_reminder = datetime.now()

# -------------------------------
# Functions
# -------------------------------
def add_water(amount):
    today = datetime.now().strftime("%Y-%m-%d")
    st.session_state.water_data[today] = st.session_state.water_data.get(today, 0) + amount
    st.session_state.last_reminder = datetime.now()  # reset reminder timer

def remove_water(amount):
    today = datetime.now().strftime("%Y-%m-%d")
    current = st.session_state.water_data.get(today, 0)
    st.session_state.water_data[today] = max(current - amount, 0)
    st.session_state.last_reminder = datetime.now()  # reset reminder timer

def reset_today():
    today = datetime.now().strftime("%Y-%m-%d")
    st.session_state.water_data[today] = 0
    st.session_state.last_reminder = datetime.now()  # reset reminder timer

def get_week_data():
    today = datetime.now()
    days, amounts = [], []
    for i in range(6, -1, -1):
        day = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        days.append(day)
        amounts.append(st.session_state.water_data.get(day, 0))
    return pd.DataFrame({"Date": days, "Intake (ml)": amounts})

# Dynamic background color based on progress
def get_bg_color(progress_ratio):
    if progress_ratio < 0.25:
        return "#ffcccc"  # light red
    elif progress_ratio < 0.5:
        return "#ffd699"  # orange
    elif progress_ratio < 0.75:
        return "#cce6ff"  # light blue
    elif progress_ratio < 1.0:
        return "#66ccff"  # blue
    else:
        return "#0066cc"  # dark blue

# -------------------------------
# Main App
# -------------------------------
st.title("💧 Water Intake Tracker")
st.markdown("Track your daily water intake and stay hydrated!")

# --- Daily Goal Input ---
goal = st.number_input("Set your daily goal (liters):", min_value=1.0, max_value=10.0,
                       value=st.session_state.daily_goal / 1000, step=0.5)
st.session_state.daily_goal = int(goal * 1000)

st.divider()

# --- Hydration Reminder ---
st.subheader("⏰ Hydration Reminder")
reminder_interval = st.number_input("Reminder interval (minutes):", min_value=30, max_value=180, value=60, step=15)
time_since_last = (datetime.now() - st.session_state.last_reminder).total_seconds() / 60
if time_since_last >= reminder_interval:
    st.warning(f"💧 Time to drink water! {int(time_since_last)} minutes since your last log.")
    st.session_state.last_reminder = datetime.now()  # reset after showing reminder

st.divider()

# --- Today's Intake Section ---
st.header("📅 Today's Intake")
today = datetime.now().strftime("%Y-%m-%d")
today_intake = st.session_state.water_data.get(today, 0)
progress = min(today_intake / st.session_state.daily_goal, 1.0)

# --- Dynamic Background Display ---
bg_color = get_bg_color(progress)
st.markdown(
    f"""
    <div style="
        background-color: {bg_color};
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    ">
        <h3 style="color: white;">💧 {today_intake} ml / {st.session_state.daily_goal} ml</h3>
    </div>
    """,
    unsafe_allow_html=True
)

st.progress(progress)

# --- Quick Add / Remove Buttons ---
st.subheader("Quick Add / Remove")
portions = [("Glass", 250), ("Bottle", 500), ("Large", 750)]
for name, amount in portions:
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button(f"+ {name} ({amount}ml)"):
            add_water(amount)
            st.rerun()
    with col2:
        if st.button(f"− {name} ({amount}ml)"):
            remove_water(amount)
            st.rerun()

# --- Custom Amount ---
custom = st.number_input("Custom Amount (ml)", min_value=0, max_value=2000, step=50)
col_add, col_remove = st.columns(2)
with col_add:
    if st.button("➕ Add Custom Amount"):
        if custom > 0:
            add_water(custom)
            st.success(f"Added {custom} ml to today's intake!")
            st.rerun()
with col_remove:
    if st.button("➖ Remove Custom Amount"):
        if custom > 0:
            remove_water(custom)
            st.success(f"Removed {custom} ml from today's intake!")
            st.rerun()

st.divider()

# --- Weekly Hydration Chart ---
st.header("📊 Weekly Hydration Chart")
week_df = get_week_data()
if week_df["Intake (ml)"].sum() == 0:
    st.info("Start logging your water intake to see weekly progress.")
else:
    st.bar_chart(data=week_df.set_index("Date"))

# --- Summary Statistics ---
st.subheader("📈 Weekly Summary")
total = week_df["Intake (ml)"].sum()
average = week_df["Intake (ml)"].mean()
col_a, col_b = st.columns(2)
col_a.metric("Total Intake (7 Days)", f"{total / 1000:.2f} L")
col_b.metric("Average Daily Intake", f"{average / 1000:.2f} L")

st.divider()

# --- Data Reset and Export ---
st.subheader("Data Management")
col_reset, col_reset_today, col_export = st.columns([1, 1, 1])

with col_reset:
    if st.button("🗑️ Clear All Data"):
        st.session_state.water_data = {}
        st.success("All data has been cleared!")
        st.rerun()

with col_reset_today:
    if st.button("♻️ Reset Today's Intake"):
        reset_today()
        st.success("Today's intake has been reset!")
        st.rerun()

with col_export:
    if st.session_state.water_data:
        export_df = pd.DataFrame(list(st.session_state.water_data.items()), columns=["Date", "Intake (ml)"])
        csv = export_df.to_csv(index=False).encode('utf-8')  # Fix for download issue
        st.download_button("📥 Download Data as CSV", data=csv, file_name="water_intake.csv", mime="text/csv")
    else:
        st.write("No data to export yet.")
