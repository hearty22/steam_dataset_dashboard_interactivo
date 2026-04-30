import plotly.express as px
import pandas as pd
import numpy as np


def create_price_histogram(df):
    if df.empty or "Price" not in df.columns:
        return None

    # Filtramos juegos absurdamente caros (errores de carga > $200) para limpiar la vista
    df_filtered = df[df["Price"] <= 150].copy()

    fig = px.histogram(
        df_filtered,
        x="Price",
        nbins=50,
        title="Distribución de Precios (Juegos < $150)",
        color_discrete_sequence=["#1f77b4"],
        log_y=True,  # ESCALA LOGARÍTMICA: Permite ver las barras pequeñas
    )
    fig.update_layout(xaxis_title="Precio ($)", yaxis_title="Cantidad (Log Scale)")
    return fig


def create_top_genres_bar(df):
    if df.empty or "Genres" not in df.columns or "Peak CCU" not in df.columns:
        return None

    # LIMPIEZA AL VUELO: Separamos los géneros por coma y creamos una fila por cada uno
    # (Esto debería hacerlo el ETL, pero lo parcheamos acá)
    df_genres = df.assign(Genres=df["Genres"].str.split(",")).explode("Genres")

    # Ahora sí agrupamos por el género limpio
    top_genres = (
        df_genres.groupby("Genres")["Peak CCU"].sum().nlargest(10).reset_index()
    )

    fig = px.bar(
        top_genres,
        x="Peak CCU",
        y="Genres",
        orientation="h",
        title="Top 10 Géneros Puros por Pico de Jugadores",
        text_auto=".2s",
        color="Peak CCU",  # Le damos un gradiente de color según la cantidad
        color_continuous_scale="Blues",
    )
    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        xaxis_title="Jugadores",
        yaxis_title="",
    )
    return fig


def create_releases_over_time(df):
    if df.empty or "Release date" not in df.columns:
        return None

    df_temp = df.copy()

    df_temp["Date_Parsed"] = pd.to_datetime(
        df_temp["Release date"], errors="coerce", format="mixed"
    )
    df_temp["Year"] = df_temp["Date_Parsed"].dt.year

    # Filtramos años absurdos (ej. 1970 por defecto o años futuros raros)
    df_temp = df_temp[(df_temp["Year"] >= 2000) & (df_temp["Year"] <= 2024)]

    releases_by_year = df_temp.groupby("Year").size().reset_index(name="Cantidad")

    fig = px.line(
        releases_by_year,
        x="Year",
        y="Cantidad",
        markers=True,
        title="Evolución de Lanzamientos (2000 - 2024)",
    )
    # Rellenamos el área debajo de la línea para que se vea más profesional
    fig.update_traces(fill="tozeroy", line_color="#ff7f0e")
    fig.update_layout(xaxis_title="Año", yaxis_title="Juegos Lanzados")
    return fig


def create_os_support_bar(df):
    """
    Genera un gráfico de barras mostrando la compatibilidad de SO.
    Reemplaza al donut chart porque las categorías se superponen.
    """
    if df.empty or not all(col in df.columns for col in ["Windows", "Mac", "Linux"]):
        return None

    # Sumamos las implementaciones
    os_counts = {
        "Windows": df["Windows"].sum(),
        "Mac": df["Mac"].sum(),
        "Linux": df["Linux"].sum(),
    }
    df_os = pd.DataFrame(list(os_counts.items()), columns=["SO", "Juegos Compatibles"])

    fig = px.bar(
        df_os,
        x="SO",
        y="Juegos Compatibles",
        title="Compatibilidad por Sistema Operativo",
        color="SO",
        color_discrete_map={"Windows": "#0078D6", "Mac": "#A2AAAD", "Linux": "#FCC624"},
        text_auto=True,
    )
    fig.update_layout(
        showlegend=False,
        xaxis_title="Sistema Operativo",
        yaxis_title="Cantidad de Juegos",
    )
    return fig


def create_scatter_price_vs_reviews(df):
    """Genera un scatter plot comparando precio y reseñas positivas sin ocultar datos."""
    if df.empty or "Price" not in df.columns or "Positive" not in df.columns:
        return None

    # Ya NO filtramos los juegos con 0 reseñas. Mostramos la cruda realidad.

    fig = px.scatter(
        df,
        x="Price",
        y="Positive",
        opacity=0.1,  # Opacidad muy baja (10%) porque va a haber una aglomeración masiva en el piso
        title="Precio vs. Reseñas Positivas (Escala Logarítmica)",
        hover_data=["Name"],
        log_y=True,
    )
    fig.update_layout(xaxis_title="Precio ($)", yaxis_title="Reseñas Positivas (Log)")
    return fig


def create_metacritic_histogram(df):
    """Genera un histograma de los puntajes de Metacritic."""
    if df.empty or "Metacritic score" not in df.columns:
        return None

    # Filtramos los juegos que no tienen puntaje (suelen venir como 0 en este dataset)
    df_filtered = df[df["Metacritic score"] > 0]

    fig = px.histogram(
        df_filtered,
        x="Metacritic score",
        nbins=20,
        title="Distribución de Puntajes Metacritic",
        color_discrete_sequence=["#2ca02c"],
    )
    fig.update_layout(xaxis_title="Puntaje", yaxis_title="Cantidad de Juegos")
    return fig


def create_playtime_boxplot(df):
    """
    Genera un diagrama de caja (Boxplot) del tiempo de juego.
    Muestra estadísticamente la distribución real, ignorando el ruido del promedio.
    """
    if (
        df.empty
        or "Average playtime forever" not in df.columns
        or "Genres" not in df.columns
    ):
        return None

    # 1. Limpieza inicial: Filtramos juegos que nadie jugó (0 minutos)
    # y datos rotos/imposibles (ej. más de 50,000 minutos promedio)
    df_play = df[
        (df["Average playtime forever"] > 0) & (df["Average playtime forever"] < 50000)
    ].copy()

    # 2. Limpiamos los géneros separados por comas
    df_play = df_play.assign(Genres=df_play["Genres"].str.split(",")).explode("Genres")

    # 3. Nos quedamos solo con los 5 géneros más populares para no hacer un gráfico ilegible
    top_5_genres = df_play["Genres"].value_counts().nlargest(5).index
    df_top_play = df_play[df_play["Genres"].isin(top_5_genres)]

    fig = px.box(
        df_top_play,
        x="Genres",
        y="Average playtime forever",
        color="Genres",
        title="Distribución de Tiempo de Juego por Género (Top 5)",
        log_y=True,
        labels={
                    "Genres": "Género",
                    "Average playtime forever": "Minutos Jugados"
                }
    )

    fig.update_layout(
        xaxis_title="Género",
        yaxis_title="Minutos Jugados (Escala Log)",
        showlegend=False,
    )
    return fig


def create_all_charts(df):
    """
    Orquestador de gráficos.
    Retorna un diccionario con TODOS los objetos de Plotly.
    """
    return {
        # Los 4 originales
        "price_hist": create_price_histogram(df),
        "scatter_reviews": create_scatter_price_vs_reviews(df),
        "top_genres": create_top_genres_bar(df),
        "release_line": create_releases_over_time(df),
        # LOS 2 NUEVOS (Faltaban estos)
        "os_bar": create_os_support_bar(df),
        "metacritic_hist": create_metacritic_histogram(df),
        "playtime_box": create_playtime_boxplot(df),
    }
