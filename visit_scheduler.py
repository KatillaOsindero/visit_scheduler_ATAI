import streamlit as st

import pandas as pd

from datetime import timedelta

# Load protocol schedule

schedule = pd.read_csv("protocol_schedule.csv")

st.title("Clinical Trial Visit Scheduler")

# Input patient ID and anchor date

patient_id = st.text_input("Patient ID")

anchor_date = st.date_input("Anchor Date (e.g., randomization/start date)")

if patient_id and anchor_date:
    # Convert anchor_date into pandas Timestamp (so math works)
    anchor_date = pd.to_datetime(anchor_date)
    # Calculate visits
    visits = schedule.copy()
    visits["Target Date"] = anchor_date + pd.to_timedelta(visits["Day From Baseline"], unit="D")
    visits["Earliest"] = visits["Target Date"] - pd.to_timedelta(visits["Window Minus"], unit="D")
    visits["Latest"] = visits["Target Date"] + pd.to_timedelta(visits["Window Plus"], unit="D")

    st.write(f"### Visit Schedule for Patient {patient_id}")

    st.dataframe(visits)

    # Export option

    csv = visits.to_csv(index=False).encode("utf-8")

    st.download_button(

        label="Download as CSV",

        data=csv,

        file_name=f"{patient_id}_visit_schedule.csv",

        mime="text/csv",

    )
 