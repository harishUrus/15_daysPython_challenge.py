import streamlit as st
import time

# -------------------------------------
# Page Configuration
# -------------------------------------
st.set_page_config(
    page_title="BMI Calculator 🏋",
    page_icon="🏋",
    layout="centered"
)

# -------------------------------------
# Custom CSS Styling
# -------------------------------------
st.markdown("""
    <style>
        /* Background Gradient */
        .stApp {
            background: linear-gradient(135deg, #ffecd2, #fcb69f, #ffdde1, #fcb69f);
            color: #2c2c2c;
            font-family: 'Arial', sans-serif;
        }

        /* Title Styling */
        h1, h2, h3 {
            text-align: center;
            color: #ff5722;
            font-weight: bold;
        }

        /* Input Labels */
        label, .stRadio label {
            color: #222 !important;
            font-weight: bold;
        }

        /* Buttons - Vibrant */
        div.stButton > button:first-child {
            background: linear-gradient(to right, #ff5722, #ff9800);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
        }

        div.stButton > button:first-child:hover {
            background: linear-gradient(to right, #e64a19, #f57c00);
            transform: scale(1.05);
        }

        /* Result Box Styling */
        .result-box {
            background: #ffffffcc;
            padding: 20px;
            border-radius: 12px;
            border: 2px solid #ff5722;
            margin-top: 20px;
            text-align: center;
            font-size: 22px;
            font-weight: bold;
            color: #222;
        }

        /* Suggestion Styling */
        .suggestion {
            background: #fff8e1;
            padding: 15px;
            border-radius: 10px;
            margin-top: 15px;
            border-left: 6px solid #ff9800;
            font-size: 18px;
            font-weight: normal;
        }

        /* Pop-up message text */
        .popup {
            font-size: 20px;
            font-weight: bold;
            color: #ff5722;
            text-align: center;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------
# Helper Functions
# -------------------------------------
def calculate_bmi(weight, height, weight_unit, height_unit):
    """Calculate BMI with selected units."""
    if weight_unit == "lbs":
        weight = weight * 0.453592  # lbs to kg

    if height_unit == "feet":
        height = height * 30.48  # feet to cm

    height_m = height / 100  # cm to meters
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)

def get_health_category(bmi):
    """Return health category and suggestions based on BMI."""
    if bmi < 18.5:
        return "Underweight", "Include more nutritious, calorie-dense foods and strength training exercises."
    elif 18.5 <= bmi < 24.9:
        return "Normal", "Maintain your healthy lifestyle with balanced meals and regular activity."
    elif 25 <= bmi < 29.9:
        return "Overweight", "Incorporate more cardio workouts and watch portion sizes to manage weight."
    else:
        return "Obese", "Consult a healthcare provider for a personalized plan, focus on diet and active routine."

# -------------------------------------
# UI Title
# -------------------------------------
st.title("🏋 BMI Calculator")

st.write("Welcome! Let's find out your **Body Mass Index** and see where you stand on your health journey.")

# -------------------------------------
# User Inputs
# -------------------------------------
name = st.text_input("Enter Your Name")
gender = st.radio("Select Gender", ["Male", "Female"])

col1, col2 = st.columns(2)

with col1:
    weight_unit = st.selectbox("Weight Unit", ["kg", "lbs"])
    weight = st.number_input(f"Enter Weight ({weight_unit})", min_value=0.0, step=0.1)

with col2:
    height_unit = st.selectbox("Height Unit", ["cm", "feet"])
    height = st.number_input(f"Enter Height ({height_unit})", min_value=0.0, step=0.1)

# -------------------------------------
# Calculate BMI Button
# -------------------------------------
if st.button("Calculate BMI"):
    if not name or weight <= 0 or height <= 0:
        st.error("⚠️ Please enter all details properly before calculating!")
    else:
        # Pop-up animation before result
        with st.spinner('🔥 Ready... Set... Go! Calculating your BMI...'):
            time.sleep(2)

        bmi_value = calculate_bmi(weight, height, weight_unit, height_unit)
        category, suggestion = get_health_category(bmi_value)

        # Display BMI Result
        st.markdown(f"""
            <div class='result-box'>
                Hi <strong>{name}</strong>! <br>
                Your BMI is: <span style='color:#ff5722;'>{bmi_value}</span><br>
                Health Category: <span style='color:#ff9800;'>{category}</span>
            </div>
        """, unsafe_allow_html=True)

        # Suggestion box
        st.markdown(f"""
            <div class='suggestion'>
                💡 <strong>Suggestion:</strong> {suggestion}
            </div>
        """, unsafe_allow_html=True)
