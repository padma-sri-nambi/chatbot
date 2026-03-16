import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from io import BytesIO

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Chatbot for College ERP", page_icon="🎓", layout="wide")

# ---------------- SESSION STATE ----------------
defaults = {
    "logged_in": False,
    "page": "login",
    "selected_option": None,
    "student_name": "",
    "rollno": "",
    "attendance": 0,
    "marks_data": [],
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(-45deg, #0a0f24, #1b1f3b, #2d1b69, #0f3460, #1a1a40, #301860);
    background-size: 400% 400%;
    animation: gradientFlow 15s ease infinite;
    color: white;
    overflow-x: hidden;
}

@keyframes gradientFlow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.galaxy, .galaxy2, .nebula {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
}

.galaxy {
    background:
        radial-gradient(2px 2px at 40px 60px, #fff, transparent),
        radial-gradient(2px 2px at 120px 180px, #cce7ff, transparent),
        radial-gradient(1.5px 1.5px at 240px 120px, #ffffff, transparent),
        radial-gradient(2px 2px at 340px 240px, #ffd6ff, transparent),
        radial-gradient(1.5px 1.5px at 430px 80px, #ffffff, transparent),
        radial-gradient(2px 2px at 560px 170px, #cce7ff, transparent),
        radial-gradient(1.5px 1.5px at 710px 260px, #ffffff, transparent),
        radial-gradient(2px 2px at 860px 110px, #f8f8ff, transparent),
        radial-gradient(1.5px 1.5px at 980px 220px, #ffffff, transparent),
        radial-gradient(2px 2px at 1100px 140px, #d8b4fe, transparent);
    background-repeat: repeat;
    background-size: 1200px 700px;
    animation: starsMove 90s linear infinite;
    opacity: 0.85;
}

.galaxy2 {
    background:
        radial-gradient(1px 1px at 70px 90px, white, transparent),
        radial-gradient(1px 1px at 210px 250px, #cce7ff, transparent),
        radial-gradient(1px 1px at 360px 140px, white, transparent),
        radial-gradient(1px 1px at 520px 290px, #ffd6ff, transparent),
        radial-gradient(1px 1px at 700px 120px, white, transparent),
        radial-gradient(1px 1px at 900px 250px, #cce7ff, transparent),
        radial-gradient(1px 1px at 1080px 320px, white, transparent);
    background-repeat: repeat;
    background-size: 1300px 800px;
    animation: starsMove 130s linear infinite reverse;
    opacity: 0.45;
}

.nebula {
    background:
        radial-gradient(circle at 15% 20%, rgba(255,255,255,0.10), transparent 90px),
        radial-gradient(circle at 75% 30%, rgba(173,216,230,0.12), transparent 120px),
        radial-gradient(circle at 50% 75%, rgba(221,160,221,0.10), transparent 130px),
        radial-gradient(circle at 85% 80%, rgba(255,182,193,0.08), transparent 100px);
    animation: nebulaFloat 18s ease-in-out infinite alternate;
}

@keyframes starsMove {
    from { transform: translateY(0px); }
    to { transform: translateY(-220px); }
}

@keyframes nebulaFloat {
    0% { transform: scale(1) translate(0, 0); }
    100% { transform: scale(1.05) translate(-18px, 18px); }
}

.block-container {
    padding-top: 1.5rem !important;
    position: relative;
    z-index: 2;
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #ffffff;
    text-shadow: 0 0 18px rgba(173,216,230,0.35);
    margin-bottom: 6px;
}

.subtitle {
    text-align: center;
    font-size: 19px;
    color: #e7efff;
    margin-bottom: 22px;
}

.card {
    background: linear-gradient(145deg, rgba(255,255,255,0.12), rgba(255,255,255,0.05));
    padding: 28px;
    border-radius: 24px;
    border: 1px solid rgba(255,255,255,0.14);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    box-shadow:
        0 12px 35px rgba(0, 0, 0, 0.35),
        inset 1px 1px 0 rgba(255,255,255,0.18),
        inset -1px -1px 0 rgba(255,255,255,0.04);
}

label, .stTextInput label, .stNumberInput label, .stSelectbox label {
    color: #ffffff !important;
    font-weight: 600 !important;
}

.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    background: rgba(255,255,255,0.96) !important;
    color: #000000 !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.20) !important;
}

.stSelectbox div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.96) !important;
    color: #000000 !important;
    border-radius: 12px !important;
    min-height: 45px !important;
    border: 1px solid rgba(255,255,255,0.20) !important;
}

.stButton > button,
.stDownloadButton > button {
    width: 100%;
    border-radius: 14px;
    border: none;
    padding: 10px 14px;
    font-size: 18px;
    font-weight: 700;
    color: white;
    background: linear-gradient(135deg, #7c3aed, #2563eb, #06b6d4);
    box-shadow: 0 10px 20px rgba(37,99,235,0.25);
}

.stSuccess, .stInfo, .stWarning, .stError, .stAlert {
    border-radius: 14px !important;
    font-size: 18px !important;
    font-weight: 700 !important;
}

.warning-box {
    background: rgba(255, 77, 109, 0.22);
    border-left: 6px solid #ff4d6d;
    padding: 15px;
    border-radius: 14px;
    color: #fff5f7;
    font-size: 18px;
    margin-top: 20px;
    font-weight: bold;
}

.fine-box {
    background: rgba(255, 193, 7, 0.22);
    border-left: 6px solid #ffd166;
    padding: 15px;
    border-radius: 14px;
    color: #fffbea;
    font-size: 20px;
    margin-top: 20px;
    font-weight: bold;
}

table {
    width: 78% !important;
    margin-left: auto !important;
    margin-right: auto !important;
    border-collapse: collapse !important;
    text-align: center !important;
    background: rgba(255,255,255,0.08) !important;
}

thead tr th {
    background: rgba(99,102,241,0.42) !important;
    color: white !important;
    padding: 12px !important;
    text-align: center !important;
}

tbody tr td {
    color: white !important;
    padding: 10px !important;
    text-align: center !important;
    background: rgba(255,255,255,0.05) !important;
}

h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
    display: none !important;
}
</style>

<div class="galaxy"></div>
<div class="galaxy2"></div>
<div class="nebula"></div>
""", unsafe_allow_html=True)

# ---------------- PDF ----------------
def generate_exam_pdf():
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, height - 50, "Exam Date Details")
    c.setFont("Helvetica", 12)
    c.drawString(60, height - 90, "Year: 2nd Year")
    c.drawString(300, height - 90, "Semester: Semester 2")

    data = [
        ["Exam Type", "Date Range"],
        ["Mid-1", "16/02/2026 - 20/02/2026"],
        ["Mid-2", "20/04/2026 - 24/04/2026"],
        ["Internals", "15/04/2026 - 17/04/2026"],
        ["Externals", "27/04/2026 - 29/04/2026"],
        ["SEM", "04/05/2026 - 17/05/2026"],
    ]

    table = Table(data, colWidths=[180, 250])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    table.wrapOn(c, width, height)
    table.drawOn(c, 80, height - 300)

    c.save()
    buffer.seek(0)
    return buffer

def card_start():
    st.markdown('<div class="card">', unsafe_allow_html=True)

def card_end():
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- PAGES ----------------
def login_page():
    st.markdown('<div class="title">🎓 AI Chatbot for College ERP</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Login to access Attendance, Marks, and Exam Details</div>', unsafe_allow_html=True)

    _, center, _ = st.columns([1, 1.4, 1])
    with center:
        card_start()
        rollno = st.text_input("Enter Roll Number")
        password = st.text_input("Enter Password", type="password")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Forgot Password"):
                st.info("Password reset link sent successfully.")
        with c2:
            if st.button("Change Password"):
                st.info("Password change option selected.")

        if st.button("Login"):
            if rollno and password:
                st.session_state.logged_in = True
                st.session_state.rollno = rollno
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("Please enter Roll Number and Password.")
        card_end()

def dashboard_page():
    st.markdown('<div class="title">📘 Student Details Input</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Choose an option and enter details</div>', unsafe_allow_html=True)

    card_start()
    option = st.selectbox("Select Query Type", ["Attendance", "Marks", "Exam Details"])

    if option == "Attendance":
        name = st.text_input("Enter Student Name")
        attendance = st.number_input("Enter Attendance Percentage", min_value=0, max_value=100, step=1)

        if st.button("Submit Attendance"):
            st.session_state.selected_option = "Attendance"
            st.session_state.student_name = name
            st.session_state.attendance = attendance
            st.session_state.page = "output"
            st.rerun()

    elif option == "Marks":
        rollno = st.text_input("Enter Roll Number", value=st.session_state.rollno)
        name = st.text_input("Enter Student Name")
        st.markdown("### Enter Marks Details")

        subjects = ["DBMS", "ML", "OT", "P&S", "DLCO"]
        marks_data = []
        for i, subject in enumerate(subjects):
            obtained = st.number_input(f"{subject} Obtained Marks", min_value=0, max_value=30, step=1, key=f"sub_{i}")
            marks_data.append([subject, obtained, 30])

        if st.button("Submit Marks"):
            st.session_state.selected_option = "Marks"
            st.session_state.rollno = rollno
            st.session_state.student_name = name
            st.session_state.marks_data = marks_data
            st.session_state.page = "output"
            st.rerun()

    elif option == "Exam Details":
        st.selectbox("Select Year", ["2nd Year"])
        st.selectbox("Select Semester", ["Semester 2"])

        if st.button("Submit Exam Details"):
            st.session_state.selected_option = "Exam Details"
            st.session_state.page = "output"
            st.rerun()
    card_end()

def output_page():
    st.markdown('<div class="title">📄 Output Page</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Student Query Result</div>', unsafe_allow_html=True)

    card_start()
    if st.session_state.selected_option == "Attendance":
        name = st.session_state.student_name
        attendance = st.session_state.attendance

        fine = 0
        if 70 <= attendance <= 74:
            fine = 1000
        elif 60 <= attendance <= 69:
            fine = 2000
        elif 50 <= attendance <= 59:
            fine = 3000
        elif attendance < 50:
            fine = 5000

        st.markdown(f"### Student Name: {name}")
        st.markdown(f"### Attendance Percentage: {attendance}%")

        if fine > 0:
            st.markdown(f'<div class="fine-box">Condition: Your attendance fine is ₹{fine}/-</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="warning-box">{name}, your attendance is low. Attend classes regularly.</div>', unsafe_allow_html=True)
        else:
            st.success(f"{name}, your attendance is good. No fine applicable.")

    elif st.session_state.selected_option == "Marks":
        rollno = st.session_state.rollno
        name = st.session_state.student_name
        marks_data = st.session_state.marks_data

        st.markdown(f"### Roll No: {rollno}")
        st.markdown(f"### Name: {name}")
        st.markdown("## Marks Details")

        df = pd.DataFrame(marks_data, columns=["Subject Name", "Obtained Marks", "Total Marks"])
        st.markdown(df.to_html(index=False), unsafe_allow_html=True)

        total_obtained = sum(row[1] for row in marks_data)
        total_marks = sum(row[2] for row in marks_data)
        percentage = (total_obtained / total_marks) * 100 if total_marks else 0

        st.markdown(f"### Total Marks: {total_obtained} / {total_marks}")
        st.markdown(f"### Percentage: {percentage:.2f}%")

    elif st.session_state.selected_option == "Exam Details":
        st.markdown("### Year: 2nd Year")
        st.markdown("### Semester: Semester 2")
        st.markdown("## Exam Dates")

        exam_df = pd.DataFrame({
            "Exam Type": ["Mid-1", "Mid-2", "Internals", "Externals", "SEM"],
            "Date Details": [
                "16/02/2026 - 20/02/2026",
                "20/04/2026 - 24/04/2026",
                "15/04/2026 - 17/04/2026",
                "27/04/2026 - 29/04/2026",
                "04/05/2026 - 17/05/2026"
            ]
        })
        st.markdown(exam_df.to_html(index=False), unsafe_allow_html=True)

        pdf_file = generate_exam_pdf()
        st.download_button("📥 Download PDF", data=pdf_file, file_name="exam_details.pdf", mime="application/pdf")

    card_end()

    if st.button("⬅ Back"):
        st.session_state.page = "dashboard"
        st.rerun()

# ---------------- MAIN ----------------
if not st.session_state.logged_in:
    login_page()
else:
    if st.session_state.page == "dashboard":
        dashboard_page()
    else:
        output_page()
