import streamlit as st
from components.charts import create_all_charts


def render_header():
    st.title("Reporte: Visualizacion de datos")


def render_dashboard_grid(df):
    if df.empty:
        st.warning("⚠️ El dataset está vacío.")
        return

    # --- KPIs (Siempre visibles arriba) ---
    st.subheader("Métricas de la Plataforma")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric(label="Total de Juegos", value=f"{len(df):,}")
    kpi2.metric(
        label="Precio Promedio",
        value=f"${df['Price'].mean():.2f}" if "Price" in df.columns else "$0",
    )
    kpi3.metric(
        label="Reseñas Positivas",
        value=f"{df['Positive'].sum():,.0f}" if "Positive" in df.columns else "0",
    )
    kpi4.metric(
        label="Máx. Jugadores",
        value=f"{df['Peak CCU'].max():,}" if "Peak CCU" in df.columns else "0",
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Obtenemos TODOS los gráficos (incluyendo los nuevos)
    charts = create_all_charts(df)

    # --- IMPLEMENTACIÓN DE PESTAÑAS (TABS) ---
    tab1, tab2 = st.tabs(["📊 Análisis Principal", "💻 Detalles Técnicos"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            if charts.get("price_hist"):
                st.plotly_chart(charts["price_hist"], use_container_width=True)
        with col2:
            if charts.get("scatter_reviews"):
                st.plotly_chart(charts["scatter_reviews"], use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            if charts.get("top_genres"):
                st.plotly_chart(charts["top_genres"], use_container_width=True)
        with col4:
            if charts.get("release_line"):
                st.plotly_chart(charts["release_line"], use_container_width=True)

    with tab2:
        col5, col6 = st.columns(2)
        with col5:
            if charts.get("os_bar"):
                st.plotly_chart(
                    charts["os_bar"], use_container_width=True
                )  # Nombre de llave sugerido
        with col6:
            if charts.get("metacritic_hist"):
                st.plotly_chart(
                    charts["metacritic_hist"], use_container_width=True
                )  # Nombre de llave sugerido
        st.markdown("")
        if charts.get("playtime_box"):
            st.plotly_chart(charts["playtime_box"], use_container_width=True)
