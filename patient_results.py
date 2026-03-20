import streamlit as st
from database import load_cases
from PIL import Image
import os

st.set_page_config(
    page_title="Patient Results",
    page_icon="👁",
    layout="centered"
)

DISEASE_NAMES = [
    'Normal', 'Diabetic Retinopathy', 'Glaucoma',
    'Cataract', 'AMD', 'Hypertension', 'Myopia', 'Other'
]

# ── Header ─────────────────────────────────────────────────────
st.title("👁 Your Screening Results")
st.caption("Enter your Case ID to view your results and doctor's feedback")
st.divider()

# ── Case ID lookup ─────────────────────────────────────────────
case_id_input = st.text_input(
    "Enter your Case ID",
    placeholder="e.g. CASE-0001"
).strip().upper()

if not case_id_input:
    st.info("Your Case ID was shown after you submitted your screening. Enter it above to view results.")
    st.stop()

# ── Find case ──────────────────────────────────────────────────
cases  = load_cases()
case   = next((c for c in cases
               if c['case_id'] == case_id_input), None)

if not case:
    st.error(f"No case found with ID {case_id_input} — please check and try again.")
    st.stop()

# ── Case found ─────────────────────────────────────────────────
st.success(f"Case found — {case['patient_name']}")
st.divider()

# ── Status banner ──────────────────────────────────────────────
status = case['status']
if status == "Reviewed":
    st.success("✅ Your case has been reviewed by a specialist")
else:
    st.warning("⏳ Your case is pending specialist review — please check back later")

# ── Patient summary ────────────────────────────────────────────
st.subheader("Screening Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Patient", case['patient_name'])
col2.metric("Age", f"{case['patient_age']} years")
col3.metric("Screened on", case['timestamp'])

col1, col2 = st.columns(2)
col1.metric("Image Quality", f"{case['quality_score']}%")
col2.metric("Reported Symptoms", case['symptoms']
            if case['symptoms'] != "Not specified"
            else "None reported")

st.divider()

# ── Retinal images ─────────────────────────────────────────────
st.subheader("Your Retinal Images")
col1, col2 = st.columns(2)
if os.path.exists(case['image_path']):
    col1.image(
        Image.open(case['image_path']),
        caption="Retinal scan", use_container_width=True
    )
if os.path.exists(case['heatmap_path']):
    col2.image(
        Image.open(case['heatmap_path']),
        caption="AI analysis map", use_container_width=True
    )

st.divider()

# ── AI screening results ───────────────────────────────────────
st.subheader("AI Screening Results")
st.caption("These are preliminary AI findings — confirmed by your doctor below")

probs = case['probs']
for i, (name, prob) in enumerate(zip(DISEASE_NAMES, probs)):
    if prob > 0.3:
        col1, col2 = st.columns([3, 1])
        col1.progress(float(prob), text=name)
        if prob > 0.7:
            col2.error(f"{prob*100:.0f}%")
        elif prob > 0.5:
            col2.warning(f"{prob*100:.0f}%")
        else:
            col2.info(f"{prob*100:.0f}%")

# Overall risk
risk = case['risk_level']
st.divider()
if "High" in risk:
    st.error(f"AI Risk Assessment: {risk}")
elif "Moderate" in risk:
    st.warning(f"AI Risk Assessment: {risk}")
else:
    st.success(f"AI Risk Assessment: {risk}")

st.divider()

# ── Doctor's response ──────────────────────────────────────────
st.subheader("Doctor's Assessment")

if status != "Reviewed":
    st.info("Your doctor has not yet reviewed your case. Please check back in 24 hours.")
else:
    st.success(f"Reviewed on: {case.get('reviewed_at', '')}")
    st.divider()

    # Diagnosis
    col1, col2 = st.columns([1, 3])
    col1.markdown("**Diagnosis**")
    col2.info(case['doctor_diagnosis'])

    # Prescription
    col1, col2 = st.columns([1, 3])
    col1.markdown("**Treatment Plan**")
    col2.info(case['doctor_prescription']
              if case['doctor_prescription']
              else "No specific prescription given")

    # Referral
    col1, col2 = st.columns([1, 3])
    col1.markdown("**Referral Decision**")
    referral = case['doctor_referral']
    if "Emergency" in referral or "Urgent" in referral:
        col2.error(referral)
    elif "month" in referral:
        col2.warning(referral)
    else:
        col2.success(referral)

    # Notes
    if case['doctor_notes']:
        col1, col2 = st.columns([1, 3])
        col1.markdown("**Doctor's Notes**")
        col2.info(case['doctor_notes'])

    st.divider()

    # ── What to do next ────────────────────────────────────────
    st.subheader("What to do next")
    if "Emergency" in referral:
        st.error(
            "Your doctor has flagged this as urgent. "
            "Please visit a hospital immediately."
        )
    elif "Urgent" in referral:
        st.warning(
            "Please visit an eye specialist within the next 7 days. "
            "Bring this report with you."
        )
    elif "month" in referral:
        st.info(
            "Please schedule a follow-up appointment as recommended. "
            "Download your report below to share with your doctor."
        )
    else:
        st.success(
            "No immediate action required. "
            "Continue regular eye check-ups as advised."
        )

st.divider()
st.info(
    "This report is generated by an AI screening system. "
    "Always follow your doctor's advice for treatment decisions."
)