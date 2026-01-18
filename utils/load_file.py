import pandas as pd
import streamlit as st
from utils.paths import DATA_DIR


@st.cache_data
def load_dataset(file_name):
    """
    Load a CSV file from the data directory.
    Uses centralized path management from utils.paths.
    """
    file_path = DATA_DIR / file_name

    if file_name.endswith(".xlsx"):
        return pd.read_excel(file_path)

    try:
        return pd.read_csv(file_path, encoding="utf-8")
    except UnicodeDecodeError:
        return pd.read_csv(file_path, encoding="latin-1")
