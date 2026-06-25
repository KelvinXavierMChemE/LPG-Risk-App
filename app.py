import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(
    page_title="LPG Risk Assessment System",
    layout="wide"
)

st.title("🔥 LPG Safety Risk Assessment System")

st.markdown(
    "Upload customer survey responses and automatically identify high-risk customers."
)

uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx"]
)

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    st.subheader("Uploaded Data")
    st.dataframe(df)

    # --------------------------
    # Risk Score Calculation
    # --------------------------

    def calculate_risk(row):

        score = 0

        if row["Stove Age"] > 15:
            score += 40

        if row["Burners"] >= 3:
            score += 10

        if str(row["Gas Smell"]).strip().lower() == "yes":
            score += 50

        if row["Last Service (Years)"] > 3:
            score += 20

        if row["Hose Age"] > 5:
            score += 20

        return score


    df["Risk Score"] = df.apply(calculate_risk, axis=1)


    def classify(score):

        if score >= 70:
            return "High"

        elif score >= 30:
            return "Medium"

        else:
            return "Low"


    df["Risk Category"] = df["Risk Score"].apply(classify)

    # --------------------------
    # KPI Section
    # --------------------------

    total = len(df)

    high = len(df[df["Risk Category"] == "High"])
    medium = len(df[df["Risk Category"] == "Medium"])
    low = len(df[df["Risk Category"] == "Low"])

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Customers", total)
    col2.metric("High Risk", high)
    col3.metric("Medium Risk", medium)
    col4.metric("Low Risk", low)

    st.divider()

    # --------------------------
    # Results Table
    # --------------------------

    st.subheader("Risk Assessment Results")

    st.dataframe(df)

    # --------------------------
    # Pie Chart
    # --------------------------

    st.subheader("Risk Distribution")

    risk_counts = df["Risk Category"].value_counts()

    fig, ax = plt.subplots(figsize=(5, 5))

    ax.pie(
        risk_counts,
        labels=risk_counts.index,
        autopct="%1.1f%%"
    )

    st.pyplot(fig)

    # --------------------------
    # High Risk Customers
    # --------------------------

    st.subheader("High Risk Customers")

    high_risk = df[df["Risk Category"] == "High"]

    st.dataframe(high_risk)

    # --------------------------
    # Download Report
    # --------------------------

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)

    st.download_button(
        label="📥 Download Risk Report",
        data=output.getvalue(),
        file_name="LPG_Risk_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
