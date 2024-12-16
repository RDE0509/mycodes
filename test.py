import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime
import random
import string
import logging
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

# Utility Functions
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
                        <p><strong>Coverage Amount:</strong> {format_currency(row['coverage_amount'])}</p>
                        <p><strong>Term:</strong> {row['term_years']} years</p>
                    </div>
                    <p><strong>Free Riders:</strong> {row.get('Free Riders', 'N/A')}</p>
                    <p><strong>Paid Riders:</strong> {row.get('Paid Riders', 'N/A')}</p>
                    <p><strong>Company Ratings:</strong> {row.get('company_ratings', 'N/A')}</p>
                    <button style="background-color: #3498db; color: white; border: none; padding: 0.5rem 1rem; border-radius: 5px; width: 100%; cursor: pointer;">
                        Get Quote
                    </button>
                </div>
                """, unsafe_allow_html=True)

# App Header
st.title("🛡️ Policy Scanner - Insurance Comparison")

# Step 1: Policy Type Selection
st.markdown('<div class="header-style">', unsafe_allow_html=True)
st.header("Step 1: Select Policy Type")
st.markdown('</div>', unsafe_allow_html=True)
policy_types = ['Life Term', 'Critical Illness', 'Whole Life']
policy_type = st.selectbox("Select Policy Type", policy_types, index=0)

# Step 2: User Details Input
st.markdown('<div class="header-style">', unsafe_allow_html=True)
st.header("Step 2: Enter Your Details")
st.markdown('</div>', unsafe_allow_html=True)

if 'user_data' not in st.session_state:
    with st.form("user_details_form"):
        name = st.text_input("Full Name")
        dob = st.date_input("Date of Birth", datetime(1990, 1, 1))
        email = st.text_input("Email")
        contact = st.text_input("Contact Number")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        province_list = ["Alberta",
                                "British Columbia",
                                "Manitoba",
                                "New Brunswick",
                                "Newfoundland and Labrador",
                                "Nova Scotia",
                                "Ontario",
                                "Prince Edward Island",
                                "Quebec",
                                "Saskatchewan",
                                "Northwest Territories",
                                "Nunavut",
                                "Yukon"
                                    ]
        province = st.selectbox("Province",province_list)
        nicotine_status = st.selectbox ("Nicotine Status",['Smoker','Non-Smoker'])
        whatsapp_notify = st.checkbox("Notify me via WhatsApp")
        submitted = st.form_submit_button("Save Details")
        if submitted:
            user_id = generate_user_id(name, email)
            user_data = {
                "user_id": user_id,
                "name": name,
                "dob": dob,
                "email": email,
                "contact": contact,
                "gender": gender,
                "province": province,
                "whatsapp_notify": whatsapp_notify,
                "nicotine_status":nicotine_status
            }
            st.session_state.user_data = user_data
            try:
                query = """
                INSERT INTO user_info (user_id, name, dob, email, contact, gender,nicotine_status, province, whats_app_notifications, created_at)
                VALUES (:user_id, :name, :dob, :email, :contact, :gender, :nicotine_status,:province, :whatsapp_notify, NOW())
                """
                run_insert(query, user_data)
                st.success("Details saved successfully!")
            except Exception as e:
                st.error(f"Error saving details: {str(e)}")
else:
    st.write(f"Welcome back, {st.session_state.user_data['name']}!")

# Step 3: Coverage and Term Selection
st.markdown('<div class="header-style">', unsafe_allow_html=True)
st.header("Step 3: Select Coverage and Term")
st.markdown('</div>', unsafe_allow_html=True)
coverage_amount = st.number_input("Coverage Amount ($)", min_value=10000, step=10000, value=100000)
term_years = st.number_input("Policy Term (Years)", min_value=1, step=1, value=10)

# Step 4: Display Plans
# Step 4: Display Plans
if st.button("Find Insurance Plans"):
    user_data = st.session_state.user_data
    query = """
    SELECT 
        c.company_name,
        p.product_display_name,
        f.face_amount AS coverage_amount,
        p.term_years,
        p.max_year_limit,
        p.annual AS annual_premium,
        r.`Free Riders`,
        r.`Paid Riders`,
        c.company_ratings
    FROM 
        product_info p
    INNER JOIN 
        company_info c ON c.id = p.company_info_id
    INNER JOIN 
        face_amount f ON p.face_amount_id = f.id
    INNER JOIN 
        riders r ON r.company_id = p.company_info_id
    WHERE 
        p.policy_type = :policy_type
        AND p.gender = :gender
        AND lower(p.nicotine_status) = lower(:nicotine_status)
        AND f.face_amount = :coverage_amount 
        AND p.term_years = :term_years
    ORDER BY 
        annual_premium DESC
    LIMIT 5
    """
    params = {
        "policy_type": policy_type.lower().replace(" ", "_"),
        "coverage_amount": coverage_amount,
        "gender": user_data['gender'],
        "nicotine_status": user_data['nicotine_status'].replace('-',''),
        "term_years": term_years
        
    }
    print(params)
    try:
        comparison_data = run_query(query, params)
        if comparison_data is not None and not comparison_data.empty:
            display_comparison_data(comparison_data)
        else:
            st.warning("No insurance plans match your criteria.")
    except Exception as e:
        st.error(f"Error fetching plans: {str(e)}")


# Footer
st.markdown("""
<div style="text-align: center; margin-top: 2rem; padding: 1rem; background-color: #f0f2f6; border-radius: 5px;">
    <p>© 2024 Policy Scanner. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
