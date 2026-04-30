import streamlit as st

def render_sidebar(df):
    """Renderiza la barra lateral interactiva basada en el dataset real."""
    with st.sidebar:
        st.header(" Panel de Control")
        st.markdown("Ajustá los parámetros para filtrar los datos en tiempo real.")

        if df.empty:
            st.warning("Esperando datos...")
            return {}

        # 1. Filtro de Precio (Rango)
        max_price = float(df['Price'].max()) if 'Price' in df.columns else 100.0
        precio_min, precio_max = st.slider(
            "Rango de Precio ($):",
            min_value=0.0,
            max_value=max_price,
            value=(0.0, max_price)
        )

        # 2. Filtro de Género (Multiselect)
        if 'Genres' in df.columns:
            generos_unicos = df['Genres'].dropna().str.split(',').explode().unique()
            generos_seleccionados = st.multiselect(
                "Filtrar por Género:",
                options=sorted(generos_unicos),
                default=[]
            )
        else:
            generos_seleccionados = []

        st.divider()
        st.info(" Estos filtros recalculan todos los gráficos automáticamente.")

        # --- SECCIÓN DE CRÉDITOS Y FUENTE (Al final) ---
        # Empujamos el contenido hacia abajo con espacios vacíos
        st.markdown("<br>" * 10, unsafe_allow_html=True)
        st.divider()
        st.markdown("###  Datos del Proyecto")
        # Enlace directo al dataset de Kaggle utilizado en el TP
        st.markdown("[Steam Games Dataset (Kaggle)](https://www.kaggle.com/datasets/fronkongames/steam-games-dataset)")
        st.caption("Información obtenida a través de la API oficial de Steam.")

        return {
            "precio_min": precio_min,
            "precio_max": precio_max,
            "generos": generos_seleccionados
        }
