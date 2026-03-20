import json
import os
from datetime import datetime

DB_FILE = "cases.json"

def load_cases():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_case(
    patient_name, patient_age, patient_gender,
    symptoms, quality_score, probs,
    detected_conditions, risk_level,
    image_path, heatmap_path,
    patient_email=""
):
    cases   = load_cases()
    case_id = f"CASE-{len(cases)+1:04d}"
    case    = {
        "case_id":             case_id,
        "timestamp":           datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "status":              "Pending",
        "patient_name":        patient_name,
        "patient_age":         int(patient_age),
        "patient_gender":      patient_gender,
        "symptoms":            symptoms,
        "quality_score":       int(quality_score),
        "probs":               probs.tolist(),
        "detected_conditions": [(n, float(p))
                                for n, p in detected_conditions],
        "risk_level":          risk_level,
        "image_path":          image_path,
        "heatmap_path":        heatmap_path,
        "patient_email":       patient_email,
        "doctor_diagnosis":    "",
        "doctor_prescription": "",
        "doctor_referral":     "",
        "doctor_notes":        "",
        "reviewed_at":         ""
    }
    cases.append(case)
    with open(DB_FILE, 'w') as f:
        json.dump(cases, f, indent=2)
    return case_id

def update_case(case_id, diagnosis, prescription, referral, notes):
    cases = load_cases()
    for case in cases:
        if case["case_id"] == case_id:
            case["doctor_diagnosis"]    = diagnosis
            case["doctor_prescription"] = prescription
            case["doctor_referral"]     = referral
            case["doctor_notes"]        = notes
            case["status"]              = "Reviewed"
            case["reviewed_at"]         = datetime.now().strftime(
                "%d %b %Y, %I:%M %p"
            )
            break
    with open(DB_FILE, 'w') as f:
        json.dump(cases, f, indent=2)