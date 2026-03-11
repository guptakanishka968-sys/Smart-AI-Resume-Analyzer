# ------------------------------
# Imports
# ------------------------------
import streamlit as st
import pdfplumber
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
import json
from streamlit_lottie import st_lottie

# ------------------------------
# Page Setup
# ------------------------------
st.set_page_config(
    page_title="Smart AI Resume Analyzer",
    layout="wide"
)

# ------------------------------
# Load Lottie Files (LOCAL)
# ------------------------------
import json
from pathlib import Path

def load_lottiefile(filepath):
    # Get the absolute path relative to app.py
    file_path = Path(__file__).parent / filepath
    with open(file_path, "r") as f:
        return json.load(f)

lottie_logo = load_lottiefile("lottie/logo.json")
lottie_upload = load_lottiefile("lottie/upload.json")
lottie_skills = load_lottiefile("lottie/skills.json")
lottie_chat = load_lottiefile("lottie/chat.json")

# ------------------------------
# Top Heading
# ------------------------------
st_lottie(lottie_logo, height=160)

st.markdown(
    "<h1 style='text-align:center;color:#3f51b5;'>💼 Smart AI Resume Analyzer</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;font-size:18px;'>Professional resume analysis, missing skills suggestions, and career AI guidance</p>",
    unsafe_allow_html=True
)

# ------------------------------
# Colorful Styling
# ------------------------------
st.markdown("""
<style>

/* ----------------- Whole App Background ----------------- */
.stApp {
    background: linear-gradient(120deg, #f6f9ff, #e0f7fa, #f3e5f5);
    background-size: 400% 400%;
    animation: gradientBG 12s ease infinite;
}

/* Gradient Animation */
@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ----------------- Headings & Text ----------------- */
h1 {
    color: #1a237e; /* Dark blue */
    font-weight: 700;
    text-align: center;
}

h2, h3, p, div, span {
    color: #212121; /* Dark grey for readability */
}

/* ----------------- File Uploader Card ----------------- */
            /* ----------------- Light File Uploader (Previous) ----------------- */
section[data-testid="stFileUploader"] {
    background: rgba(255, 255, 255, 0.95); /* Light background */
    border: 2px dashed #2196f3;           /* Blue dashed border */
    border-radius: 16px;
    padding: 30px;
    text-align: center;
    backdrop-filter: blur(6px);
    box-shadow: 0px 6px 18px rgba(0,0,0,0.15);
    width: 80%;
    margin: auto;
}
        
/* Center icon and text inside uploader */
div[data-testid="stFileUploader"] > div:first-child {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

/* Center icon and text inside uploader */
div[data-testid="stFileUploader"] > div:first-child {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

/* Placeholder text inside uploader */
div[data-testid="stFileUploader"] p {
    color: black !important;  /* Black text */
    font-weight: bold;
    font-size: 18px;
}

/* Center file uploader text and icon */
div[data-testid="stFileUploader"] > label {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
/* ----------------- Buttons ----------------- */
.stButton > button {
    background: linear-gradient(45deg, #ff4081, #7c4dff);
    color: white;
    border: none;
    border-radius: 10px;
    height: 3em;
    width: 9em;
    font-weight: 600;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.05);
}

/* ----------------- Tabs Styling ----------------- */
div[data-baseweb="tab-list"] {
    gap: 20px;
}

button[data-baseweb="tab"] {
    background: Dark Blue;
    border-radius: 10px;
    padding: 10px 18px;
    font-weight: 600;
    color: #3f51b5;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
}

/* Tabs content text */
div[data-baseweb="tab-panel"] {
    color: #212121; /* ensures content text is readable */
}

/* ----------------- Remove Black Background Behind Lottie ----------------- */
div[data-testid="stLottie"] {
    background: transparent !important;
    display: flex;
    justify-content: center;
}

div[data-testid="stLottie"] > div {
    background: transparent !important;
}

div[data-testid="stLottie"] svg {
    background: transparent !important;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------
from pathlib import Path

# Get the folder where app.py is located
base_path = Path(__file__).parent

# Load skills.txt
with open(base_path / "skills.txt") as f:
    skills = [line.strip().lower() for line in f]

# Load roles.txt
roles = {}
with open(base_path / "roles.txt") as f:
    for line in f:
        role, s = line.split(":")
        roles[role.strip()] = [skill.strip().lower() for skill in s.split(",")]

# Load trending_skills.txt
with open(base_path / "trending_skills.txt") as f:
    trending_skills = [line.strip().lower() for line in f]
# ------------------------------
# Utility Functions
# ------------------------------
def extract_text(pdf_file):

    text = ""

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + " "

    return text.lower()

def detect_skills(text):
    # Ensure skills are strings
    return [str(skill) for skill in skills if skill in text]

def predict_role(found_skills):

    role_scores = {}

    for role_name, role_skills in roles.items():

        match_count = sum([1 for s in role_skills if s in found_skills])

        role_scores[role_name] = match_count / len(role_skills)

    return max(role_scores, key=role_scores.get)

def get_missing_skills(predicted_role, found_skills):
    # Ensure missing skills are strings
    return [str(s) for s in roles[predicted_role] if s not in found_skills]

def get_trending_skills(found_skills):

    return [s for s in trending_skills if s not in found_skills]

# ------------------------------
# Tabs Layout
# ------------------------------
tab1, tab2, tab3 = st.tabs(
    ["📄 Resume Analysis", "🔥 Trending Skills", "🤖 Career AI Chat"]
)

uploaded_file = None

# ------------------------------
# TAB 1
# ------------------------------
with tab1:

    col1, col2 = st.columns([1,2])

    with col1:
        st_lottie(lottie_upload, height=120)
        uploaded_file = st.file_uploader(
            "Upload Resume PDF",
            type="pdf"
        )

    # After col1 & col2, check if a file is uploaded
    if uploaded_file:
        resume_text = extract_text(uploaded_file)
        st.success(f"{uploaded_file.name} uploaded successfully")

        # ATS simulation goes here
        st.subheader("ATS Simulation")
        job_desc = st.text_area(
            "Paste the job description here to simulate ATS scoring",
            height=150
        )

        if job_desc:
            job_desc_text = job_desc.lower()
            # Use your existing skills list
            required_skills = [skill for skill in skills if skill in job_desc_text]

            # Find matched skills (you may need to extract them from resume here)
            # For example, using your existing function or simple matching
            matched_skills = [s for s in required_skills if s in resume_text.lower()]
            ats_score = int(len(matched_skills) / len(required_skills) * 100) if required_skills else 0

            st.write(f"✅ **ATS Match Score:** {ats_score}%")
            st.write(f"**Matched Skills:** {', '.join(matched_skills) if matched_skills else 'None'}")
            missing_from_job = [s for s in required_skills if s not in matched_skills]
            st.write(f"**Missing Skills:** {', '.join(missing_from_job) if missing_from_job else 'None'}")
            st.progress(ats_score / 100)
    with col2:
       if uploaded_file:
        # Extract text from resume
        resume_text = extract_text(uploaded_file)
        
        # Detect skills (ensure this returns actual skill names)
        found_skills = [skill for skill in skills if skill.lower() in resume_text.lower()]
        predicted_role = predict_role(found_skills)
        missing_skills = [s for s in roles[predicted_role] if s not in found_skills]

        # ---------------------------
        # Skills Found (Indexed)
        # ---------------------------
        st.subheader("Skills Found")
        if found_skills:
            for i, skill in enumerate(found_skills, start=1):
                st.write(f"{i}. {skill}")  # Numbered skill names
        else:
            st.write("No skills detected in resume.")

        # ---------------------------
        # Missing Skills (Indexed)
        # ---------------------------
        st.subheader("Missing Skills")
        if missing_skills:
            for i, skill in enumerate(missing_skills, start=1):
                st.write(f"{i}. {skill}")  # Numbered missing skill names
        else:
            st.write("No missing skills! Great job!")

        # ---------------------------
        # Dynamic Skill Gap Graph
        # ---------------------------
        if "skill_history" not in st.session_state:
            st.session_state.skill_history = {}

        st.session_state.skill_history[uploaded_file.name] = [
            1 if s in found_skills else 0 for s in roles[predicted_role]
        ]

        st.subheader("Skill Gap Graph")
        plt.figure(figsize=(10, 4))
        for resume_name, status in st.session_state.skill_history.items():
            plt.bar(
                [f"{s} ({resume_name})" for s in roles[predicted_role]],
                status,
                color=['green' if v == 1 else 'red' for v in status],
                alpha=0.6
            )
        plt.ylabel("Skill Status (1=Have, 0=Missing)")
        plt.title(f"Skill Gap for {predicted_role}")
        plt.xticks(rotation=45)
        st.pyplot(plt)

        # ---------------------------
        # WordCloud for current resume
        # ---------------------------
        st.subheader("WordCloud of Skills in Resume")
        wordcloud = WordCloud(
            width=600,
            height=300,
            background_color="white"
        ).generate(resume_text)

        plt.figure(figsize=(10,5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(plt)
# ------------------------------
# TAB 2
# ------------------------------
with tab2:

    st_lottie(lottie_skills, height=120)

    st.subheader("Trending Skills Recommendations")  # Heading always visible

    # Initialize toggle state for button
    if "show_trending" not in st.session_state:
        st.session_state["show_trending"] = False

    # Streamlit native button styled via CSS (preferred)
    if st.button("Show Trending Skills"):
        st.session_state["show_trending"] = True  # Toggle to show skills

    # Display trending skills numbered
    if st.session_state["show_trending"]:
        if trending_skills:
            for i, skill in enumerate(trending_skills, start=1):
                st.markdown(
                    f"<div style='background-color:#e3f2fd;"
                    f"padding:10px; margin:5px; border-radius:6px;"
                    f"color:#0d47a1; font-weight:600;'>{i}. {skill}</div>",
                    unsafe_allow_html=True
                )
        else:
            st.write("No trending skills found!")
# ------------------------------
# TAB 3
# ------------------------------
with tab3:

    st_lottie(lottie_chat, height=120)

    st.subheader("Career AI Assistant")

    question = st.text_input(
        "Ask about resume, skills or placement"
    )

    if question:

        q = question.lower()

        if "resume" in q:

            st.write(
                "Add measurable achievements, projects and quantified results."
            )

        elif "skills" in q:

            st.write(
                "Focus on Python, SQL, React, Power BI, Machine Learning."
            )

        elif "placement" in q or "interview" in q:

            st.write(
                "Practice DSA, build projects and prepare system design."
            )

        else:

            st.write(
                "Focus on projects, internships and real-world skills."
            )

# ------------------------------
# Session History
# ------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if uploaded_file:

    analysis = {
        "file_name": uploaded_file.name,
        "predicted_role": predicted_role,
        "skills_found": found_skills,
        "missing_skills": missing_skills
    }

    if analysis not in st.session_state.history:
        st.session_state.history.append(analysis)

st.subheader("Previous Resume Analyses")

for i, record in enumerate(st.session_state.history):

    st.write(f"{i+1}. {record['file_name']} → {record['predicted_role']}")
    st.write("Skills Found:", ", ".join(record["skills_found"]) if record["skills_found"] else "No skills found")
    st.write("Missing Skills:", ", ".join(record["missing_skills"]) if record["missing_skills"] else "None! Great job!")

    st.markdown("---")




