def load_css(dark_mode=True):
    if dark_mode:
        bg          = "#0f1117"
        surface     = "#161b27"
        card_bg     = "#1e2535"
        card_tint   = "#1a2847"
        border      = "rgba(59,130,246,0.15)"
        border2     = "rgba(59,130,246,0.35)"
        accent      = "#3b82f6"       # blue-500
        accent2     = "#0d9488"       # teal-600
        accent3     = "#f59e0b"       # amber-500 (brand wordmark)
        text        = "#f1f5f9"       # slate-100  — 12:1 on bg
        text_muted  = "#94a3b8"       # slate-400  — 4.6:1 on bg
        text_dim    = "#cbd5e1"       # slate-300
        logo_col    = "#3b82f6"
        input_bg    = "#161b27"
        input_brd   = "rgba(59,130,246,0.25)"
        hero_bg     = "#161b27"
        hero_stripe = "rgba(59,130,246,0.07)"
        stat_num    = "#93c5fd"       # blue-300
        stat_lbl    = "rgba(148,163,184,0.8)"
        scroll_bg   = "#0f1117"
        scroll_th   = "#1e3a5f"
        metric_bg   = "#161b27"
        metric_v    = "#3b82f6"
        exp_bg      = "#161b27"
        exp_sum     = "#f1f5f9"
        tab_inact   = "#64748b"
        tab_act     = "#3b82f6"
        tab_brd     = "rgba(59,130,246,0.12)"
        prog_tr     = "rgba(255,255,255,0.06)"
        hr_col      = "rgba(59,130,246,0.12)"
        step_pend   = "#1e2535"
        step_plbl   = "#475569"
        topnav_brd  = "rgba(59,130,246,0.14)"
        sidebar_acc = "#3b82f6"
        success_bg  = "rgba(13,148,136,0.12)"
        success_brd = "rgba(13,148,136,0.35)"
        success_col = "#5eead4"
        warning_bg  = "rgba(245,158,11,0.12)"
        warning_brd = "rgba(245,158,11,0.35)"
        warning_col = "#fcd34d"
        danger_bg   = "rgba(220,38,38,0.12)"
        danger_brd  = "rgba(220,38,38,0.35)"
        danger_col  = "#fca5a5"
    else:
        bg          = "#f4f7fa"       # soft medical gray-blue
        surface     = "#ffffff"
        card_bg     = "#ffffff"
        card_tint   = "#f0f4f8"
        border      = "rgba(15,98,254,0.15)"
        border2     = "rgba(15,98,254,0.30)"
        accent      = "#0f62fe"       # clinical blue
        accent2     = "#008272"       # medical teal
        accent3     = "#f59e0b"       # amber highlight
        text        = "#111827"       # gray-900
        text_muted  = "#4b5563"       # gray-600
        text_dim    = "#374151"       # gray-700
        logo_col    = "#0f62fe"
        input_bg    = "#ffffff"
        input_brd   = "rgba(15,98,254,0.25)"
        hero_bg     = "#ffffff"
        hero_stripe = "rgba(15,98,254,0.03)"
        stat_num    = "#0f62fe"
        stat_lbl    = "rgba(17,24,39,0.7)"
        scroll_bg   = "#f4f7fa"
        scroll_th   = "#cbd5e1"
        metric_bg   = "#ffffff"
        metric_v    = "#0f62fe"
        exp_bg      = "#ffffff"
        exp_sum     = "#111827"
        tab_inact   = "#6b7280"
        tab_act     = "#0f62fe"
        tab_brd     = "rgba(15,98,254,0.15)"
        prog_tr     = "rgba(15,98,254,0.08)"
        hr_col      = "rgba(15,98,254,0.12)"
        step_pend   = "#f3f4f6"
        step_plbl   = "#6b7280"
        topnav_brd  = "rgba(15,98,254,0.15)"
        sidebar_acc = "#0f62fe"
        success_bg  = "rgba(0,130,114,0.08)"
        success_brd = "rgba(0,130,114,0.3)"
        success_col = "#008272"
        warning_bg  = "rgba(245,158,11,0.08)"
        warning_brd = "rgba(245,158,11,0.3)"
        warning_col = "#d97706"
        danger_bg   = "rgba(220,38,38,0.08)"
        danger_brd  = "rgba(220,38,38,0.3)"
        danger_col  = "#b91c1c"

    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"], .stApp {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    background: {bg} !important;
    color: {text} !important;
    -webkit-font-smoothing: antialiased;
}}

h1, h2, h3, h4 {{
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    color: {text} !important;
    letter-spacing: -0.3px;
}}

p, span, li, div, label, caption {{
    color: {text} !important;
}}

/* Streamlit markdown containers */
.stMarkdown, .stMarkdown p, .stMarkdown span,
.stText, [data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] span {{
    color: {text} !important;
}}

#MainMenu, footer, header, .stDeployButton {{ display: none !important; }}

.main .block-container {{
    padding-top: 1.75rem !important;
    padding-bottom: 4rem !important;
    max-width: 940px !important;
}}

/* ── Inputs ── */
input[type="text"],
input[type="password"],
input[type="email"],
input[type="number"],
textarea,
.stTextInput input,
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {{
    background: {input_bg} !important;
    color: {text} !important;
    border: 1.5px solid {input_brd} !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    caret-color: {accent} !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}}

input[type="text"]:focus,
input[type="password"]:focus,
.stTextInput input:focus {{
    border-color: {accent} !important;
    box-shadow: 0 0 0 3px {border} !important;
    outline: none !important;
}}

input::placeholder {{ color: {text_muted} !important; opacity: 0.7; }}

/* Password eye icon */
[data-testid="stTextInput"] button {{
    background: transparent !important;
    border: none !important;
}}
[data-testid="stTextInput"] button svg {{
    color: {accent} !important;
    fill: {accent} !important;
}}

/* Number input buttons */
[data-testid="stNumberInput"] button {{
    background: {card_bg} !important;
    border: 1px solid {border} !important;
    color: {text} !important;
    border-radius: 6px !important;
}}

/* Textarea */
textarea {{
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
}}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {{
    background: {input_bg} !important;
    border: 1.5px solid {input_brd} !important;
    border-radius: 8px !important;
    color: {text} !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
}}
[data-testid="stSelectbox"] > div > div > div {{ color: {text} !important; }}
[data-testid="stSelectbox"] svg {{ color: {accent} !important; }}
[data-baseweb="popover"], [role="listbox"] {{
    background: {card_bg} !important;
    border: 1px solid {border2} !important;
    border-radius: 8px !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.2) !important;
}}
[role="option"] {{
    background: {card_bg} !important;
    color: {text} !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    padding: 10px 14px !important;
}}
[role="option"]:hover {{ background: {border} !important; }}

/* ── Radio & Checkboxes ── */
[data-testid="stRadio"] label {{
    color: {text_dim} !important;
    font-size: 14px !important;
    font-family: 'Inter', sans-serif !important;
}}
[data-testid="stCheckbox"] label {{
    color: {text} !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
}}

/* ── Buttons ── */
.stButton > button[kind="primary"],
button[data-testid="baseButton-primary"] {{
    background: {accent} !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 10px 24px !important;
    min-height: 44px !important;
    letter-spacing: 0.1px !important;
    transition: background 0.15s, transform 0.1s, box-shadow 0.15s !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.2) !important;
}}
.stButton > button[kind="primary"]:hover {{
    background: {accent2} !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px {border2} !important;
}}

.stButton > button[kind="secondary"],
button[data-testid="baseButton-secondary"] {{
    background: transparent !important;
    color: {accent} !important;
    border: 1.5px solid {border2} !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    min-height: 44px !important;
    transition: background 0.15s, transform 0.1s !important;
}}
.stButton > button[kind="secondary"]:hover {{
    background: {border} !important;
    transform: translateY(-1px) !important;
}}

.stButton > button {{
    background: {card_bg} !important;
    color: {text_dim} !important;
    border: 1.5px solid {border} !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    min-height: 44px !important;
    transition: border-color 0.15s, color 0.15s !important;
}}
.stButton > button:hover {{
    border-color: {accent} !important;
    color: {accent} !important;
}}

/* Camera button */
[data-testid="stCameraInputButton"],
[data-testid="stCameraInput"] button {{
    background-color: {accent} !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 8px !important;
}}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
    background: transparent !important;
    border-bottom: 1.5px solid {tab_brd} !important;
    gap: 4px !important;
    padding-bottom: 0 !important;
}}
.stTabs [data-baseweb="tab"] {{
    background: transparent !important;
    color: {tab_inact} !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    border-radius: 6px 6px 0 0 !important;
    padding: 10px 20px !important;
    border-bottom: 2px solid transparent !important;
    transition: color 0.15s !important;
}}
.stTabs [aria-selected="true"] {{
    color: {tab_act} !important;
    border-bottom: 2px solid {tab_act} !important;
    font-weight: 600 !important;
    background: transparent !important;
}}

/* ── Expander ── */
[data-testid="stExpander"] {{
    background: {exp_bg} !important;
    border: 1px solid {border} !important;
    border-radius: 10px !important;
    overflow: hidden !important;
    margin-bottom: 8px !important;
}}
[data-testid="stExpander"] summary {{
    background: {exp_bg} !important;
    color: {exp_sum} !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 14px 18px !important;
}}
[data-testid="stExpander"] summary:hover {{ background: {border} !important; }}
[data-testid="stExpander"] svg {{ color: {accent} !important; }}

/* ── Metrics ── */
[data-testid="stMetric"] {{
    background: {metric_bg} !important;
    border: 1px solid {border} !important;
    border-radius: 10px !important;
    padding: 16px 18px !important;
}}
[data-testid="stMetricValue"] {{
    color: {metric_v} !important;
    font-family: 'Space Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 22px !important;
}}
[data-testid="stMetricLabel"] {{
    color: {text_muted} !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    font-weight: 600 !important;
}}

/* ── Alerts ── */
[data-testid="stAlert"] {{
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    border-left-width: 4px !important;
}}

/* ── File uploader ── */
[data-testid="stFileUploader"],
[data-testid="stFileUploader"] *,
[data-testid="stFileUploader"] div,
[data-testid="stFileUploader"] section,
[data-testid="stFileUploaderDropzone"],
[data-testid="stFileUploaderDropzone"] *,
[data-testid="stFileUploaderDropzone"] div {{
    background: {input_bg} !important;
    background-color: {input_bg} !important;
    color: {text} !important;
}}
[data-testid="stFileUploader"] {{
    border: 1.5px dashed {border2} !important;
    border-radius: 10px !important;
    transition: border-color 0.15s !important;
}}
[data-testid="stFileUploader"]:hover {{ border-color: {accent} !important; }}
[data-testid="stFileUploader"] button {{
    background: {card_bg} !important;
    color: {accent} !important;
    border: 1.5px solid {border2} !important;
    border-radius: 6px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
}}

/* ── Download button ── */
[data-testid="stDownloadButton"] button {{
    background: {accent} !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    width: 100% !important;
    min-height: 44px !important;
}}
[data-testid="stDownloadButton"] button:hover {{
    background: {accent2} !important;
    transform: translateY(-1px) !important;
}}

/* ── Progress ── */
.stProgress > div > div {{
    background: {accent} !important;
    border-radius: 4px !important;
}}
.stProgress > div {{
    background: {prog_tr} !important;
    border-radius: 4px !important;
}}

hr {{ border-color: {hr_col} !important; margin: 20px 0 !important; }}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: {scroll_bg}; }}
::-webkit-scrollbar-thumb {{ background: {scroll_th}; border-radius: 6px; }}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: {surface} !important;
    border-right: 1px solid {border} !important;
}}
[data-testid="stSidebar"] * {{
    color: {text} !important;
}}
[data-testid="stSidebar"] .stButton > button {{
    background: transparent !important;
    color: {text_dim} !important;
    border: 1px solid {border} !important;
    border-radius: 7px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    width: 100% !important;
    text-align: left !important;
    padding: 9px 14px !important;
    transition: background 0.12s, color 0.12s, border-color 0.12s !important;
}}
[data-testid="stSidebar"] .stButton > button:hover {{
    background: {border} !important;
    border-color: {accent} !important;
    color: {accent} !important;
}}
[data-testid="stSidebar"] .stButton > button[kind="primary"] {{
    background: {accent} !important;
    color: #ffffff !important;
    border: none !important;
    font-weight: 600 !important;
}}
[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {{
    background: {accent2} !important;
    color: #ffffff !important;
}}
[data-testid="stSidebar"] [data-testid="stMetric"] {{
    background: {card_bg} !important;
    border: 1px solid {border} !important;
    border-radius: 8px !important;
    padding: 12px 14px !important;
}}
[data-testid="stSidebar"] [data-testid="stMetricValue"] {{
    color: {metric_v} !important;
    font-size: 18px !important;
}}
[data-testid="stSidebar"] hr {{
    border-color: {hr_col} !important;
}}

/* ══════════════════════════════════════════
   Custom Components
══════════════════════════════════════════ */

/* ── Hero ── */
.nayana-hero {{
    background: {hero_bg};
    border-radius: 16px;
    padding: 52px 48px 44px;
    margin-bottom: 40px;
    position: relative;
    overflow: hidden;
    border: 1px solid {border2};
}}
.nayana-hero::before {{
    content: '';
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
        -55deg,
        {hero_stripe} 0px,
        {hero_stripe} 1px,
        transparent 1px,
        transparent 28px
    );
    pointer-events: none;
}}
.nayana-hero::after {{
    content: '';
    position: absolute;
    bottom: 0; right: 0;
    width: 340px; height: 340px;
    background: radial-gradient(circle at bottom right, rgba(13,148,136,0.12), transparent 70%);
    pointer-events: none;
}}
.nayana-wordmark {{
    font-family: 'Space Mono', monospace;
    font-size: 52px;
    font-weight: 700;
    color: {text};
    letter-spacing: -2px;
    line-height: 1;
    margin-bottom: 8px;
    position: relative;
    z-index: 1;
}}
.nayana-wordmark span {{
    color: {accent3} !important;
}}
.nayana-meaning {{
    font-size: 11px;
    color: {text_muted};
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 18px;
    font-style: italic;
    position: relative;
    z-index: 1;
}}
.nayana-tagline {{
    font-size: 16px;
    color: {text_dim};
    font-weight: 400;
    max-width: 480px;
    margin: 0 0 36px;
    line-height: 1.75;
    position: relative;
    z-index: 1;
}}
.stat-row {{
    display: flex;
    gap: 0;
    flex-wrap: wrap;
    margin-bottom: 0;
    position: relative;
    z-index: 1;
    border-top: 1px solid {hr_col};
    padding-top: 28px;
}}
.stat-item {{
    flex: 1;
    min-width: 100px;
    padding-right: 24px;
    border-right: 1px solid {hr_col};
    margin-right: 24px;
}}
.stat-item:last-child {{
    border-right: none;
    margin-right: 0;
    padding-right: 0;
}}
.stat-num {{
    font-family: 'Space Mono', monospace;
    font-size: 26px;
    font-weight: 700;
    color: {stat_num};
    line-height: 1;
    margin-bottom: 4px;
}}
.stat-lbl {{
    font-size: 11px;
    color: {stat_lbl};
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 500;
}}

/* ── Portal Cards ── */
.portal-card {{
    background: {card_bg};
    border-radius: 12px;
    padding: 28px 22px 28px 26px;
    transition: transform 0.15s, border-color 0.15s, box-shadow 0.15s;
    border: 1px solid {border};
    border-left: 4px solid {accent};
    width: 100%;
    cursor: pointer;
}}
.portal-card:hover {{
    transform: translateY(-3px);
    border-color: {accent};
    border-left-color: {accent2};
    box-shadow: 0 8px 24px {border};
}}
.portal-card.doctor {{
    border-left-color: {accent2};
}}
.portal-card.admin {{
    border-left-color: {accent3};
}}
.portal-icon {{ font-size: 32px; margin-bottom: 12px; }}
.portal-title {{
    font-family: 'Inter', sans-serif;
    font-size: 17px;
    font-weight: 700;
    color: {text};
    margin-bottom: 6px;
    letter-spacing: -0.1px;
}}
.portal-sub {{ font-size: 13px; color: {text_muted}; line-height: 1.6; }}

/* ── Top nav ── */
.topnav {{
    display: flex; align-items: center; justify-content: space-between;
    padding: 12px 0 16px;
    border-bottom: 1px solid {topnav_brd};
    margin-bottom: 28px;
}}
.topnav-brand {{
    font-family: 'Space Mono', monospace;
    font-size: 20px;
    font-weight: 700;
    color: {logo_col};
    letter-spacing: -1px;
}}
.topnav-user {{
    font-size: 12px;
    color: {text_muted};
    font-weight: 500;
    background: {border};
    padding: 4px 12px;
    border-radius: 20px;
    border: 1px solid {border2};
}}

/* ── Page heading ── */
.page-title {{
    font-family: 'Inter', sans-serif;
    font-size: 26px;
    font-weight: 800;
    color: {text};
    letter-spacing: -0.5px;
    margin-bottom: 4px;
    line-height: 1.2;
}}
.page-sub {{
    font-size: 14px;
    color: {text_muted};
    font-weight: 400;
    margin-bottom: 24px;
    line-height: 1.5;
}}

/* ── Section label ── */
.section-label {{
    font-family: 'Inter', sans-serif;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    color: {text_muted};
    margin-bottom: 10px;
}}

/* ── Cards ── */
.card {{
    background: {card_bg};
    border: 1px solid {border};
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 16px;
}}
.card.highlight {{
    border-color: {accent2};
    background: {success_bg};
    border-left: 3px solid {accent2};
}}
.card.danger {{
    border-color: {danger_brd};
    background: {danger_bg};
    border-left: 3px solid #dc2626;
}}
.card.warning {{
    border-color: {warning_brd};
    background: {warning_bg};
    border-left: 3px solid #d97706;
}}
.card-flat {{
    background: transparent;
    border: 1px solid {border};
    border-radius: 10px;
    padding: 18px;
    margin-bottom: 12px;
}}

/* ── Quality number ── */
.quality-num {{
    font-family: 'Space Mono', monospace;
    font-size: 44px;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 4px;
}}

/* ── Risk pills — shape + text + color (accessible) ── */
.risk-pill {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 14px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 700;
    font-family: 'Inter', sans-serif;
    letter-spacing: 0.3px;
}}
.risk-pill::before {{
    font-size: 10px;
    font-style: normal;
}}
.risk-high {{
    background: {danger_bg};
    color: {danger_col};
    border: 1.5px solid {danger_brd};
}}
.risk-high::before {{ content: '▲ HIGH'; }}
.risk-moderate {{
    background: {warning_bg};
    color: {warning_col};
    border: 1.5px solid {warning_brd};
}}
.risk-moderate::before {{ content: '◆ MODERATE'; }}
.risk-low {{
    background: {success_bg};
    color: {success_col};
    border: 1.5px solid {success_brd};
}}
.risk-low::before {{ content: '● LOW'; }}

/* Override text inside risk-pill */
.risk-pill span {{ color: inherit !important; }}

/* ── Status badges ── */
.status-pending {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: {warning_bg};
    color: {warning_col};
    border: 1.5px solid {warning_brd};
    padding: 3px 10px;
    border-radius: 5px;
    font-size: 11px;
    font-weight: 700;
    font-family: 'Inter', sans-serif;
    letter-spacing: 0.5px;
}}
.status-pending::before {{ content: '⏳'; font-size: 10px; }}
.status-reviewed {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: {success_bg};
    color: {success_col};
    border: 1.5px solid {success_brd};
    padding: 3px 10px;
    border-radius: 5px;
    font-size: 11px;
    font-weight: 700;
    font-family: 'Inter', sans-serif;
    letter-spacing: 0.5px;
}}
.status-reviewed::before {{ content: '✓'; font-size: 11px; font-weight: 900; }}

/* ── Step bar ── */
.step-bar {{
    display: flex;
    align-items: center;
    margin-bottom: 28px;
    background: {card_bg};
    border: 1px solid {border};
    border-radius: 10px;
    padding: 14px 20px;
}}
.step {{ display: flex; align-items: center; gap: 8px; flex: 1; }}
.step-dot {{
    width: 28px; height: 28px;
    border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
    font-size: 12px; font-weight: 700;
    font-family: 'Space Mono', monospace;
    flex-shrink: 0;
    transition: background 0.2s;
}}
.step-dot.done {{
    background: {accent2};
    color: white;
}}
.step-dot.done::after {{ content: '✓'; font-family: sans-serif; font-size: 13px; }}
.step-dot.active {{
    background: {accent};
    color: white;
    box-shadow: 0 0 0 3px {border};
}}
.step-dot.pending {{
    background: {step_pend};
    color: {step_plbl};
    border: 1px solid {border};
}}
.step-label {{
    font-size: 13px;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
}}
.step-label.done {{ color: {accent2}; }}
.step-label.active {{ color: {text}; }}
.step-label.pending {{ color: {text_muted}; }}
.step-line {{
    flex: 1;
    height: 1.5px;
    background: {border};
    margin: 0 6px;
    max-width: 48px;
}}
.step-line.done {{ background: {accent2}; }}

/* ── Empty state ── */
.empty-state {{
    text-align: center;
    padding: 56px 32px;
    background: {card_bg};
    border: 1.5px dashed {border};
    border-radius: 12px;
}}
.empty-icon {{ font-size: 40px; margin-bottom: 14px; opacity: 0.5; }}
.empty-title {{
    font-family: 'Inter', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: {text};
    margin-bottom: 6px;
}}
.empty-sub {{ font-size: 14px; color: {text_muted}; }}

/* ── Doc / info card ── */
.doc-card {{
    background: {card_bg};
    border: 1px solid {border};
    border-radius: 10px;
    padding: 18px;
}}
.doc-name {{
    font-family: 'Inter', sans-serif;
    font-size: 17px;
    font-weight: 700;
    color: {text};
    margin-bottom: 2px;
}}
.doc-meta {{ font-size: 13px; color: {text_muted}; margin-top: 3px; }}

/* ── Doctor avatar badge ── */
.doc-avatar {{
    width: 38px; height: 38px;
    border-radius: 8px;
    background: {accent};
    color: white;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: 15px;
    flex-shrink: 0;
}}

/* ── Info banner ── */
.info-banner {{
    background: {card_tint};
    border: 1px solid {border2};
    border-left: 4px solid {accent};
    border-radius: 8px;
    padding: 14px 18px;
    font-size: 13px;
    color: {text_dim};
    line-height: 1.6;
    margin-bottom: 16px;
}}

/* ── Sidebar brand block ── */
.sidebar-brand {{
    padding-bottom: 18px;
    margin-bottom: 18px;
    border-bottom: 1px solid {hr_col};
}}
.sidebar-wordmark {{
    font-family: 'Space Mono', monospace;
    font-size: 20px;
    font-weight: 700;
    color: {accent3};
    letter-spacing: -1px;
    margin-bottom: 2px;
}}
.sidebar-tag {{
    font-size: 10px;
    color: {text_muted};
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 600;
}}

/* ── Sidebar user card ── */
.sidebar-user {{
    background: {border};
    border: 1px solid {border2};
    border-radius: 8px;
    padding: 12px 14px;
    margin-bottom: 20px;
}}
.sidebar-user-name {{
    font-size: 14px;
    font-weight: 700;
    color: {text};
    margin-bottom: 2px;
}}
.sidebar-user-meta {{
    font-size: 11px;
    color: {text_muted};
}}

/* ── Sidebar nav label ── */
.sidebar-nav-label {{
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: {text_muted};
    margin: 16px 0 6px;
    padding: 0 2px;
}}

/* Consent modal styling */
.consent-card {{
    background: {surface};
    border: 1px solid {border2};
    border-radius: 14px;
    padding: 36px 32px;
    margin-top: 48px;
}}
.consent-brand {{
    font-family: 'Space Mono', monospace;
    font-size: 28px;
    font-weight: 700;
    color: {accent3};
    letter-spacing: -1px;
    text-align: center;
    margin-bottom: 4px;
}}
.consent-subtitle {{
    text-align: center;
    font-size: 11px;
    letter-spacing: 2px;
    color: {text_muted};
    text-transform: uppercase;
    margin-bottom: 28px;
    font-weight: 500;
}}
.consent-body {{
    font-size: 14px;
    color: {text_dim};
    line-height: 1.75;
    margin-bottom: 14px;
}}
.consent-emergency {{
    font-size: 13px;
    color: {danger_col};
    line-height: 1.6;
    padding: 12px 16px;
    background: {danger_bg};
    border: 1.5px solid {danger_brd};
    border-radius: 8px;
    margin-top: 16px;
}}
</style>
"""
