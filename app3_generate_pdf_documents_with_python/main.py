from fpdf import FPDF
import pandas as pd

pdf = FPDF(orientation="portrait", unit="mm", format="A4")
pdf.set_auto_page_break(auto=False, margin=0)

df = pd.read_csv("topics.csv")

current_page = 1

for i, row in df.iterrows():

    pdf.add_page()

    # Set the header
    pdf.set_font(family="Times", style="B", size=24)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(w=0, h=24, txt=row["Topic"], align="L", ln=1)

    pdf.set_draw_color(200, 200, 200)
    for y in range(32, 280, 10):
        pdf.line(10, y, 200, y)

    # Set the footer
    pdf.ln(250)
    pdf.set_font(family="Times", style="I", size=8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(w=0, h=10, txt=str(current_page), align="L")
    pdf.cell(w=0, h=10, txt=row["Topic"], align="R")

    for j in range(row["Pages"] - 1):
        pdf.add_page()
        # Set the footer
        pdf.ln(272)
        pdf.set_font(family="Times", style="I", size=8)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(w=0, h=10, txt=str(current_page + j + 1), align="L")
        pdf.cell(w=0, h=10, txt=row["Topic"], align="R")
        pdf.set_draw_color(200, 200, 200)
        for y in range(16, 280, 10):
            pdf.line(10, y, 200, y)

    current_page += row["Pages"]

pdf.output("output.pdf")
