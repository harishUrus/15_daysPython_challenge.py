import streamlit as st

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Simple Calculator",
    page_icon="🧮",
    layout="centered",
)

# -------------------------------
# Custom CSS Styling
# -------------------------------
st.markdown("""
    <style>
        /* Background color */
        .stApp {
            background-color: #722f37; /* Wine red */
            color: white;
        }

        /* Labels and input text */
        label, .stTextInput label, .stNumberInput label, .stSelectbox label {
            color: white !important;
            font-weight: bold;
        }

        /* Button styling - Beige with grey text */
        div.stButton > button:first-child {
            background-color: #f5f5dc !important; /* Beige */
            color: #333333 !important; /* Grey text */
            border: 1px solid #999999;
            padding: 0.5em 1.2em;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
        }

        div.stButton > button:first-child:hover {
            background-color: #e2e2c4 !important;
            border-color: #777777;
        }

        /* Result box styling */
        .result-box {
            background-color: white;
            color: #333333;
            padding: 20px;
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            border-radius: 10px;
            border: 2px solid #555555;
            margin-top: 20px;
        }

        /* Success message override */
        .stSuccess {
            background-color: transparent !important;
            border: none !important;
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# App Title
# -------------------------------
st.title("🧮 Simple Calculator")

# -------------------------------
# Inputs
# -------------------------------
st.subheader("Enter Your Numbers")

col1, col2 = st.columns(2)
with col1:
    num1 = st.number_input("First Number", value=0.0, step=1.0)

with col2:
    num2 = st.number_input("Second Number", value=0.0, step=1.0)

operation = st.selectbox("Choose Operation", ["Addition (+)", "Subtraction (-)", "Multiplication (×)", "Division (÷)"])

# -------------------------------
# Calculation Logic
# -------------------------------
result = None

if st.button("Calculate"):
    try:
        if operation == "Addition (+)":
            result = num1 + num2
        elif operation == "Subtraction (-)":
            result = num1 - num2
        elif operation == "Multiplication (×)":
            result = num1 * num2
        elif operation == "Division (÷)":
            if num2 == 0:
                st.error("❌ Cannot divide by zero.")
            else:
                result = num1 / num2

        # Display result in styled box
        if result is not None:
            st.markdown(f"""
                <div class='result-box'>
                    Result: {result}
                </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
