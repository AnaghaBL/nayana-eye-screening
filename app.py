import streamlit as st
import cv2
import numpy as np
import torch
from torchvision import transforms
import timm
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image
from report_generator import generate_report
from voice_input import record_voice
from database import load_cases, save_case, update_case
from auth import (register_patient, login_patient,
                  register_doctor, login_doctor)
from styles import load_css
import tempfile
import os

st.set_page_config(
    page_title="Nayana — AI Eye Screening",
    page_icon="👁",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown(load_css(), unsafe_allow_html=True)

DISEASE_NAMES = [
    'Normal', 'Diabetic Retinopathy', 'Glaucoma',
    'Cataract', 'AMD', 'Hypertension', 'Myopia', 'Other'
]
DISEASE_COLORS = [
    '#10b981','#ef4444','#f97316','#3b82f6',
    '#a855f7','#eab308','#06b6d4','#64748b'
]

for key, val in {
    'role': None,
    'patient_logged_in': False,
    'patient_user': None,
    'doctor_logged_in': False,
    'doctor_user': None,
    'page': 'screening'
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── Helpers ────────────────────────────────────────────────────
def check_quality(image_np):
    gray  = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
    score = 100
    tips  = []
    blur  = cv2.Laplacian(gray, cv2.CV_64F).var()
    if blur < 100:
        score -= 30
        tips.append("Image is blurry — hold the camera steady")
    brightness = gray.mean()
    if brightness < 60:
        score -= 25
        tips.append("Too dark — move to better lighting")
    elif brightness > 200:
        score -= 20
        tips.append("Too bright — reduce light or move away")
    circles = cv2.HoughCircles(
        gray, cv2.HOUGH_GRADIENT, 1, 20,
        param1=50, param2=30, minRadius=30, maxRadius=200
    )
    if circles is None:
        score -= 25
        tips.append("Eye not detected — center the eye in frame")
    return max(score, 0), tips

def preprocess_retinal(image_pil):
    img = np.array(image_pil.resize((224, 224)))
    lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    l = clahe.apply(l)
    enhanced = cv2.cvtColor(cv2.merge([l,a,b]),
                             cv2.COLOR_LAB2RGB)
    return Image.fromarray(enhanced)

@st.cache_resource
def load_model():
    m = timm.create_model('efficientnet_b0',
                           pretrained=False, num_classes=8)
    m.load_state_dict(torch.load('odir_model.pth',
                                  map_location='cpu'))
    m.eval()
    return m

def predict(image_pil):
    image_pil = preprocess_retinal(image_pil)
    tf = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485,0.456,0.406],
                             [0.229,0.224,0.225])
    ])
    with torch.no_grad():
        probs = torch.sigmoid(
            load_model()(tf(image_pil).unsqueeze(0))
        )[0]
    return probs.numpy()

def get_heatmap(image_pil):
    image_pil = preprocess_retinal(image_pil)
    tf = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485,0.456,0.406],
                             [0.229,0.224,0.225])
    ])
    tensor = tf(image_pil).unsqueeze(0)
    m      = load_model()
    cam    = GradCAM(model=m,
                     target_layers=[m.blocks[-1][-1]])
    gcam   = cam(input_tensor=tensor)[0]
    rgb    = np.array(image_pil.resize((224,224))) / 255.0
    return show_cam_on_image(rgb.astype(np.float32),
                              gcam, use_rgb=True)

def get_risk(probs):
    nn = [(DISEASE_NAMES[i], probs[i])
          for i in range(1,8) if probs[i] > 0.3]
    if not nn:
        return "Low Risk — No significant findings", "low"
    elif max(p for _,p in nn) > 0.6:
        top = max(nn, key=lambda x: x[1])
        return (f"High Risk — {top[0]} likely. "
                f"Refer to specialist immediately."), "high"
    else:
        return ("Moderate Risk — Follow-up recommended "
                "within 4 weeks"), "moderate"

def dark_chart(probs):
    fig, ax = plt.subplots(figsize=(7, 3.2))
    fig.patch.set_facecolor('#0d1830')
    ax.set_facecolor('#0d1830')
    bars = ax.barh(DISEASE_NAMES, probs*100,
                   color=DISEASE_COLORS,
                   height=0.55, edgecolor='none')
    ax.set_xlabel("Confidence (%)",
                  color='#475569', fontsize=9)
    ax.set_xlim(0, 108)
    ax.tick_params(colors='#64748b', labelsize=9)
    for s in ax.spines.values():
        s.set_color('#1e3a5f')
    ax.axvline(50, color='#1e3a5f', lw=0.8, ls='--')
    for bar, p in zip(bars, probs):
        ax.text(p*100+1.5,
                bar.get_y()+bar.get_height()/2,
                f'{p*100:.1f}%',
                va='center', fontsize=8.5, color='#64748b')
    plt.tight_layout(pad=0.5)
    return fig

model = load_model()

# ── Top navbar ─────────────────────────────────────────────────
def patient_navbar(user):
    st.markdown(f"""
    <div style="display:flex;align-items:center;
                justify-content:space-between;
                padding:12px 0 16px;
                border-bottom:1px solid rgba(245,158,11,0.12);
                margin-bottom:28px;">
        <div style="font-family:'Nunito',sans-serif;
                    font-size:26px;font-weight:900;
                    color:#f59e0b;letter-spacing:-1px;">
            Nayana
        </div>
        <div style="font-size:13px;color:#475569;">
            {user['name']} · Patient
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3,c4,c5 = st.columns([2,1,1,1,1])
    if c2.button("🔬 Screening",
                 type=("primary"
                       if st.session_state['page']=='screening'
                       else "secondary"),
                 use_container_width=True,
                 key="nav_scr"):
        st.session_state['page'] = 'screening'
        st.rerun()
    if c3.button("📋 My Results",
                 type=("primary"
                       if st.session_state['page']=='results'
                       else "secondary"),
                 use_container_width=True,
                 key="nav_res"):
        st.session_state['page'] = 'results'
        st.rerun()
    if c4.button("🏠 Home",
                 use_container_width=True,
                 key="nav_home"):
        st.session_state['role']              = None
        st.session_state['patient_logged_in'] = False
        st.session_state['patient_user']      = None
        st.rerun()
    if c5.button("Sign Out",
                 use_container_width=True,
                 key="nav_so"):
        st.session_state['patient_logged_in'] = False
        st.session_state['patient_user']      = None
        st.rerun()
    st.write("")

def doctor_navbar(doc):
    st.markdown(f"""
    <div style="display:flex;align-items:center;
                justify-content:space-between;
                padding:12px 0 16px;
                border-bottom:1px solid rgba(59,130,246,0.2);
                margin-bottom:28px;">
        <div style="font-family:'Nunito',sans-serif;
                    font-size:26px;font-weight:900;
                    color:#f59e0b;letter-spacing:-1px;">
            Nayana
            <span style="font-size:12px;font-weight:600;
                         color:#93c5fd;letter-spacing:1px;
                         margin-left:8px;font-family:
                         'Nunito Sans',sans-serif;">
                DOCTOR
            </span>
        </div>
        <div style="font-size:13px;color:#475569;">
            Dr. {doc['name']} ·
            {doc['specialization']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3 = st.columns([4,1,1])
    if c2.button("🏠 Home",
                 use_container_width=True,
                 key="dnav_home"):
        st.session_state['role']             = None
        st.session_state['doctor_logged_in'] = False
        st.session_state['doctor_user']      = None
        st.rerun()
    if c3.button("Sign Out",
                 use_container_width=True,
                 key="dnav_so"):
        st.session_state['doctor_logged_in'] = False
        st.session_state['doctor_user']      = None
        st.rerun()
    st.write("")

# ── Results renderer ───────────────────────────────────────────
def render_my_results(my_cases):
    if not my_cases:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">👁</div>
            <div class="empty-title">No screenings yet</div>
            <div class="empty-sub">Go to New Screening to
            submit your first retinal scan</div>
        </div>
        """, unsafe_allow_html=True)
        return

    total    = len(my_cases)
    reviewed = sum(1 for c in my_cases
                   if c['status']=='Reviewed')
    pending  = total - reviewed
    high     = sum(1 for c in my_cases
                   if 'High' in c['risk_level'])

    m1,m2,m3,m4 = st.columns(4)
    m1.metric("Total Scans", total)
    m2.metric("Reviewed",    reviewed)
    m3.metric("Pending",     pending)
    m4.metric("High Risk",   high)
    st.write("")

    for case in reversed(my_cases):
        status = case['status']
        risk   = case['risk_level']
        icon   = "✅" if status=="Reviewed" else "⏳"
        ri     = ("🔴" if "High" in risk
                  else "🟡" if "Moderate" in risk else "🟢")

        with st.expander(
            f"{icon} {case['case_id']} — "
            f"{case['timestamp']} — {ri} {status}",
            expanded=case['case_id']==st.session_state.get(
                'last_case_id')
        ):
            c1,c2 = st.columns(2)
            with c1:
                if os.path.exists(case['image_path']):
                    st.image(
                        Image.open(case['image_path']),
                        caption="Retinal scan",
                        width='stretch'
                    )
                if os.path.exists(case['heatmap_path']):
                    st.image(
                        Image.open(case['heatmap_path']),
                        caption="AI heatmap",
                        width='stretch'
                    )
            with c2:
                st.markdown("**AI Results**")
                probs = case['probs']
                for i,(name,p) in enumerate(
                    zip(DISEASE_NAMES,probs)
                ):
                    if p > 0.3:
                        pc1,pc2 = st.columns([3,1])
                        pc1.progress(float(p), text=name)
                        if p>0.7:
                            pc2.error(f"{p*100:.0f}%")
                        elif p>0.5:
                            pc2.warning(f"{p*100:.0f}%")
                        else:
                            pc2.info(f"{p*100:.0f}%")
                if "High" in risk:
                    st.error(f"Risk: {risk}")
                elif "Moderate" in risk:
                    st.warning(f"Risk: {risk}")
                else:
                    st.success(f"Risk: {risk}")

            st.divider()
            st.markdown("**Doctor's Response**")
            if status != "Reviewed":
                st.info("Awaiting specialist review — "
                        "check back in 24 hours")
            else:
                st.success(
                    f"Reviewed: {case.get('reviewed_at','')}"
                )
                for lbl, val in [
                    ("Diagnosis",
                     case['doctor_diagnosis']),
                    ("Treatment",
                     case['doctor_prescription'] or "None given"),
                ]:
                    r1,r2 = st.columns([1,3])
                    r1.markdown(f"**{lbl}**")
                    r2.info(val)
                r1,r2 = st.columns([1,3])
                r1.markdown("**Referral**")
                ref = case['doctor_referral']
                if "Emergency" in ref or "Urgent" in ref:
                    r2.error(ref)
                elif "month" in ref:
                    r2.warning(ref)
                else:
                    r2.success(ref)
                if case['doctor_notes']:
                    r1,r2 = st.columns([1,3])
                    r1.markdown("**Notes**")
                    r2.info(case['doctor_notes'])

# ══════════════════════════════════════════════════════════════
# LANDING
# ══════════════════════════════════════════════════════════════
if st.session_state['role'] is None:
    st.markdown("""
    <div class="nayana-hero">
        <div class="nayana-wordmark">Nayana</div>
        <div class="nayana-meaning">नयन · the eye</div>
        <div class="nayana-tagline">
            AI-powered retinal screening that connects rural
            patients to city specialists in minutes, not months.
        </div>
        <div class="stat-row">
            <div class="stat-item">
                <div class="stat-num">8</div>
                <div class="stat-lbl">diseases screened</div>
            </div>
            <div class="stat-item">
                <div class="stat-num">6,392</div>
                <div class="stat-lbl">training records</div>
            </div>
            <div class="stat-item">
                <div class="stat-num">5</div>
                <div class="stat-lbl">languages</div>
            </div>
            <div class="stat-item">
                <div class="stat-num">3 min</div>
                <div class="stat-lbl">scan to specialist</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div style="text-align:center;margin-bottom:24px;">'
        '<span style="font-family:Nunito,sans-serif;'
        'font-size:20px;font-weight:800;color:#f0f4ff;">'
        'Who are you?</span></div>',
        unsafe_allow_html=True
    )

    _,c1,c2,_ = st.columns([1,1,1,1])
    with c1:
        st.markdown("""
        <div class="portal-card patient">
            <div class="portal-icon">🧑‍⚕️</div>
            <div class="portal-title">I am a Patient</div>
            <div class="portal-sub">Upload retinal images,
            describe symptoms, receive AI screening results</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Enter Patient Portal →",
                     type="primary",
                     use_container_width=True,
                     key="go_patient"):
            st.session_state['role'] = 'patient'
            st.rerun()

    with c2:
        st.markdown("""
        <div class="portal-card doctor">
            <div class="portal-icon">👨‍⚕️</div>
            <div class="portal-title">I am a Doctor</div>
            <div class="portal-sub">Review AI-augmented cases,
            issue diagnoses and e-prescriptions</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Enter Doctor Portal →",
                     use_container_width=True,
                     key="go_doctor"):
            st.session_state['role'] = 'doctor'
            st.rerun()

# ══════════════════════════════════════════════════════════════
# PATIENT PORTAL
# ══════════════════════════════════════════════════════════════
elif st.session_state['role'] == 'patient':

    if not st.session_state['patient_logged_in']:
        _,col,_ = st.columns([1,1.4,1])
        with col:
            st.markdown(
                '<div class="page-title" '
                'style="text-align:center;">'
                'Patient Portal</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                '<div class="page-sub" '
                'style="text-align:center;">'
                'Sign in or create an account</div>',
                unsafe_allow_html=True
            )
            tab1,tab2 = st.tabs(["Sign In","Create Account"])

            with tab1:
                st.write("")
                email = st.text_input(
                    "Email", key="li_e",
                    placeholder="you@example.com"
                )
                pw = st.text_input(
                    "Password", type="password", key="li_p"
                )
                st.write("")
                if st.button("Sign In →", type="primary",
                             key="li_btn",
                             use_container_width=True):
                    if email and pw:
                        ok,user,msg = login_patient(email, pw)
                        if ok:
                            st.session_state[
                                'patient_logged_in'] = True
                            st.session_state[
                                'patient_user'] = user
                            st.rerun()
                        else:
                            st.error(msg)
                    else:
                        st.error("Please fill in both fields")
                st.write("")
                if st.button("← Back", key="back_p",
                             use_container_width=True):
                    st.session_state['role'] = None
                    st.rerun()

            with tab2:
                st.write("")
                c1,c2 = st.columns(2)
                rn  = c1.text_input("Full name",  key="rn")
                ra  = c2.number_input("Age",1,120,30, key="ra")
                rg  = st.selectbox(
                    "Gender",
                    ["Male","Female","Other"], key="rg"
                )
                re  = st.text_input("Email", key="re")
                c1,c2 = st.columns(2)
                rp  = c1.text_input("Password",
                                     type="password", key="rp")
                rp2 = c2.text_input("Confirm",
                                     type="password", key="rp2")
                st.write("")
                if st.button("Create Account →",
                             type="primary", key="r_btn",
                             use_container_width=True):
                    if not all([rn,re,rp,rp2]):
                        st.error("Please fill in all fields")
                    elif rp != rp2:
                        st.error("Passwords do not match")
                    elif len(rp) < 6:
                        st.error("Min 6 characters")
                    else:
                        ok,msg = register_patient(
                            rn,ra,rg,re,rp)
                        if ok:
                            st.success(
                                "Account created! Sign in.")
                        else:
                            st.error(msg)
    else:
        user = st.session_state['patient_user']
        patient_navbar(user)

        if st.session_state['page'] == 'screening':
            st.markdown(
                '<div class="page-title">New Screening</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                '<div class="page-sub">Upload a retinal image '
                'for AI-powered multi-disease analysis</div>',
                unsafe_allow_html=True
            )

            with st.expander("Patient Details",
                             expanded=True):
                c1,c2,c3 = st.columns(3)
                pname   = c1.text_input(
                    "Name", value=user['name'])
                page_   = c2.number_input(
                    "Age",1,120, value=user['age'])
                pgender = c3.selectbox(
                    "Gender",["Male","Female","Other"],
                    index=["Male","Female","Other"].index(
                        user['gender'])
                )

            with st.expander("Symptom Input", expanded=True):
                method = st.radio(
                    "Method",["Type","Voice"],
                    horizontal=True
                )
                if method == "Type":
                    symp = st.text_input(
                        "Symptoms",
                        placeholder="blurred vision, eye pain..."
                    )
                    detected = symp or "Not specified"
                else:
                    lang = st.selectbox(
                        "Language",
                        ["Kannada","Hindi","Tamil",
                         "Telugu","English"]
                    )
                    if st.button("🎤  Start Recording",
                                 type="primary"):
                        with st.spinner(
                            f"Listening in {lang}..."
                        ):
                            res = record_voice(lang)
                        if res["success"]:
                            st.success(
                                f"Heard: {res['text']}")
                            if lang != "English":
                                st.caption(
                                    f"Translated: "
                                    f"{res.get('english_text','')}"
                                )
                            st.info(
                                f"Symptoms: "
                                f"{', '.join(res['symptoms'])}"
                            )
                            detected = ", ".join(
                                res["symptoms"])
                            st.session_state[
                                'symptoms'] = detected
                            st.session_state[
                                'raw_speech'] = res['text']
                        else:
                            st.error(res["error"])
                            detected = "Not specified"
                    else:
                        detected = st.session_state.get(
                            'symptoms','Not specified')
                symp_final = detected

            st.write("")
            st.markdown(
                '<div class="section-label">'
                'Retinal Image</div>',
                unsafe_allow_html=True
            )
            uploaded = st.file_uploader(
                "Upload", type=["jpg","jpeg","png"],
                label_visibility="collapsed"
            )

            if uploaded:
                image_pil = Image.open(
                    uploaded).convert('RGB')
                image_np  = np.array(image_pil)

                c1,c2 = st.columns([1,1.6])
                with c1:
                    st.image(
                        image_pil,
                        use_container_width=True,
                        caption="Uploaded image"
                    )
                with c2:
                    score, tips = check_quality(image_np)
                    qc = ("#10b981" if score>=70
                          else "#f59e0b" if score>=40
                          else "#ef4444")
                    ql = ("Good" if score>=70
                          else "Fair" if score>=40
                          else "Poor")
                    st.markdown(f"""
                    <div class="card">
                        <div class="section-label">
                            Image quality
                        </div>
                        <div class="quality-num"
                             style="color:{qc};">
                            {score}%
                        </div>
                        <div style="font-size:13px;
                                    color:#64748b;">
                            {ql} — {'ready for analysis'
                                    if score>=70 else
                                    'proceed with caution'
                                    if score>=40 else
                                    'retake recommended'}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    for tip in tips:
                        st.warning(f"⚠ {tip}")

                st.divider()
                st.markdown(
                    '<div class="page-title" '
                    'style="font-size:22px;">'
                    'AI Analysis</div>',
                    unsafe_allow_html=True
                )

                with st.spinner("Running analysis..."):
                    probs = predict(image_pil)

                fig = dark_chart(probs)
                st.pyplot(fig)
                plt.close()

                risk_txt, risk_type = get_risk(probs)
                risk_css = {
                    "high":     "risk-high",
                    "moderate": "risk-moderate",
                    "low":      "risk-low"
                }[risk_type]
                threshold = 0.5
                det_conds = [
                    (DISEASE_NAMES[i], probs[i])
                    for i in range(8)
                    if probs[i] > threshold
                ]

                st.markdown(f"""
                <div class="card">
                    <div style="display:flex;
                        align-items:center;
                        justify-content:space-between;
                        margin-bottom:10px;">
                        <div style="font-size:15px;
                            font-weight:700;
                            font-family:'Nunito',sans-serif;
                            color:#f0f4ff;">
                            Overall Assessment
                        </div>
                        <span class="risk-pill {risk_css}">
                            {risk_type.title()} Risk
                        </span>
                    </div>
                    <div style="font-size:13px;
                                color:#64748b;">
                        {risk_txt}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                for name,p in sorted(
                    det_conds,
                    key=lambda x: x[1], reverse=True
                ):
                    if name == 'Normal':
                        st.success(
                            f"✓ {name} — {p*100:.1f}%")
                    elif p > 0.7:
                        st.error(
                            f"⚠ {name} detected — "
                            f"{p*100:.1f}%")
                    else:
                        st.warning(
                            f"⚠ {name} possible — "
                            f"{p*100:.1f}%")

                st.divider()
                st.markdown(
                    '<div class="page-title" '
                    'style="font-size:22px;">'
                    'AI Attention Heatmap</div>',
                    unsafe_allow_html=True
                )
                st.markdown(
                    '<div class="page-sub" '
                    'style="margin-bottom:16px;">'
                    'Red areas indicate where the AI '
                    'detected abnormalities</div>',
                    unsafe_allow_html=True
                )
                with st.spinner("Generating heatmap..."):
                    heatmap = get_heatmap(image_pil)
                hc1,hc2 = st.columns(2)
                hc1.image(
                    image_pil.resize((224,224)),
                    caption="Original", width=220
                )
                hc2.image(
                    heatmap,
                    caption="AI attention", width=220
                )

                st.divider()
                ac1,ac2 = st.columns(2)

                with ac1:
                    st.markdown(
                        '<div class="section-label">'
                        'Send to specialist</div>',
                        unsafe_allow_html=True
                    )
                    if st.button(
                        "📤  Send to Doctor",
                        use_container_width=True
                    ):
                        with st.spinner("Sending..."):
                            os.makedirs("cases_images",
                                        exist_ok=True)
                            n  = len(os.listdir(
                                "cases_images"))
                            ip = (f"cases_images/"
                                  f"{pname.replace(' ','_')}"
                                  f"_{n}_original.png")
                            hp = (f"cases_images/"
                                  f"{pname.replace(' ','_')}"
                                  f"_{n}_heatmap.png")
                            image_pil.resize(
                                (300,300)).save(ip)
                            Image.fromarray(
                                heatmap).save(hp)
                            cid = save_case(
                                patient_name=pname,
                                patient_age=page_,
                                patient_gender=pgender,
                                symptoms=symp_final,
                                quality_score=score,
                                probs=probs,
                                detected_conditions=det_conds,
                                risk_level=risk_txt,
                                image_path=ip,
                                heatmap_path=hp,
                                patient_email=user['email']
                            )
                        st.success(
                            f"Sent! Case ID: **{cid}**")
                        st.session_state[
                            'last_case_id'] = cid

                with ac2:
                    st.markdown(
                        '<div class="section-label">'
                        'Download report</div>',
                        unsafe_allow_html=True
                    )
                    if st.button(
                        "📄  Generate PDF",
                        type="primary",
                        use_container_width=True
                    ):
                        with st.spinner("Generating..."):
                            with tempfile.NamedTemporaryFile(
                                delete=False, suffix='.pdf'
                            ) as tmp:
                                pdf_path = generate_report(
                                    patient_name=pname,
                                    patient_age=page_,
                                    patient_gender=pgender,
                                    symptoms=symp_final,
                                    quality_score=score,
                                    quality_tips=tips,
                                    probs=probs,
                                    detected_conditions=det_conds,
                                    risk_level=risk_txt,
                                    original_image_pil=image_pil,
                                    heatmap_array=heatmap,
                                    output_path=tmp.name
                                )
                        with open(pdf_path,'rb') as f:
                            st.download_button(
                                "⬇  Download PDF",
                                data=f.read(),
                                file_name=f"nayana_{pname.replace(' ','_')}.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )

                st.write("")
                st.caption(
                    "Nayana provides AI-assisted screening "
                    "only. A qualified ophthalmologist must "
                    "confirm all diagnoses."
                )

        elif st.session_state['page'] == 'results':
            st.markdown(
                '<div class="page-title">My Results</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                '<div class="page-sub">Your complete '
                'screening history and doctor '
                'responses</div>',
                unsafe_allow_html=True
            )
            all_cases = load_cases()
            my_cases  = [
                c for c in all_cases
                if c.get('patient_email','') == user['email']
            ]
            render_my_results(my_cases)

# ══════════════════════════════════════════════════════════════
# DOCTOR PORTAL
# ══════════════════════════════════════════════════════════════
elif st.session_state['role'] == 'doctor':

    if not st.session_state['doctor_logged_in']:
        _,col,_ = st.columns([1,1.4,1])
        with col:
            st.markdown(
                '<div class="page-title" '
                'style="text-align:center;">'
                'Doctor Portal</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                '<div class="page-sub" '
                'style="text-align:center;">'
                'Sign in to review patient cases</div>',
                unsafe_allow_html=True
            )
            tab1,tab2 = st.tabs(["Sign In","Register"])

            with tab1:
                st.write("")
                de = st.text_input(
                    "Email", key="dli_e",
                    placeholder="doctor@hospital.com"
                )
                dp = st.text_input(
                    "Password", type="password", key="dli_p"
                )
                st.write("")
                if st.button("Sign In →", type="primary",
                             key="dli_btn",
                             use_container_width=True):
                    if de and dp:
                        ok,user,msg = login_doctor(de, dp)
                        if ok:
                            st.session_state[
                                'doctor_logged_in'] = True
                            st.session_state[
                                'doctor_user'] = user
                            st.rerun()
                        else:
                            st.error(msg)
                    else:
                        st.error("Please fill in both fields")
                st.write("")
                if st.button("← Back", key="back_d",
                             use_container_width=True):
                    st.session_state['role'] = None
                    st.rerun()

            with tab2:
                st.write("")
                c1,c2 = st.columns(2)
                dn   = c1.text_input("Full name",   key="dn")
                dsp  = c2.text_input(
                    "Specialization",
                    placeholder="Ophthalmologist", key="dsp"
                )
                c1,c2 = st.columns(2)
                dh   = c1.text_input("Hospital",    key="dh")
                dl   = c2.text_input("License No.", key="dl")
                dme  = st.text_input("Email",       key="dme")
                c1,c2 = st.columns(2)
                dpa  = c1.text_input(
                    "Password", type="password", key="dpa"
                )
                dpa2 = c2.text_input(
                    "Confirm",  type="password", key="dpa2"
                )
                st.write("")
                if st.button("Register →", type="primary",
                             key="dr_btn",
                             use_container_width=True):
                    if not all([dn,dsp,dh,dl,dme,dpa]):
                        st.error("Please fill in all fields")
                    elif dpa != dpa2:
                        st.error("Passwords do not match")
                    elif len(dpa) < 6:
                        st.error("Min 6 characters")
                    else:
                        ok,msg = register_doctor(
                            dn,dsp,dh,dl,dme,dpa)
                        if ok:
                            st.success(
                                "Registered! Sign in.")
                        else:
                            st.error(msg)
    else:
        doc = st.session_state['doctor_user']
        doctor_navbar(doc)

        st.markdown(
            '<div class="page-title">Patient Cases</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="page-sub">AI-augmented retinal '
            'screening cases awaiting your review</div>',
            unsafe_allow_html=True
        )

        cases = load_cases()

        if not cases:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">📋</div>
                <div class="empty-title">No cases yet</div>
                <div class="empty-sub">Cases will appear here
                once patients submit screenings</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            total    = len(cases)
            pending  = sum(1 for c in cases
                           if c['status']=='Pending')
            reviewed = sum(1 for c in cases
                           if c['status']=='Reviewed')
            high     = sum(1 for c in cases
                           if 'High' in c['risk_level'])

            m1,m2,m3,m4 = st.columns(4)
            m1.metric("Total Cases",    total)
            m2.metric("Pending Review", pending)
            m3.metric("Reviewed",       reviewed)
            m4.metric("High Risk",      high)
            st.write("")

            fc1,fc2 = st.columns([2,4])
            sf   = fc1.selectbox(
                "Filter", ["All","Pending","Reviewed"]
            )
            srch = fc2.text_input(
                "Search",
                placeholder="Search patient name..."
            )

            filtered = cases
            if sf != "All":
                filtered = [c for c in filtered
                            if c['status']==sf]
            if srch:
                filtered = [
                    c for c in filtered
                    if srch.lower() in
                    c['patient_name'].lower()
                ]
            filtered = sorted(
                filtered,
                key=lambda c: (
                    0 if c['status']=='Pending' else 1,
                    0 if 'High' in c['risk_level'] else 1
                )
            )

            st.write(f"Showing {len(filtered)} cases")
            st.write("")

            for case in filtered:
                risk    = case['risk_level']
                status  = case['status']
                is_high = 'High' in risk
                is_pend = status == 'Pending'
                ri      = ("🔴" if is_high
                           else "🟡" if is_pend else "🟢")
                risk_type_str = (
                    'High' if 'High' in risk
                    else 'Moderate' if 'Moderate' in risk
                    else 'Low'
                )
                risk_css = (
                    "risk-high" if is_high
                    else "risk-moderate"
                    if "Moderate" in risk
                    else "risk-low"
                )
                stat_html = (
                    '<span class="status-pending">'
                    'Pending</span>'
                    if is_pend else
                    '<span class="status-reviewed">'
                    'Reviewed</span>'
                )

                with st.expander(
                    f"{ri} {case['case_id']} — "
                    f"{case['patient_name']} "
                    f"({case['patient_age']}y) — "
                    f"{status} — {case['timestamp']}",
                    expanded=is_high and is_pend
                ):
                    c1,c2 = st.columns([1,1])

                    with c1:
                        st.markdown(f"""
                        <div class="card doctor-card">
                            <div class="section-label">
                                Patient
                            </div>
                            <div style="font-size:18px;
                                font-weight:800;
                                font-family:'Nunito',sans-serif;
                                color:#f0f4ff;
                                margin-bottom:4px;">
                                {case['patient_name']}
                                {stat_html}
                            </div>
                            <div style="font-size:13px;
                                color:#475569;
                                margin-bottom:12px;">
                                {case['patient_age']}y ·
                                {case['patient_gender']} ·
                                {case.get('patient_email','N/A')}
                            </div>
                            <div style="font-size:13px;
                                color:#64748b;
                                margin-bottom:4px;">
                                Symptoms: {case['symptoms']}
                            </div>
                            <div style="font-size:13px;
                                color:#64748b;">
                                Quality: {case['quality_score']}%
                                · {case['timestamp']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown("**AI Predictions**")
                        probs = case['probs']
                        for i,(name,p) in enumerate(
                            zip(DISEASE_NAMES,probs)
                        ):
                            if p > 0.3:
                                bar = ("🔴" if p>0.7
                                       else "🟡" if p>0.5
                                       else "🔵")
                                st.write(
                                    f"{bar} {name}: "
                                    f"{p*100:.1f}%"
                                )
                        st.markdown(f"""
                        <div style="margin-top:12px;">
                            <span class="risk-pill {risk_css}">
                                {risk_type_str} Risk
                            </span>
                        </div>
                        """, unsafe_allow_html=True)

                    with c2:
                        if os.path.exists(case['image_path']):
                            ic1,ic2 = st.columns(2)
                            ic1.image(
                                Image.open(
                                    case['image_path']),
                                caption="Retinal scan",
                                width='stretch'
                            )
                            if os.path.exists(
                                case['heatmap_path']
                            ):
                                ic2.image(
                                    Image.open(
                                        case['heatmap_path']),
                                    caption="AI heatmap",
                                    width='stretch'
                                )

                        st.markdown("**Your Assessment**")

                        already_reviewed = (
                            status == "Reviewed" and
                            not st.session_state.get(
                                f"edit_{case['case_id']}",
                                False)
                        )

                        if already_reviewed:
                            st.success(
                                f"Reviewed: "
                                f"{case.get('reviewed_at','')}"
                            )
                            st.write(
                                f"Diagnosis: "
                                f"{case['doctor_diagnosis']}"
                            )
                            st.write(
                                f"Treatment: "
                                f"{case['doctor_prescription']}"
                            )
                            st.write(
                                f"Referral: "
                                f"{case['doctor_referral']}"
                            )
                            if case['doctor_notes']:
                                st.write(
                                    f"Notes: "
                                    f"{case['doctor_notes']}"
                                )
                            if st.button(
                                "Edit",
                                key=f"edit_btn_"
                                    f"{case['case_id']}"
                            ):
                                st.session_state[
                                    f"edit_"
                                    f"{case['case_id']}"
                                ] = True
                                st.rerun()
                        else:
                            diag = st.text_area(
                                "Diagnosis",
                                placeholder="e.g. Moderate "
                                "Non-Proliferative DR",
                                key=f"diag_{case['case_id']}"
                            )
                            pres = st.text_area(
                                "Treatment Plan",
                                placeholder="e.g. Lucentis "
                                "0.5mg, follow up 4 weeks",
                                key=f"pres_{case['case_id']}"
                            )
                            ref = st.selectbox(
                                "Referral",
                                ["No referral needed",
                                 "Follow-up in 1 month",
                                 "Follow-up in 3 months",
                                 "Urgent — within 1 week",
                                 "Emergency — immediate"],
                                key=f"ref_{case['case_id']}"
                            )
                            notes = st.text_area(
                                "Notes",
                                placeholder="Additional "
                                "observations",
                                key=f"notes_{case['case_id']}"
                            )
                            st.write("")
                            if st.button(
                                "✅  Submit Review",
                                type="primary",
                                key=f"sub_{case['case_id']}",
                                use_container_width=True
                            ):
                                if diag:
                                    update_case(
                                        case['case_id'],
                                        diag,pres,ref,notes
                                    )
                                    st.success("Review saved!")
                                    st.session_state[
                                        f"edit_"
                                        f"{case['case_id']}"
                                    ] = False
                                    st.rerun()
                                else:
                                    st.error(
                                        "Please enter a "
                                        "diagnosis"
                                    )
                st.write("")