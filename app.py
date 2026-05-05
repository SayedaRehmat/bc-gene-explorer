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

/* Background */
.stApp {
    background-color: #f4f8fc;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0f172a;
}
section[data-testid="stSidebar"] * {
    color: white;
}

/* Titles */
h1, h2, h3 {
    color: #0f172a;
}

/* Metric Cards */
div[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0px 3px 12px rgba(0,0,0,0.08);
}

/* Buttons */
.stButton button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 0.6rem 1rem;
}

.stButton button:hover {
    background-color: #1d4ed8;
}

/* Info boxes */
div.stAlert {
    border-radius: 12px;
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
    plot_bgcolor="white",
    paper_bgcolor="white"
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
