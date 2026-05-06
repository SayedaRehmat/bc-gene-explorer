import streamlit as st
import pandas as pd
import json
import plotly.express as px
import subprocess
import os

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="BC Gene Explorer",
    page_icon="🧬",
    layout="wide"
)

# =============================
# PROFESSIONAL THEME (FIXED)
# =============================
st.markdown("""
<style>

/* =========================
   GLOBAL APP
========================= */
html, body, [class*="css"] {
    background-color: #0b1220 !important;
    color: #e5e7eb !important;
}

/* Main app */
.stApp,
[data-testid="stAppViewContainer"],
section.main,
.block-container,
.main > div {
    background-color: #0b1220 !important;
    color: #e5e7eb !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827 !important;
}
section[data-testid="stSidebar"] * {
    color: #f9fafb !important;
}

/* Headings */
h1, h2, h3, h4 {
    color: #f9fafb !important;
}

/* Paragraphs / markdown */
p, span, div, label {
    color: #d1d5db !important;
}

/* Metrics */
div[data-testid="stMetric"] {
    background: #111827 !important;
    border: 1px solid #1f2937 !important;
    border-radius: 16px !important;
    padding: 18px !important;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.35) !important;
}
div[data-testid="stMetric"] label,
div[data-testid="stMetric"] div {
    color: #f9fafb !important;
}

/* Buttons */
.stButton button {
    background-color: #2563eb !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}
.stButton button:hover {
    background-color: #1d4ed8 !important;
}

/* Selectbox */
div[data-baseweb="select"] > div {
    background-color: #111827 !important;
    color: #f9fafb !important;
    border: 1px solid #374151 !important;
}

/* Alert boxes */
div.stAlert {
    background-color: #111827 !important;
    color: #f9fafb !important;
    border-radius: 14px !important;
    border: 1px solid #1f2937 !important;
}

/* Divider */
hr {
    border-color: #1f2937 !important;
}

/* Caption */
[data-testid="stCaptionContainer"] {
    color: #9ca3af !important;
}

</style>
""", unsafe_allow_html=True)
# =============================
# LOAD DATA (ONLY 2 FILES)
# =============================
@st.cache_data
def load_expression():
    return pd.read_csv("data/mock_expression.csv")

@st.cache_data
def load_gene_info():
    with open("data/gene_info.json", "r") as f:
        return json.load(f)

expr_df = load_expression()
gene_info = load_gene_info()

# =============================
# HEADER
# =============================
st.title("🧬 BC Gene Explorer")
st.markdown("**Breast cancer gene expression & biomarker interpretation platform (mock prototype)**")

st.divider()

# =============================
# SIDEBAR
# =============================
st.sidebar.title("Gene Selection")

selected_gene = st.sidebar.selectbox(
    "Choose gene",
    expr_df["gene"].tolist()
)

gene_row = expr_df[expr_df["gene"] == selected_gene].iloc[0]
gene_meta = gene_info[selected_gene]

# =============================
# REPORT BUTTON (FIXED FEATURE)
# =============================
st.sidebar.divider()

if st.sidebar.button("📄 Generate PDF Report"):
    with st.spinner("Generating report..."):
        result = subprocess.run(
            ["python", "report.py"],
            capture_output=True,
            text=True
        )

    if result.returncode == 0:
        st.sidebar.success("Report generated successfully")
        st.sidebar.info("Saved in reports/sample_gene_report.pdf")
    else:
        st.sidebar.error("Report generation failed")
        st.sidebar.text(result.stderr)

# =============================
# SUMMARY METRICS
# =============================
col1, col2, col3 = st.columns(3)

col1.metric("Tumor Expression", gene_row["tumor_mean"])
col2.metric("Normal Expression", gene_row["normal_mean"])
col3.metric("log2 Fold Change", gene_row["log2_fc"])

st.markdown(f"### Status: **{gene_row['status']}**")

st.divider()

# =============================
# EXPRESSION PLOT
# =============================
st.subheader("Expression Profile")

plot_df = pd.DataFrame({
    "Condition": ["Normal", "Tumor"],
    "Expression": [gene_row["normal_mean"], gene_row["tumor_mean"]]
})

fig = px.bar(
    plot_df,
    x="Condition",
    y="Expression",
    text="Expression",
    color="Condition",
    height=420
)

fig.update_layout(
    plot_bgcolor="#111827",
    paper_bgcolor="#111827",
    font=dict(color="#f9fafb"),
    xaxis=dict(color="#f9fafb"),
    yaxis=dict(color="#f9fafb"),
    showlegend=False
)
fig.update_traces(textposition="outside")

st.plotly_chart(fig, use_container_width=True)

# =============================
# BIOLOGICAL INTERPRETATION
# =============================
st.subheader("Biological Interpretation")

c1, c2 = st.columns(2)

with c1:
    st.info(f"**Function**\n\n{gene_meta['function']}")
    st.info(f"**Pathway**\n\n{gene_meta['pathway']}")

with c2:
    st.success(f"**Biomarker Role**\n\n{gene_meta['biomarker_role']}")
    st.warning(f"**Clinical Insight**\n\n{gene_meta['clinical_note']}")

st.divider()

# =============================
# STATISTICS PANEL
# =============================
st.subheader("Statistical Summary")

c1, c2 = st.columns(2)

c1.metric("P-value", gene_row["p_value"])
c2.metric("Expression Status", gene_row["status"])

# =============================
# FOOTER
# =============================
st.divider()
st.caption("BC Gene Explorer | Mock translational bioinformatics dashboard (Streamlit prototype)")
