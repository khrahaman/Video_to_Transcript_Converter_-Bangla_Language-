# -*- coding: utf-8 -*-
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable
)

BASE = "D:/vid_to_audio/_work"

pdfmetrics.registerFont(TTFont("Nirmala", f"{BASE}/fonts/Nirmala-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Nirmala-Bold", f"{BASE}/fonts/Nirmala-Bold.ttf"))

styles = getSampleStyleSheet()

title_style = ParagraphStyle("TitleX", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=22, spaceAfter=6)
subtitle_style = ParagraphStyle("SubtitleX", parent=styles["Normal"], fontName="Helvetica", fontSize=12, alignment=TA_CENTER, textColor="#444444", spaceAfter=4)
disclaimer_style = ParagraphStyle("Disclaimer", parent=styles["Normal"], fontName="Helvetica-Oblique", fontSize=9.5, leading=14, textColor="#555555", spaceBefore=14, spaceAfter=4)

speech_heading = ParagraphStyle("SpeechHeading", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=16, spaceBefore=4, spaceAfter=2, textColor="#1a1a2e")
speech_meta = ParagraphStyle("SpeechMeta", parent=styles["Normal"], fontName="Helvetica", fontSize=9.5, textColor="#666666", spaceAfter=10)

section_label = ParagraphStyle("SectionLabel", parent=styles["Heading2"], fontName="Nirmala-Bold", fontSize=11.5, textColor="#8b0000", spaceBefore=10, spaceAfter=6)

bn_body = ParagraphStyle("BnBody", parent=styles["Normal"], fontName="Nirmala", fontSize=11, leading=18, spaceAfter=10, alignment=4)
en_body = ParagraphStyle("EnBody", parent=styles["Normal"], fontName="Helvetica", fontSize=10.5, leading=15, spaceAfter=8, alignment=4)
note_style = ParagraphStyle("Note", parent=styles["Normal"], fontName="Helvetica-Oblique", fontSize=9, leading=13, textColor="#777777", spaceAfter=8)

SPEECHES = [
    ("20260928_100728", "10:07 AM", "2 min 42 sec", "Opening Remarks"),
    ("20260928_101025", "10:10 AM", "14 min 6 sec", "Nutrition International: Programme Overview"),
    ("20260928_102437", "10:24 AM", "4 min 15 sec", "Adolescent Empowerment & Awareness"),
    ("20260928_103027", "10:30 AM", "57 min 46 sec", "District Data Review & Technical Discussion"),
    ("20260928_114807", "11:48 AM", "83 min 52 sec", "District Implementation & Extended Discussion (Jamalpur)"),
    ("20260928_131213", "1:12 PM", "37 min 58 sec", "National Policy, Fortification & Coordination"),
    ("20260928_135016", "1:50 PM", "4 min 47 sec", "Closing Remarks"),
]

def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read().strip()

def bn_paragraphs(text):
    flow = []
    for para in text.split("\n\n"):
        para = para.strip()
        if para:
            flow.append(Paragraph(para, bn_body))
    return flow

def en_paragraphs(text):
    flow = []
    for para in text.split("\n\n"):
        para = para.strip()
        if not para:
            continue
        if para.startswith("[Note:") or para.startswith("[Video"):
            flow.append(Paragraph(para, note_style))
        else:
            flow.append(Paragraph(para, en_body))
    return flow


def build_transcript_pdf():
    doc = SimpleDocTemplate(
        f"{BASE}/output/Combined_Transcripts_Bangla_English.pdf",
        pagesize=A4,
        topMargin=2.2*cm, bottomMargin=2.2*cm, leftMargin=2.2*cm, rightMargin=2.2*cm,
    )
    story = []
    story.append(Spacer(1, 4*cm))
    story.append(Paragraph("Adolescent Nutrition Programme", title_style))
    story.append(Paragraph("Review Meeting — Combined Transcripts", title_style))
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph("28 September 2026 &nbsp;|&nbsp; Bangla original with English translation", subtitle_style))
    story.append(Paragraph(
        "This document was produced by automatic speech-to-text transcription (faster-whisper, "
        "large-v3 model) of audio recorded on-site, followed by translation. The speaker's accent, "
        "audio quality, and heavy code-switching between Bangla and English made parts of the source "
        "audio difficult for the model to capture accurately; the Bangla text below reflects the "
        "transcription as produced, including its imperfections, and the English translation renders "
        "the discernible meaning as faithfully as possible. Speech titles are descriptive labels "
        "inferred from content, not official session titles.",
        disclaimer_style
    ))
    story.append(PageBreak())

    for idx, (fname, time_str, dur_str, title) in enumerate(SPEECHES, start=1):
        bn_text = read(f"{BASE}/cleaned/{fname}.txt")
        en_text = read(f"{BASE}/english/{fname}.txt")

        story.append(Paragraph(f"Speech {idx}: {title}", speech_heading))
        story.append(Paragraph(f"Recorded {time_str} &nbsp;&middot;&nbsp; Duration {dur_str} &nbsp;&middot;&nbsp; File {fname}.mp4", speech_meta))
        story.append(HRFlowable(width="100%", thickness=0.7, color="#cccccc", spaceAfter=8))

        story.append(Paragraph("মূল বাংলা অনুলিপি &nbsp;(Original Bangla Transcript)", section_label))
        story.extend(bn_paragraphs(bn_text))

        story.append(Spacer(1, 0.3*cm))
        story.append(Paragraph("English Translation", section_label))
        story.extend(en_paragraphs(en_text))

        if idx < len(SPEECHES):
            story.append(PageBreak())

    doc.build(story)
    print("Built Combined_Transcripts_Bangla_English.pdf")


def build_summary_pdf():
    doc = SimpleDocTemplate(
        f"{BASE}/output/Speech_Summaries_Bangla_English.pdf",
        pagesize=A4,
        topMargin=2.2*cm, bottomMargin=2.2*cm, leftMargin=2.2*cm, rightMargin=2.2*cm,
    )
    story = []
    story.append(Spacer(1, 4*cm))
    story.append(Paragraph("Adolescent Nutrition Programme", title_style))
    story.append(Paragraph("Review Meeting — Speech Summaries", title_style))
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph("28 September 2026 &nbsp;|&nbsp; Bangla and English summaries of each speech", subtitle_style))
    story.append(Paragraph(
        "Summaries are based on automatic transcription of on-site audio recordings; source audio quality "
        "and accent made some portions difficult to capture precisely, so figures and names should be "
        "treated as indicative. See the companion \u201cCombined Transcripts\u201d document for the full "
        "bilingual transcripts.",
        disclaimer_style
    ))
    story.append(PageBreak())

    for idx, (fname, time_str, dur_str, title) in enumerate(SPEECHES, start=1):
        bn_sum = read(f"{BASE}/summary_bn/{fname}.txt")
        en_sum = read(f"{BASE}/summary_en/{fname}.txt")

        story.append(Paragraph(f"Speech {idx}: {title}", speech_heading))
        story.append(Paragraph(f"Recorded {time_str} &nbsp;&middot;&nbsp; Duration {dur_str}", speech_meta))
        story.append(HRFlowable(width="100%", thickness=0.7, color="#cccccc", spaceAfter=8))

        story.append(Paragraph("সারসংক্ষেপ (বাংলা)", section_label))
        story.append(Paragraph(bn_sum, bn_body))

        story.append(Spacer(1, 0.2*cm))
        story.append(Paragraph("Summary (English)", section_label))
        story.append(Paragraph(en_sum, en_body))

        if idx < len(SPEECHES):
            story.append(Spacer(1, 0.6*cm))
            story.append(HRFlowable(width="100%", thickness=1.2, color="#1a1a2e", spaceAfter=14))

    doc.build(story)
    print("Built Speech_Summaries_Bangla_English.pdf")


if __name__ == "__main__":
    os.makedirs(f"{BASE}/output", exist_ok=True)
    build_transcript_pdf()
    build_summary_pdf()
