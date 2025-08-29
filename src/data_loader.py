import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Define the columns we expect to be numeric for data cleaning
NUMERIC_COLS = [
    "Round ID",
    "Hole",
    "Distance",
    "Par",
    "Shots",
    "Tee Shot Distance",
    "Approach Distance",
    "Shots Inside 100y",
    "Putts",
    "Strokes",
    "Score",
]
BINARY_COLS = ["FIR", "GIR"]


def load_data() -> pd.DataFrame:
    """
    Connects to Google Sheets, fetches the data, and returns a cleaned pandas DataFrame.

    Returns:
        pd.DataFrame: A clean DataFrame containing the data with appropriate data types.
                      Returns an empty DataFrame if the connection fails.
    """
    try:
        # Establish the connection to Google Sheets
        conn = st.connection("gsheets", type=GSheetsConnection)

        # Read the data from the default worksheet
        df = conn.read(worksheet="Raw Data")

        # --- Data Cleaning and Type Conversion ---
        # Drop rows where all elements are NaN (empty rows from the sheet)
        df.dropna(how="all", inplace=True)

        # Convert date column to datetime objects
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)

        # Convert binary 'Yes'/'No' columns to 1/0 for calculations.
        # 'N/A' and other values will become NaN.
        binary_cols = ["FIR", "GIR"]
        for col in binary_cols:
            if col in df.columns:
                df[col] = df[col].map({"Yes": 1, "No": 0})

        # Convert remaining numeric columns, coercing errors to NaN
        for col in NUMERIC_COLS:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # Replace empty strings with None for consistency
        df.replace("", None, inplace=True)

        st.success("Successfully loaded and cleaned data from Google Sheets.")
        return df

    except Exception as e:
        st.error(f"An error occurred while loading data: {e}")
        return pd.DataFrame()
