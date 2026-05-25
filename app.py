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

st.title("ANÁLISIS ESTADÍSTICO")

st.write("Aplicación desarrollada con Streamlit y panda")

# ----------------------------------------
# CARGAR CSV
# ----------------------------------------

df_est = pd.read_csv("estimated_data.csv")

# ----------------------------------------
# MOSTRAR BASE DE DATOS
# ----------------------------------------

st.subheader("Base de Datos")

st.dataframe(df_est)

# ----------------------------------------
# TABLA DE FRECUENCIAS CARRERA
# ----------------------------------------

st.subheader("Tabla de Frecuencias - Carrera")

frec_cualita = df_est["carrera"].value_counts().reset_index()

frec_cualita.columns = ["carrera", "fi"]

# frecuencia relativa
frec_cualita["hi"] = frec_cualita["fi"] / len(df_est)

# frecuencia relativa porcentual
frec_cualita["hip"] = frec_cualita["hi"] * 100

# frecuencia acumulada
frec_cualita["Fi"] = frec_cualita["fi"].cumsum()

# frecuencia relativa acumulada
frec_cualita["Hi"] = frec_cualita["hi"].cumsum()

st.dataframe(frec_cualita)

# ----------------------------------------
# GRAFICO DE BARRAS
# ----------------------------------------

st.subheader("Gráfico de Barras")

fig, ax = plt.subplots(figsize=(10,5))

ax.bar(
    frec_cualita['carrera'],
    frec_cualita['fi'],
    color='skyblue'
)

ax.set_title('DISTRIBUCIÓN POR CARRERA', fontweight='bold')

ax.set_xlabel('Carreras')

ax.set_ylabel('Frecuencia')

st.pyplot(fig)

# ----------------------------------------
# TABLA DE FRECUENCIAS MATERIAS
# ----------------------------------------

st.subheader("Tabla de Frecuencias - Materias Aprobadas")

tabla_discreta = df_est["materias_aprobadas"] \
    .value_counts() \
    .sort_index() \
    .reset_index()

tabla_discreta.columns = ["Materias_X", "fi"]

# frecuencia relativa
tabla_discreta["hi"] = tabla_discreta["fi"] / len(df_est)

# frecuencia acumulada
tabla_discreta["Fi"] = tabla_discreta["fi"].cumsum()

# frecuencia relativa acumulada
tabla_discreta["Hi"] = tabla_discreta["hi"].cumsum()

# frecuencia relativa porcentual
tabla_discreta["hip"] = tabla_discreta["hi"] * 100

st.dataframe(tabla_discreta)

# ----------------------------------------
# GRAFICO DE BASTONES
# ----------------------------------------

st.subheader("Gráfico de Bastones")

fig, ax = plt.subplots(figsize=(10,5))

ax.vlines(
    tabla_discreta['Materias_X'],
    ymin=0,
    ymax=tabla_discreta['fi'],
    color='navy',
    linewidth=2
)

ax.plot(
    tabla_discreta['Materias_X'],
    tabla_discreta['fi'],
    "o",
    color='red'
)

ax.set_xticks(tabla_discreta['Materias_X'])

ax.set_title('MATERIAS APROBADAS', fontweight='bold')

ax.set_xlabel('Número de Materias')

ax.set_ylabel('Frecuencia')

st.pyplot(fig)

# ----------------------------------------
# TABLA AGRUPADA EDADES
# ----------------------------------------

st.subheader("Tabla Agrupada de Edades")

n = len(df_est)

rango = df_est['edad'].max() - df_est['edad'].min()

# regla de Sturges
k = int(np.ceil(1 + 3.322 * np.log10(n)))

# amplitud
amplitud = rango / k

# intervalos
cortes = np.arange(
    df_est["edad"].min(),
    df_est["edad"].max() + amplitud,
    amplitud
)

# crear intervalos
df_est["intervalos"] = pd.cut(
    df_est["edad"],
    bins=cortes,
    include_lowest=True,
    right=False
)

# tabla agrupada
tabla_agrupada = df_est["intervalos"] \
    .value_counts() \
    .sort_index() \
    .reset_index()

tabla_agrupada.columns = ["intervalos", "fi"]

# marca de clase
tabla_agrupada["marca_clase"] = tabla_agrupada["intervalos"] \
    .apply(lambda x: x.mid)

# frecuencia relativa
tabla_agrupada["hi"] = tabla_agrupada["fi"] / len(df_est)

# frecuencia relativa porcentual
tabla_agrupada["hip"] = tabla_agrupada["hi"] * 100

# frecuencia acumulada
tabla_agrupada["Fi"] = tabla_agrupada["fi"].cumsum()

# frecuencia relativa acumulada
tabla_agrupada["Hi"] = tabla_agrupada["hi"].cumsum()

st.dataframe(tabla_agrupada)

# ----------------------------------------
# HISTOGRAMA Y POLIGONO
# ----------------------------------------

st.subheader("Histograma de Edades")

fig, ax = plt.subplots(figsize=(12,6))

# histograma
ax.hist(
    df_est['edad'],
    bins=cortes,
    color='#1fcaa0',
    edgecolor='white',
    alpha=0.6,
    label='Histograma'
)

# poligono
ax.plot(
    tabla_agrupada['marca_clase'],
    tabla_agrupada['fi'],
    color='red',
    marker='D',
    linewidth=2,
    label='Polígono'
)

ax.set_title(
    'DISTRIBUCIÓN DE EDADES',
    fontweight='bold'
)

ax.set_xlabel('Edades')

ax.set_ylabel('Frecuencia')

ax.legend()

st.pyplot(fig)

# ----------------------------------------
# OJIVA
# ----------------------------------------

st.subheader("Ojiva de Frecuencia Acumulada")

fig, ax = plt.subplots(figsize=(10,5))

ax.plot(
    tabla_agrupada['marca_clase'],
    tabla_agrupada['Fi'],
    color='red',
    marker='s',
    linewidth=2,
    label='Ojiva'
)

ax.fill_between(
    tabla_agrupada['marca_clase'],
    tabla_agrupada['Fi'],
    color='purple',
    alpha=0.3
)

ax.set_title(
    'FRECUENCIA ACUMULADA',
    fontweight='bold'
)

ax.set_xlabel('Marca de Clase')

ax.set_ylabel('Frecuencia Acumulada')

ax.legend()

st.pyplot(fig)

# ----------------------------------------
# GRAFICO DE TORTA
# ----------------------------------------

st.subheader("Gráfico de Torta")

fig, ax = plt.subplots(figsize=(8,8))

ax.pie(
    frec_cualita['hi'],
    labels=frec_cualita['carrera'],
    autopct='%1.1f%%',
    startangle=90,
    colors=sns.color_palette('pastel')
)

ax.set_title(
    "PORCENTAJE DE ESTUDIANTES POR CARRERA",
    fontweight="bold"
)

st.pyplot(fig)