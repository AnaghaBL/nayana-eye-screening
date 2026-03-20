def load_css():
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;500;600;700;800;900&family=Nunito+Sans:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Nunito Sans', sans-serif !important;
    background: #060d1f !important;
}
h1, h2, h3, h4 {
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    color: #f0f4ff !important;
}
#MainMenu, footer, header, .stDeployButton { display: none !important; }

[data-testid="stSidebar"] {
    background: #080f22 !important;
    border-right: 1px solid rgba(245,158,11,0.12) !important;
    padding-top: 0 !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }
section[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
[data-testid="stSidebar"] .stButton button {
    background: transparent !important;
    border: none !important;
    border-radius: 12px !important;
    color: #94a3b8 !important;
    font-family: 'Nunito Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    text-align: left !important;
    padding: 10px 14px !important;
    width: 100% !important;
    transition: all 0.15s !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(245,158,11,0.1) !important;
    color: #fbbf24 !important;
    transform: none !important;
}

.main .block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 960px !important;
}

input[type="text"],
input[type="password"],
input[type="email"],
input[type="number"],
textarea,
.stTextInput input,
.stTextInput > div > div > input,
.stNumberInput input,
.stNumberInput > div > div > input,
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    background-color: #0d1830 !important;
    background: #0d1830 !important;
    color: #f0f4ff !important;
    border: 1.5px solid rgba(245,158,11,0.25) !important;
    border-radius: 12px !important;
    font-family: 'Nunito Sans', sans-serif !important;
    font-size: 14px !important;
    caret-color: #f59e0b !important;
}
input[type="text"]:focus,
input[type="password"]:focus,
.stTextInput input:focus {
    border-color: #f59e0b !important;
    box-shadow: 0 0 0 3px rgba(245,158,11,0.15) !important;
    outline: none !important;
}
input::placeholder { color: #475569 !important; }

[data-testid="stSelectbox"] > div > div {
    background: #0d1830 !important;
    border: 1.5px solid rgba(245,158,11,0.25) !important;
    border-radius: 12px !important;
    color: #f0f4ff !important;
    font-family: 'Nunito Sans', sans-serif !important;
}
[data-testid="stSelectbox"] svg { color: #f59e0b !important; }

[data-testid="stRadio"] label {
    color: #94a3b8 !important;
    font-size: 14px !important;
    font-family: 'Nunito Sans', sans-serif !important;
}

.stButton > button[kind="primary"],
button[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #d97706, #f59e0b) !important;
    color: #1a0a00 !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    font-size: 14px !important;
    padding: 10px 24px !important;
    transition: all 0.2s !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #b45309, #d97706) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(245,158,11,0.3) !important;
}
.stButton > button[kind="secondary"],
button[data-testid="baseButton-secondary"] {
    background: rgba(245,158,11,0.08) !important;
    color: #fbbf24 !important;
    border: 1.5px solid rgba(245,158,11,0.3) !important;
    border-radius: 12px !important;
    font-family: 'Nunito Sans', sans-serif !important;
    font-weight: 600 !important;
}
.stButton > button[kind="secondary"]:hover {
    background: rgba(245,158,11,0.15) !important;
    transform: translateY(-1px) !important;
}
.stButton > button {
    background: rgba(255,255,255,0.05) !important;
    color: #94a3b8 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    font-family: 'Nunito Sans', sans-serif !important;
    transition: all 0.15s !important;
}
.stButton > button:hover {
    background: rgba(255,255,255,0.08) !important;
    color: #f0f4ff !important;
    transform: translateY(-1px) !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid rgba(255,255,255,0.08) !important;
    gap: 8px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #64748b !important;
    font-family: 'Nunito Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    border-radius: 10px 10px 0 0 !important;
    padding: 10px 20px !important;
}
.stTabs [aria-selected="true"] {
    color: #f59e0b !important;
    border-bottom: 2px solid #f59e0b !important;
    background: rgba(245,158,11,0.05) !important;
}

[data-testid="stExpander"] {
    background: #0d1830 !important;
    border: 1px solid rgba(245,158,11,0.12) !important;
    border-radius: 16px !important;
    overflow: hidden !important;
}
[data-testid="stExpander"] summary {
    background: #0d1830 !important;
    color: #f0f4ff !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    padding: 14px 18px !important;
}
[data-testid="stExpander"] summary:hover {
    background: rgba(245,158,11,0.06) !important;
}
[data-testid="stExpander"] svg { color: #f59e0b !important; }

[data-testid="stMetric"] {
    background: #0d1830 !important;
    border: 1px solid rgba(245,158,11,0.15) !important;
    border-radius: 16px !important;
    padding: 18px 20px !important;
}
[data-testid="stMetricValue"] {
    color: #f59e0b !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 900 !important;
}
[data-testid="stMetricLabel"] {
    color: #64748b !important;
    font-size: 12px !important;
    font-family: 'Nunito Sans', sans-serif !important;
}

[data-testid="stAlert"] {
    border-radius: 12px !important;
    font-family: 'Nunito Sans', sans-serif !important;
    font-size: 14px !important;
}
[data-testid="stFileUploader"] {
    background: #0d1830 !important;
    border: 2px dashed rgba(245,158,11,0.35) !important;
    border-radius: 16px !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(245,158,11,0.6) !important;
}
[data-testid="stFileUploader"] * { color: #94a3b8 !important; }
.stProgress > div > div {
    background: linear-gradient(90deg, #d97706, #f59e0b) !important;
    border-radius: 4px !important;
}
.stProgress > div {
    background: rgba(255,255,255,0.06) !important;
    border-radius: 4px !important;
}
hr { border-color: rgba(245,158,11,0.1) !important; }
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #060d1f; }
::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #f59e0b; }

.nayana-hero {
    background: #080f22;
    border: 1px solid rgba(245,158,11,0.2);
    border-radius: 28px;
    padding: 56px 48px;
    text-align: center;
    margin-bottom: 36px;
    position: relative;
    overflow: hidden;
}
.nayana-hero::before {
    content: '';
    position: absolute;
    top: -80px; left: 50%;
    transform: translateX(-50%);
    width: 500px; height: 400px;
    background: radial-gradient(circle,
        rgba(245,158,11,0.07) 0%, transparent 70%);
    pointer-events: none;
}
.nayana-wordmark {
    font-family: 'Nunito', sans-serif;
    font-size: 72px;
    font-weight: 900;
    color: #f59e0b;
    letter-spacing: -3px;
    line-height: 1;
    margin-bottom: 10px;
}
.nayana-meaning {
    font-family: 'Nunito Sans', sans-serif;
    font-size: 13px;
    color: #475569;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 18px;
    font-style: italic;
}
.nayana-tagline {
    font-size: 17px;
    color: #94a3b8;
    font-weight: 400;
    max-width: 500px;
    margin: 0 auto 36px;
    line-height: 1.8;
    font-family: 'Nunito Sans', sans-serif;
}
.stat-row {
    display: flex;
    justify-content: center;
    gap: 40px;
    flex-wrap: wrap;
    margin-bottom: 40px;
}
.stat-item { text-align: center; }
.stat-num {
    font-family: 'Nunito', sans-serif;
    font-size: 32px;
    font-weight: 900;
    color: #fbbf24;
    line-height: 1;
}
.stat-lbl {
    font-size: 11px;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 5px;
    font-family: 'Nunito Sans', sans-serif;
}
.portal-row {
    display: flex;
    gap: 20px;
    justify-content: center;
    flex-wrap: wrap;
}
.portal-card {
    flex: 1;
    min-width: 220px;
    max-width: 280px;
    background: #0d1830;
    border-radius: 20px;
    padding: 36px 24px;
    text-align: center;
    transition: all 0.2s;
}
.portal-card.patient {
    border: 1.5px solid rgba(245,158,11,0.3);
}
.portal-card.doctor {
    border: 1.5px solid rgba(59,130,246,0.3);
}
.portal-card:hover { transform: translateY(-4px); }
.portal-icon { font-size: 44px; margin-bottom: 16px; }
.portal-title {
    font-family: 'Nunito', sans-serif;
    font-size: 20px;
    font-weight: 800;
    color: #f0f4ff;
    margin-bottom: 10px;
}
.portal-sub {
    font-size: 13px;
    color: #475569;
    line-height: 1.6;
    font-family: 'Nunito Sans', sans-serif;
}
.sidebar-brand {
    padding: 28px 20px 20px;
    border-bottom: 1px solid rgba(245,158,11,0.1);
    margin-bottom: 16px;
}
.brand-name {
    font-family: 'Nunito', sans-serif;
    font-size: 28px;
    font-weight: 900;
    color: #f59e0b;
    letter-spacing: -1px;
    line-height: 1;
}
.brand-role {
    font-size: 11px;
    color: #334155;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-top: 4px;
    font-family: 'Nunito Sans', sans-serif;
}
.brand-role.doctor { color: #3b82f6 !important; opacity: 0.8; }
.user-pill {
    background: rgba(245,158,11,0.07);
    border: 1px solid rgba(245,158,11,0.15);
    border-radius: 14px;
    padding: 14px 16px;
    margin: 0 12px 20px;
}
.user-pill.doctor {
    background: rgba(59,130,246,0.07) !important;
    border-color: rgba(59,130,246,0.15) !important;
}
.user-name {
    font-family: 'Nunito', sans-serif;
    font-size: 15px;
    font-weight: 800;
    color: #fbbf24;
}
.user-name.doctor { color: #93c5fd !important; }
.user-email {
    font-size: 11px;
    color: #475569;
    margin-top: 2px;
    font-family: 'Nunito Sans', sans-serif;
}
.page-title {
    font-family: 'Nunito', sans-serif;
    font-size: 32px;
    font-weight: 900;
    color: #f0f4ff;
    letter-spacing: -0.5px;
    margin-bottom: 4px;
}
.page-sub {
    font-size: 14px;
    color: #475569;
    font-weight: 400;
    margin-bottom: 28px;
    font-family: 'Nunito Sans', sans-serif;
}
.card {
    background: #0d1830;
    border: 1px solid rgba(245,158,11,0.12);
    border-radius: 18px;
    padding: 24px;
    margin-bottom: 20px;
}
.card.doctor-card {
    border-color: rgba(59,130,246,0.15) !important;
}
.quality-num {
    font-family: 'Nunito', sans-serif;
    font-size: 54px;
    font-weight: 900;
    line-height: 1;
    margin-bottom: 6px;
}
.risk-pill {
    display: inline-block;
    padding: 5px 16px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    font-family: 'Nunito', sans-serif;
    letter-spacing: 0.3px;
}
.risk-high {
    background: rgba(239,68,68,0.15);
    color: #fca5a5;
    border: 1px solid rgba(239,68,68,0.3);
}
.risk-moderate {
    background: rgba(245,158,11,0.15);
    color: #fde68a;
    border: 1px solid rgba(245,158,11,0.3);
}
.risk-low {
    background: rgba(16,185,129,0.15);
    color: #6ee7b7;
    border: 1px solid rgba(16,185,129,0.3);
}
.status-pending {
    background: rgba(245,158,11,0.12);
    color: #fde68a;
    border: 1px solid rgba(245,158,11,0.25);
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    font-family: 'Nunito', sans-serif;
}
.status-reviewed {
    background: rgba(16,185,129,0.12);
    color: #6ee7b7;
    border: 1px solid rgba(16,185,129,0.25);
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    font-family: 'Nunito', sans-serif;
}
.empty-state {
    text-align: center;
    padding: 64px 32px;
    background: #0d1830;
    border: 1px dashed rgba(245,158,11,0.2);
    border-radius: 22px;
}
.empty-icon { font-size: 52px; margin-bottom: 16px; opacity: 0.5; }
.empty-title {
    font-family: 'Nunito', sans-serif;
    font-size: 22px;
    font-weight: 800;
    color: #f0f4ff;
    margin-bottom: 8px;
}
.empty-sub {
    font-size: 14px;
    color: #475569;
    font-family: 'Nunito Sans', sans-serif;
}
.section-label {
    font-family: 'Nunito Sans', sans-serif;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 12px;
}
.sidebar-stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 9px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.sidebar-stat-label {
    font-size: 13px;
    color: #475569;
    font-family: 'Nunito Sans', sans-serif;
}
.sidebar-stat-val {
    font-size: 14px;
    font-weight: 800;
    color: #fbbf24;
    font-family: 'Nunito', sans-serif;
}
.sidebar-stat-val.doctor { color: #93c5fd !important; }
</style>
"""