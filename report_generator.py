from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image,
    Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
import io
import os

DISEASE_NAMES = [
    'Normal', 'Diabetic Retinopathy', 'Glaucoma',
    'Cataract', 'AMD', 'Hypertension', 'Myopia', 'Other'
]
DISEASE_COLORS = [
    '#2ecc71', '#e74c3c', '#e67e22', '#3498db',
    '#9b59b6', '#f39c12', '#1abc9c', '#95a5a6'
]

def generate_report(
    patient_name, patient_age, patient_gender,
    symptoms, quality_score, quality_tips,
    probs, detected_conditions, risk_level,
    original_image_pil, heatmap_array,
    output_path="screening_report.pdf"
):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()

    # ── Custom styles ──────────────────────────────────────────
    title_style = ParagraphStyle(
        'Title', parent=styles['Normal'],
        fontSize=22, fontName='Helvetica-Bold',
        textColor=colors.HexColor('#1F4E79'),
        alignment=TA_CENTER, spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'Subtitle', parent=styles['Normal'],
        fontSize=11, fontName='Helvetica',
        textColor=colors.HexColor('#2E75B6'),
        alignment=TA_CENTER, spaceAfter=2
    )
    section_style = ParagraphStyle(
        'Section', parent=styles['Normal'],
        fontSize=13, fontName='Helvetica-Bold',
        textColor=colors.HexColor('#1F4E79'),
        spaceBefore=14, spaceAfter=6,
        borderPad=4
    )
    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'],
        fontSize=10, fontName='Helvetica',
        textColor=colors.HexColor('#333333'),
        spaceAfter=4, leading=14
    )
    small_style = ParagraphStyle(
        'Small', parent=styles['Normal'],
        fontSize=8, fontName='Helvetica',
        textColor=colors.HexColor('#888888'),
        alignment=TA_CENTER
    )

    story = []

    # ── Header ─────────────────────────────────────────────────
    story.append(Paragraph("AI Tele-Ophthalmology", title_style))
    story.append(Paragraph("Retinal Screening Report", title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Powered by EfficientNet-B0 trained on ODIR-5K — 8 Disease Screening", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2,
                             color=colors.HexColor('#1F4E79'), spaceAfter=12))

    # ── Patient info table ─────────────────────────────────────
    story.append(Paragraph("Patient Information", section_style))
    now = datetime.now().strftime("%d %B %Y, %I:%M %p")
    patient_data = [
        ["Patient Name", patient_name,
         "Date & Time", now],
        ["Age", f"{patient_age} years",
         "Gender", patient_gender],
        ["Reported Symptoms", symptoms,
         "Image Quality", f"{quality_score}%"],
    ]
    patient_table = Table(patient_data, colWidths=[3.5*cm, 6*cm, 3.5*cm, 4*cm])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EBF3FB')),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#F7FBFF')),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor('#EBF3FB')),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (2,0), (2,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor('#1F4E79')),
        ('TEXTCOLOR', (2,0), (2,-1), colors.HexColor('#1F4E79')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(patient_table)
    story.append(Spacer(1, 12))

    # ── Quality tips ───────────────────────────────────────────
    if quality_tips:
        story.append(Paragraph("Image Quality Notes", section_style))
        for tip in quality_tips:
            story.append(Paragraph(f"• {tip}", body_style))
        story.append(Spacer(1, 8))

    # ── Images side by side ────────────────────────────────────
    story.append(Paragraph("Retinal Images", section_style))

    # Save original image to buffer
    orig_buf = io.BytesIO()
    original_image_pil.resize((300, 300)).save(orig_buf, format='PNG')
    orig_buf.seek(0)

    # Save heatmap to buffer
    heat_buf = io.BytesIO()
    heat_img = plt.cm.jet(heatmap_array / 255.0) if heatmap_array.ndim == 2 \
               else heatmap_array
    plt.imsave(heat_buf, heatmap_array.astype(np.uint8), format='png')
    heat_buf.seek(0)

    img_orig = Image(orig_buf, width=7*cm, height=7*cm)
    img_heat = Image(heat_buf, width=7*cm, height=7*cm)

    img_table = Table(
        [[img_orig, img_heat],
         [Paragraph("Original Retinal Image", small_style),
          Paragraph("AI Attention Heatmap\n(Red = areas of concern)", small_style)]],
        colWidths=[8.5*cm, 8.5*cm]
    )
    img_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (0,1), 0.5, colors.HexColor('#CCCCCC')),
        ('BOX', (1,0), (1,1), 0.5, colors.HexColor('#CCCCCC')),
    ]))
    story.append(img_table)
    story.append(Spacer(1, 12))

    # ── AI predictions chart ───────────────────────────────────
    story.append(Paragraph("AI Screening Results", section_style))

    fig, ax = plt.subplots(figsize=(7, 3.5))
    bars = ax.barh(DISEASE_NAMES, [p * 100 for p in probs],
                   color=DISEASE_COLORS, edgecolor='none', height=0.6)
    ax.set_xlabel("Confidence (%)", fontsize=9)
    ax.set_xlim(0, 100)
    ax.axvline(x=50, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)
    for bar, prob in zip(bars, probs):
        ax.text(bar.get_width() + 1,
                bar.get_y() + bar.get_height() / 2,
                f'{prob*100:.1f}%', va='center', fontsize=8)
    ax.set_title("Multi-Disease Probability — 50% threshold line shown",
                 fontsize=9, color='#444444')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()

    chart_buf = io.BytesIO()
    plt.savefig(chart_buf, format='png', dpi=150, bbox_inches='tight')
    plt.close()
    chart_buf.seek(0)

    chart_img = Image(chart_buf, width=17*cm, height=8*cm)
    story.append(chart_img)
    story.append(Spacer(1, 12))

    # ── Detected conditions ────────────────────────────────────
    story.append(Paragraph("Detected Conditions", section_style))

    if detected_conditions:
        cond_data = [["Condition", "Confidence", "Severity"]]
        for name, prob in sorted(detected_conditions,
                                  key=lambda x: x[1], reverse=True):
            severity = "High Risk" if prob > 0.7 else "Moderate Risk"
            sev_color = colors.HexColor('#C00000') if prob > 0.7 \
                        else colors.HexColor('#9C5700')
            cond_data.append([name, f"{prob*100:.1f}%", severity])

        cond_table = Table(cond_data,
                           colWidths=[8*cm, 4*cm, 5*cm])
        style_cmds = [
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1F4E79')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
            ('PADDING', (0,0), (-1,-1), 7),
            ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ]
        for i, (name, prob) in enumerate(
            sorted(detected_conditions, key=lambda x: x[1], reverse=True), 1
        ):
            bg = colors.HexColor('#FFF0F0') if prob > 0.7 \
                 else colors.HexColor('#FFFBE6')
            style_cmds.append(('BACKGROUND', (0,i), (-1,i), bg))

        cond_table.setStyle(TableStyle(style_cmds))
        story.append(cond_table)
    else:
        story.append(Paragraph("No conditions detected above 50% threshold.", body_style))

    story.append(Spacer(1, 12))

    # ── Risk assessment box ────────────────────────────────────
    story.append(Paragraph("Overall Risk Assessment", section_style))

    risk_color = '#C00000' if 'High' in risk_level \
                 else '#9C5700' if 'Moderate' in risk_level \
                 else '#1D6F42'
    risk_bg = '#FFF0F0' if 'High' in risk_level \
              else '#FFFBE6' if 'Moderate' in risk_level \
              else '#F0FFF4'

    risk_style = ParagraphStyle(
        'Risk', parent=styles['Normal'],
        fontSize=12, fontName='Helvetica-Bold',
        textColor=colors.HexColor(risk_color),
        alignment=TA_CENTER, leading=18
    )
    risk_table = Table(
        [[Paragraph(risk_level, risk_style)]],
        colWidths=[17*cm]
    )
    risk_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(risk_bg)),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor(risk_color)),
        ('PADDING', (0,0), (-1,-1), 14),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(risk_table)
    story.append(Spacer(1, 16))

    # ── Disclaimer ─────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=1,
                             color=colors.HexColor('#CCCCCC'), spaceAfter=8))
    disclaimer = (
        "DISCLAIMER: This report is generated by an AI screening system trained on the ODIR-5K "
        "dataset and is intended for preliminary screening purposes only. It does NOT constitute "
        "a medical diagnosis. All findings must be reviewed and confirmed by a qualified "
        "ophthalmologist before any clinical decisions are made. In case of high-risk findings, "
        "please refer the patient to a specialist immediately."
    )
    story.append(Paragraph(disclaimer, small_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "AI Tele-Ophthalmology Screening Platform | EfficientNet-B0 | ODIR-5K Dataset",
        small_style
    ))

    doc.build(story)
    return output_path