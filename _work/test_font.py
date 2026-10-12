from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

pdfmetrics.registerFont(TTFont("Nirmala", "D:/vid_to_audio/_work/fonts/Nirmala-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Nirmala-Bold", "D:/vid_to_audio/_work/fonts/Nirmala-Bold.ttf"))

styles = getSampleStyleSheet()
bn_style = ParagraphStyle("bn", parent=styles["Normal"], fontName="Nirmala", fontSize=12, leading=18)

doc = SimpleDocTemplate("D:/vid_to_audio/_work/font_test.pdf", pagesize=A4)
text = "এপন কি সহাজুকিতার মাস্ববে তারা বিদ্যানার কর্যে সাস্তকর হাক্তাক্ষন নয়েনে উষ্টিশিক্ষা, আজন, উজ্যতা, BMI"
story = [Paragraph(text, bn_style)]
doc.build(story)
print("built font_test.pdf")
