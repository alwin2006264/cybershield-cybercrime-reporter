
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="CyberShield - Cyber Crime Reporter",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- Styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 85% 5%, rgba(16,185,129,.10), transparent 25%),
        radial-gradient(circle at 5% 95%, rgba(6,182,212,.08), transparent 25%),
        #020617;
    color: #e2e8f0;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.cyber-card {
    background: rgba(15, 23, 42, .72);
    border: 1px solid #1e293b;
    border-radius: 16px;
    padding: 22px;
    box-shadow: 0 10px 35px rgba(0,0,0,.18);
}

.login-card {
    max-width: 520px;
    margin: 8vh auto 0 auto;
    background: rgba(15, 23, 42, .82);
    border: 1px solid #1e293b;
    border-radius: 22px;
    padding: 36px;
    box-shadow: 0 20px 70px rgba(16,185,129,.06);
}

.logo {
    width: 64px;
    height: 64px;
    border-radius: 18px;
    margin: 0 auto 16px auto;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(16,185,129,.10);
    border: 1px solid rgba(16,185,129,.20);
    font-size: 32px;
}

.login-title {
    text-align: center;
    color: white;
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 4px;
}

.login-subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 26px;
}

.header-title {
    color: white;
    font-size: 25px;
    font-weight: 700;
    margin-bottom: 0;
}

.header-subtitle {
    color: #94a3b8;
    font-size: 13px;
}

.secure {
    color: #34d399;
    background: rgba(16,185,129,.10);
    border: 1px solid rgba(16,185,129,.20);
    border-radius: 999px;
    padding: 7px 12px;
    font-size: 12px;
    font-weight: 600;
    display: inline-block;
}

.stat-label { color: #94a3b8; font-size: 14px; }
.stat-value { color: white; font-size: 32px; font-weight: 700; margin-top: 4px; }

.report-title {
    color: white;
    font-size: 18px;
    font-weight: 650;
}

.report-meta {
    color: #94a3b8;
    font-size: 13px;
}

.report-description {
    color: #cbd5e1;
    font-size: 14px;
    line-height: 1.6;
}

.badge {
    display: inline-block;
    padding: 4px 9px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 700;
    margin-left: 8px;
}
.badge-low { color:#60a5fa; background:rgba(59,130,246,.10); border:1px solid rgba(59,130,246,.20); }
.badge-medium { color:#facc15; background:rgba(234,179,8,.10); border:1px solid rgba(234,179,8,.20); }
.badge-high { color:#fb923c; background:rgba(249,115,22,.10); border:1px solid rgba(249,115,22,.20); }
.badge-critical { color:#f87171; background:rgba(239,68,68,.10); border:1px solid rgba(239,68,68,.20); }

div.stButton > button {
    border-radius: 9px;
    font-weight: 600;
}

div.stButton > button[kind="primary"] {
    background: #059669;
    border-color: #059669;
}

div.stButton > button[kind="primary"]:hover {
    background: #10b981;
    border-color: #10b981;
}

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background-color: rgba(30,41,59,.55) !important;
    color: white !important;
    border-color: #334155 !important;
}

div[data-testid="stForm"] {
    background: rgba(15,23,42,.60);
    border: 1px solid #1e293b;
    border-radius: 16px;
    padding: 22px;
}
</style>
""", unsafe_allow_html=True)

CATEGORIES = [
    "Phishing", "Malware", "Ransomware", "Identity Theft",
    "Data Breach", "Online Fraud", "Cyber Stalking", "Other"
]
SEVERITIES = ["Low", "Medium", "High", "Critical"]
STATUSES = ["Open", "In Progress", "Resolved"]

DEFAULT_REPORTS = [
    {
        "id": "1",
        "title": "Phishing email targeting employees",
        "category": "Phishing",
        "severity": "High",
        "description": "Received suspicious email claiming to be from IT department requesting password reset.",
        "date": "2024-01-15",
        "status": "In Progress",
    },
    {
        "id": "2",
        "title": "Ransomware attack on company server",
        "category": "Ransomware",
        "severity": "Critical",
        "description": "Company server encrypted with ransom note demanding payment in cryptocurrency.",
        "date": "2024-01-14",
        "status": "Open",
    },
]

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "reports" not in st.session_state:
    st.session_state.reports = DEFAULT_REPORTS.copy()
if "show_form" not in st.session_state:
    st.session_state.show_form = False


def badge(severity):
    return f'<span class="badge badge-{severity.lower()}">{severity}</span>'


# ---------- Login ----------
if not st.session_state.authenticated:
    st.markdown("""
    <div class="login-card">
        <div class="logo">🛡️</div>
        <div class="login-title">CyberShield</div>
        <div class="login-subtitle">Secure portal for reporting cyber crimes</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        email = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        login = st.form_submit_button("Sign In", type="primary", use_container_width=True)

        if login:
            if not email or not password:
                st.error("Please fill in all fields.")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters.")
            else:
                st.session_state.authenticated = True
                st.rerun()

    st.markdown(
        "<p style='text-align:center;color:#64748b;font-size:13px;'>"
        "Demo credentials: any email + password (min 6 chars)"
        "</p>",
        unsafe_allow_html=True,
    )
    st.stop()


# ---------- Header ----------
header_left, header_right = st.columns([3, 1])
with header_left:
    st.markdown(
        '<div class="header-title">🛡️ CyberShield</div>'
        '<div class="header-subtitle">Incident Reporting Portal</div>',
        unsafe_allow_html=True,
    )
with header_right:
    st.markdown('<div style="text-align:right;"><span class="secure">● Secure Connection</span></div>',
                unsafe_allow_html=True)
    if st.button("↪ Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

st.divider()

# ---------- Stats ----------
reports = st.session_state.reports
total = len(reports)
critical = sum(r["severity"] == "Critical" for r in reports)
open_count = sum(r["status"] == "Open" for r in reports)
resolved = sum(r["status"] == "Resolved" for r in reports)

s1, s2, s3, s4 = st.columns(4)
for col, label, value, icon in [
    (s1, "Total Reports", total, "📄"),
    (s2, "Critical", critical, "⚠️"),
    (s3, "Open", open_count, "🕒"),
    (s4, "Resolved", resolved, "📈"),
]:
    with col:
        st.markdown(
            f'<div class="cyber-card">'
            f'<div class="stat-label">{icon} {label}</div>'
            f'<div class="stat-value">{value}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

st.write("")

# ---------- New report ----------
if not st.session_state.show_form:
    if st.button("＋ New Incident Report", type="primary"):
        st.session_state.show_form = True
        st.rerun()
else:
    st.markdown('<div class="cyber-card"><h3 style="color:white;">New Incident Report</h3>'
                '<p style="color:#94a3b8;">Provide detailed information about the cyber crime incident</p></div>',
                unsafe_allow_html=True)

    with st.form("report_form"):
        c1, c2 = st.columns(2)
        with c1:
            title = st.text_input("Incident Title", placeholder="e.g., Phishing email received")
            category = st.selectbox("Category", ["Select category"] + CATEGORIES)
        with c2:
            severity = st.selectbox("Severity", SEVERITIES, index=1)
            st.selectbox("Status", ["Open"], disabled=True)

        description = st.text_area(
            "Incident Description",
            placeholder="Describe the incident in detail, including any relevant information...",
            height=130,
        )

        b1, b2 = st.columns([1, 1])
        with b1:
            submit = st.form_submit_button("Submit Report", type="primary", use_container_width=True)
        with b2:
            cancel = st.form_submit_button("Cancel", use_container_width=True)

        if cancel:
            st.session_state.show_form = False
            st.rerun()

        if submit:
            if not title or category == "Select category" or not description:
                st.error("Please complete the incident title, category and description.")
            else:
                st.session_state.reports.insert(0, {
                    "id": str(int(datetime.now().timestamp() * 1000)),
                    "title": title,
                    "category": category,
                    "severity": severity,
                    "description": description,
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "status": "Open",
                })
                st.session_state.show_form = False
                st.success("Incident report submitted successfully.")
                st.rerun()

st.write("")

# ---------- Reports ----------
st.markdown("## Recent Reports")

if not reports:
    st.markdown(
        '<div class="cyber-card" style="text-align:center;">'
        '<div style="font-size:42px;">🛡️</div>'
        '<h3 style="color:white;">No Reports Yet</h3>'
        '<p style="color:#94a3b8;">Start by creating your first incident report</p>'
        '</div>',
        unsafe_allow_html=True,
    )
else:
    for index, report in enumerate(list(reports)):
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        left, right = st.columns([4, 1.2])

        with left:
            st.markdown(
                f'<div class="report-title">{report["title"]}'
                f'{badge(report["severity"])}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="report-meta">📄 {report["category"]} &nbsp;&nbsp; '
                f'🕒 {report["date"]}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="report-description">{report["description"]}</div>',
                unsafe_allow_html=True,
            )

        with right:
            new_status = st.selectbox(
                "Status",
                STATUSES,
                index=STATUSES.index(report["status"]),
                key=f"status_{report['id']}",
                label_visibility="collapsed",
            )
            if new_status != report["status"]:
                st.session_state.reports[index]["status"] = new_status
                st.rerun()

            if st.button("🗑️ Delete", key=f"delete_{report['id']}", use_container_width=True):
                st.session_state.reports.pop(index)
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
        st.write("")
