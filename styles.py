def load_css():
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800;900&family=Nunito+Sans:wght@300;400;500;600;700&display=swap');
* {
    color: #0d3b2e !important;
}

input, textarea, select {
    color: #0d3b2e !important;
    background: #ffffff !important;
}
html, body, [class*="css"], .stApp {
    font-family: 'Nunito Sans', sans-serif !important;
    background: #f0faf4 !important;
}
h1, h2, h3, h4 {
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    color: #0d3b2e !important;
}
#MainMenu, footer, header, .stDeployButton { display: none !important; }

.main .block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 860px !important;
}

/* ── Inputs ── */
input[type="text"],
input[type="password"],
input[type="email"],
input[type="number"],
textarea,
.stTextInput input,
.stTextInput > div > div > input,
.stNumberInput input,
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    background-color: #ffffff !important;
    color: #0d3b2e !important;
    border: 2px solid #b7e4c7 !important;
    border-radius: 12px !important;
    font-family: 'Nunito Sans', sans-serif !important;
    font-size: 15px !important;
}
input:focus { border-color: #2d9e6b !important; box-shadow: 0 0 0 3px rgba(45,158,107,0.15) !important; }
input::placeholder { color: #a0c4b0 !important; }

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background: #ffffff !important;
    border: 2px solid #b7e4c7 !important;
    border-radius: 12px !important;
    color: #0d3b2e !important;
}
[data-testid="stSelectbox"] svg { color: #2d9e6b !important; }

/* ── Radio ── */
[data-testid="stRadio"] label { color: #2d6a4f !important; font-size: 15px !important; }

/* ── Primary buttons ── */
.stButton > button[kind="primary"],
button[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #2d9e6b, #40c285) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 14px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    font-size: 16px !important;
    padding: 12px 28px !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 15px rgba(45,158,107,0.3) !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #1e7a52, #2d9e6b) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(45,158,107,0.4) !important;
}

/* ── Secondary buttons ── */
.stButton > button[kind="secondary"],
button[data-testid="baseButton-secondary"] {
    background: #ffffff !important;
    color: #2d9e6b !important;
    border: 2px solid #2d9e6b !important;
    border-radius: 14px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    font-size: 15px !important;
}
.stButton > button[kind="secondary"]:hover {
    background: #f0faf4 !important;
    transform: translateY(-1px) !important;
}

/* ── Default buttons ── */
.stButton > button {
    background: #ffffff !important;
    color: #2d6a4f !important;
    border: 2px solid #b7e4c7 !important;
    border-radius: 14px !important;
    font-family: 'Nunito Sans', sans-serif !important;
    font-weight: 600 !important;
    transition: all 0.15s !important;
}
.stButton > button:hover {
    border-color: #2d9e6b !important;
    color: #2d9e6b !important;
    transform: translateY(-1px) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 2px solid #b7e4c7 !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #74c69d !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    border-radius: 10px 10px 0 0 !important;
    padding: 10px 24px !important;
}
.stTabs [aria-selected="true"] {
    color: #2d9e6b !important;
    border-bottom: 3px solid #2d9e6b !important;
    background: rgba(45,158,107,0.05) !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 2px solid #b7e4c7 !important;
    border-radius: 16px !important;
    overflow: hidden !important;
    box-shadow: 0 2px 12px rgba(45,158,107,0.08) !important;
}
[data-testid="stExpander"] summary {
    background: #ffffff !important;
    color: #0d3b2e !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    padding: 16px 20px !important;
}
[data-testid="stExpander"] summary:hover { background: #f0faf4 !important; }
[data-testid="stExpander"] svg { color: #2d9e6b !important; }

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 2px solid #b7e4c7 !important;
    border-radius: 16px !important;
    padding: 20px !important;
    box-shadow: 0 2px 12px rgba(45,158,107,0.08) !important;
}
[data-testid="stMetricValue"] {
    color: #2d9e6b !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 900 !important;
    font-size: 32px !important;
}
[data-testid="stMetricLabel"] { color: #74c69d !important; font-size: 13px !important; }

/* ── Alerts ── */
[data-testid="stAlert"] { border-radius: 14px !important; font-family: 'Nunito Sans', sans-serif !important; font-size: 14px !important; }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: #ffffff !important;
    border: 2px dashed #74c69d !important;
    border-radius: 16px !important;
}
[data-testid="stFileUploader"]:hover { border-color: #2d9e6b !important; }

/* ── Progress ── */
.stProgress > div > div { background: linear-gradient(90deg, #2d9e6b, #40c285) !important; border-radius: 4px !important; }
.stProgress > div { background: #d8f3dc !important; border-radius: 4px !important; }

hr { border-color: #b7e4c7 !important; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #f0faf4; }
::-webkit-scrollbar-thumb { background: #74c69d; border-radius: 3px; }

/* ── Camera input ── */
[data-testid="stCameraInput"] { border-radius: 16px !important; overflow: hidden !important; }
[data-testid="stCameraInput"] button { background: #2d9e6b !important; color: white !important; border-radius: 10px !important; }

/* ── Custom components ── */
.nayana-hero {
    background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 50%, #40916c 100%);
    border-radius: 28px;
    padding: 56px 48px;
    text-align: center;
    margin-bottom: 36px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(27,67,50,0.25);
}
.nayana-hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.nayana-wordmark {
    font-family: 'Nunito', sans-serif;
    font-size: 72px;
    font-weight: 900;
    color: #ffffff;
    letter-spacing: -3px;
    line-height: 1;
    margin-bottom: 10px;
    text-shadow: 0 2px 20px rgba(0,0,0,0.2);
}
.nayana-meaning {
    font-size: 13px;
    color: rgba(255,255,255,0.6);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 16px;
    font-style: italic;
}
.nayana-tagline {
    font-size: 17px;
    color: rgba(255,255,255,0.85);
    font-weight: 400;
    max-width: 500px;
    margin: 0 auto 36px;
    line-height: 1.8;
}
.stat-row {
    display: flex;
    justify-content: center;
    gap: 40px;
    flex-wrap: wrap;
    margin-bottom: 40px;
}
.stat-item { text-align: center; }
.stat-num { font-family: 'Nunito', sans-serif; font-size: 32px; font-weight: 900; color: #95d5b2; line-height: 1; }
.stat-lbl { font-size: 11px; color: rgba(255,255,255,0.5); text-transform: uppercase; letter-spacing: 1.5px; margin-top: 5px; }
.portal-row { display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; }
.portal-card { flex: 1; min-width: 220px; max-width: 280px; background: #ffffff; border-radius: 20px; padding: 36px 24px; text-align: center; transition: all 0.2s; border: 2px solid #b7e4c7; box-shadow: 0 4px 20px rgba(45,158,107,0.1); }
.portal-card:hover { transform: translateY(-4px); box-shadow: 0 8px 30px rgba(45,158,107,0.2); }
.portal-icon { font-size: 44px; margin-bottom: 16px; }
.portal-title { font-family: 'Nunito', sans-serif; font-size: 20px; font-weight: 800; color: #0d3b2e; margin-bottom: 10px; }
.portal-sub { font-size: 13px; color: #74c69d; line-height: 1.6; }

.topnav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 0 18px;
    border-bottom: 2px solid #b7e4c7;
    margin-bottom: 32px;
}
.topnav-brand { font-family: 'Nunito', sans-serif; font-size: 26px; font-weight: 900; color: #2d9e6b; letter-spacing: -1px; }
.topnav-user { font-size: 13px; color: #74c69d; font-weight: 500; }

.page-title { font-family: 'Nunito', sans-serif; font-size: 30px; font-weight: 900; color: #0d3b2e; letter-spacing: -0.5px; margin-bottom: 4px; }
.page-sub { font-size: 15px; color: #74c69d; font-weight: 400; margin-bottom: 28px; }

.card {
    background: #ffffff;
    border: 2px solid #b7e4c7;
    border-radius: 18px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 2px 12px rgba(45,158,107,0.08);
}
.card.highlight { border-color: #2d9e6b; background: #f0faf4; }
.card.danger { border-color: #e63946; background: #fff5f5; }
.card.warning { border-color: #f4a261; background: #fffbf0; }

.quality-num { font-family: 'Nunito', sans-serif; font-size: 54px; font-weight: 900; line-height: 1; margin-bottom: 6px; }

.risk-pill { display: inline-block; padding: 6px 18px; border-radius: 20px; font-size: 13px; font-weight: 800; font-family: 'Nunito', sans-serif; }
.risk-high { background: #ffe8e8; color: #c1121f; border: 2px solid #f4a5a5; }
.risk-moderate { background: #fff3e0; color: #e76f51; border: 2px solid #f4c89a; }
.risk-low { background: #d8f3dc; color: #1b4332; border: 2px solid #74c69d; }

.status-pending { background: #fff3e0; color: #e76f51; border: 2px solid #f4c89a; padding: 3px 12px; border-radius: 20px; font-size: 11px; font-weight: 800; }
.status-reviewed { background: #d8f3dc; color: #1b4332; border: 2px solid #74c69d; padding: 3px 12px; border-radius: 20px; font-size: 11px; font-weight: 800; }

.step-bar {
    display: flex;
    align-items: center;
    gap: 0;
    margin-bottom: 32px;
    background: #ffffff;
    border: 2px solid #b7e4c7;
    border-radius: 16px;
    padding: 16px 24px;
    box-shadow: 0 2px 12px rgba(45,158,107,0.08);
}
.step { display: flex; align-items: center; gap: 10px; flex: 1; }
.step-dot { width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 800; font-family: 'Nunito', sans-serif; flex-shrink: 0; }
.step-dot.done { background: #2d9e6b; color: white; }
.step-dot.active { background: #0d3b2e; color: white; box-shadow: 0 0 0 4px rgba(45,158,107,0.2); }
.step-dot.pending { background: #d8f3dc; color: #74c69d; }
.step-label { font-size: 13px; font-weight: 700; font-family: 'Nunito', sans-serif; }
.step-label.done { color: #2d9e6b; }
.step-label.active { color: #0d3b2e; }
.step-label.pending { color: #b7e4c7; }
.step-line { flex: 1; height: 2px; background: #b7e4c7; margin: 0 8px; max-width: 40px; }
.step-line.done { background: #2d9e6b; }

.section-label { font-family: 'Nunito Sans', sans-serif; font-size: 11px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #74c69d; margin-bottom: 10px; }

.empty-state { text-align: center; padding: 64px 32px; background: #ffffff; border: 2px dashed #b7e4c7; border-radius: 22px; }
.empty-icon { font-size: 52px; margin-bottom: 16px; opacity: 0.6; }
.empty-title { font-family: 'Nunito', sans-serif; font-size: 22px; font-weight: 800; color: #0d3b2e; margin-bottom: 8px; }
.empty-sub { font-size: 14px; color: #74c69d; }

.doc-card { background: #f0faf4; border: 2px solid #b7e4c7; border-radius: 16px; padding: 20px; }
.doc-name { font-family: 'Nunito', sans-serif; font-size: 18px; font-weight: 800; color: #0d3b2e; }
.doc-meta { font-size: 13px; color: #74c69d; margin-top: 4px; }
</style>
"""