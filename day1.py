import streamlit as st

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Greeting Application",
    page_icon="👋",
    layout="centered",
)

# -------------------------------
# Custom CSS for Styling
# -------------------------------
st.markdown("""
    <style>
        /* Background color */
        .stApp {
            background-color: #0b1d3a; /* Dark navy blue */
            color: white;
        }

        /* Make labels white */
        label, .stSlider label, .stTextInput label {
            color: white !important;
            font-weight: bold;
        }
        
        /* Gradient button styling */
        div.stButton > button:first-child {
            background: linear-gradient(to right, #6a11cb, #2575fc);
            color: white !important;
            border: none;
            padding: 0.6em 1.2em;
            border-radius: 12px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
        }

        div.stButton > button:first-child:hover {
            background: linear-gradient(to right, #2575fc, #6a11cb);
            transform: scale(1.05);
        }

        /* Pop-up styling */
        .popup-alert {
            padding: 10px;
            background-color: #ff4d4d;
            color: white;
            border-radius: 8px;
            font-weight: bold;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# Title
# -------------------------------
st.title("👋 Greeting Application")

# -------------------------------
# Form Inputs
# -------------------------------
st.write("Please fill out the form below:")

with st.form("greeting_form"):
    # Name input
    name = st.text_input("Enter your name")

    # Age slider
    age = st.slider(
        "Select your age",
        min_value=1,
        max_value=100,
        value=18,
        step=1
    )

    # Show selected age dynamically below the slider
    if age < 30:
        age_color = "green"
    elif age < 60:
        age_color = "orange"
    else:
        age_color = "red"

    st.markdown(
        f"<p style='color:{age_color};font-weight:bold;margin-top:5px;'>Selected Age: {age}</p>",
        unsafe_allow_html=True
    )

    # Submit button
    submitted = st.form_submit_button("Submit")

    # -------------------------------
    # Validation and Response
    # -------------------------------
    if submitted:
        if not name or age == 0:
            st.markdown(
                "<div class='popup-alert'>⚠️ Please enter your name and select your age before submitting.</div>",
                unsafe_allow_html=True
            )
        else:
            st.success(f"Hello, {name}! You are {age} years old. Welcome to the Greeting Application 🎉")
