import pandas as pd
import streamlit as st


@st.cache_data
@st.cache_data
def load_data(filepath):
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        st.error(f"Error crítico: No se encontró el archivo en {filepath}")
        return pd.DataFrame()
