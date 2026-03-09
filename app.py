import streamlit as st

st.set_page_config(
    page_title="InternFlow AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="collapsedControl"] {display: none;}

    .stApp {
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 50%, #0f0f0f 100%);
    }
    .hero-title {
        font-size: 80px;
        font-weight: 900;
        background: linear-gradient(90deg, #76B900, #ffffff, #76B900);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        letter-spacing: -2px;
        line-height: 1.1;
        margin-bottom: 0px;
    }
    .hero-subtitle {
        font-size: 22px;
        color: #aaaaaa;
        text-align: center;
        margin-top: 12px;
        margin-bottom: 40px;
        font-weight: 300;
    }
    .nvidia-badge {
        background: #76B900;
        color: #000000;
        padding: 6px 18px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 32px;
    }
    .feature-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(118, 185, 0, 0.3);
        border-radius: 16px;
        padding: 28px 24px;
        height: 100%;
    }
    .feature-icon { font-size: 36px; margin-bottom: 12px; }
    .feature-title { color: #76B900; font-size: 18px; font-weight: 700; margin-bottom: 8px; }
    .feature-desc { color: #aaaaaa; font-size: 14px; line-height: 1.6; }
    .stat-number { font-size: 48px; font-weight: 900; color: #76B900; text-align: center; }
    .stat-label { font-size: 14px; color: #888; text-align: center; margin-top: -8px; }
    .divider { border: none; border-top: 1px solid rgba(118, 185, 0, 0.2); margin: 48px 0; }
    .problem-text { font-size: 18px; color: #cccccc; line-height: 1.8; text-align: center; }
    .highlight { color: #76B900; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.markdown("<div style='text-align:center'><span class='nvidia-badge'>⚡ Powered by NVIDIA Nemotron</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-title'>InternFlow AI</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-subtitle'>The only platform that doesn't just find internships — it helps you <b>land</b> them.<br>AI-powered resume tailoring, smart project selection, and ATS-ready PDF generation.</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    b1, b2, b3 = st.columns([2, 2, 2])
    with b2:
        if st.button("🚀 Get Started", type="primary", use_container_width=True):
            st.switch_page("pages/2_onboarding.py")

st.markdown("<br><br>", unsafe_allow_html=True)

# ── Stats ─────────────────────────────────────────────────────────────────────
st.markdown("<hr class='divider'>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("<div class='stat-number'>500+</div>", unsafe_allow_html=True)
    st.markdown("<div class='stat-label'>Live Internship Listings</div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='stat-number'>3</div>", unsafe_allow_html=True)
    st.markdown("<div class='stat-label'>Nemotron Models Used</div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class='stat-number'>< 30s</div>", unsafe_allow_html=True)
    st.markdown("<div class='stat-label'>Resume Tailoring Time</div>", unsafe_allow_html=True)
with col4:
    st.markdown("<div class='stat-number'>1-Page</div>", unsafe_allow_html=True)
    st.markdown("<div class='stat-label'>ATS-Perfect PDF Output</div>", unsafe_allow_html=True)
st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ── Problem ───────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.markdown("<h2 style='color:#fff;text-align:center'>The Problem Every Student Faces</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div class='problem-text'>
        Students spend <span class='highlight'>10–20 hours per week</span> manually tailoring resumes and applying to internships.
        Existing tools help with <span class='highlight'>discovery</span> — but none close the loop with intelligent, autonomous application.
        <br><br>
        You have <span class='highlight'>10 projects</span>. A resume fits <span class='highlight'>3</span>.
        Which ones do you pick? That decision alone could cost you the interview.
    </div>
    """, unsafe_allow_html=True)
st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ── Features ──────────────────────────────────────────────────────────────────
st.markdown("<h2 style='color:#fff;text-align:center;margin-bottom:32px'>What Makes InternFlow Different</h2>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""<div class='feature-card'>
        <div class='feature-icon'>🗂️</div>
        <div class='feature-title'>Resume Arsenal</div>
        <div class='feature-desc'>Store all your resume versions in one place. Base resumes, role-specific variants, and auto-saved company-tailored versions — organized and always ready.</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""<div class='feature-card'>
        <div class='feature-icon'>🧠</div>
        <div class='feature-title'>Smart Project Selection</div>
        <div class='feature-desc'>Have 10 projects but only space for 3? Nemotron reads the JD and picks your most relevant projects automatically — then rewrites them in the role's language.</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""<div class='feature-card'>
        <div class='feature-icon'>📊</div>
        <div class='feature-title'>Full JD Diagnostics</div>
        <div class='feature-desc'>Not just a match score. Get a complete gap analysis — missing keywords, mismatched signals, and ATS issues — with specific fixes suggested by AI.</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""<div class='feature-card'>
        <div class='feature-icon'>📄</div>
        <div class='feature-title'>ATS-Perfect PDF</div>
        <div class='feature-desc'>Nemotron generates a LaTeX resume — strictly 1 page, ATS-friendly, professionally formatted. Download and apply in seconds.</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""<div class='feature-card'>
        <div class='feature-icon'>🐙</div>
        <div class='feature-title'>GitHub Integration</div>
        <div class='feature-desc'>Drop your GitHub link — we scrape your repos, README files, and stats to automatically build your project portfolio. No manual entry needed.</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""<div class='feature-card'>
        <div class='feature-icon'>✅</div>
        <div class='feature-title'>Application Tracker</div>
        <div class='feature-desc'>Track every application, resume version used, and status in one dashboard. Never lose track of where you applied and with what resume.</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ── How it works ──────────────────────────────────────────────────────────────
st.markdown("<h2 style='color:#fff;text-align:center;margin-bottom:32px'>How It Works</h2>", unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)
steps = [
    ("1", "📝", "Set Up Profile", "Add your details, upload resume, connect GitHub"),
    ("2", "💼", "Browse Jobs", "Live internships filtered for you"),
    ("3", "🤖", "Run AI Agent", "Nemotron analyzes JD, selects projects, rewrites resume"),
    ("4", "📄", "Download PDF", "1-page ATS-perfect LaTeX resume instantly"),
    ("5", "✅", "Track & Apply", "One-click apply tracking across all applications"),
]
for col, (num, icon, title, desc) in zip([col1, col2, col3, col4, col5], steps):
    with col:
        st.markdown(f"""
        <div style='text-align:center;padding:16px'>
            <div style='background:#76B900;color:#000;width:36px;height:36px;border-radius:50%;
                display:flex;align-items:center;justify-content:center;font-weight:900;
                font-size:16px;margin:0 auto 12px auto'>{num}</div>
            <div style='font-size:28px'>{icon}</div>
            <div style='color:#76B900;font-weight:700;font-size:14px;margin:8px 0'>{title}</div>
            <div style='color:#888;font-size:12px;line-height:1.5'>{desc}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ── Final CTA ─────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("<h2 style='color:#fff;text-align:center'>Ready to land your internship?</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#888;text-align:center'>Stop applying manually. Let Nemotron do the heavy lifting.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Get Started — It's Free", type="primary", use_container_width=True):
        st.switch_page("pages/2_onboarding.py")

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<p style='color:#444;text-align:center;font-size:12px'>Built with ❤️ using NVIDIA Nemotron · SJSU Agents for Impact Hackathon 2026</p>", unsafe_allow_html=True)