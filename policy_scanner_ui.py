import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime
import random
import string
import logging
import json
import hashlib

# Set page configuration
st.set_page_config(
    page_title="Policy Scanner",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
    }
    .comparison-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .header-style {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database Configuration
DATABASE_URL = "mysql+pymysql://compulife_user:compulife0509@146.190.247.209/prd_policy_scanner"
engine = create_engine(DATABASE_URL, echo=True)

def generate_user_hash(email, contact):
    """Generate a unique hash for the user"""
    return hashlib.md5(f"{email}{contact}".encode()).hexdigest()

def check_existing_user(email, contact):
    """Check if user already exists in database"""
    query = """
    SELECT 
        ui.*, 
        ucs.coverage_selected,
        ucs.created_at as coverage_date
    FROM user_info ui
    LEFT JOIN user_coverage_selected ucs ON ui.id = ucs.user_info_id
    WHERE ui.email = :email AND ui.contact = :contact
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query), {"email": email, "contact": contact})
            user_data = result.fetchone()
            return user_data._asdict() if user_data else None
    except Exception as e:
        logger.error(f"Error checking existing user: {e}")
        return None

def run_query(query, params=None):
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query), params)
            if result.returns_rows:
                return pd.DataFrame(result.fetchall(), columns=result.keys())
            return None
    except Exception as e:
        logger.error(f"Database query error: {str(e)}")
        raise e

def run_insert(query, params):
    try:
        with engine.begin() as connection:
            result = connection.execute(text(query), params)
            return result
    except Exception as e:
        logger.error(f"Database insert error: {str(e)}")
        raise e

def generate_user_id(name, email):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    return f"{name[:3]}_{email.split('@')[0]}_{timestamp}_{random_string}".lower()

def format_currency(amount):
    return f"${amount:,.2f}"

def display_comparison_data(comparison_data):
    st.markdown("### Available Insurance Plans")
    
    cols = st.columns(3)
    for idx, row in comparison_data.iterrows():
        with cols[idx % 3]:
            with st.container():
                st.markdown(f"""
                <div class="comparison-card">
                    <h3 style="color: #1f77b4;">{row['company_name']}</h3>
                    <h4>{row['product_display_name']}</h4>
                    <div class="metric-card">
                        <p style="color: #666;">Annual Premium</p>
                        <h2 style="color: #2ecc71;">{format_currency(row['annual_premium'])}</h2>
                    </div>
                    <div style="margin: 1rem 0;">
                        <p><strong>Term:</strong> {row['term_years']} years</p>
                        <p><strong>Max Age:</strong> {row['max_coverage_age']} years</p>
                    </div>
                    <button style="background-color: #3498db; color: white; border: none; padding: 0.5rem 1rem; border-radius: 5px; width: 100%; cursor: pointer;">
                        Get Quote
                    </button>
                </div>
                """, unsafe_allow_html=True)

# Initialize session state
if 'user_data' not in st.session_state:
    st.session_state.user_data = None

# App Header
st.title("🛡️ Policy Scanner - Insurance Comparison")

# Main content area
if st.session_state.user_data is None:
    # User Input Form
    with st.form("user_input_form"):
        st.markdown('<div class="header-style">', unsafe_allow_html=True)
        st.header("Enter Your Details")
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name", max_chars=50)
            dob = st.date_input("Date of Birth", min_value=datetime(1900, 1, 1))
            contact = st.text_input("Contact Number", max_chars=15)
            email = st.text_input("Email Address")
        
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            smoker_status = st.radio("Smoking Status", ["Non-Smoker", "Smoker"])
            coverage_amount = st.number_input("Coverage Amount ($)", min_value=0, step=1000)
            term = st.number_input("Term (Years)", min_value=1, step=1)
        
        submitted = st.form_submit_button("Find Insurance Plans")
        
        if submitted:
            try:
                # Check for existing user
                existing_user = check_existing_user(email, contact)
                
                if existing_user:
                    st.session_state.user_data = existing_user
                    st.success("Welcome back! We've loaded your previous information.")
                else:
                    # Input validation
                    if not all([name, email, contact, coverage_amount > 0]):
                        st.error("Please fill in all required fields.")
                        st.stop()

                    # Handle smoker restriction
                    is_smoker = smoker_status == "Smoker"
                    if is_smoker:
                        st.error("Sorry, we currently provide comparisons only for non-smokers.")
                        st.stop()

                    # Generate user ID and insert new user
                    user_id = generate_user_id(name, email)
                    
                    insert_user_query = """
                    INSERT INTO user_info 
                    (user_id, name, contact, email, dob, gender, nicotine_status, status, created_at, updated_at)
                    VALUES 
                    (:user_id, :name, :contact, :email, :dob, :gender, :smoking_status, 'Active', NOW(), NOW())
                    """
                    
                    user_params = {
                        "user_id": user_id,
                        "name": name,
                        "contact": contact,
                        "email": email,
                        "dob": dob,
                        "gender": gender,
                        "smoking_status": 1 if not is_smoker else 0,
                    }

                    run_insert(insert_user_query, user_params)
                    
                    # Get the user_info_id and insert coverage
                    user_result = run_query("SELECT id FROM user_info WHERE user_id = :user_id", {"user_id": user_id})
                    
                    if user_result is not None and not user_result.empty:
                        user_info_id = user_result.iloc[0]['id']
                        
                        coverage_query = """
                        INSERT INTO user_coverage_selected 
                        (user_info_id, coverage_selected)
                        VALUES 
                        (:user_info_id, :coverage_amount)
                        """
                        
                        run_insert(coverage_query, {
                            "user_info_id": user_info_id,
                            "coverage_amount": coverage_amount
                        })
                        
                        # Store user data in session state
                        st.session_state.user_data = {
                            "user_id": user_id,
                            "name": name,
                            "email": email,
                            "contact": contact,
                            "dob": dob,
                            "coverage_selected": coverage_amount
                        }
                        
                        st.success("Profile created successfully!")
                
                # Store additional calculation data
                st.session_state.coverage_amount = coverage_amount
                st.session_state.user_age = (datetime.now().date() - dob).days // 365
                st.session_state.term = term
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                logger.error(f"Error in form submission: {str(e)}")

else:
    # Display user profile and allow edit
    st.sidebar.markdown("### Your Profile")
    st.sidebar.write(f"Name: {st.session_state.user_data['name']}")
    st.sidebar.write(f"Email: {st.session_state.user_data['email']}")
    if st.sidebar.button("Edit Profile"):
        st.session_state.user_data = None
        st.experimental_rerun()

# Display insurance comparison if user data exists
if st.session_state.get('user_data') is not None:
    comparison_query = """
    SELECT 
        c.company_name,
        p.product_display_name,
        p.term_years,
        p.annual AS annual_premium,
        (p.term_years + :user_age) AS max_coverage_age
    FROM 
        company_info c
    INNER JOIN 
        product_info p ON c.id = p.company_info_id
    INNER JOIN 
        face_amount f ON p.face_amount_id = f.id
    WHERE 
        f.face_amount = :coverage_amount
        AND (:user_age + :term) <= p.term_years
    ORDER BY 
        annual_premium ASC
    """

    try:
        comparison_data = run_query(comparison_query, {
            "coverage_amount": st.session_state.coverage_amount,
            "user_age": st.session_state.user_age,
            "term": st.session_state.term
        })

        if comparison_data is not None and not comparison_data.empty:
            display_comparison_data(comparison_data)
        else:
            st.warning("No insurance products match your selected coverage amount and term length.")
    
    except Exception as e:
        st.error(f"Error retrieving comparison data: {str(e)}")
        logger.error(f"Comparison query error: {str(e)}")

# Add footer
st.markdown("""
<div style="text-align: center; margin-top: 2rem; padding: 1rem; background-color: #f0f2f6; border-radius: 5px;">
    <p>© 2024 Policy Scanner. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)