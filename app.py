import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(
    page_title="Canteen Feedback Form",
    page_icon="🍽️",
    layout="centered"
)

# ---------------------- CUSTOM CSS ----------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #fdeee0;
    }
    .top-banner {
        background: linear-gradient(90deg, #ff9800, #ff5722);
        padding: 18px 20px;
        border-radius: 8px 8px 0px 0px;
        margin-bottom: 0px;
    }
    .card {
        background-color: white;
        padding: 25px 22px;
        border-radius: 0px 0px 12px 12px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 25px;
    }
    .title-text {
        font-size: 30px;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 5px;
    }
    .subtitle-text {
        font-size: 15px;
        color: #333;
        margin-bottom: 15px;
    }
    .desc-text {
        font-size: 15px;
        color: #333;
        line-height: 1.6;
    }
    .section-label {
        font-size: 15px;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 8px;
    }
    /* Style the real Streamlit bordered containers to look like white cards */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: white;
        border-radius: 12px !important;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.07);
        margin-bottom: 18px;
        padding: 6px;
    }
    div.stButton > button {
        background-color: #ff5722;
        color: white;
        font-weight: 600;
        padding: 10px 30px;
        border-radius: 8px;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #e64a19;
        color: white;
    }
    .thankyou-box {
        background-color: white;
        padding: 40px 30px;
        border-radius: 12px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
        text-align: center;
    }
    .thankyou-title {
        font-size: 26px;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 10px;
    }
    .thankyou-text {
        font-size: 16px;
        color: #333;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- HEADER CARD ----------------------
st.markdown('<div class="top-banner"></div>', unsafe_allow_html=True)
st.markdown("""
    <div class="card">
        <div class="title-text">🍛 College Canteen — Feedback Form</div>
        <div class="subtitle-text">Feedback Form &nbsp;|&nbsp; 🙋 Individual &nbsp;|&nbsp; ⏱️ Time: 2 min</div>
        <div class="desc-text">
            Hello! 🙏 We would love to hear your feedback to make our canteen
            better for everyone. Please share your thoughts on food quality,
            cleanliness, staff behavior, and any suggestions you have.
            Your feedback means a lot to us. Thank you! 😊
        </div>
    </div>
""", unsafe_allow_html=True)

# ---------------------- SESSION STATE DEFAULTS ----------------------
defaults = {
    "name": "",
    "branch": "",
    "year": "1st Year",
    "favorite_item": "",
    "suggestions": "",
    "pricing": "Yes, they're fair",
    "food_quality": None,
    "hygiene": None,
    "staff_behavior": None,
    "overall": None,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

if "submitted" not in st.session_state:
    st.session_state["submitted"] = False

# If the previous run asked for a reset, do it here -- BEFORE any widget
# below is created (Streamlit does not allow changing a widget's
# session_state value after that widget has been instantiated in the
# same run).
if st.session_state.get("_do_reset"):
    for key, value in defaults.items():
        st.session_state[key] = value
    st.session_state["_do_reset"] = False

# ---------------------- THANK YOU PAGE ----------------------
if st.session_state["submitted"]:
    st.markdown("""
        <div class="thankyou-box">
            <div class="thankyou-title">🎉 Thank you!</div>
            <div class="thankyou-text">
                Your feedback has been submitted successfully.<br>
                We really appreciate you taking the time to help us improve the canteen. 😊
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Submit another response"):
        st.session_state["submitted"] = False
        st.session_state["_do_reset"] = True
        st.rerun()
    st.stop()

# ---------------------- FORM FIELDS ----------------------
st.markdown("<p style='color:red; font-size:14px;'>* Indicates required question</p>", unsafe_allow_html=True)

with st.container(border=True):
    st.text_input("Name *", key="name")

with st.container(border=True):
    st.text_input("Branch / Department *", key="branch")

with st.container(border=True):
    st.selectbox("Year *", ["1st Year", "2nd Year", "3rd Year", "4th Year", "Staff / Faculty"], key="year")

with st.container(border=True):
    st.markdown('<div class="section-label">How was the food quality? *</div>', unsafe_allow_html=True)
    st.feedback("stars", key="food_quality")

with st.container(border=True):
    st.markdown('<div class="section-label">How was the cleanliness / hygiene? *</div>', unsafe_allow_html=True)
    st.feedback("stars", key="hygiene")

with st.container(border=True):
    st.markdown('<div class="section-label">How was the staff\'s behavior? *</div>', unsafe_allow_html=True)
    st.feedback("stars", key="staff_behavior")

with st.container(border=True):
    st.radio("Do you think the food prices are fair? *",
             ["Yes, they're fair", "A bit expensive", "Very expensive"], key="pricing")

with st.container(border=True):
    st.text_input("What is your favorite canteen item?", key="favorite_item")

with st.container(border=True):
    st.text_area("Suggestions (if any)", key="suggestions")

with st.container(border=True):
    st.markdown('<div class="section-label">Overall Rating *</div>', unsafe_allow_html=True)
    st.feedback("stars", key="overall")

# ---------------------- SUBMIT ----------------------
if st.button("Submit Feedback ✅"):
    if st.session_state.name.strip() == "" or st.session_state.branch.strip() == "":
        st.error("Please fill in both Name and Branch (required fields).")
    elif None in (st.session_state.food_quality, st.session_state.hygiene,
                  st.session_state.staff_behavior, st.session_state.overall):
        st.error("Please give a star rating for all rating questions.")
    else:
        new_entry = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Name": st.session_state.name,
            "Branch": st.session_state.branch,
            "Year": st.session_state.year,
            # st.feedback stores 0-4, so +1 to show it as 1-5 stars
            "Food Quality": st.session_state.food_quality + 1,
            "Hygiene": st.session_state.hygiene + 1,
            "Staff Behavior": st.session_state.staff_behavior + 1,
            "Pricing Feedback": st.session_state.pricing,
            "Favorite Item": st.session_state.favorite_item,
            "Suggestions": st.session_state.suggestions,
            "Overall Rating": st.session_state.overall + 1,
        }

        file_path = "feedback_data.csv"
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        else:
            df = pd.DataFrame([new_entry])
        df.to_csv(file_path, index=False)

        st.session_state["submitted"] = True
        st.rerun()

# ---------------------- ADMIN VIEW ----------------------
with st.expander("📊 View All Feedback (Admin Only)"):
    file_path = "feedback_data.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        st.dataframe(df)
        st.download_button("Download CSV", df.to_csv(index=False), file_name="canteen_feedback.csv")
    else:
        st.info("No feedback has been submitted yet.")