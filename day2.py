import streamlit as st
import pandas as pd

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Bill Splitter App",
    page_icon="💰",
    layout="centered",
)

# -------------------------------
# Custom CSS for Styling
# -------------------------------
st.markdown("""
    <style>
        /* Background */
        .stApp {
            background-color: #0b1d3a; /* Dark navy blue */
            color: white;
        }

        /* White labels and text */
        label, .stTextInput label, .stNumberInput label, .stSelectbox label {
            color: white !important;
            font-weight: bold;
        }

        /* Normal button styling (not for download buttons) */
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

        /* Section titles */
        .section-title {
            color: #FFD700; /* Golden yellow for visibility */
            font-size: 22px;
            font-weight: bold;
        }

        /* Bright text for important numbers */
        .bright-text {
            color: #00FFCC; /* Bright teal */
            font-size: 18px;
            font-weight: bold;
        }

        /* Suggested Transactions Styling */
        .transactions-box {
            background-color: white;
            color: black;
            padding: 15px;
            border-radius: 10px;
        }

        /* Download section style */
        .download-section {
            color: black;
            background-color: white;
            padding: 10px;
            border-radius: 8px;
        }

        /* Streamlit download button default (clean white with black text) */
        div[data-testid="stDownloadButton"] > button {
            background-color: white !important;
            color: black !important;
            border: 1px solid #000 !important;
            border-radius: 8px;
            font-size: 14px;
            font-weight: bold;
            padding: 8px 16px;
        }

        div[data-testid="stDownloadButton"] > button:hover {
            background-color: #f0f0f0 !important;
            color: black !important;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# App Title
# -------------------------------
st.title("💰 Bill Splitter App")

# -------------------------------
# Inputs: Total Amount & People
# -------------------------------
st.subheader("Step 1: Enter Bill Details")
total_amount = st.number_input("Total Bill Amount", min_value=0.0, step=0.01, format="%.2f")
num_people = st.number_input("Number of People", min_value=1, step=1)

# Split mode
split_mode = st.selectbox("Choose Split Mode", ["Equal Split", "Individual Contribution"])

# -------------------------------
# Inputs for Individual Contributions
# -------------------------------
people_data = []

if num_people > 0:
    st.subheader("Step 2: Enter Names and Contributions")

    for i in range(int(num_people)):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input(f"Person {i+1} Name", key=f"name_{i}")
        with col2:
            contribution = 0.0
            if split_mode == "Individual Contribution":
                contribution = st.number_input(
                    f"{name or 'Person'}'s Contribution", 
                    min_value=0.0, step=0.01, key=f"contribution_{i}"
                )
            people_data.append({"Name": name, "Contribution": contribution})

# -------------------------------
# Processing
# -------------------------------
if st.button("Calculate Settlements"):
    if not total_amount or not num_people:
        st.error("Please enter both Total Amount and Number of People.")
    elif any(p["Name"] == "" for p in people_data):
        st.error("Please enter all names before calculating.")
    else:
        df = pd.DataFrame(people_data)

        # Equal split logic
        if split_mode == "Equal Split":
            equal_share = total_amount / num_people
            df["Contribution"] = equal_share
            st.info(f"Each person should contribute: ₹{equal_share:.2f}")
        else:
            total_contributions = df["Contribution"].sum()
            if total_contributions != total_amount:
                st.warning(
                    f"⚠️ Total contributions ({total_contributions:.2f}) "
                    f"do not match the total bill ({total_amount:.2f})."
                )

        # Fair share calculation
        fair_share = total_amount / num_people
        df["Net Balance"] = df["Contribution"] - fair_share

        # -------------------------------
        # Show Totals Section
        # -------------------------------
        st.markdown("<p class='section-title'>📊 Totals Overview</p>", unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Overall Group Total", f"₹{total_amount:.2f}")
        with col_b:
            st.metric("Fair Share Per Person", f"₹{fair_share:.2f}")

        st.write("### Each Person's Total Contribution:")
        st.dataframe(df[["Name", "Contribution"]])

        # -------------------------------
        # Who Needs to Pay or Receive
        # -------------------------------
        st.markdown("<p class='section-title'>💰 Payment Status</p>", unsafe_allow_html=True)

        payers = df[df["Net Balance"] < 0].copy()
        receivers = df[df["Net Balance"] >= 0].copy()

        st.markdown("<div class='bright-text'>People Who Paid / Settled:</div>", unsafe_allow_html=True)
        if not receivers.empty:
            for index, row in receivers.iterrows():
                st.write(f"✅ **{row['Name']}** contributed or is settled with ₹{row['Contribution']:.2f}")
        else:
            st.info("No one has fully paid yet.")

        st.markdown("<div class='bright-text'>People Who Still Need to Pay:</div>", unsafe_allow_html=True)
        if not payers.empty:
            for index, row in payers.iterrows():
                st.write(f"❌ **{row['Name']}** needs to pay ₹{abs(row['Net Balance']):.2f}")
        else:
            st.info("Everyone has settled up!")

        # -------------------------------
        # Suggested Transactions
        # -------------------------------
        st.markdown("<p class='section-title'>💱 Suggested Transactions</p>", unsafe_allow_html=True)

        payers_copy = payers.copy()
        receivers_copy = receivers[receivers["Net Balance"] > 0].copy()

        payers_copy["Net Balance"] = payers_copy["Net Balance"].abs()
        transactions = []

        for i, payer in payers_copy.iterrows():
            for j, receiver in receivers_copy.iterrows():
                if payer["Net Balance"] == 0:
                    break
                if receiver["Net Balance"] == 0:
                    continue

                amount_to_settle = min(payer["Net Balance"], receiver["Net Balance"])
                transactions.append({
                    "From": payer["Name"],
                    "To": receiver["Name"],
                    "Amount": round(amount_to_settle, 2)
                })

                payer["Net Balance"] -= amount_to_settle
                receivers_copy.at[j, "Net Balance"] -= amount_to_settle

        transactions_df = pd.DataFrame(transactions)

        # Display transactions box
        if not transactions_df.empty:
            st.markdown("<div class='transactions-box'>", unsafe_allow_html=True)
            st.write("Here are the suggested transactions for settling up:")
            st.dataframe(transactions_df)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No transactions needed. Everyone has paid their fair share.")

        # -------------------------------
        # Download Options
        # -------------------------------
        st.markdown("<div class='download-section'><h4>Download Options</h4></div>", unsafe_allow_html=True)

        # CSV for people who paid / settled
        settled_csv = receivers.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Contribution CSV (Paid)",
            data=settled_csv,
            file_name="paid_contributions.csv",
            mime="text/csv",
        )

        # CSV for people who need to pay
        pay_csv = payers.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Pending Payment CSV (Unpaid)",
            data=pay_csv,
            file_name="pending_payments.csv",
            mime="text/csv",
        )

        # Settlement summary
        settlements_csv = transactions_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Settlement Summary CSV",
            data=settlements_csv,
            file_name="settlement_summary.csv",
            mime="text/csv",
        )

# -------------------------------
# Utility Buttons
# -------------------------------
st.subheader("Utility Options")
col_clear, col_recheck = st.columns(2)

with col_clear:
    if st.button("Clear Contributions"):
        st.experimental_rerun()

with col_recheck:
    if st.button("Recheck / Start New Bill Split"):
        st.experimental_rerun()
