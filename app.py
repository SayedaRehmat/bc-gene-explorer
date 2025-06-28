import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("BC_GeneExpression_GSE15852.csv")

# Page title and header
st.set_page_config(page_title="BC-GeneExplorer")
st.title("🧬 BC-GeneExplorer")
st.markdown("""
Explore breast cancer gene expression in tumor vs. normal tissue  
**Based on Malaysian dataset GSE15852**
""")

# User input
gene = st.text_input("Enter Gene Symbol (e.g., TP53, BRCA1)").upper()

# Search and display results
if gene:
    result = df[df["GeneSymbol"] == gene]

    if not result.empty:
        tumor = result["Tumor_Avg_Expression"].values[0]
        normal = result["Normal_Avg_Expression"].values[0]

        st.write(f"**Tumor Expression:** {tumor}")
        st.write(f"**Normal Expression:** {normal}")

        if tumor > normal:
            st.success("This gene is **UPREGULATED** in tumor tissue.")
        elif tumor < normal:
            st.warning("This gene is **DOWNREGULATED** in tumor tissue.")
        else:
            st.info("No expression difference.")

        # Plot
        fig, ax = plt.subplots()
        ax.bar(["Tumor", "Normal"], [tumor, normal], color=["crimson", "skyblue"])
        ax.set_ylabel("Average Expression")
        ax.set_title(f"{gene} Expression in GSE15852")
        st.pyplot(fig)
    else:
        st.error(f"Gene '{gene}' not found in dataset.")
