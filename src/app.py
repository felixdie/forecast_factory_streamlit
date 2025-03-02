import streamlit as st
import pandas as pd

from utils.utility_functions import initialise_states

# ------------------------ Page Config ------------------------ #

st.set_page_config(layout="wide")

# ------------------------ Ses States  ------------------------ #

# initialise_states(states={"forecasting": False})

# ------------------------ Page Layout ------------------------ #

st.header("Forecasting Factory")
st.write("Upload your data and forecast anything")

col1, col2 = st.columns(2)

with col1:

    # File upload container
    with st.container(border=True, height=150):

        upload = st.file_uploader(
            "Upload your CSV", type="csv", label_visibility="collapsed"
        )
        if upload is not None:
            data = pd.read_csv(upload)

with col2:

    with st.container(border=True, height=150):

        subcol1, subcol2 = st.columns(2)

        with subcol1:
            # Drop down to select model
            model = st.selectbox(
                "Choose your model",
                ("Exponential Smoothing", "ETS", "ARIMA"),
                placeholder="Choose model",
                index=None,
                label_visibility="collapsed",
            )

        with subcol2:
            # Drop down to select model
            forecasting_period = st.selectbox(
                "Choose your forecasting period",
                ("3 Months", "6 Months", "12 Months"),
                placeholder="Choose period",
                index=None,
                label_visibility="collapsed",
            )

        # Button to start forecasting
        forecasting = st.button("Forecast")

if forecasting:

    # Show forecast visualisation
    with st.container(border=True):
        # Take data
        # Preprocessing: Dataframe, stationarity
        # Forecast
        # Plot TS
        # Calculate Metrics (MAPE, avg. change over forecasting period)
        st.write("hello")
