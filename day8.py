import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Currency Converter 💱",
    page_icon="💱",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E8B57;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .converter-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .currency-flag {
        font-size: 2rem;
        margin-right: 0.5rem;
    }
    
    .rate-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        border-left: 4px solid #2E8B57;
    }
    
    .conversion-result {
        background: linear-gradient(45deg, #2E8B57, #3CB371);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    
    .quick-amount {
        background: #f8f9fa;
        border: 2px solid #2E8B57;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .quick-amount:hover {
        background: #2E8B57;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Static exchange rates (base currency: USD)
EXCHANGE_RATES = {
    'USD': {'rate': 1.0, 'symbol': '$', 'flag': '🇺🇸', 'name': 'US Dollar'},
    'EUR': {'rate': 0.85, 'symbol': '€', 'flag': '🇪🇺', 'name': 'Euro'},
    'GBP': {'rate': 0.73, 'symbol': '£', 'flag': '🇬🇧', 'name': 'British Pound'},
    'INR': {'rate': 83.12, 'symbol': '₹', 'flag': '🇮🇳', 'name': 'Indian Rupee'},
    'JPY': {'rate': 149.50, 'symbol': '¥', 'flag': '🇯🇵', 'name': 'Japanese Yen'},
    'CNY': {'rate': 7.24, 'symbol': '¥', 'flag': '🇨🇳', 'name': 'Chinese Yuan'},
    'CAD': {'rate': 1.36, 'symbol': 'C$', 'flag': '🇨🇦', 'name': 'Canadian Dollar'},
    'AUD': {'rate': 1.53, 'symbol': 'A$', 'flag': '🇦🇺', 'name': 'Australian Dollar'},
    'CHF': {'rate': 0.89, 'symbol': 'Fr', 'flag': '🇨🇭', 'name': 'Swiss Franc'},
    'SGD': {'rate': 1.35, 'symbol': 'S$', 'flag': '🇸🇬', 'name': 'Singapore Dollar'},
    'KRW': {'rate': 1327.45, 'symbol': '₩', 'flag': '🇰🇷', 'name': 'South Korean Won'},
    'SEK': {'rate': 10.87, 'symbol': 'kr', 'flag': '🇸🇪', 'name': 'Swedish Krona'},
    'NOK': {'rate': 10.65, 'symbol': 'kr', 'flag': '🇳🇴', 'name': 'Norwegian Krone'},
    'DKK': {'rate': 6.34, 'symbol': 'kr', 'flag': '🇩🇰', 'name': 'Danish Krone'},
    'NZD': {'rate': 1.64, 'symbol': 'NZ$', 'flag': '🇳🇿', 'name': 'New Zealand Dollar'},
}

# Initialize session state
if 'conversion_history' not in st.session_state:
    st.session_state.conversion_history = []

if 'favorite_pairs' not in st.session_state:
    st.session_state.favorite_pairs = [('USD', 'INR'), ('EUR', 'USD'), ('GBP', 'USD')]

def convert_currency(amount, from_currency, to_currency):
    """Convert currency using static rates"""
    if from_currency == to_currency:
        return amount
    
    # Convert to USD first, then to target currency
    usd_amount = amount / EXCHANGE_RATES[from_currency]['rate']
    converted_amount = usd_amount * EXCHANGE_RATES[to_currency]['rate']
    
    return converted_amount

def add_to_history(amount, from_curr, to_curr, result):
    """Add conversion to history"""
    st.session_state.conversion_history.append({
        'timestamp': datetime.now(),
        'amount': amount,
        'from_currency': from_curr,
        'to_currency': to_curr,
        'result': result,
        'rate': result / amount if amount != 0 else 0
    })
    
    # Keep only last 20 conversions
    if len(st.session_state.conversion_history) > 20:
        st.session_state.conversion_history.pop(0)

def format_currency(amount, currency):
    """Format currency with proper symbol and decimals"""
    symbol = EXCHANGE_RATES[currency]['symbol']
    
    if currency in ['JPY', 'KRW']:  # No decimals for these currencies
        return f"{symbol}{amount:,.0f}"
    else:
        return f"{symbol}{amount:,.2f}"

# Main header
st.markdown('<h1 class="main-header">💱 Currency Converter</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #666;'>Convert between major world currencies with real-time calculations</p>", unsafe_allow_html=True)

# Main converter section
st.markdown("---")

# Converter interface
col1, col2, col3 = st.columns([1, 0.2, 1])

with col1:
    st.markdown("### 💸 From Currency")
    from_currency = st.selectbox(
        "Select source currency:",
        options=list(EXCHANGE_RATES.keys()),
        format_func=lambda x: f"{EXCHANGE_RATES[x]['flag']} {x} - {EXCHANGE_RATES[x]['name']}",
        index=0,  # USD default
        key="from_curr"
    )
    
    # Initialize amount in session state if not exists
    if 'current_amount' not in st.session_state:
        st.session_state.current_amount = 100.00
    
    amount = st.number_input(
        f"Amount in {from_currency}:",
        min_value=0.01,
        max_value=1000000.00,
        value=st.session_state.current_amount,
        step=0.01,
        format="%.2f",
        key="amount_input"
    )
    
    # Update session state when input changes
    if amount != st.session_state.current_amount:
        st.session_state.current_amount = amount
    
    # Quick amount buttons
    st.markdown("**Quick amounts:**")
    quick_amounts = [1, 10, 50, 100, 500, 1000]
    cols = st.columns(len(quick_amounts))
    
    for i, qa in enumerate(quick_amounts):
        with cols[i]:
            if st.button(f"{qa}", key=f"quick_{qa}", use_container_width=True):
                st.session_state.current_amount = float(qa)
                st.rerun()

with col2:
    st.markdown("### ")
    st.markdown("<div style='text-align: center; margin-top: 3rem;'>", unsafe_allow_html=True)
    if st.button("🔄", help="Swap currencies", use_container_width=True):
        # Swap currencies
        temp = st.session_state.from_curr
        st.session_state.from_curr = st.session_state.to_curr
        st.session_state.to_curr = temp
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("### 💰 To Currency")
    to_currency = st.selectbox(
        "Select target currency:",
        options=list(EXCHANGE_RATES.keys()),
        format_func=lambda x: f"{EXCHANGE_RATES[x]['flag']} {x} - {EXCHANGE_RATES[x]['name']}",
        index=4,  # INR default
        key="to_curr"
    )
    
    # Perform conversion
    if amount > 0:
        converted_amount = convert_currency(amount, from_currency, to_currency)
        exchange_rate = converted_amount / amount
        
        # Display result
        st.markdown("### Result:")
        result_html = f"""
        <div class="conversion-result">
            {format_currency(amount, from_currency)} = {format_currency(converted_amount, to_currency)}
        </div>
        """
        st.markdown(result_html, unsafe_allow_html=True)
        
        # Show exchange rate
        st.info(f"📊 Exchange Rate: 1 {from_currency} = {exchange_rate:.4f} {to_currency}")
        
        # Add to history button
        if st.button("💾 Save to History", use_container_width=True):
            add_to_history(amount, from_currency, to_currency, converted_amount)
            st.success("Conversion saved to history!")

# Additional sections
st.markdown("---")

# Create tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["📊 Currency Rates", "📈 Rate Comparison", "📝 History", "⭐ Favorites"])

with tab1:
    st.markdown("### 💹 Current Exchange Rates (Base: USD)")
    
    # Create rate comparison table
    rates_data = []
    for currency, data in EXCHANGE_RATES.items():
        if currency != 'USD':
            rates_data.append({
                'Currency': f"{data['flag']} {currency}",
                'Name': data['name'],
                'Rate (per USD)': data['rate'],
                'USD per Unit': 1/data['rate'],
                'Symbol': data['symbol']
            })
    
    rates_df = pd.DataFrame(rates_data)
    st.dataframe(rates_df, use_container_width=True)
    
    # Rate visualization
    st.markdown("### 📊 Exchange Rates Visualization")
    
    # Create bar chart of rates
    fig_rates = px.bar(
        rates_df, 
        x='Currency', 
        y='Rate (per USD)',
        title="Exchange Rates relative to USD",
        color='Rate (per USD)',
        color_continuous_scale='viridis'
    )
    fig_rates.update_layout(height=400)
    st.plotly_chart(fig_rates, use_container_width=True)

with tab2:
    st.markdown("### 🔍 Currency Rate Comparison")
    
    # Multi-currency converter
    st.markdown("**Convert 100 units to multiple currencies:**")
    
    base_curr = st.selectbox(
        "Base Currency:",
        options=list(EXCHANGE_RATES.keys()),
        format_func=lambda x: f"{EXCHANGE_RATES[x]['flag']} {x}",
        key="comparison_base"
    )
    
    base_amount = st.number_input("Amount:", value=100.0, key="comparison_amount")
    
    if st.button("🔄 Convert to All Currencies"):
        comparison_data = []
        for curr, data in EXCHANGE_RATES.items():
            if curr != base_curr:
                converted = convert_currency(base_amount, base_curr, curr)
                comparison_data.append({
                    'Currency': f"{data['flag']} {curr}",
                    'Amount': format_currency(converted, curr),
                    'Numeric Value': converted,
                    'Rate': converted / base_amount
                })
        
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df[['Currency', 'Amount', 'Rate']], use_container_width=True)
        
        # Chart showing converted amounts
        fig_comparison = px.bar(
            comparison_df,
            x='Currency',
            y='Numeric Value',
            title=f"Value of {base_amount} {base_curr} in different currencies",
            color='Numeric Value',
            color_continuous_scale='blues'
        )
        fig_comparison.update_layout(height=400)
        st.plotly_chart(fig_comparison, use_container_width=True)

with tab3:
    st.markdown("### 📝 Conversion History")
    
    if st.session_state.conversion_history:
        # Display history
        history_data = []
        for entry in reversed(st.session_state.conversion_history[-10:]):  # Last 10 entries
            history_data.append({
                'Time': entry['timestamp'].strftime("%H:%M:%S"),
                'Date': entry['timestamp'].strftime("%Y-%m-%d"),
                'From': f"{format_currency(entry['amount'], entry['from_currency'])}",
                'To': f"{format_currency(entry['result'], entry['to_currency'])}",
                'Rate': f"1 {entry['from_currency']} = {entry['rate']:.4f} {entry['to_currency']}"
            })
        
        history_df = pd.DataFrame(history_data)
        st.dataframe(history_df, use_container_width=True)
        
        # Clear history button
        if st.button("🗑️ Clear History", type="secondary"):
            st.session_state.conversion_history = []
            st.success("History cleared!")
            st.rerun()
        
        # Export history
        if len(st.session_state.conversion_history) > 0:
            export_df = pd.DataFrame(st.session_state.conversion_history)
            csv = export_df.to_csv(index=False)
            st.download_button(
                "📥 Download History",
                csv,
                "currency_conversion_history.csv",
                "text/csv"
            )
    else:
        st.info("No conversion history yet. Start converting to build your history!")

with tab4:
    st.markdown("### ⭐ Favorite Currency Pairs")
    
    # Display favorite pairs with quick conversion
    st.markdown("**Quick conversions for your favorite pairs:**")
    
    for i, (from_curr, to_curr) in enumerate(st.session_state.favorite_pairs):
        with st.expander(f"{EXCHANGE_RATES[from_curr]['flag']} {from_curr} ↔ {EXCHANGE_RATES[to_curr]['flag']} {to_curr}"):
            col_fav1, col_fav2 = st.columns(2)
            
            with col_fav1:
                fav_amount = st.number_input(f"Amount in {from_curr}:", value=100.0, key=f"fav_{i}")
                if fav_amount > 0:
                    fav_result = convert_currency(fav_amount, from_curr, to_curr)
                    st.success(f"{format_currency(fav_amount, from_curr)} = {format_currency(fav_result, to_curr)}")
            
            with col_fav2:
                st.metric(
                    "Exchange Rate",
                    f"1 {from_curr} = {convert_currency(1, from_curr, to_curr):.4f} {to_curr}"
                )
                if st.button(f"🗑️ Remove", key=f"remove_fav_{i}"):
                    st.session_state.favorite_pairs.pop(i)
                    st.rerun()
    
    # Add new favorite pair
    st.markdown("**Add new favorite pair:**")
    col_add1, col_add2, col_add3 = st.columns([1, 1, 0.3])
    
    with col_add1:
        new_from = st.selectbox(
            "From:",
            options=list(EXCHANGE_RATES.keys()),
            key="new_fav_from"
        )
    
    with col_add2:
        new_to = st.selectbox(
            "To:",
            options=list(EXCHANGE_RATES.keys()),
            key="new_fav_to"
        )
    
    with col_add3:
        if st.button("➕", help="Add to favorites"):
            if (new_from, new_to) not in st.session_state.favorite_pairs:
                st.session_state.favorite_pairs.append((new_from, new_to))
                st.success("Added to favorites!")
                st.rerun()
            else:
                st.warning("Pair already in favorites!")

# Footer with additional info
st.markdown("---")
st.markdown("### ℹ️ About")

col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    st.markdown("""
    **📊 Exchange Rates**
    - Based on recent market rates
    - Updated periodically
    - For reference purposes only
    """)

with col_info2:
    st.markdown("""
    **🔧 Features**
    - Real-time conversion
    - Conversion history
    - Favorite currency pairs
    - Rate comparisons
    """)

with col_info3:
    st.markdown("""
    **💡 Tips**
    - Use quick amount buttons
    - Save frequent conversions
    - Check rate trends
    - Export your history
    """)

# Disclaimer
st.markdown(
    """
    <div style='background-color: #f8f9fa; padding: 1rem; border-radius: 8px; border-left: 4px solid #ffc107; margin-top: 2rem;'>
    <strong>⚠️ Disclaimer:</strong> Exchange rates are static and for demonstration purposes only. 
    For actual financial transactions, please use real-time rates from reliable financial sources.
    </div>
    """,
    unsafe_allow_html=True
)

# Motivational footer
st.markdown(
    """
    <div style='text-align: center; margin-top: 2rem; padding: 1rem; background: linear-gradient(45deg, #2E8B57, #3CB371); border-radius: 10px;'>
    <h4 style='color: white; margin: 0;'>💱 "Money has no borders in the global economy!" 💱</h4>
    <p style='color: white; margin: 0.5rem 0 0 0;'>Convert currencies with confidence and precision!</p>
    </div>
    """,
    unsafe_allow_html=True
)