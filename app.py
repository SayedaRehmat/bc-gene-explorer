import streamlit as st
import pandas as pd
import json
import plotly.express as px

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="BC Gene Explorer",
    page_icon="🧬",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
    .main {
        background-color: #f8fbff;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    h1, h2, h3 {
        color: #102a43;
        font-family: 'Arial', sans-serif;
    }

    .subtitle {
        font-size: 1rem;
        color: #486581;
        margin-top: -10px;
        margin-bottom: 20px;
    }

    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
        border: 1px solid #e6edf5;
        text-align: center;
    }

    .info-card {
        background: white;
        padding: 18px;
        border-radius: 16px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.05);
        border: 1px solid #e6edf5;
        margin-bottom: 15px;
    }

    .status-up {
        color: #b42318;
        font-weight: 700;
    }

    .status-down {
        color: #175cd3;
        font-weight: 700;
    }

    .status-stable {
        color: #027a48;
        font-weight: 700;
    }

    .footer {
        text-align: center;
        color: #7b8794;
        font-size: 0.85rem;
        margin-top: 30px;
    }

    section[data-testid="stSidebar"] {
        background-color: #eef4fa;
        border-right: 1px solid #d9e2ec;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_expression():
    return pd.read_csv("data/mock_expression.csv")

@st.cache_data
def load_gene_info():
    with open("data/gene_info.json", "r") as f:
        return json.load(f)

expr_df = load_expression()
gene_info = load_gene_info()

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.markdown("## 🧬 BC Gene Explorer")
st.sidebar.markdown("Explore breast cancer biomarker signals")
st.sidebar.divider()

selected_gene = st.sidebar.selectbox("Select Gene", expr_df["gene"].tolist())

st.sidebar.markdown("### Legend")
st.sidebar.markdown("🟥 Upregulated")
st.sidebar.markdown("🟦 Downregulated")
st.sidebar.markdown("🟩 Stable")

gene_row = expr_df[expr_df["gene"] == selected_gene].iloc[0]
gene_meta = gene_info[selected_gene]

# -----------------------------
# Header
# -----------------------------
colA, colB = st.columns([6, 1])

with colA:
    st.markdown("# 🧬 BC Gene Explorer")
    st.markdown(
        "<div class='subtitle'>Breast cancer gene expression visualizer for biomarker exploration and pathway-level interpretation.</div>",
        unsafe_allow_html=True
    )

with colB:
    st.markdown(
        "<div style='background:#dbeafe;padding:10px 14px;border-radius:12px;text-align:center;font-weight:600;color:#1d4ed8;'>Prototype v1</div>",
        unsafe_allow_html=True
    )

st.divider()

# -----------------------------
# Summary Cards
# -----------------------------
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"<div class='metric-card'><h3>Tumor Mean</h3><h2>{gene_row['tumor_mean']}</h2></div>", unsafe_allow_html=True)

with c2:
    st.markdown(f"<div class='metric-card'><h3>Normal Mean</h3><h2>{gene_row['normal_mean']}</h2></div>", unsafe_allow_html=True)

with c3:
    st.markdown(f"<div class='metric-card'><h3>log2 Fold Change</h3><h2>{gene_row['log2_fc']}</h2></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

status_class = {
    "Upregulated": "status-up",
    "Downregulated": "status-down",
    "Stable": "status-stable"
}[gene_row["status"]]

st.markdown(f"### Expression Status: <span class='{status_class}'>{gene_row['status']}</span>", unsafe_allow_html=True)

st.divider()

# -----------------------------
# Expression Plot
# -----------------------------
st.subheader("Expression View")

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
    title=f"{selected_gene}: Tumor vs Normal Expression",
    height=430
)

fig.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(color="#102a43"),
    showlegend=False
)

fig.update_traces(textposition="outside")
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Biological Interpretation
# -----------------------------
st.subheader("Biological Interpretation")

x1, x2 = st.columns(2)

with x1:
    st.markdown(f"<div class='info-card'><b>Function</b><br>{gene_meta['function']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='info-card'><b>Pathway</b><br>{gene_meta['pathway']}</div>", unsafe_allow_html=True)

with x2:
    st.markdown(f"<div class='info-card'><b>Biomarker Role</b><br>{gene_meta['biomarker_role']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='info-card'><b>Clinical Note</b><br>{gene_meta['clinical_note']}</div>", unsafe_allow_html=True)

st.divider()

# -----------------------------
# Statistical Summary
# -----------------------------
st.subheader("Statistical Summary")

s1, s2 = st.columns(2)

with s1:
    st.markdown(f"<div class='metric-card'><h3>P-value</h3><h2>{gene_row['p_value']}</h2></div>", unsafe_allow_html=True)

with s2:
    st.markdown(f"<div class='metric-card'><h3>Status</h3><h2>{gene_row['status']}</h2></div>", unsafe_allow_html=True)

# -----------------------------
# Footer
# -----------------------------
st.markdown("<div class='footer'>BC Gene Explorer | Prototype for rapid breast cancer biomarker interpretation</div>", unsafe_allow_html=True)
