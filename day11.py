import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import uuid
import base64
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Restaurant Order & Billing 🍔",
    page_icon="🍔",
    layout="wide"
)

# Custom CSS for restaurant theme
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #E74C3C;
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .restaurant-info {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .menu-card {
        background: white;
        border: 2px solid #E74C3C;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .menu-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    .menu-item {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .category-header {
        background: linear-gradient(45deg, #E74C3C, #FF6B6B);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-size: 1.3rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    
    .order-summary {
        background: linear-gradient(135deg, #2ECC71, #27AE60);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .bill-section {
        background: white;
        border: 3px solid #E74C3C;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    
    .total-amount {
        background: linear-gradient(45deg, #E74C3C, #C0392B);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        font-size: 1.8rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    
    .invoice-header {
        text-align: center;
        border-bottom: 2px solid #E74C3C;
        padding-bottom: 1rem;
        margin-bottom: 2rem;
    }
    
    .order-item {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        border-bottom: 1px solid #eee;
    }
    
    .price-tag {
        background: #E74C3C;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
    }
    
    .category-emoji {
        font-size: 2rem;
        margin-right: 0.5rem;
    }
    
    .quantity-control {
        display: flex;
        align-items: center;
        gap: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Restaurant Menu Data
MENU_DATA = {
    "Appetizers": {
        "emoji": "🥗",
        "items": {
            "Chicken Wings (6 pcs)": {"price": 350, "description": "Crispy chicken wings with BBQ sauce"},
            "Mozzarella Sticks (4 pcs)": {"price": 280, "description": "Golden fried mozzarella with marinara sauce"},
            "Onion Rings": {"price": 220, "description": "Beer-battered onion rings with ranch dip"},
            "Caesar Salad": {"price": 320, "description": "Fresh romaine lettuce with caesar dressing"},
            "Garlic Bread": {"price": 180, "description": "Toasted bread with garlic butter and herbs"}
        }
    },
    "Main Course": {
        "emoji": "🍽️",
        "items": {
            "Grilled Chicken Burger": {"price": 450, "description": "Juicy grilled chicken with lettuce, tomato, and mayo"},
            "Beef Steak (250g)": {"price": 750, "description": "Premium beef steak with mashed potatoes"},
            "Fish & Chips": {"price": 420, "description": "Beer-battered fish with crispy fries"},
            "Margherita Pizza (12\")": {"price": 520, "description": "Classic pizza with mozzarella and basil"},
            "Chicken Biryani": {"price": 380, "description": "Aromatic basmati rice with spiced chicken"},
            "Paneer Tikka Masala": {"price": 340, "description": "Cottage cheese in creamy tomato gravy"},
            "Pasta Carbonara": {"price": 400, "description": "Creamy pasta with bacon and parmesan"}
        }
    },
    "Beverages": {
        "emoji": "🥤",
        "items": {
            "Fresh Orange Juice": {"price": 120, "description": "Freshly squeezed orange juice"},
            "Coffee (Hot/Cold)": {"price": 80, "description": "Premium coffee beans, hot or iced"},
            "Masala Chai": {"price": 60, "description": "Traditional Indian spiced tea"},
            "Mango Lassi": {"price": 100, "description": "Yogurt-based mango smoothie"},
            "Coca Cola": {"price": 50, "description": "Chilled cola drink"},
            "Mineral Water": {"price": 30, "description": "500ml mineral water bottle"},
            "Fresh Lime Soda": {"price": 80, "description": "Refreshing lime soda with mint"}
        }
    },
    "Desserts": {
        "emoji": "🍰",
        "items": {
            "Chocolate Brownie": {"price": 180, "description": "Warm brownie with vanilla ice cream"},
            "Tiramisu": {"price": 220, "description": "Classic Italian coffee-flavored dessert"},
            "Gulab Jamun (2 pcs)": {"price": 120, "description": "Sweet milk dumplings in sugar syrup"},
            "Ice Cream Sundae": {"price": 160, "description": "Vanilla ice cream with chocolate sauce"},
            "Cheesecake Slice": {"price": 200, "description": "New York style cheesecake"}
        }
    }
}

# Tax configuration
TAX_RATE = 0.18  # 18% GST
SERVICE_CHARGE_RATE = 0.10  # 10% service charge

# Initialize session state
def init_session_state():
    if 'current_order' not in st.session_state:
        st.session_state.current_order = {}
    if 'order_history' not in st.session_state:
        st.session_state.order_history = []
    if 'table_number' not in st.session_state:
        st.session_state.table_number = 1
    if 'customer_name' not in st.session_state:
        st.session_state.customer_name = ""
    if 'customer_phone' not in st.session_state:
        st.session_state.customer_phone = ""

def add_to_order(item_name, category, price, quantity):
    """Add item to current order"""
    if quantity > 0:
        item_key = f"{category}_{item_name}"
        st.session_state.current_order[item_key] = {
            'name': item_name,
            'category': category,
            'price': price,
            'quantity': quantity,
            'total': price * quantity
        }
    elif item_key in st.session_state.current_order:
        del st.session_state.current_order[item_key]

def calculate_bill():
    """Calculate bill totals"""
    if not st.session_state.current_order:
        return 0, 0, 0, 0, 0
    
    subtotal = sum(item['total'] for item in st.session_state.current_order.values())
    service_charge = subtotal * SERVICE_CHARGE_RATE
    tax_amount = (subtotal + service_charge) * TAX_RATE
    total_amount = subtotal + service_charge + tax_amount
    
    return subtotal, service_charge, tax_amount, total_amount, len(st.session_state.current_order)

def generate_invoice_data():
    """Generate invoice data for export"""
    subtotal, service_charge, tax_amount, total_amount, item_count = calculate_bill()
    
    invoice_data = {
        'invoice_number': f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'table_number': st.session_state.table_number,
        'customer_name': st.session_state.customer_name or "Walk-in Customer",
        'customer_phone': st.session_state.customer_phone or "N/A",
        'items': list(st.session_state.current_order.values()),
        'subtotal': subtotal,
        'service_charge': service_charge,
        'tax_amount': tax_amount,
        'total_amount': total_amount,
        'item_count': item_count
    }
    
    return invoice_data

def save_to_history():
    """Save current order to history"""
    if st.session_state.current_order:
        invoice_data = generate_invoice_data()
        st.session_state.order_history.append(invoice_data)
        st.session_state.current_order = {}

# Initialize session state
init_session_state()

# Restaurant Header
st.markdown('<h1 class="main-header">🍔 Delicious Bites Restaurant</h1>', unsafe_allow_html=True)

# Restaurant info
st.markdown("""
<div class="restaurant-info">
    <h3>📍 123 Food Street, Gourmet City | 📞 +91-98765-43210</h3>
    <p>🕒 Open Daily: 11:00 AM - 11:00 PM | 🚚 Home Delivery Available</p>
</div>
""", unsafe_allow_html=True)

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["🍽️ Menu & Order", "🧾 Current Bill", "📊 Analytics", "📋 Order History"])

# TAB 1: Menu & Order
with tab1:
    # Customer details
    st.markdown("### 👤 Customer Information")
    col_cust1, col_cust2, col_cust3 = st.columns(3)
    
    with col_cust1:
        st.session_state.table_number = st.number_input("🪑 Table Number", min_value=1, max_value=50, value=st.session_state.table_number)
    
    with col_cust2:
        st.session_state.customer_name = st.text_input("👤 Customer Name (Optional)", value=st.session_state.customer_name)
    
    with col_cust3:
        st.session_state.customer_phone = st.text_input("📱 Phone Number (Optional)", value=st.session_state.customer_phone)
    
    st.markdown("---")
    
    # Menu display
    st.markdown("### 🍽️ Our Menu")
    
    # Quick order summary sidebar
    with st.sidebar:
        st.markdown("### 🛒 Quick Order Summary")
        
        if st.session_state.current_order:
            total_items = sum(item['quantity'] for item in st.session_state.current_order.values())
            subtotal, _, _, total_amount, _ = calculate_bill()
            
            st.metric("Items in Cart", total_items)
            st.metric("Subtotal", f"₹{subtotal:.2f}")
            st.metric("Total Amount", f"₹{total_amount:.2f}")
            
            if st.button("🧾 View Full Bill", use_container_width=True):
                st.switch_page("Current Bill")
        else:
            st.info("Your cart is empty")
        
        st.markdown("---")
        st.markdown("### 🏷️ Today's Special")
        st.markdown("**🍕 Margherita Pizza**")
        st.markdown("**20% OFF!**")
        st.markdown("*Valid till midnight*")
    
    # Display menu by category
    for category, category_data in MENU_DATA.items():
        st.markdown(f"""
        <div class="category-header">
            <span class="category-emoji">{category_data['emoji']}</span>
            {category}
        </div>
        """, unsafe_allow_html=True)
        
        # Create columns for menu items
        cols = st.columns(2)
        
        for i, (item_name, item_data) in enumerate(category_data['items'].items()):
            with cols[i % 2]:
                with st.container():
                    col_item1, col_item2 = st.columns([3, 1])
                    
                    with col_item1:
                        st.markdown(f"**{item_name}**")
                        st.markdown(f"*{item_data['description']}*")
                        st.markdown(f'<span class="price-tag">₹{item_data["price"]}</span>', unsafe_allow_html=True)
                    
                    with col_item2:
                        item_key = f"{category}_{item_name}"
                        current_qty = st.session_state.current_order.get(item_key, {}).get('quantity', 0)
                        
                        new_quantity = st.number_input(
                            "Qty", 
                            min_value=0, 
                            max_value=10, 
                            value=current_qty,
                            key=f"qty_{item_key}",
                            help=f"Add {item_name} to order"
                        )
                        
                        if new_quantity != current_qty:
                            add_to_order(item_name, category, item_data['price'], new_quantity)
                            st.rerun()
                
                st.markdown("---")

# TAB 2: Current Bill
with tab2:
    st.markdown("### 🧾 Current Bill")
    
    if not st.session_state.current_order:
        st.info("No items in current order. Please add items from the menu.")
    else:
        # Bill header
        col_bill1, col_bill2 = st.columns(2)
        
        with col_bill1:
            st.markdown(f"**🪑 Table:** {st.session_state.table_number}")
            st.markdown(f"**👤 Customer:** {st.session_state.customer_name or 'Walk-in Customer'}")
        
        with col_bill2:
            st.markdown(f"**📅 Date:** {datetime.now().strftime('%Y-%m-%d')}")
            st.markdown(f"**⏰ Time:** {datetime.now().strftime('%H:%M:%S')}")
        
        st.markdown("---")
        
        # Order items
        st.markdown("### 📋 Order Items")
        
        # Create order items table
        order_items = []
        for item_key, item_info in st.session_state.current_order.items():
            order_items.append({
                'Item': item_info['name'],
                'Category': item_info['category'],
                'Price (₹)': f"₹{item_info['price']:.2f}",
                'Quantity': item_info['quantity'],
                'Total (₹)': f"₹{item_info['total']:.2f}"
            })
        
        order_df = pd.DataFrame(order_items)
        st.dataframe(order_df, use_container_width=True)
        
        # Edit quantities
        st.markdown("### ✏️ Edit Order")
        for item_key, item_info in st.session_state.current_order.items():
            col_edit1, col_edit2, col_edit3 = st.columns([2, 1, 1])
            
            with col_edit1:
                st.markdown(f"**{item_info['name']}** - ₹{item_info['price']}")
            
            with col_edit2:
                new_qty = st.number_input(
                    "New Qty", 
                    min_value=0, 
                    max_value=10, 
                    value=item_info['quantity'],
                    key=f"edit_{item_key}"
                )
            
            with col_edit3:
                if st.button("Update", key=f"update_{item_key}"):
                    if new_qty == 0:
                        del st.session_state.current_order[item_key]
                    else:
                        st.session_state.current_order[item_key]['quantity'] = new_qty
                        st.session_state.current_order[item_key]['total'] = item_info['price'] * new_qty
                    st.rerun()
        
        # Bill calculation
        st.markdown("---")
        subtotal, service_charge, tax_amount, total_amount, item_count = calculate_bill()
        
        st.markdown(f"""
        <div class="bill-section">
            <h4>💰 Bill Summary</h4>
            <div class="order-item">
                <span><strong>Subtotal ({item_count} items):</strong></span>
                <span><strong>₹{subtotal:.2f}</strong></span>
            </div>
            <div class="order-item">
                <span>Service Charge (10%):</span>
                <span>₹{service_charge:.2f}</span>
            </div>
            <div class="order-item">
                <span>GST (18%):</span>
                <span>₹{tax_amount:.2f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="total-amount">
            💳 TOTAL AMOUNT: ₹{total_amount:.2f}
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col_action1, col_action2, col_action3, col_action4 = st.columns(4)
        
        with col_action1:
            if st.button("💾 Save Order", use_container_width=True, type="primary"):
                save_to_history()
                st.success("Order saved successfully!")
                st.rerun()
        
        with col_action2:
            # CSV Export
            if st.session_state.current_order:
                invoice_data = generate_invoice_data()
                
                # Create CSV data
                csv_rows = []
                csv_rows.append(["DELICIOUS BITES RESTAURANT"])
                csv_rows.append(["45 Usman Road, T. Nagar, Chennai - 600017"])
                csv_rows.append(["+91-98765-43210"])
                csv_rows.append([])
                csv_rows.append([f"Invoice: {invoice_data['invoice_number']}"])
                csv_rows.append([f"Date: {invoice_data['date']}"])
                csv_rows.append([f"Table: {invoice_data['table_number']}"])
                csv_rows.append([f"Customer: {invoice_data['customer_name']}"])
                csv_rows.append([])
                csv_rows.append(["Item", "Category", "Price", "Qty", "Total"])
                
                for item in invoice_data['items']:
                    csv_rows.append([
                        item['name'], 
                        item['category'], 
                        f"₹{item['price']}", 
                        item['quantity'], 
                        f"₹{item['total']}"
                    ])
                
                csv_rows.append([])
                csv_rows.append(["Subtotal", "", "", "", f"₹{invoice_data['subtotal']:.2f}"])
                csv_rows.append(["Service Charge (10%)", "", "", "", f"₹{invoice_data['service_charge']:.2f}"])
                csv_rows.append(["GST (18%)", "", "", "", f"₹{invoice_data['tax_amount']:.2f}"])
                csv_rows.append(["TOTAL", "", "", "", f"₹{invoice_data['total_amount']:.2f}"])
                
                csv_content = "\n".join([",".join(map(str, row)) for row in csv_rows])
                
                st.download_button(
                    "📄 Download CSV",
                    csv_content,
                    f"invoice_{invoice_data['invoice_number']}.csv",
                    "text/csv",
                    use_container_width=True
                )
        
        with col_action3:
            # Generate printable invoice
            if st.button("🖨️ Print Invoice", use_container_width=True):
                invoice_data = generate_invoice_data()
                
                # Create HTML invoice
                invoice_html = f"""
                <div class="invoice-header">
                    <h2>🍔 DELICIOUS BITES RESTAURANT</h2>
                    <p>📍 45 Usman Road, T. Nagar, Chennai - 600017</p>
                    <p>📞 +91-98765-43210</p>
                </div>
                
                <div style="margin: 2rem 0;">
                    <p><strong>Invoice Number:</strong> {invoice_data['invoice_number']}</p>
                    <p><strong>Date:</strong> {invoice_data['date']}</p>
                    <p><strong>Table Number:</strong> {invoice_data['table_number']}</p>
                    <p><strong>Customer:</strong> {invoice_data['customer_name']}</p>
                </div>
                
                <table style="width: 100%; border-collapse: collapse; margin: 2rem 0;">
                    <tr style="background-color: #f8f9fa; border: 1px solid #dee2e6;">
                        <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Item</th>
                        <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Price</th>
                        <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Qty</th>
                        <th style="padding: 10px; text-align: right; border: 1px solid #dee2e6;">Total</th>
                    </tr>
                """
                
                for item in invoice_data['items']:
                    invoice_html += f"""
                    <tr style="border: 1px solid #dee2e6;">
                        <td style="padding: 8px; border: 1px solid #dee2e6;">{item['name']}</td>
                        <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">₹{item['price']}</td>
                        <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">{item['quantity']}</td>
                        <td style="padding: 8px; text-align: right; border: 1px solid #dee2e6;">₹{item['total']}</td>
                    </tr>
                    """
                
                invoice_html += f"""
                </table>
                
                <div style="margin-top: 2rem; text-align: right;">
                    <p><strong>Subtotal: ₹{invoice_data['subtotal']:.2f}</strong></p>
                    <p>Service Charge (10%): ₹{invoice_data['service_charge']:.2f}</p>
                    <p>GST (18%): ₹{invoice_data['tax_amount']:.2f}</p>
                    <hr style="border: 2px solid #E74C3C; margin: 1rem 0;">
                    <h3 style="color: #E74C3C;">TOTAL: ₹{invoice_data['total_amount']:.2f}</h3>
                </div>
                
                <div style="text-align: center; margin-top: 2rem; font-style: italic;">
                    <p>Thank you for dining with us! 🙏</p>
                    <p>Visit us again soon! 🍽️</p>
                </div>
                """
                
                st.markdown(invoice_html, unsafe_allow_html=True)
        
        with col_action4:
            if st.button("🗑️ Clear Order", use_container_width=True, type="secondary"):
                st.session_state.current_order = {}
                st.success("Order cleared!")
                st.rerun()

# TAB 3: Analytics
with tab3:
    st.markdown("### 📊 Restaurant Analytics")
    
    if not st.session_state.order_history:
        st.info("No order history available yet. Complete some orders to see analytics.")
    else:
        # Overall statistics
        total_orders = len(st.session_state.order_history)
        total_revenue = sum(order['total_amount'] for order in st.session_state.order_history)
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        
        with col_stat1:
            st.metric("Total Orders", total_orders)
        
        with col_stat2:
            st.metric("Total Revenue", f"₹{total_revenue:.2f}")
        
        with col_stat3:
            st.metric("Avg Order Value", f"₹{avg_order_value:.2f}")
        
        with col_stat4:
            total_items_sold = sum(order['item_count'] for order in st.session_state.order_history)
            st.metric("Items Sold", total_items_sold)
        
        # Charts
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            # Revenue by hour
            hourly_data = {}
            for order in st.session_state.order_history:
                hour = datetime.strptime(order['date'], '%Y-%m-%d %H:%M:%S').hour
                hourly_data[hour] = hourly_data.get(hour, 0) + order['total_amount']
            
            if hourly_data:
                hours_df = pd.DataFrame(list(hourly_data.items()), columns=['Hour', 'Revenue'])
                fig_hours = px.bar(hours_df, x='Hour', y='Revenue', title='Revenue by Hour')
                st.plotly_chart(fig_hours, use_container_width=True)
        
        with col_chart2:
            # Popular items
            item_sales = {}
            for order in st.session_state.order_history:
                for item in order['items']:
                    item_name = item['name']
                    item_sales[item_name] = item_sales.get(item_name, 0) + item['quantity']
            
            if item_sales:
                items_df = pd.DataFrame(list(item_sales.items()), columns=['Item', 'Quantity Sold'])
                items_df = items_df.sort_values('Quantity Sold', ascending=False).head(10)
                fig_items = px.bar(items_df, x='Quantity Sold', y='Item', orientation='h', 
                                 title='Top 10 Popular Items')
                st.plotly_chart(fig_items, use_container_width=True)
        
        # Category analysis
        category_revenue = {}
        for order in st.session_state.order_history:
            for item in order['items']:
                category = item['category']
                category_revenue[category] = category_revenue.get(category, 0) + item['total']
        
        if category_revenue:
            cat_df = pd.DataFrame(list(category_revenue.items()), columns=['Category', 'Revenue'])
            fig_category = px.pie(cat_df, values='Revenue', names='Category', title='Revenue by Category')
            st.plotly_chart(fig_category, use_container_width=True)

# TAB 4: Order History
with tab4:
    st.markdown("### 📋 Order History")
    
    if not st.session_state.order_history:
        st.info("No order history available.")
    else:
        # Filters
        col_filter1, col_filter2 = st.columns(2)
        
        with col_filter1:
            date_filter = st.date_input("Filter by Date", value=datetime.now().date())
        
        with col_filter2:
            table_filter = st.selectbox(
                "Filter by Table",
                ["All Tables"] + [f"Table {i}" for i in range(1, 51)]
            )
        
        # Display orders
        filtered_orders = st.session_state.order_history.copy()
        
        # Apply filters
        if date_filter:
            filtered_orders = [
                order for order in filtered_orders 
                if datetime.strptime(order['date'], '%Y-%m-%d %H:%M:%S').date() == date_filter
            ]
        
        if table_filter != "All Tables":
            table_num = int(table_filter.split()[1])
        if table_filter != "All Tables":
            table_num = int(table_filter.split()[1])
            filtered_orders = [order for order in filtered_orders if order['table_number'] == table_num]
        
        st.markdown(f"**Showing {len(filtered_orders)} of {len(st.session_state.order_history)} orders**")
        
        # Display order cards
        for i, order in enumerate(reversed(filtered_orders)):  # Show latest first
            with st.expander(f"🧾 Invoice {order['invoice_number']} - ₹{order['total_amount']:.2f} | {order['date']}"):
                col_order1, col_order2 = st.columns(2)
                
                with col_order1:
                    st.markdown(f"**📅 Date:** {order['date']}")
                    st.markdown(f"**🪑 Table:** {order['table_number']}")
                    st.markdown(f"**👤 Customer:** {order['customer_name']}")
                
                with col_order2:
                    st.markdown(f"**📱 Phone:** {order['customer_phone']}")
                    st.markdown(f"**🛍️ Items:** {order['item_count']}")
                    st.markdown(f"**💰 Total:** ₹{order['total_amount']:.2f}")
                
                # Order items
                st.markdown("**Order Items:**")
                order_items_df = pd.DataFrame([
                    {
                        'Item': item['name'],
                        'Category': item['category'],
                        'Price': f"₹{item['price']}",
                        'Qty': item['quantity'],
                        'Total': f"₹{item['total']}"
                    }
                    for item in order['items']
                ])
                st.dataframe(order_items_df, use_container_width=True)
                
                # Bill breakdown
                col_bill1, col_bill2 = st.columns(2)
                
                with col_bill1:
                    st.markdown(f"**Subtotal:** ₹{order['subtotal']:.2f}")
                    st.markdown(f"**Service Charge:** ₹{order['service_charge']:.2f}")
                
                with col_bill2:
                    st.markdown(f"**GST:** ₹{order['tax_amount']:.2f}")
                    st.markdown(f"**Total:** ₹{order['total_amount']:.2f}")
                
                # Download options for individual orders
                col_download1, col_download2 = st.columns(2)
                
                with col_download1:
                    # Individual CSV download
                    csv_rows = []
                    csv_rows.append(["DELICIOUS BITES RESTAURANT"])
                    csv_rows.append(["45 Usman Road, T. Nagar, Chennai - 600017"])
                    csv_rows.append(["+91-98765-43210"])
                    csv_rows.append([])
                    csv_rows.append([f"Invoice: {order['invoice_number']}"])
                    csv_rows.append([f"Date: {order['date']}"])
                    csv_rows.append([f"Table: {order['table_number']}"])
                    csv_rows.append([f"Customer: {order['customer_name']}"])
                    csv_rows.append([])
                    csv_rows.append(["Item", "Category", "Price", "Qty", "Total"])
                    
                    for item in order['items']:
                        csv_rows.append([
                            item['name'], 
                            item['category'], 
                            f"₹{item['price']}", 
                            item['quantity'], 
                            f"₹{item['total']}"
                        ])
                    
                    csv_rows.append([])
                    csv_rows.append(["Subtotal", "", "", "", f"₹{order['subtotal']:.2f}"])
                    csv_rows.append(["Service Charge (10%)", "", "", "", f"₹{order['service_charge']:.2f}"])
                    csv_rows.append(["GST (18%)", "", "", "", f"₹{order['tax_amount']:.2f}"])
                    csv_rows.append(["TOTAL", "", "", "", f"₹{order['total_amount']:.2f}"])
                    
                    individual_csv = "\n".join([",".join(map(str, row)) for row in csv_rows])
                    
                    st.download_button(
                        "📄 Download Invoice CSV",
                        individual_csv,
                        f"invoice_{order['invoice_number']}.csv",
                        "text/csv",
                        key=f"csv_{order['invoice_number']}"
                    )
                
                with col_download2:
                    if st.button("🔄 Reorder", key=f"reorder_{order['invoice_number']}"):
                        # Clear current order and add items from this order
                        st.session_state.current_order = {}
                        
                        for item in order['items']:
                            item_key = f"{item['category']}_{item['name']}"
                            st.session_state.current_order[item_key] = {
                                'name': item['name'],
                                'category': item['category'],
                                'price': item['price'],
                                'quantity': item['quantity'],
                                'total': item['total']
                            }
                        
                        st.success(f"Items from invoice {order['invoice_number']} added to current order!")
                        st.rerun()
        
        # Bulk export for all filtered orders
        if filtered_orders:
            st.markdown("---")
            st.markdown("### 📊 Bulk Export")
            
            col_bulk1, col_bulk2 = st.columns(2)
            
            with col_bulk1:
                # Export all filtered orders as CSV
                all_orders_data = []
                
                for order in filtered_orders:
                    for item in order['items']:
                        all_orders_data.append({
                            'Invoice Number': order['invoice_number'],
                            'Date': order['date'],
                            'Table Number': order['table_number'],
                            'Customer Name': order['customer_name'],
                            'Customer Phone': order['customer_phone'],
                            'Item Name': item['name'],
                            'Category': item['category'],
                            'Price': item['price'],
                            'Quantity': item['quantity'],
                            'Item Total': item['total'],
                            'Subtotal': order['subtotal'],
                            'Service Charge': order['service_charge'],
                            'GST': order['tax_amount'],
                            'Order Total': order['total_amount']
                        })
                
                if all_orders_data:
                    all_orders_df = pd.DataFrame(all_orders_data)
                    bulk_csv = all_orders_df.to_csv(index=False)
                    
                    st.download_button(
                        "📊 Export All Orders (CSV)",
                        bulk_csv,
                        f"restaurant_orders_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        "text/csv"
                    )
            
            with col_bulk2:
                # Summary report
                if st.button("📈 Generate Summary Report"):
                    total_filtered_revenue = sum(order['total_amount'] for order in filtered_orders)
                    total_filtered_orders = len(filtered_orders)
                    avg_filtered_order = total_filtered_revenue / total_filtered_orders if total_filtered_orders > 0 else 0
                    
                    # Category breakdown for filtered orders
                    filtered_category_sales = {}
                    for order in filtered_orders:
                        for item in order['items']:
                            category = item['category']
                            filtered_category_sales[category] = filtered_category_sales.get(category, 0) + item['total']
                    
                    st.markdown(f"""
                    <div class="order-summary">
                        <h4>📊 Summary Report</h4>
                        <p><strong>Total Orders:</strong> {total_filtered_orders}</p>
                        <p><strong>Total Revenue:</strong> ₹{total_filtered_revenue:.2f}</p>
                        <p><strong>Average Order Value:</strong> ₹{avg_filtered_order:.2f}</p>
                        <p><strong>Date Range:</strong> {date_filter if date_filter else 'All dates'}</p>
                        <p><strong>Table Filter:</strong> {table_filter}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if filtered_category_sales:
                        st.markdown("**Revenue by Category:**")
                        for category, revenue in filtered_category_sales.items():
                            st.markdown(f"• {category}: ₹{revenue:.2f}")

# Clear history option
if st.session_state.order_history:
    st.markdown("---")
    col_clear1, col_clear2 = st.columns([3, 1])
    
    with col_clear2:
        if st.button("🗑️ Clear All History", type="secondary"):
            if st.button("⚠️ Confirm Clear", type="secondary"):
                st.session_state.order_history = []
                st.success("Order history cleared!")
                st.rerun()

# Footer with restaurant info
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; margin-top: 2rem; padding: 1.5rem; background: linear-gradient(45deg, #E74C3C, #C0392B); border-radius: 15px;'>
    <h4 style='color: white; margin: 0;'>🍔 "Great food, great service, great memories!" 🍔</h4>
    <p style='color: white; margin: 0.5rem 0 0 0;'>Thank you for choosing Delicious Bites Restaurant!</p>
    <p style='color: white; margin: 0.5rem 0 0 0; font-size: 0.9rem;'>📍 45 Usman Road, T. Nagar, Chennai - 600017 | 📞 +91-98765-43210 | 🌐 www.deliciousbites.com</p>
    </div>
    """,
    unsafe_allow_html=True
)