import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import re
import uuid

# Page configuration
st.set_page_config(
    page_title="Event Registration System 🎉",
    page_icon="🎉",
    layout="wide"
)

# Custom CSS for modern event styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #6C5CE7;
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .event-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        margin: 1rem 0;
        color: white;
        border-left: 5px solid #FF6B6B;
    }
    
    .registration-form {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border: 2px solid #6C5CE7;
    }
    
    .stats-card {
        background: linear-gradient(45deg, #11998e, #38ef7d);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .success-banner {
        background: linear-gradient(45deg, #00b894, #00cec9);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .event-item {
        background: #f8f9fa;
        border: 2px solid #e9ecef;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .event-item:hover {
        border-color: #6C5CE7;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    .event-selected {
        background: linear-gradient(135deg, #6C5CE7, #A29BFE);
        color: white;
        border-color: #6C5CE7;
    }
    
    .registration-count {
        background: #FF6B6B;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: bold;
        margin-left: 1rem;
    }
    
    .capacity-full {
        background: #e74c3c;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .capacity-low {
        background: #f39c12;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .capacity-good {
        background: #27ae60;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .attendee-card {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #6C5CE7;
    }
    
    .event-emoji {
        font-size: 2rem;
        margin-right: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Event configuration
EVENTS = {
    "tech_conf_2025": {
        "name": "Tech Conference 2025",
        "description": "Latest trends in technology, AI, and digital transformation",
        "date": "2025-12-15",
        "time": "09:00 AM - 06:00 PM",
        "venue": "Convention Center, Downtown",
        "capacity": 500,
        "price": "Free",
        "category": "Technology",
        "emoji": "💻",
        "features": ["Networking", "Workshops", "Keynote Speakers", "Certificates"]
    },
    "startup_pitch": {
        "name": "Startup Pitch Night",
        "description": "Entrepreneurs showcase their innovative ideas to investors",
        "date": "2025-12-20",
        "time": "07:00 PM - 10:00 PM",
        "venue": "Innovation Hub, Tech Park",
        "capacity": 200,
        "price": "₹1,500",
        "category": "Business",
        "emoji": "🚀",
        "features": ["Investor Panel", "Networking", "Prize Money", "Mentorship"]
    },
    "workshop_ai": {
        "name": "AI/ML Workshop",
        "description": "Hands-on workshop on Artificial Intelligence and Machine Learning",
        "date": "2025-12-22",
        "time": "10:00 AM - 04:00 PM",
        "venue": "University Campus, Lab Building",
        "capacity": 150,
        "price": "₹3,000",
        "category": "Education",
        "emoji": "🤖",
        "features": ["Hands-on Training", "Certificates", "Project Work", "Expert Guidance"]
    },
    "music_festival": {
        "name": "Winter Music Festival",
        "description": "Live music performances by local and international artists",
        "date": "2025-12-25",
        "time": "06:00 PM - 11:00 PM",
        "venue": "City Park Amphitheater",
        "capacity": 1000,
        "price": "₹4,500",
        "category": "Entertainment",
        "emoji": "🎵",
        "features": ["Live Performances", "Food Stalls", "Art Exhibitions", "Dance Floor"]
    },
    "food_festival": {
        "name": "Gourmet Food Festival",
        "description": "Taste cuisines from around the world by renowned chefs",
        "date": "2025-12-28",
        "time": "12:00 PM - 09:00 PM",
        "venue": "Riverside Park",
        "capacity": 800,
        "price": "₹2,500",
        "category": "Food & Beverage",
        "emoji": "🍽️",
        "features": ["Chef Demonstrations", "Tastings", "Cooking Classes", "Recipe Books"]
    },
    "charity_run": {
        "name": "Charity Marathon 2025",
        "description": "5K/10K run to support local charities and community causes",
        "date": "2025-12-30",
        "time": "07:00 AM - 11:00 AM",
        "venue": "Central Park",
        "capacity": 600,
        "price": "₹2,000",
        "category": "Sports",
        "emoji": "🏃",
        "features": ["Multiple Distances", "Medals", "Charity Support", "Health Checkup"]
    }
}

# Initialize session state
def init_session_state():
    if 'registrations' not in st.session_state:
        st.session_state.registrations = []
    if 'registration_success' not in st.session_state:
        st.session_state.registration_success = False
    if 'last_registered_name' not in st.session_state:
        st.session_state.last_registered_name = ""
    if 'last_registered_event' not in st.session_state:
        st.session_state.last_registered_event = ""

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number format"""
    pattern = r'^\+?1?[- ]?\(?[0-9]{3}\)?[- ]?[0-9]{3}[- ]?[0-9]{4}$'
    return re.match(pattern, phone) is not None

def register_attendee(name, email, phone, event_id, special_requirements, dietary_requirements):
    """Register a new attendee"""
    registration_id = str(uuid.uuid4())[:8]
    
    registration = {
        'id': registration_id,
        'name': name,
        'email': email,
        'phone': phone,
        'event_id': event_id,
        'event_name': EVENTS[event_id]['name'],
        'special_requirements': special_requirements,
        'dietary_requirements': dietary_requirements,
        'registration_date': datetime.now(),
        'status': 'Confirmed'
    }
    
    st.session_state.registrations.append(registration)
    st.session_state.registration_success = True
    st.session_state.last_registered_name = name
    st.session_state.last_registered_event = EVENTS[event_id]['name']

def get_registration_stats():
    """Get registration statistics"""
    if not st.session_state.registrations:
        return {}
    
    stats = {}
    for event_id, event_info in EVENTS.items():
        event_registrations = [r for r in st.session_state.registrations if r['event_id'] == event_id]
        stats[event_id] = {
            'count': len(event_registrations),
            'capacity': event_info['capacity'],
            'percentage': (len(event_registrations) / event_info['capacity']) * 100 if event_info['capacity'] > 0 else 0
        }
    
    return stats

def get_capacity_status(event_id, stats):
    """Get capacity status for an event"""
    if event_id not in stats:
        return "available", "capacity-good"
    
    percentage = stats[event_id]['percentage']
    
    if percentage >= 100:
        return "FULL", "capacity-full"
    elif percentage >= 80:
        return f"{stats[event_id]['capacity'] - stats[event_id]['count']} left", "capacity-low"
    else:
        return f"{stats[event_id]['capacity'] - stats[event_id]['count']} left", "capacity-good"

# Initialize session state
init_session_state()

# Main header
st.markdown('<h1 class="main-header">🎉 Event Registration System</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.3rem; color: #666;'>Register for exciting events and manage your participation</p>", unsafe_allow_html=True)

# Navigation tabs
tab1, tab2, tab3, tab4 = st.tabs(["🎫 Register", "📊 Dashboard", "👥 Attendees", "⚙️ Admin"])

# TAB 1: Registration Form
with tab1:
    # Success message
    if st.session_state.registration_success:
        st.markdown(f"""
        <div class="success-banner">
            ✅ Registration Successful!<br>
            Welcome {st.session_state.last_registered_name}!<br>
            You're registered for: <strong>{st.session_state.last_registered_event}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎉 Register for Another Event", use_container_width=True):
            st.session_state.registration_success = False
            st.rerun()
    
    else:
        st.markdown("### 🎫 Event Registration Form")
        
        # Get current stats
        stats = get_registration_stats()
        
        # Event selection with details
        st.markdown("#### Choose Your Event:")
        
        selected_event = None
        
        # Display events in grid
        cols = st.columns(2)
        
        for i, (event_id, event_info) in enumerate(EVENTS.items()):
            with cols[i % 2]:
                capacity_text, capacity_class = get_capacity_status(event_id, stats)
                current_count = stats.get(event_id, {}).get('count', 0)
                
                if st.button(
                    f"{event_info['emoji']} {event_info['name']}\n"
                    f"📅 {event_info['date']} • ⏰ {event_info['time']}\n"
                    f"📍 {event_info['venue']}\n"
                    f"💰 {event_info['price']} • 👥 {current_count}/{event_info['capacity']}",
                    key=f"event_{event_id}",
                    use_container_width=True,
                    disabled=(capacity_text == "FULL")
                ):
                    selected_event = event_id
        
        # Show selected event details
        if 'selected_event_id' not in st.session_state:
            st.session_state.selected_event_id = None
        
        # Event selection dropdown as backup
        st.markdown("#### Or select from dropdown:")
        available_events = {
            event_id: f"{event_info['emoji']} {event_info['name']} ({get_capacity_status(event_id, stats)[0]})"
            for event_id, event_info in EVENTS.items()
            if get_capacity_status(event_id, stats)[0] != "FULL"
        }
        
        if available_events:
            selected_event_dropdown = st.selectbox(
                "Available Events:",
                options=list(available_events.keys()),
                format_func=lambda x: available_events[x],
                key="event_selector"
            )
            
            if selected_event:
                st.session_state.selected_event_id = selected_event
            elif selected_event_dropdown:
                st.session_state.selected_event_id = selected_event_dropdown
            
            # Show selected event details
            if st.session_state.selected_event_id:
                event_details = EVENTS[st.session_state.selected_event_id]
                
                st.markdown(f"""
                <div class="event-card">
                    <h3>{event_details['emoji']} {event_details['name']}</h3>
                    <p><strong>Description:</strong> {event_details['description']}</p>
                    <p><strong>📅 Date & Time:</strong> {event_details['date']} • {event_details['time']}</p>
                    <p><strong>📍 Venue:</strong> {event_details['venue']}</p>
                    <p><strong>💰 Price:</strong> {event_details['price']}</p>
                    <p><strong>🏷️ Category:</strong> {event_details['category']}</p>
                    <p><strong>✨ Features:</strong> {', '.join(event_details['features'])}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Registration form
                st.markdown("### 📝 Your Information")
                
                with st.form("registration_form"):
                    col_form1, col_form2 = st.columns(2)
                    
                    with col_form1:
                        name = st.text_input("👤 Full Name *", placeholder="Enter your full name")
                        email = st.text_input("📧 Email Address *", placeholder="your.email@example.com")
                    
                    with col_form2:
                        phone = st.text_input("📱 Phone Number *", placeholder="+1 (555) 123-4567")
                        dietary_requirements = st.selectbox(
                            "🍽️ Dietary Requirements",
                            ["None", "Vegetarian", "Vegan", "Gluten-Free", "Halal", "Kosher", "Other"]
                        )
                    
                    special_requirements = st.text_area(
                        "♿ Special Requirements/Accessibility Needs",
                        placeholder="Please describe any special requirements or accessibility needs...",
                        height=100
                    )
                    
                    # Terms and conditions
                    terms_accepted = st.checkbox("I agree to the Terms and Conditions and Privacy Policy *")
                    marketing_consent = st.checkbox("I consent to receive marketing emails about future events")
                    
                    submitted = st.form_submit_button("🎉 Register Now", use_container_width=True, type="primary")
                    
                    if submitted:
                        # Validation
                        errors = []
                        
                        if not name.strip():
                            errors.append("Name is required")
                        if not email.strip():
                            errors.append("Email is required")
                        elif not validate_email(email):
                            errors.append("Please enter a valid email address")
                        if not phone.strip():
                            errors.append("Phone number is required")
                        elif not validate_phone(phone):
                            errors.append("Please enter a valid phone number")
                        if not terms_accepted:
                            errors.append("You must accept the Terms and Conditions")
                        
                        # Check if email already registered for this event
                        existing_registration = any(
                            r['email'].lower() == email.lower() and r['event_id'] == st.session_state.selected_event_id
                            for r in st.session_state.registrations
                        )
                        
                        if existing_registration:
                            errors.append("This email is already registered for this event")
                        
                        # Check capacity
                        current_stats = get_registration_stats()
                        if (st.session_state.selected_event_id in current_stats and 
                            current_stats[st.session_state.selected_event_id]['count'] >= 
                            EVENTS[st.session_state.selected_event_id]['capacity']):
                            errors.append("Sorry, this event is now full")
                        
                        if errors:
                            for error in errors:
                                st.error(f"❌ {error}")
                        else:
                            # Register the attendee
                            register_attendee(
                                name.strip(),
                                email.strip().lower(),
                                phone.strip(),
                                st.session_state.selected_event_id,
                                special_requirements.strip(),
                                dietary_requirements if dietary_requirements != "None" else ""
                            )
                            st.rerun()
        else:
            st.warning("🚫 All events are currently full. Please check back later!")

# TAB 2: Dashboard
with tab2:
    st.markdown("### 📊 Registration Dashboard")
    
    if not st.session_state.registrations:
        st.info("No registrations yet. Start promoting your events!")
    else:
        # Overall statistics
        total_registrations = len(st.session_state.registrations)
        total_capacity = sum(event['capacity'] for event in EVENTS.values())
        
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        
        with col_stat1:
            st.metric("Total Registrations", total_registrations)
        
        with col_stat2:
            st.metric("Total Capacity", total_capacity)
        
        with col_stat3:
            utilization = (total_registrations / total_capacity) * 100
            st.metric("Overall Utilization", f"{utilization:.1f}%")
        
        with col_stat4:
            active_events = len([e for e in EVENTS.keys() if get_registration_stats().get(e, {}).get('count', 0) > 0])
            st.metric("Active Events", f"{active_events}/{len(EVENTS)}")
        
        # Event-wise breakdown
        st.markdown("### 📈 Event-wise Registration Analytics")
        
        stats = get_registration_stats()
        
        # Create charts
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            # Registration count by event
            event_data = []
            for event_id, event_info in EVENTS.items():
                count = stats.get(event_id, {}).get('count', 0)
                event_data.append({
                    'Event': event_info['name'],
                    'Registrations': count,
                    'Capacity': event_info['capacity'],
                    'Category': event_info['category']
                })
            
            df_events = pd.DataFrame(event_data)
            
            fig_registrations = px.bar(
                df_events,
                x='Event',
                y='Registrations',
                title='Registrations by Event',
                color='Category',
                text='Registrations'
            )
            fig_registrations.update_traces(textposition='outside')
            fig_registrations.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig_registrations, use_container_width=True)
        
        with col_chart2:
            # Capacity utilization
            fig_capacity = px.bar(
                df_events,
                x='Event',
                y=['Registrations', 'Capacity'],
                title='Capacity vs Registrations',
                barmode='group'
            )
            fig_capacity.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig_capacity, use_container_width=True)
        
        # Registration timeline
        st.markdown("### 📅 Registration Timeline")
        
        # Group registrations by date
        registration_dates = [r['registration_date'].date() for r in st.session_state.registrations]
        date_counts = pd.Series(registration_dates).value_counts().sort_index()
        
        if len(date_counts) > 0:
            fig_timeline = px.line(
                x=date_counts.index,
                y=date_counts.values,
                title='Daily Registration Trend',
                markers=True
            )
            fig_timeline.update_layout(height=400)
            fig_timeline.update_xaxes(title='Date')
            fig_timeline.update_yaxes(title='Registrations')
            st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Category breakdown
        category_data = df_events.groupby('Category')['Registrations'].sum().reset_index()
        
        if not category_data.empty and category_data['Registrations'].sum() > 0:
            fig_categories = px.pie(
                category_data,
                values='Registrations',
                names='Category',
                title='Registrations by Category'
            )
            st.plotly_chart(fig_categories, use_container_width=True)

# TAB 3: Attendees List
with tab3:
    st.markdown("### 👥 Registered Attendees")
    
    if not st.session_state.registrations:
        st.info("No attendees registered yet.")
    else:
        # Filters
        col_filter1, col_filter2, col_filter3 = st.columns(3)
        
        with col_filter1:
            event_filter = st.selectbox(
                "Filter by Event:",
                ["All Events"] + [EVENTS[eid]['name'] for eid in EVENTS.keys()],
                key="attendee_event_filter"
            )
        
        with col_filter2:
            category_filter = st.selectbox(
                "Filter by Category:",
                ["All Categories"] + list(set(event['category'] for event in EVENTS.values())),
                key="attendee_category_filter"
            )
        
        with col_filter3:
            search_term = st.text_input("🔍 Search by Name or Email:", key="attendee_search")
        
        # Filter registrations
        filtered_registrations = st.session_state.registrations.copy()
        
        if event_filter != "All Events":
            filtered_registrations = [
                r for r in filtered_registrations 
                if r['event_name'] == event_filter
            ]
        
        if category_filter != "All Categories":
            filtered_registrations = [
                r for r in filtered_registrations 
                if EVENTS[r['event_id']]['category'] == category_filter
            ]
        
        if search_term:
            search_term = search_term.lower()
            filtered_registrations = [
                r for r in filtered_registrations 
                if search_term in r['name'].lower() or search_term in r['email'].lower()
            ]
        
        st.markdown(f"**Showing {len(filtered_registrations)} of {len(st.session_state.registrations)} attendees**")
        
        # Display attendees
        if filtered_registrations:
            # Convert to DataFrame for better display
            attendee_data = []
            for reg in filtered_registrations:
                attendee_data.append({
                    'ID': reg['id'],
                    'Name': reg['name'],
                    'Email': reg['email'],
                    'Phone': reg['phone'],
                    'Event': reg['event_name'],
                    'Category': EVENTS[reg['event_id']]['category'],
                    'Registration Date': reg['registration_date'].strftime("%Y-%m-%d %H:%M"),
                    'Status': reg['status'],
                    'Special Requirements': reg['special_requirements'] or 'None',
                    'Dietary Requirements': reg['dietary_requirements'] or 'None'
                })
            
            attendees_df = pd.DataFrame(attendee_data)
            
            # Display with option to show/hide columns
            columns_to_show = st.multiselect(
                "Select columns to display:",
                options=attendees_df.columns.tolist(),
                default=['Name', 'Email', 'Event', 'Registration Date', 'Status'],
                key="attendee_columns"
            )
            
            if columns_to_show:
                st.dataframe(attendees_df[columns_to_show], use_container_width=True)
            
            # Individual attendee cards for detailed view
            if st.checkbox("Show Detailed View"):
                for reg in filtered_registrations[:10]:  # Show first 10 for performance
                    with st.expander(f"👤 {reg['name']} - {reg['event_name']}"):
                        col_detail1, col_detail2 = st.columns(2)
                        
                        with col_detail1:
                            st.markdown(f"**📧 Email:** {reg['email']}")
                            st.markdown(f"**📱 Phone:** {reg['phone']}")
                            st.markdown(f"**🆔 Registration ID:** {reg['id']}")
                        
                        with col_detail2:
                            st.markdown(f"**📅 Registered:** {reg['registration_date'].strftime('%Y-%m-%d %H:%M')}")
                            st.markdown(f"**✅ Status:** {reg['status']}")
                            st.markdown(f"**🏷️ Category:** {EVENTS[reg['event_id']]['category']}")
                        
                        if reg['special_requirements']:
                            st.markdown(f"**♿ Special Requirements:** {reg['special_requirements']}")
                        
                        if reg['dietary_requirements']:
                            st.markdown(f"**🍽️ Dietary Requirements:** {reg['dietary_requirements']}")

# TAB 4: Admin Panel
with tab4:
    st.markdown("### ⚙️ Admin Panel")
    
    # Export functionality
    st.markdown("#### 📥 Data Export")
    
    if st.session_state.registrations:
        col_export1, col_export2 = st.columns(2)
        
        with col_export1:
            # Export all registrations
            export_df = pd.DataFrame([
                {
                    'Registration ID': reg['id'],
                    'Name': reg['name'],
                    'Email': reg['email'],
                    'Phone': reg['phone'],
                    'Event ID': reg['event_id'],
                    'Event Name': reg['event_name'],
                    'Event Category': EVENTS[reg['event_id']]['category'],
                    'Event Date': EVENTS[reg['event_id']]['date'],
                    'Event Venue': EVENTS[reg['event_id']]['venue'],
                    'Registration Date': reg['registration_date'].strftime("%Y-%m-%d %H:%M:%S"),
                    'Status': reg['status'],
                    'Special Requirements': reg['special_requirements'],
                    'Dietary Requirements': reg['dietary_requirements']
                }
                for reg in st.session_state.registrations
            ])
            
            csv_data = export_df.to_csv(index=False)
            st.download_button(
                "📊 Download All Registrations (CSV)",
                csv_data,
                f"event_registrations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "text/csv",
                use_container_width=True
            )
        
        with col_export2:
            # Export by event
            selected_export_event = st.selectbox(
                "Export specific event:",
                options=list(EVENTS.keys()),
                format_func=lambda x: EVENTS[x]['name'],
                key="export_event_selector"
            )
            
            if selected_export_event:
                event_registrations = [r for r in st.session_state.registrations if r['event_id'] == selected_export_event]
                
                if event_registrations:
                    event_df = export_df[export_df['Event ID'] == selected_export_event]
                    event_csv = event_df.to_csv(index=False)
                    
                    st.download_button(
                        f"📋 Download {EVENTS[selected_export_event]['name']} (CSV)",
                        event_csv,
                        f"{selected_export_event}_registrations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        "text/csv",
                        use_container_width=True
                    )