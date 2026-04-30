import streamlit as st
from utils.data_manager import load_data
from components.layout import render_dashboard_grid, render_header
from components.sidebar import render_sidebar

# Configuración global
st.set_page_config(page_title="Dashboard: Visualizacion de datos", layout="wide")


def main():
    # 1. Cargar datos
    df = load_data("data/dataset_limpio.csv")

    if df.empty:
        st.error("No hay datos para cargar.")
        return

    # 2. Renderizar UI estática y obtener filtros
    render_header()
    filtros = render_sidebar(df)

    # 3. Lógica de Filtrado (El Colador)
    df_filtrado = df.copy()

    # Aplicar filtro de precio
    df_filtrado = df_filtrado[
        (df_filtrado["Price"] >= filtros["precio_min"])
        & (df_filtrado["Price"] <= filtros["precio_max"])
    ]

    # Aplicar filtro de géneros
    if len(filtros["generos"]) > 0:
        pattern = "|".join(filtros["generos"])
        df_filtrado = df_filtrado[
            df_filtrado["Genres"].str.contains(pattern, case=False, na=False)
        ]



    # 4. Renderizar la grilla con los datos filtrados (¡Asegurate de que diga df_filtrado!)
    render_dashboard_grid(df_filtrado)


if __name__ == "__main__":
    main()
