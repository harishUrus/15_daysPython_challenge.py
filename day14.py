import streamlit as st
import time
from datetime import timedelta, datetime
import pandas as pd
import plotly.graph_objects as go
import os

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(page_title="Advanced Stopwatch ⏱", page_icon="⏱", layout="wide")

# -------------------------------
# CSV Setup for Session History
# -------------------------------
DATA_FILE = "stopwatch_sessions.csv"
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=["session_id", "start_time", "end_time", "duration_seconds"]).to_csv(DATA_FILE, index=False)

# -------------------------------
# Session State Initialization
# -------------------------------
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "elapsed_time" not in st.session_state:
    st.session_state.elapsed_time = 0.0
if "running" not in st.session_state:
    st.session_state.running = False
if "laps" not in st.session_state:
    st.session_state.laps = []
if "session_id" not in st.session_state:
    st.session_state.session_id = None

# -------------------------------
# Stopwatch Functions
# -------------------------------
def start_timer():
    """Start the stopwatch instantly."""
    if not st.session_state.running:
        st.session_state.start_time = time.time() - st.session_state.elapsed_time
        st.session_state.running = True
        if st.session_state.session_id is None:
            st.session_state.session_id = datetime.now().strftime("%Y%m%d%H%M%S")

def stop_timer():
    """Stop the stopwatch and save the session."""
    if st.session_state.running:
        st.session_state.elapsed_time = time.time() - st.session_state.start_time
        st.session_state.running = False

        # Save session to CSV
        df = pd.read_csv(DATA_FILE)
        new_session = pd.DataFrame({
            "session_id": [st.session_state.session_id],
            "start_time": [datetime.fromtimestamp(st.session_state.start_time).strftime("%Y-%m-%d %H:%M:%S")],
            "end_time": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "duration_seconds": [st.session_state.elapsed_time]
        })
        df = pd.concat([df, new_session], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)

def reset_timer():
    """Reset everything instantly."""
    st.session_state.start_time = None
    st.session_state.elapsed_time = 0.0
    st.session_state.running = False
    st.session_state.laps = []
    st.session_state.session_id = None

def add_lap():
    """Record a lap time."""
    if st.session_state.running:
        current_time = time.time() - st.session_state.start_time
        lap_number = len(st.session_state.laps) + 1
        st.session_state.laps.append({
            "Lap": lap_number,
            "Time": str(timedelta(seconds=int(current_time)))
        })

# -------------------------------
# Title
# -------------------------------
st.markdown("<h1 style='text-align:center;color:#0077b6;'>⏱ Advanced Stopwatch</h1>", unsafe_allow_html=True)

# -------------------------------
# Control Buttons
# -------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.button("▶ Start", on_click=start_timer, use_container_width=True)
with col2:
    st.button("⏸ Stop", on_click=stop_timer, use_container_width=True)
with col3:
    st.button("🔄 Reset", on_click=reset_timer, use_container_width=True)
with col4:
    st.button("🏁 Lap", on_click=add_lap, use_container_width=True)

# -------------------------------
# Real-Time Display Placeholders
# -------------------------------
timer_placeholder = st.empty()
gauge_placeholder = st.empty()

# Create stable circular gauge only once
def create_gauge(seconds_value=0):
    """Create a stable circular gauge with fixed layout to prevent shaking."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=seconds_value,
        title={"text": "Seconds", "font": {"size": 20}},
        gauge={
            "axis": {"range": [0, 60]},
            "bar": {"color": "#0077b6"},
            "bgcolor": "#f1f1f1",
            "steps": [
                {"range": [0, 30], "color": "#90e0ef"},
                {"range": [30, 60], "color": "#48cae4"}
            ],
            "borderwidth": 2,
            "bordercolor": "gray",
        },
        number={"font": {"size": 36}}
    ))
    fig.update_layout(
        height=300, width=300,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="white"
    )
    return fig

# Render the initial stable gauge
fig = create_gauge()
gauge_chart = gauge_placeholder.plotly_chart(fig, use_container_width=True)

# -------------------------------
# Live Timer Update Loop
# -------------------------------
while st.session_state.running:
    current_time = time.time() - st.session_state.start_time

    # Update the gauge needle only
    fig = create_gauge(current_time % 60)
    gauge_chart.plotly_chart(fig, use_container_width=True)

    # Update digital display
    timer_placeholder.markdown(
        f"<h2 style='text-align:center;color:#023e8a;'>Elapsed Time: {str(timedelta(seconds=int(current_time)))}</h2>",
        unsafe_allow_html=True
    )

    # Small sleep to keep updates smooth
    time.sleep(0.1)

# Show final frozen time when stopped
final_time = st.session_state.elapsed_time if not st.session_state.running else time.time() - st.session_state.start_time
timer_placeholder.markdown(
    f"<h2 style='text-align:center;color:#023e8a;'>Elapsed Time: {str(timedelta(seconds=int(final_time)))}</h2>",
    unsafe_allow_html=True
)

# -------------------------------
# Lap Times Table
# -------------------------------
if st.session_state.laps:
    st.subheader("🏃 Lap Times")
    lap_df = pd.DataFrame(st.session_state.laps)
    st.table(lap_df)

# -------------------------------
# Session History and Stats
# -------------------------------
st.subheader("📊 Session History & Stats")

history_df = pd.read_csv(DATA_FILE)

if not history_df.empty:
    history_df = history_df.sort_values(by="start_time", ascending=False)
    st.dataframe(history_df, use_container_width=True)

    total_time = history_df["duration_seconds"].sum()
    average_time = history_df["duration_seconds"].mean()

    st.markdown(f"**Total Tracked Time:** {str(timedelta(seconds=int(total_time)))}")
    st.markdown(f"**Average Session Duration:** {str(timedelta(seconds=int(average_time)))}")
else:
    st.info("No sessions recorded yet.")

# -------------------------------
# Footer
# -------------------------------
st.markdown("""
<div style='text-align:center;margin-top:2rem;font-size:0.9rem;color:#666;'>
    ⏳ Real-time stopwatch with laps, session history, and stable circular timer!
</div>
""", unsafe_allow_html=True)
