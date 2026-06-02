import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# ----------------------------------------
# CONFIGURACION GENERAL
# ----------------------------------------

plt.style.use('seaborn-v0_8-whitegrid')

# ----------------------------------------
# TITULO
# ----------------------------------------

st.title("ANÁLISIS ESTADÍSTICO DE VIDEOJUEGOS")

st.write("""
Aplicación desarrollada con Streamlit y Pandas para analizar
videojuegos según su género, año de lanzamiento y puntuación.
""")

# ----------------------------------------
# CARGAR CSV
# ----------------------------------------

df_est = pd.read_csv("estimated_data.csv")

# ----------------------------------------
# INFORMACION GENERAL
# ----------------------------------------

st.header("INFORMACIÓN")

st.write("""
Este proyecto analiza un conjunto de videojuegos utilizando
técnicas de estadística descriptiva.

Variables:

- Género del videojuego
- Año de lanzamiento
- Puntuación obtenida
         
trabajo del estudiante: Carlos Andres Vera Terrazas
""")

# ----------------------------------------
# MOSTRAR BASE DE DATOS
# ----------------------------------------

st.subheader("Base de Datos")

st.dataframe(df_est)

# ----------------------------------------
# ESTADISTICAS GENERALES
# ----------------------------------------

st.header("DATOS GENERALES")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Videojuegos",
    len(df_est)
)

col2.metric(
    "Media de Puntuación",
    round(df_est["Puntuación"].mean(), 2)
)

col3.metric(
    "Mediana de Puntuación",
    round(df_est["Puntuación"].median(), 2)
)

# ----------------------------------------
# TABLA DE FRECUENCIAS GENERO
# ----------------------------------------

st.header("ANÁLISIS DE VARIABLE CUALITATIVA (GÉNERO)")

st.subheader("Tabla de Frecuencias por Género")

frec_cualita = df_est["Género"].value_counts().reset_index()

frec_cualita.columns = ["género", "fi"]

frec_cualita["hi"] = frec_cualita["fi"] / len(df_est)

frec_cualita["hip"] = frec_cualita["hi"] * 100

frec_cualita["Fi"] = frec_cualita["fi"].cumsum()

frec_cualita["Hi"] = frec_cualita["hi"].cumsum()

st.dataframe(frec_cualita)

# ----------------------------------------
# BARRAS
# ----------------------------------------

st.subheader("Gráfico de Barras por Género")

fig, ax = plt.subplots(figsize=(10, 5))

ax.bar(
    frec_cualita["género"],
    frec_cualita["fi"],
    color="skyblue"
)

ax.set_title("DISTRIBUCIÓN DE VIDEOJUEGOS POR GÉNERO")

ax.set_xlabel("Género")

ax.set_ylabel("Frecuencia")

st.pyplot(fig)

# ----------------------------------------
# TORTA
# ----------------------------------------

st.subheader("Gráfico de Torta")

fig, ax = plt.subplots(figsize=(8, 8))

ax.pie(
    frec_cualita["hi"],
    labels=frec_cualita["género"],
    autopct="%1.1f%%",
    startangle=90,
    colors=sns.color_palette("pastel")
)

ax.set_title("PORCENTAJE DE VIDEOJUEGOS POR GÉNERO")

st.pyplot(fig)

# ----------------------------------------
# PUNTUACIONES
# ----------------------------------------

st.header("ANÁLISIS DE VARIABLE CUANTITATIVA DISCRETA (PUNTUACIÓN)")

st.subheader("Tabla de Frecuencias de Puntuaciones")

tabla_discreta = (
    df_est["Puntuación"]
    .value_counts()
    .sort_index()
    .reset_index()
)

tabla_discreta.columns = ["Puntuación", "fi"]

tabla_discreta["hi"] = tabla_discreta["fi"] / len(df_est)

tabla_discreta["Fi"] = tabla_discreta["fi"].cumsum()

tabla_discreta["Hi"] = tabla_discreta["hi"].cumsum()

tabla_discreta["hip"] = tabla_discreta["hi"] * 100

st.dataframe(tabla_discreta)

# ----------------------------------------
# BASTONES
# ----------------------------------------

st.subheader("Gráfico de Bastones")

fig, ax = plt.subplots(figsize=(10, 5))

ax.vlines(
    tabla_discreta["Puntuación"],
    ymin=0,
    ymax=tabla_discreta["fi"],
    color="navy",
    linewidth=2
)

ax.plot(
    tabla_discreta["Puntuación"],
    tabla_discreta["fi"],
    "o",
    color="red"
)

ax.set_xticks(tabla_discreta["Puntuación"])

ax.set_title("PUNTUACIONES DE VIDEOJUEGOS")

ax.set_xlabel("Puntuación")

ax.set_ylabel("Frecuencia")

st.pyplot(fig)

# ----------------------------------------
# AÑOS DE LANZAMIENTO
# ----------------------------------------

st.header("ANÁLISIS DE VARIABLE CUANTITATIVA CONTINUA (AÑOS DE LANZAMIENTO)")

n = len(df_est)

# Fijamos los cortes de manera exacta de año en año (+2 asegura el límite superior inclusivo)
cortes = np.arange(
    df_est["año"].min(),
    df_est["año"].max() + 2,
    1
)

df_est["intervalos"] = pd.cut(
    df_est["año"],
    bins=cortes,
    include_lowest=True,
    right=False
)

tabla_agrupada = (
    df_est["intervalos"]
    .value_counts()
    .sort_index()
    .reset_index()
)

tabla_agrupada.columns = ["Intervalos", "fi"]

# Forzamos la marca de clase al valor entero izquierdo del intervalo para centrar los puntos
tabla_agrupada["marca_clase"] = (
    tabla_agrupada["Intervalos"]
    .apply(lambda x: int(x.left))
)

tabla_agrupada["hi"] = (
    tabla_agrupada["fi"] / len(df_est)
)

tabla_agrupada["hip"] = (
    tabla_agrupada["hi"] * 100
)

tabla_agrupada["Fi"] = (
    tabla_agrupada["fi"].cumsum()
)

tabla_agrupada["Hi"] = (
    tabla_agrupada["hi"].cumsum()
)

st.subheader("Tabla Agrupada")

st.dataframe(tabla_agrupada)

# ----------------------------------------
# HISTOGRAMA
# ----------------------------------------

st.subheader("Histograma de Años")

fig, ax = plt.subplots(figsize=(12, 6))

ax.hist(
    df_est["año"],
    bins=cortes,
    color="#1fcaa0",
    edgecolor="white",
    alpha=0.6,
    label="Histograma"
)

ax.plot(
    tabla_agrupada["marca_clase"],
    tabla_agrupada["fi"],
    color="red",
    marker="D",
    linewidth=2,
    label="Polígono"
)

ax.set_title(
    "DISTRIBUCIÓN DE AÑOS DE LANZAMIENTO"
)

ax.set_xlabel("Año")

ax.set_ylabel("Frecuencia")

ax.legend()

st.pyplot(fig)

# ----------------------------------------
# OJIVA
# ----------------------------------------

st.subheader("Ojiva de Frecuencia Acumulada")

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(
    tabla_agrupada["marca_clase"],
    tabla_agrupada["Fi"],
    color="red",
    marker="s",
    linewidth=2,
    label="Ojiva"
)

ax.fill_between(
    tabla_agrupada["marca_clase"],
    tabla_agrupada["Fi"],
    color="purple",
    alpha=0.3
)

ax.set_title(
    "FRECUENCIA ACUMULADA DE AÑOS"
)

ax.set_xlabel("Marca de Clase (Año)")

ax.set_ylabel("Frecuencia Acumulada")

ax.legend()

st.pyplot(fig)

# ----------------------------------------
# PIE DE PAGINA
# ----------------------------------------

st.markdown("---")

st.write(
    "Proyecto de Estadística I - Análisis Estadístico de Videojuegos - Streamlit - Pandas"
)