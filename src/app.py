import streamlit as st
import pandas as pd
from prophet import Prophet

# from utils.utility_functions import initialise_states
from helpers.helper_functions import rolling_cv_mape, plot_rolling_cv

# ------------------------ Page Config ------------------------ #
st.set_page_config(layout="wide")
# initialise_states(states={"forecasting": False})

# ------------------------ Page Layout ------------------------ #

st.header("Forecasting Factory")
st.write("Upload your data and forecast anything")

col1, col2 = st.columns(2)

with col1:

    # File upload container
    with st.container(border=True, height=150):

        upload = st.file_uploader(
            "Upload your CSV", type=("xlsx"), label_visibility="collapsed"
        )
        if upload is not None:
            data = pd.read_excel(upload, engine="openpyxl")

with col2:

    with st.container(border=True, height=150):

        subcol1, subcol2 = st.columns(2)

        with subcol1:
            # Drop down to select model
            model = st.selectbox(
                "Choose your model",
                ("Exponential Smoothing", "ETS", "ARIMA", "Prophet"),
                placeholder="Choose model",
                index=None,
                label_visibility="collapsed",
            )

        with subcol2:
            # Drop down to select forecasting period
            forecasting_period = st.selectbox(
                "Choose your forecasting period",
                ("3 Months", "6 Months", "12 Months"),
                placeholder="Choose period",
                index=None,
                label_visibility="collapsed",
            )

        # Button to start forecasting
        forecasting = st.button("Forecast")

# ------------------------ Forecasting ------------------------ #

with st.container(border=True):
    
    if upload is not None and forecasting is False:

        # Preprocessing
        data.columns = ["ds", "y"]

        # Display data
        st.write("Actuals")
        st.line_chart(data=data, x="ds", y="y", x_label="", y_label="")

    if forecasting:

        if model == "Prophet":
                
            # Initialise model
            m = Prophet()

            # Preprocessing
            data.columns = ["ds", "y"]

            # Fitting
            m.fit(data)
            
            # Forecast
            if forecasting_period == "3 Months":
                future = m.make_future_dataframe(periods=90)
            elif forecasting_period == "6 Months":
                future = m.make_future_dataframe(periods=180)
            elif forecasting_period == "12 Months":
                future = m.make_future_dataframe(periods=365)
            forecast = m.predict(future)

            # Postprocess
            forecast["ds"] = pd.to_datetime(forecast["ds"])
            actuals_vs_forecast = forecast.merge(data, on="ds", how="left")
            actuals_vs_forecast = actuals_vs_forecast[["ds", "y", "yhat"]]
            actuals_vs_forecast.columns = ["ds", "Actuals", "Forecast"]

            # Calculate MAPE
            mean_mape = rolling_cv_mape(df=actuals_vs_forecast, actual_col="Actuals", forecast_col="Forecast", min_train_size=12, test_size=1, start_date=None)

            # Plot results
            st.write(f"Actuals vs Forecast: {mean_mape}% MAPE")
            st.line_chart(data=actuals_vs_forecast, x="ds", y=["Actuals", "Forecast"], x_label="", y_label="")
            
            # Make recommendation/ comment with LLM
