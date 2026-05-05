from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import pandas as pd
import json
import os

# -----------------------------
# Load Data
# -----------------------------
expr_df = pd.read_csv("data/mock_expression.csv")

with open("data/gene_info.json", "r") as f:
    gene_info = json.load(f)

# -----------------------------
# Select Gene
# -----------------------------
gene = "ERBB2"
row = expr_df[expr_df["gene"] == gene].iloc[0]
meta = gene_info[gene]

# -----------------------------
# Output Path
# -----------------------------
os.makedirs("reports", exist_ok=True)
output_path = "reports/sample_gene_report.pdf"

# -----------------------------
# PDF Setup
# -----------------------------
c = canvas.Canvas(output_path, pagesize=A4)
width, height = A4

y = height - 60

# -----------------------------
# Title
# -----------------------------
c.setFont("Helvetica-Bold", 18)
c.drawString(50, y, "BC Gene Explorer – Biomarker Summary Report")
y -= 40

# -----------------------------
# Gene Header
# -----------------------------
c.setFont("Helvetica-Bold", 14)
c.drawString(50, y, f"Gene: {gene}")
y -= 30

# -----------------------------
# Section Helper
# -----------------------------
def draw_section(title, content):
    global y
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, title)
    y -= 20
    c.setFont("Helvetica", 11)

    if isinstance(content, list):
        for line in content:
            c.drawString(65, y, f"- {line}")
            y -= 18
    else:
        text = c.beginText(50, y)
        text.setFont("Helvetica", 11)
        for line in content.split("\n"):
            text.textLine(line)
            y -= 15
        c.drawText(text)

    y -= 10

# -----------------------------
# Report Content
# -----------------------------
draw_section("Expression Summary", [
    f"Tumor Mean: {row['tumor_mean']}",
    f"Normal Mean: {row['normal_mean']}",
    f"log2 Fold Change: {row['log2_fc']}",
    f"P-value: {row['p_value']}",
    f"Status: {row['status']}"
])

draw_section("Biological Function", meta["function"])
draw_section("Pathway", meta["pathway"])
draw_section("Biomarker Role", meta["biomarker_role"])
draw_section("Clinical Interpretation", meta["clinical_note"])

summary = (
    f"{gene} shows strong overexpression in tumor tissue relative to normal controls, "
    f"consistent with HER2-positive breast cancer biology. Elevated {gene} is clinically "
    f"actionable and associated with targeted anti-HER2 therapeutic strategies."
)

draw_section("Interpretation Summary", summary)

# -----------------------------
# Save PDF
# -----------------------------
c.save()

print(f"Report saved to: {output_path}")
