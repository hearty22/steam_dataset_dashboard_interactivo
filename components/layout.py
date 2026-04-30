import streamlit as st
from components.charts import create_all_charts


def render_header():
    st.title("Reporte: Visualización de datos - Steam Games")
    st.markdown("---")


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

    # Obtenemos TODOS los gráficos
    charts = create_all_charts(df)

    # --- IMPLEMENTACIÓN DE PESTAÑAS (TABS) ---
    tab1, tab2 = st.tabs(["Análisis Principal", "Detalles Técnicos"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            if charts.get("price_hist"):
                st.plotly_chart(charts["price_hist"], use_container_width=True)
                with st.expander(" Interpretar Gráfico"):
                    st.markdown("El **Histograma** muestra la concentración de juegos según su costo. Se utiliza una **escala logarítmica** en el eje vertical para visualizar los juegos de mayor valor sin que la abrumadora cantidad de juegos gratuitos aplaste la gráfica.")

        with col2:
            if charts.get("scatter_reviews"):
                st.plotly_chart(charts["scatter_reviews"], use_container_width=True)
                with st.expander("Interpretar Gráfico"):
                    st.markdown("El **Gráfico de Dispersión** busca correlación entre el precio y la aceptación. La escala logarítmica permite observar la inmensa cantidad de juegos con pocas reseñas y aislar los *outliers* (juegos virales con millones de críticas positivas).")

        st.markdown("<br>", unsafe_allow_html=True)
        col3, col4 = st.columns(2)

        with col3:
            if charts.get("top_genres"):
                st.plotly_chart(charts["top_genres"], use_container_width=True)
                with st.expander(" Interpretar Gráfico"):
                    st.markdown("Este **Gráfico de Barras** establece un ranking visual claro de los géneros que atraen mayor cantidad de jugadores en simultáneo (Peak CCU), facilitando la comparación directa.")

        with col4:
            if charts.get("release_line"):
                st.plotly_chart(charts["release_line"], use_container_width=True)
                with st.expander(" Interpretar Gráfico"):
                    st.markdown("El **Gráfico de Líneas** es el estándar para series temporales. Aquí evidencia la tendencia y el crecimiento exponencial en el volumen de publicaciones en la plataforma año tras año.")

    with tab2:
        col5, col6 = st.columns(2)
        with col5:
            if charts.get("os_bar"):
                st.plotly_chart(charts["os_bar"], use_container_width=True)
                # Usamos caption porque es una advertencia corta y técnica importante
                st.caption("⚠️ Nota: Las categorías no son excluyentes. Un mismo juego puede estar disponible y contabilizarse en múltiples sistemas operativos a la vez.")

        with col6:
            if charts.get("metacritic_hist"):
                st.plotly_chart(charts["metacritic_hist"], use_container_width=True)
                with st.expander("Interpretar Gráfico"):
                    st.markdown("Muestra la distribución de las calificaciones de la prensa. Permite observar el sesgo de la industria, donde la gran mayoría de las notas se agrupan entre los 70 y 85 puntos.")

        st.markdown("---")

        if charts.get("playtime_box"):
            st.plotly_chart(charts["playtime_box"], use_container_width=True)
            # El expander clave con la teoría estadística que pediste
            with st.expander(" ¿Cómo leer las métricas de este Boxplot?"):
                st.markdown("""
                Este **Diagrama de Caja (Boxplot)** muestra la distribución real de retención de jugadores por género, evitando el sesgo que generarían los promedios engañosos:
                * **Límite Inferior (Lower fence / min):** El tiempo mínimo jugado dentro del comportamiento estadístico normal.
                * **Q1 (Primer Cuartil):** El 25% de los juegos acumulan este tiempo de retención o menos.
                * **Mediana (Q2 / Median):** El valor central exacto. La mitad de los juegos retienen menos que esto, y la otra mitad más.
                * **Q3 (Tercer Cuartil):** La marca de éxito. Solo el 25% superior de los juegos logran retener a los jugadores por encima de esta barrera de tiempo.
                * **Límite Superior (Upper fence):** La barrera estadística. Cualquier punto (juego) graficado por encima de esta línea es un valor atípico (*outlier*), representando casos de jugadores con retención extrema.
                """)
