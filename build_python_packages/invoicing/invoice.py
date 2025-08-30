from pathlib import Path
import glob
import pandas as pd
from fpdf import FPDF


def generate(
    input_dir: str,
    output_dir: str,
    product_id_col: str,
    product_name_col: str,
    amount_purchased_col: str,
    price_per_unit_col: str,
    total_price_col: str,
):
    """This function converts Excel invoices files into PDF files."""
    filepaths = glob.glob(f"{input_dir}/*.xlsx")

    for filepath in filepaths:
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()
        filename = Path(filepath).stem
        invoice_number, invoice_date = filename.split("-")

        pdf.set_font(family="Times", size=20, style="B")
        pdf.set_text_color(0, 0, 0)
        pdf.cell(w=0, h=20, txt=f"Invoice no.{invoice_number}", ln=1)

        pdf.set_font(family="Times", size=12, style="I")
        pdf.set_text_color(150, 150, 150)
        pdf.cell(w=0, h=12, txt=f"Date: {invoice_date}", ln=1)

        df = pd.read_excel(filepath, sheet_name="Sheet 1")

        columns = [col.replace("_", " ").capitalize() for col in df.columns]
        pdf.set_font(family="Times", size=10, style="B")
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=10, txt=columns[0], border=1)
        pdf.cell(w=60, h=10, txt=columns[1], border=1)
        pdf.cell(w=40, h=10, txt=columns[2], border=1)
        pdf.cell(w=30, h=10, txt=columns[3], border=1)
        pdf.cell(w=30, h=10, txt=columns[4], border=1, ln=1)

        for _, row in df.iterrows():
            pdf.set_font(family="Times", size=10)
            pdf.set_text_color(120, 120, 120)
            pdf.cell(w=30, h=10, txt=str(row[product_id_col]), border=1)
            pdf.cell(w=60, h=10, txt=row[product_name_col], border=1)
            pdf.cell(w=40, h=10, txt=str(row[amount_purchased_col]), border=1)
            pdf.cell(w=30, h=10, txt=str(row[price_per_unit_col]), border=1)
            pdf.cell(w=30, h=10, txt=str(row[total_price_col]), border=1, ln=1)

        total_sum = df[total_price_col].sum()
        pdf.set_font(family="Times", size=10, style="B")
        pdf.set_text_color(100, 100, 100)
        pdf.cell(w=30, h=10, txt="", border=1)
        pdf.cell(w=60, h=10, txt="", border=1)
        pdf.cell(w=40, h=10, txt="", border=1)
        pdf.cell(w=30, h=10, txt="", border=1)
        pdf.cell(w=30, h=10, txt=str(total_sum), border=1, ln=1)

        pdf.set_font(family="Times", size=12)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(w=0, h=12, txt=f"Total price: {total_sum}", ln=1)

        pdf.set_font(family="Times", size=12, style="B")
        pdf.set_text_color(100, 100, 100)
        pdf.cell(w=30, h=12, txt="PythonHow")

        pdf.output(f"{output_dir}/{filename}.pdf")
