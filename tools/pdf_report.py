from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from datetime import datetime
import re


def parse_markdown_table(lines):
    table_data = []
    for line in lines:
        if "|" in line:
            row = [cell.strip() for cell in line.split("|") if cell.strip()]
            table_data.append(row)
    return table_data


def generate_pdf_report(summary_text):

    file_name = "store_manager_report.pdf"

    styles = getSampleStyleSheet()

    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        spaceAfter=12,
        spaceBefore=12,
        fontSize=14,
        leading=16
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=10,
        leading=14
    )

    bullet_style = ParagraphStyle(
        "Bullet",
        parent=styles["BodyText"],
        leftIndent=15
    )

    elements = []

    # Title
    elements.append(Paragraph("AI Ecommerce Business Performance Report", styles["Title"]))
    elements.append(Spacer(1, 10))

    # Date
    date = datetime.now().strftime("%Y-%m-%d")
    elements.append(Paragraph(f"<b>Date:</b> {date}", body_style))
    elements.append(Spacer(1, 20))

    lines = summary_text.split("\n")

    table_buffer = []

    for line in lines:

        line = line.strip()

        if "|" in line:
            table_buffer.append(line)
            continue
        else:
            if table_buffer:
                table_data = parse_markdown_table(table_buffer)

                table = Table(table_data, hAlign="LEFT")

                table.setStyle(TableStyle([
                    ("BACKGROUND", (0,0), (-1,0), colors.grey),
                    ("TEXTCOLOR",(0,0),(-1,0),colors.whitesmoke),
                    ("GRID", (0,0), (-1,-1), 1, colors.grey),
                    ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
                    ("ALIGN",(1,1),(-1,-1),"CENTER")
                ]))

                elements.append(table)
                elements.append(Spacer(1,15))
                table_buffer = []

        # headings
        if line.startswith("###") or line.startswith("##"):
            clean = re.sub("#","",line)
            elements.append(Paragraph(f"<b>{clean}</b>", heading_style))

        # bullets
        elif line.startswith("-"):
            elements.append(Paragraph(f"• {line[1:].strip()}", bullet_style))

        elif line == "" or line == "--":
            elements.append(Spacer(1,10))

        else:
            elements.append(Paragraph(line, body_style))

    doc = SimpleDocTemplate(
        file_name,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        topMargin=60,
        bottomMargin=50
    )

    doc.build(elements)

    return file_name