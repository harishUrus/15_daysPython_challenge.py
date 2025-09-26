import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(page_title="Advanced Gym Workout Logger 🏋", page_icon="🏋", layout="wide")

# -------------------------------
# Enhanced Gym Theme CSS
# -------------------------------
st.markdown(
    """
    <style>
    /* Main app background with gym-themed gradient */
    .stApp {
        background: linear-gradient(135deg, #0f0f0f, #1a1a2e, #16213e, #0f0f23);
        color: #ffffff;
    }
    
    /* Headers and text styling */
    .main-header {
        color: #FFFFFF;
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .section-header {
        color: #FFFFFF;
        border-bottom: 2px solid #FF6B35;
        padding-bottom: 0.5rem;
    }
    
    /* Override Streamlit default header colors */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #2d2d2d;
        color: #FFFFFF !important;
        border-radius: 5px 5px 0 0;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #FF6B35 !important;
        color: #FFFFFF !important;
    }
    
    /* Subheader styling */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }
    
    .stSelectbox label, .stNumberInput label, .stTextInput label, .stTextArea label, .stMultiSelect label, .stCheckbox label, .stSlider label {
        color: #FFFFFF !important;
    }
    
    /* Metric labels */
    .metric-container label {
        color: #FFFFFF !important;
    }
    
    /* Metric cards styling */
    .metric-card {
        background: linear-gradient(135deg, #2d2d2d, #3d3d3d);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #FF6B35;
        margin: 0.5rem 0;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(45deg, #FF6B35, #F7931E);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1a1a1a;
    }
    
    /* Success/Info messages */
    .stSuccess {
        background-color: #28a745;
        color: white;
    }
    
    /* DataFrame styling */
    .stDataFrame {
        background-color: #2d2d2d;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------
# Initialize Enhanced Session State
# -------------------------------
if "workout_data" not in st.session_state:
    st.session_state.workout_data = []

if "current_session" not in st.session_state:
    st.session_state.current_session = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if "exercise_templates" not in st.session_state:
    st.session_state.exercise_templates = {
        "Chest": ["Bench Press", "Incline Press", "Dumbbell Press", "Push-ups", "Chest Flyes"],
        "Back": ["Pull-ups", "Lat Pulldown", "Deadlift", "Bent Over Row", "T-Bar Row"],
        "Legs": ["Squat", "Leg Press", "Lunges", "Leg Curl", "Calf Raises"],
        "Shoulders": ["Overhead Press", "Lateral Raises", "Rear Delt Flyes", "Arnold Press", "Shrugs"],
        "Biceps": ["Barbell Curls", "Dumbbell Curls", "Hammer Curls", "Preacher Curls", "Cable Curls"],
        "Triceps": ["Tricep Dips", "Close Grip Press", "Overhead Extension", "Cable Pushdowns", "Diamond Push-ups"],
        "Abs": ["Crunches", "Plank", "Russian Twists", "Leg Raises", "Mountain Climbers"],
        "Full Body": ["Burpees", "Thrusters", "Clean and Press", "Turkish Get-ups", "Battle Ropes"]
    }

if "personal_records" not in st.session_state:
    st.session_state.personal_records = {}

if "workout_goals" not in st.session_state:
    st.session_state.workout_goals = {
        "weekly_sessions": 4,
        "weekly_volume": 5000,
        "target_exercises": 20
    }

# -------------------------------
# Enhanced Functions
# -------------------------------
def log_exercise(exercise, sets, reps, weight, muscle_group, equipment, notes="", rest_time=60):
    total_volume = sets * reps * weight
    st.session_state.workout_data.append({
        "Session": st.session_state.current_session,
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Exercise": exercise,
        "Muscle Group": muscle_group,
        "Equipment": equipment,
        "Sets": sets,
        "Reps": reps,
        "Weight (kg)": weight,
        "Volume": total_volume,
        "Rest Time (s)": rest_time,
        "Notes": notes,
        "RPE": None  # Rate of Perceived Exertion (1-10)
    })
    
    # Update personal records
    exercise_key = f"{exercise}_{muscle_group}"
    if exercise_key not in st.session_state.personal_records:
        st.session_state.personal_records[exercise_key] = {"max_weight": weight, "max_volume": total_volume}
    else:
        if weight > st.session_state.personal_records[exercise_key]["max_weight"]:
            st.session_state.personal_records[exercise_key]["max_weight"] = weight
        if total_volume > st.session_state.personal_records[exercise_key]["max_volume"]:
            st.session_state.personal_records[exercise_key]["max_volume"] = total_volume

def remove_entry(index):
    if 0 <= index < len(st.session_state.workout_data):
        st.session_state.workout_data.pop(index)

def get_filtered_data(exercise_filter="All", date_from=None, date_to=None, muscle_group_filter="All"):
    df = pd.DataFrame(st.session_state.workout_data)
    if df.empty:
        return df
    
    # Apply filters
    if exercise_filter != "All":
        df = df[df["Exercise"] == exercise_filter]
    
    if muscle_group_filter != "All":
        df = df[df["Muscle Group"] == muscle_group_filter]
    
    if date_from and date_to:
        df = df[(df["Date"] >= date_from.strftime("%Y-%m-%d")) & 
                (df["Date"] <= date_to.strftime("%Y-%m-%d"))]
    
    return df

def get_weekly_analytics():
    if not st.session_state.workout_data:
        return None
    
    df = pd.DataFrame(st.session_state.workout_data)
    today = datetime.now()
    week_ago = today - timedelta(days=7)
    
    # Filter last 7 days
    week_df = df[df["Date"] >= week_ago.strftime("%Y-%m-%d")]
    
    analytics = {
        "total_sessions": len(week_df["Session"].unique()),
        "total_exercises": len(week_df),
        "total_volume": week_df["Volume"].sum(),
        "avg_session_duration": 0,  # Would need session end times
        "muscle_groups_trained": week_df["Muscle Group"].nunique(),
        "top_exercise": week_df["Exercise"].mode().iloc[0] if not week_df.empty else "None",
        "pr_count": 0  # Count of personal records this week
    }
    
    return analytics

def calculate_progress_metrics():
    if not st.session_state.workout_data:
        return {}
    
    df = pd.DataFrame(st.session_state.workout_data)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Group by exercise and calculate progress
    progress_data = {}
    for exercise in df['Exercise'].unique():
        exercise_df = df[df['Exercise'] == exercise].sort_values('Date')
        if len(exercise_df) >= 2:
            latest_weight = exercise_df['Weight (kg)'].iloc[-1]
            earliest_weight = exercise_df['Weight (kg)'].iloc[0]
            progress_data[exercise] = {
                'weight_progress': latest_weight - earliest_weight,
                'volume_trend': exercise_df['Volume'].pct_change().mean()
            }
    
    return progress_data

# -------------------------------
# Main App Header
# -------------------------------
st.markdown('<h1 class="main-header">💪 Advanced Gym Workout Logger</h1>', unsafe_allow_html=True)
st.markdown(f"**🏋️ Current Session:** {st.session_state.current_session}")

# -------------------------------
# Sidebar - Quick Stats & Controls
# -------------------------------
with st.sidebar:
    st.markdown("### 📊 Quick Stats")
    
    if st.session_state.workout_data:
        total_workouts = len(set([w["Session"] for w in st.session_state.workout_data]))
        total_volume = sum([w["Volume"] for w in st.session_state.workout_data])
        
        st.metric("Total Sessions", total_workouts)
        st.metric("Total Volume (kg)", f"{total_volume:,.0f}")
        st.metric("Exercises Logged", len(st.session_state.workout_data))
    
    st.markdown("---")
    st.markdown("### ⚙️ Session Controls")
    
    if st.button("🔄 New Session", use_container_width=True):
        st.session_state.current_session = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.success("New session started!")
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 🎯 Weekly Goals")
    
    # Goal setting
    st.session_state.workout_goals["weekly_sessions"] = st.number_input(
        "Target Sessions/Week", 1, 7, st.session_state.workout_goals["weekly_sessions"]
    )
    st.session_state.workout_goals["weekly_volume"] = st.number_input(
        "Target Volume/Week (kg)", 1000, 20000, st.session_state.workout_goals["weekly_volume"]
    )

# -------------------------------
# Main Content Tabs
# -------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📥 Log Workout", "📊 Analytics", "📋 History", "🏆 Records", "📈 Progress"])

# -------------------------------
# TAB 1: Log Workout (Enhanced)
# -------------------------------
with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h3 style="color: white; border-bottom: 2px solid #FF6B35; padding-bottom: 0.5rem;">Log New Exercise</h3>', unsafe_allow_html=True)
        
        # Enhanced exercise input
        muscle_group = st.selectbox("🎯 Muscle Group", 
                                    ["Chest", "Back", "Legs", "Shoulders", "Biceps", "Triceps", "Abs", "Full Body"])
        
        # Exercise template or custom
        use_template = st.checkbox("📝 Use Exercise Template")
        
        if use_template:
            exercise = st.selectbox("Exercise", st.session_state.exercise_templates[muscle_group])
        else:
            exercise = st.text_input("Custom Exercise Name")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            sets = st.number_input("Sets", 1, 10, 3)
        with col_b:
            reps = st.number_input("Reps", 1, 50, 10)
        with col_c:
            weight = st.number_input("Weight (kg)", 0.0, 500.0, 20.0, 1.0)
        
        equipment = st.multiselect("🛠️ Equipment", 
                                   ["Barbell", "Dumbbell", "Machine", "Cable", "Bodyweight", "Kettlebell", "Resistance Band", "Other"])
        
        col_d, col_e = st.columns(2)
        with col_d:
            rest_time = st.number_input("Rest Time (seconds)", 30, 300, 60)
        with col_e:
            rpe = st.slider("RPE (Rate of Perceived Exertion)", 1, 10, 7)
        
        notes = st.text_area("📝 Notes", placeholder="Any additional notes about this set...")
        
        if st.button("💪 Log Exercise", type="primary", use_container_width=True):
            if exercise.strip():
                log_exercise(exercise, sets, reps, weight, muscle_group, ", ".join(equipment), notes, rest_time)
                st.success(f"✅ Logged: {exercise} - {sets}×{reps} @ {weight}kg")
                st.balloons()
                st.rerun()
            else:
                st.warning("Please enter an exercise name.")
    
    with col2:
        st.markdown('<h3 style="color: white; border-bottom: 2px solid #FF6B35; padding-bottom: 0.5rem;">Session Summary</h3>', unsafe_allow_html=True)
        
        # Current session stats
        current_session_data = [w for w in st.session_state.workout_data if w["Session"] == st.session_state.current_session]
        
        if current_session_data:
            session_volume = sum([w["Volume"] for w in current_session_data])
            session_exercises = len(current_session_data)
            session_muscle_groups = len(set([w["Muscle Group"] for w in current_session_data]))
            
            st.metric("Session Volume", f"{session_volume:,.0f} kg")
            st.metric("Exercises Done", session_exercises)
            st.metric("Muscle Groups", session_muscle_groups)
            
            # Quick session overview
            st.markdown("**Current Session:**")
            for exercise_data in current_session_data[-3:]:  # Show last 3
                st.markdown(f"• {exercise_data['Exercise']}: {exercise_data['Sets']}×{exercise_data['Reps']} @ {exercise_data['Weight (kg)']}kg")
        else:
            st.info("Start logging exercises to see session summary!")

# -------------------------------
# TAB 2: Enhanced Analytics
# -------------------------------
with tab2:
    st.markdown('<h3 style="color: white; border-bottom: 2px solid #FF6B35; padding-bottom: 0.5rem;">Workout Analytics Dashboard</h3>', unsafe_allow_html=True)
    
    if st.session_state.workout_data:
        analytics = get_weekly_analytics()
        
        # Key metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Weekly Sessions", analytics["total_sessions"], 
                     delta=analytics["total_sessions"] - st.session_state.workout_goals["weekly_sessions"])
        with col2:
            st.metric("Weekly Volume", f"{analytics['total_volume']:,.0f} kg",
                     delta=f"{analytics['total_volume'] - st.session_state.workout_goals['weekly_volume']:,.0f}")
        with col3:
            st.metric("Total Exercises", analytics["total_exercises"])
        with col4:
            st.metric("Muscle Groups", analytics["muscle_groups_trained"])
        
        # Charts section
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("📈 Weekly Volume Trend")
            df = pd.DataFrame(st.session_state.workout_data)
            df['Date'] = pd.to_datetime(df['Date'])
            
            # Group by date and sum volume
            daily_volume = df.groupby('Date')['Volume'].sum().reset_index()
            daily_volume = daily_volume.tail(14)  # Last 14 days
            
            fig_volume = px.line(daily_volume, x='Date', y='Volume',
                               title="Daily Training Volume",
                               color_discrete_sequence=['#FF6B35'])
            fig_volume.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig_volume, use_container_width=True)
        
        with col_right:
            st.subheader("🎯 Muscle Group Distribution")
            muscle_dist = df.groupby('Muscle Group')['Volume'].sum().reset_index()
            
            fig_muscle = px.pie(muscle_dist, values='Volume', names='Muscle Group',
                              title="Training Volume by Muscle Group",
                              color_discrete_sequence=px.colors.qualitative.Set3)
            fig_muscle.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig_muscle, use_container_width=True)
        
        # Exercise frequency analysis
        st.subheader("🔥 Most Frequent Exercises")
        exercise_freq = df.groupby('Exercise').agg({
            'Volume': 'sum',
            'Exercise': 'count'
        }).rename(columns={'Exercise': 'Frequency'}).sort_values('Frequency', ascending=False).head(10)
        
        fig_freq = px.bar(exercise_freq.reset_index(), x='Exercise', y=['Volume', 'Frequency'],
                         title="Top Exercises by Frequency and Volume",
                         barmode='group',
                         color_discrete_sequence=['#FF6B35', '#FFD700'])
        fig_freq.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_freq, use_container_width=True)
        
    else:
        st.info("Start logging workouts to see analytics!")

# -------------------------------
# TAB 3: Enhanced History with Filters
# -------------------------------
with tab3:
    st.markdown('<h3 style="color: white; border-bottom: 2px solid #FF6B35; padding-bottom: 0.5rem;">Workout History</h3>', unsafe_allow_html=True)
    
    if st.session_state.workout_data:
        # Advanced filters
        st.markdown("### 🔍 Filters")
        filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
        
        with filter_col1:
            exercises = ["All"] + list(set([w["Exercise"] for w in st.session_state.workout_data]))
            exercise_filter = st.selectbox("Exercise", exercises)
        
        with filter_col2:
            muscle_groups = ["All"] + list(set([w["Muscle Group"] for w in st.session_state.workout_data]))
            muscle_filter = st.selectbox("Muscle Group", muscle_groups)
        
        with filter_col3:
            date_from = st.date_input("From Date", datetime.now() - timedelta(days=30))
        
        with filter_col4:
            date_to = st.date_input("To Date", datetime.now())
        
        # Apply filters and display
        filtered_df = get_filtered_data(exercise_filter, date_from, date_to, muscle_filter)
        
        if not filtered_df.empty:
            st.markdown(f"**Showing {len(filtered_df)} records**")
            
            # Enhanced display with better formatting
            display_df = filtered_df[['Date', 'Time', 'Exercise', 'Muscle Group', 'Sets', 'Reps', 'Weight (kg)', 'Volume', 'Notes']].copy()
            st.dataframe(display_df, use_container_width=True)
            
            # Bulk operations
            col_export, col_delete = st.columns(2)
            
            with col_export:
                csv = filtered_df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Export Filtered Data", csv, "filtered_workout_data.csv", "text/csv")
            
            with col_delete:
                if st.button("🗑️ Clear Filtered Data", type="secondary"):
                    st.warning("This will delete all filtered records. Confirm?")
                    if st.button("⚠️ Confirm Delete"):
                        # Remove filtered records from session state
                        for idx in filtered_df.index:
                            if idx < len(st.session_state.workout_data):
                                st.session_state.workout_data.pop(idx)
                        st.success("Filtered data deleted!")
                        st.rerun()
        else:
            st.info("No records match the selected filters.")
    else:
        st.info("No workout history available yet.")

# -------------------------------
# TAB 4: Personal Records
# -------------------------------
with tab4:
    st.markdown('<h3 style="color: white; border-bottom: 2px solid #FF6B35; padding-bottom: 0.5rem;">Personal Records 🏆</h3>', unsafe_allow_html=True)
    
    if st.session_state.personal_records:
        pr_data = []
        for exercise_key, records in st.session_state.personal_records.items():
            exercise, muscle_group = exercise_key.split('_', 1)
            pr_data.append({
                'Exercise': exercise,
                'Muscle Group': muscle_group,
                'Max Weight (kg)': records['max_weight'],
                'Max Volume (kg)': records['max_volume']
            })
        
        pr_df = pd.DataFrame(pr_data).sort_values('Max Weight (kg)', ascending=False)
        st.dataframe(pr_df, use_container_width=True)
        
        # PR achievements chart
        st.subheader("💪 Strength Progression")
        
        if len(pr_df) > 0:
            fig_pr = px.bar(pr_df.head(10), x='Exercise', y='Max Weight (kg)',
                           color='Muscle Group',
                           title="Top 10 Personal Records by Weight")
            fig_pr.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig_pr, use_container_width=True)
    else:
        st.info("Keep working out to establish your personal records!")

# -------------------------------
# TAB 5: Progress Tracking
# -------------------------------
with tab5:
    st.markdown('<h3 style="color: white; border-bottom: 2px solid #FF6B35; padding-bottom: 0.5rem;">Progress Tracking 📈</h3>', unsafe_allow_html=True)
    
    if len(st.session_state.workout_data) > 1:
        progress_metrics = calculate_progress_metrics()
        
        if progress_metrics:
            st.subheader("🎯 Exercise Progress")
            
            progress_data = []
            for exercise, metrics in progress_metrics.items():
                progress_data.append({
                    'Exercise': exercise,
                    'Weight Progress (kg)': round(metrics['weight_progress'], 2),
                    'Volume Trend (%)': round(metrics['volume_trend'] * 100, 2) if not pd.isna(metrics['volume_trend']) else 0
                })
            
            progress_df = pd.DataFrame(progress_data)
            st.dataframe(progress_df, use_container_width=True)
            
            # Progress visualization
            df = pd.DataFrame(st.session_state.workout_data)
            df['Date'] = pd.to_datetime(df['Date'])
            
            # Select exercise for detailed progress
            exercise_options = df['Exercise'].unique()
            selected_exercise = st.selectbox("Select Exercise for Detailed Progress", exercise_options)
            
            if selected_exercise:
                exercise_data = df[df['Exercise'] == selected_exercise].sort_values('Date')
                
                fig_progress = make_subplots(
                    rows=2, cols=1,
                    subplot_titles=('Weight Progression', 'Volume Progression'),
                    specs=[[{"secondary_y": False}],
                           [{"secondary_y": False}]]
                )
                
                # Weight progression
                fig_progress.add_trace(
                    go.Scatter(x=exercise_data['Date'], y=exercise_data['Weight (kg)'],
                             mode='lines+markers', name='Weight',
                             line=dict(color='#FF6B35')),
                    row=1, col=1
                )
                
                # Volume progression
                fig_progress.add_trace(
                    go.Scatter(x=exercise_data['Date'], y=exercise_data['Volume'],
                             mode='lines+markers', name='Volume',
                             line=dict(color='#FFD700')),
                    row=2, col=1
                )
                
                fig_progress.update_layout(
                    title=f"Progress Tracking: {selected_exercise}",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    height=600
                )
                
                st.plotly_chart(fig_progress, use_container_width=True)
        else:
            st.info("Need more workout data to calculate progress trends!")
    else:
        st.info("Log more workouts to track your progress over time!")

# -------------------------------
# Footer with Additional Controls
# -------------------------------
st.markdown("---")
st.markdown("### 🔧 Data Management")

col_footer1, col_footer2, col_footer3 = st.columns(3)

with col_footer1:
    if st.button("💾 Export All Data", use_container_width=True):
        if st.session_state.workout_data:
            full_df = pd.DataFrame(st.session_state.workout_data)
            csv = full_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Complete Dataset", csv, "complete_workout_data.csv", "text/csv")

with col_footer2:
    if st.button("🔄 Reset Session", type="secondary", use_container_width=True):
        st.session_state.current_session = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.success("Session reset!")

with col_footer3:
    if st.button("⚠️ Clear All Data", type="secondary", use_container_width=True):
        if st.button("Confirm Clear All", type="secondary"):
            st.session_state.workout_data = []
            st.session_state.personal_records = {}
            st.success("All data cleared!")
            st.rerun()

# -------------------------------
# Motivational Footer
# -------------------------------
st.markdown(
    """
    <div style='text-align: center; margin-top: 2rem; padding: 1rem; background: linear-gradient(45deg, #FF6B35, #F7931E); border-radius: 10px;'>
    <h4 style='color: white; margin: 0;'>💪 "The only bad workout is the one that didn't happen!" 💪</h4>
    <p style='color: white; margin: 0.5rem 0 0 0;'>Keep pushing your limits and track every rep!</p>
    </div>
    """, 
    unsafe_allow_html=True
)