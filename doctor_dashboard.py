import streamlit as st
from database import load_cases, update_case
from auth import register_doctor, login_doctor
from PIL import Image
import os

st.set_page_config(
    page_title="Doctor Dashboard",
    page_icon="🏥",
    layout="wide"
)

DISEASE_NAMES = [
    'Normal', 'Diabetic Retinopathy', 'Glaucoma',
    'Cataract', 'AMD', 'Hypertension', 'Myopia', 'Other'
]

if 'doctor_logged_in' not in st.session_state:
    st.session_state['doctor_logged_in'] = False
if 'doctor_user' not in st.session_state:
    st.session_state['doctor_user'] = None

# ══════════════════════════════════════════════════════════════
# NOT LOGGED IN
# ══════════════════════════════════════════════════════════════
if not st.session_state['doctor_logged_in']:

    st.title("🏥 Doctor Portal")
    st.caption("AI-Augmented Tele-Ophthalmology Review System")
    st.divider()

    auth_tab1, auth_tab2 = st.tabs(["Login", "Register"])

    with auth_tab1:
        st.subheader("Doctor Login")
        email    = st.text_input("Email", key="doc_login_email")
        password = st.text_input("Password", type="password",
                                  key="doc_login_pass")
        if st.button("Login", type="primary", key="doc_login_btn"):
            if email and password:
                success, user, msg = login_doctor(email, password)
                if success:
                    st.session_state['doctor_logged_in'] = True
                    st.session_state['doctor_user']      = user
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.error("Please enter email and password")

    with auth_tab2:
        st.subheader("Doctor Registration")
        col1, col2 = st.columns(2)
        doc_name = col1.text_input("Full Name",         key="doc_name")
        doc_spec = col2.text_input(
            "Specialization",
            placeholder="e.g. Ophthalmologist",
            key="doc_spec"
        )
        col1, col2 = st.columns(2)
        doc_hosp  = col1.text_input("Hospital / Clinic", key="doc_hosp")
        doc_lic   = col2.text_input("License Number",    key="doc_lic")
        doc_email = st.text_input("Email",               key="doc_email")
        col1, col2 = st.columns(2)
        doc_pass  = col1.text_input("Password", type="password",
                                     key="doc_pass")
        doc_pass2 = col2.text_input("Confirm Password", type="password",
                                     key="doc_pass2")

        if st.button("Register", type="primary", key="doc_reg_btn"):
            if not all([doc_name, doc_spec, doc_hosp,
                        doc_lic, doc_email, doc_pass]):
                st.error("Please fill in all fields")
            elif doc_pass != doc_pass2:
                st.error("Passwords do not match")
            elif len(doc_pass) < 6:
                st.error("Password must be at least 6 characters")
            else:
                success, msg = register_doctor(
                    doc_name, doc_spec, doc_hosp,
                    doc_lic, doc_email, doc_pass
                )
                if success:
                    st.success("Registered successfully! Please login.")
                else:
                    st.error(msg)

# ══════════════════════════════════════════════════════════════
# LOGGED IN
# ══════════════════════════════════════════════════════════════
else:
    doc = st.session_state['doctor_user']

    col1, col2 = st.columns([4, 1])
    col1.title("🏥 Ophthalmologist Dashboard")
    col1.caption(
        f"Dr. {doc['name']} — {doc['specialization']} — "
        f"{doc['hospital']}"
    )
    if col2.button("Logout"):
        st.session_state['doctor_logged_in'] = False
        st.session_state['doctor_user']      = None
        st.rerun()

    st.divider()

    cases = load_cases()

    if not cases:
        st.info("No patient cases yet.")
        st.stop()

    # Summary metrics
    total    = len(cases)
    pending  = sum(1 for c in cases if c['status'] == 'Pending')
    reviewed = sum(1 for c in cases if c['status'] == 'Reviewed')
    high     = sum(1 for c in cases if 'High' in c['risk_level'])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Cases",    total)
    col2.metric("Pending Review", pending,
                delta=f"{pending} to review",
                delta_color="inverse")
    col3.metric("Reviewed",       reviewed)
    col4.metric("High Risk",      high,
                delta="urgent" if high > 0 else "none",
                delta_color="inverse" if high > 0 else "off")

    st.divider()

    # Filter
    col1, col2 = st.columns([2, 4])
    status_filter = col1.selectbox(
        "Filter by status",
        ["All", "Pending", "Reviewed"]
    )
    search = col2.text_input(
        "Search by patient name",
        placeholder="Type name..."
    )

    filtered = cases
    if status_filter != "All":
        filtered = [c for c in filtered
                    if c['status'] == status_filter]
    if search:
        filtered = [c for c in filtered
                    if search.lower() in c['patient_name'].lower()]

    filtered = sorted(
        filtered,
        key=lambda c: (
            0 if c['status'] == 'Pending' else 1,
            0 if 'High' in c['risk_level'] else 1
        )
    )

    st.write(f"Showing {len(filtered)} cases")
    st.divider()

    # Case list
    for case in filtered:
        risk       = case['risk_level']
        status     = case['status']
        is_high    = 'High' in risk
        is_pending = status == 'Pending'

        with st.expander(
            f"{'🔴' if is_high else '🟡' if is_pending else '🟢'} "
            f"{case['case_id']} — {case['patient_name']} "
            f"({case['patient_age']}y, {case['patient_gender']}) — "
            f"{status} — {case['timestamp']}",
            expanded=is_high and is_pending
        ):
            col1, col2 = st.columns([1, 1])

            with col1:
                st.markdown("**Patient Information**")
                st.write(f"Name:      {case['patient_name']}")
                st.write(f"Age:       {case['patient_age']} | "
                         f"Gender: {case['patient_gender']}")
                st.write(f"Email:     {case.get('patient_email','N/A')}")
                st.write(f"Symptoms:  {case['symptoms']}")
                st.write(f"Quality:   {case['quality_score']}%")
                st.write(f"Submitted: {case['timestamp']}")

                st.markdown("**AI Screening Results**")
                probs = case['probs']
                for i, (name, prob) in enumerate(
                    zip(DISEASE_NAMES, probs)
                ):
                    if prob > 0.3:
                        bar = "🔴" if prob > 0.7 \
                              else "🟡" if prob > 0.5 else "🔵"
                        st.write(f"{bar} {name}: {prob*100:.1f}%")

                if is_high:
                    st.error(f"Risk: {risk}")
                elif 'Moderate' in risk:
                    st.warning(f"Risk: {risk}")
                else:
                    st.success(f"Risk: {risk}")

                if case['detected_conditions']:
                    st.markdown("**Flagged Conditions**")
                    for name, prob in sorted(
                        case['detected_conditions'],
                        key=lambda x: x[1], reverse=True
                    ):
                        st.write(f"• {name}: {prob*100:.1f}%")

            with col2:
                if os.path.exists(case['image_path']):
                    st.markdown("**Retinal Images**")
                    img_col1, img_col2 = st.columns(2)
                    img_col1.image(
                        Image.open(case['image_path']),
                        caption="Original",
                        width='stretch'
                    )
                    if os.path.exists(case['heatmap_path']):
                        img_col2.image(
                            Image.open(case['heatmap_path']),
                            caption="AI Heatmap",
                            width='stretch'
                        )

                st.markdown("**Doctor's Assessment**")

                if status == "Reviewed" and not st.session_state.get(
                    f"editing_{case['case_id']}", False
                ):
                    st.success(
                        f"Reviewed: {case.get('reviewed_at','')}"
                    )
                    st.write(f"Diagnosis:    {case['doctor_diagnosis']}")
                    st.write(f"Prescription: {case['doctor_prescription']}")
                    st.write(f"Referral:     {case['doctor_referral']}")
                    st.write(f"Notes:        {case['doctor_notes']}")
                    if st.button("Edit Review",
                                 key=f"edit_{case['case_id']}"):
                        st.session_state[
                            f"editing_{case['case_id']}"
                        ] = True
                        st.rerun()
                else:
                    diagnosis = st.text_area(
                        "Diagnosis",
                        placeholder="e.g. Moderate Non-Proliferative "
                                    "Diabetic Retinopathy",
                        key=f"diag_{case['case_id']}"
                    )
                    prescription = st.text_area(
                        "Prescription / Treatment Plan",
                        placeholder="e.g. Lucentis 0.5mg intravitreal "
                                    "injection, follow up in 4 weeks",
                        key=f"pres_{case['case_id']}"
                    )
                    referral = st.selectbox(
                        "Referral Decision",
                        [
                            "No referral needed",
                            "Follow-up in 1 month",
                            "Follow-up in 3 months",
                            "Urgent referral — visit within 1 week",
                            "Emergency — immediate hospital visit required"
                        ],
                        key=f"ref_{case['case_id']}"
                    )
                    notes = st.text_area(
                        "Additional Notes",
                        placeholder="Any additional observations",
                        key=f"notes_{case['case_id']}"
                    )

                    if st.button(
                        "✅ Submit Review",
                        key=f"submit_{case['case_id']}",
                        type="primary"
                    ):
                        if diagnosis:
                            update_case(
                                case['case_id'],
                                diagnosis, prescription,
                                referral, notes
                            )
                            st.success("Review saved successfully!")
                            st.session_state[
                                f"editing_{case['case_id']}"
                            ] = False
                            st.rerun()
                        else:
                            st.error(
                                "Please enter a diagnosis "
                                "before submitting"
                            )

        st.write("")