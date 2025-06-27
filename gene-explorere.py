import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load the dataset
df = pd.read_csv("BC_GeneExpression_GSE15852.csv")

# Step 2: Ask user to enter a gene name
gene = input("Enter gene symbol (e.g., TP53): ").strip().upper()

# Step 3: Search for gene in the dataset
result = df[df["GeneSymbol"] == gene]

# Step 4: Show results
if not result.empty:
    tumor = result["Tumor_Avg_Expression"].values[0]
    normal = result["Normal_Avg_Expression"].values[0]

    print(f"\nGene: {gene}")
    print(f"Tumor Expression: {tumor}")
    print(f"Normal Expression: {normal}")

    if tumor > normal:
        print("✅ This gene is UPREGULATED in tumor tissue.")
    elif tumor < normal:
        print("⚠️ This gene is DOWNREGULATED in tumor tissue.")
    else:
        print("No difference in expression.")

    # Plot
    plt.bar(["Tumor", "Normal"], [tumor, normal], color=["crimson", "skyblue"])
    plt.title(f"{gene} Expression in Breast Cancer (GSE15852)")
    plt.ylabel("Average Expression")
    plt.grid(True)
    plt.show()

else:
    print(f"❌ Gene '{gene}' not found in dataset.")

