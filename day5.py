import streamlit as st

# ------------------------------------
# Page Configuration
# ------------------------------------
st.set_page_config(
    page_title="Unit Converter Playground 🎉",
    page_icon="🔄",
    layout="centered"
)

# ------------------------------------
# Custom CSS for Styling
# ------------------------------------
st.markdown("""
    <style>
        /* Background */
        .stApp {
            background: #f9f9fb;
            font-family: 'Arial', sans-serif;
        }

        /* Title */
        h1 {
            text-align: center;
            color: #1f2937;
            font-size: 38px;
            font-weight: bold;
            margin-bottom: 10px;
        }

        /* Subtitles */
        h2, h3 {
            color: #333333;
            text-align: center;
            font-weight: bold;
        }

        /* Gradient Button Styling */
        div.stButton > button:first-child {
            background: linear-gradient(to right, #ff9a9e, #fad0c4);
            color: #000000;
            border: none;
            border-radius: 12px;
            padding: 12px 30px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
        }

        div.stButton > button:first-child:hover {
            background: linear-gradient(to right, #fbc2eb, #a6c1ee);
            transform: scale(1.05);
        }

        /* Result Box */
        .result-box {
            background: white;
            border: 2px solid #00bcd4;
            border-radius: 12px;
            padding: 20px;
            margin-top: 20px;
            text-align: center;
            font-size: 24px;
            color: #e91e63;
            font-weight: bold;
        }

        /* Footer */
        .footer {
            text-align: center;
            font-size: 14px;
            margin-top: 30px;
            color: #777;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------
# Conversion Logic Functions
# ------------------------------------

# Currency conversion (static rates for demo)
CURRENCY_RATES = {
    "USD": 1.0,
    "INR": 83.0,
    "EUR": 0.92,
    "GBP": 0.78
}

def convert_currency(amount, from_currency, to_currency):
    usd_amount = amount / CURRENCY_RATES[from_currency]
    return round(usd_amount * CURRENCY_RATES[to_currency], 2)

# Temperature conversion
def convert_temperature(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    if from_unit == "Celsius":
        return round((value * 9/5) + 32, 2) if to_unit == "Fahrenheit" else round(value + 273.15, 2)
    elif from_unit == "Fahrenheit":
        return round((value - 32) * 5/9, 2) if to_unit == "Celsius" else round(((value - 32) * 5/9) + 273.15, 2)
    elif from_unit == "Kelvin":
        return round(value - 273.15, 2) if to_unit == "Celsius" else round(((value - 273.15) * 9/5) + 32, 2)

# Length conversion
def convert_length(value, from_unit, to_unit):
    factors = {
        "Meters": 1.0,
        "Feet": 3.28084,
        "Kilometers": 0.001,
        "Miles": 0.000621371
    }
    meters = value / factors[from_unit]
    return round(meters * factors[to_unit], 3)

# Weight conversion
def convert_weight(value, from_unit, to_unit):
    factors = {
        "Kilograms": 1.0,
        "Grams": 1000,
        "Pounds": 2.20462,
        "Ounces": 35.274
    }
    kg = value / factors[from_unit]
    return round(kg * factors[to_unit], 3)

# ------------------------------------
# Top Tabs
# ------------------------------------
tab = st.tabs(["💵 Currency", "🌡️ Temp", "📏 Length", "⚖️ Weight"])

# ------------------------------------
# Currency Converter
# ------------------------------------
with tab[0]:
    st.subheader("Currency Converter")
    col1, col2, col3 = st.columns(3)
    with col1:
        from_currency = st.selectbox("From", CURRENCY_RATES.keys())
    with col2:
        to_currency = st.selectbox("To", CURRENCY_RATES.keys())
    with col3:
        amount = st.number_input("Amount", min_value=0.0, step=0.01)

    if st.button("Convert Currency 💰"):
        result = convert_currency(amount, from_currency, to_currency)
        st.markdown(f"<div class='result-box'>{amount} {from_currency} = {result} {to_currency}</div>", unsafe_allow_html=True)

# ------------------------------------
# Temperature Converter
# ------------------------------------
with tab[1]:
    st.subheader("Temperature Converter")
    units = ["Celsius", "Fahrenheit", "Kelvin"]
    col1, col2, col3 = st.columns(3)
    with col1:
        temp_from = st.selectbox("From", units)
    with col2:
        temp_to = st.selectbox("To", units)
    with col3:
        temp_value = st.number_input("Temperature", step=0.1)

    if st.button("Convert Temperature 🌡️"):
        result = convert_temperature(temp_value, temp_from, temp_to)
        st.markdown(f"<div class='result-box'>{temp_value} {temp_from} = {result} {temp_to}</div>", unsafe_allow_html=True)

# ------------------------------------
# Length Converter
# ------------------------------------
with tab[2]:
    st.subheader("Stretchy Length Converter")
    length_units = ["Meters", "Feet", "Kilometers", "Miles"]
    col1, col2 = st.columns(2)
    with col1:
        from_unit = st.selectbox("From", length_units)
    with col2:
        to_unit = st.selectbox("To", length_units)

    length_value = st.slider("Length", 0.0, 100.0, 1.0, step=0.1)

    if st.button("🌈 Stretch!"):
        result = convert_length(length_value, from_unit, to_unit)
        st.markdown(f"<div class='result-box'>{length_value} {from_unit} = {result} {to_unit}</div>", unsafe_allow_html=True)

# ------------------------------------
# Weight Converter
# ------------------------------------
with tab[3]:
    st.subheader("Weight Converter")
    weight_units = ["Kilograms", "Grams", "Pounds", "Ounces"]
    col1, col2, col3 = st.columns(3)
    with col1:
        w_from = st.selectbox("From", weight_units)
    with col2:
        w_to = st.selectbox("To", weight_units)
    with col3:
        weight_value = st.number_input("Weight", step=0.1)

    if st.button("Convert Weight ⚖️"):
        result = convert_weight(weight_value, w_from, w_to)
        st.markdown(f"<div class='result-box'>{weight_value} {w_from} = {result} {w_to}</div>", unsafe_allow_html=True)

# ------------------------------------
# Footer
# ------------------------------------
st.markdown("<div class='footer'>✨ Every conversion’s a party! ✨<br>Streamlit Playground Edition</div>", unsafe_allow_html=True)
