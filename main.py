import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os


def read_data(file_paths):
    """
    Lee los archivos CSV y devuelve un diccionario de DataFrames.
    """
    dataframes = {}
    for key, path in file_paths.items():
        dataframes[key] = pd.read_csv(path)
    return dataframes


def transform_data(df):
    """
    Realiza la transformación de datos sobre un DataFrame.
    """
    df = df.set_index('id')
    diccionario_columnas = {
        "first_name": "Nombre",
        "last_name": "Apellido",
        "email": "Correo",
        "phone": "Contacto",
        "gender": "Género",
        "birth": "Fecha Nac.",
        "dengue": "Analisis Dengue",
        "covid": "Analisis Covid",
        "influenza": "Analisis Influenza",
        "date": "Fecha Analisis"
    }
    df = df.rename(columns=diccionario_columnas)
    df['Fecha Analisis'] = pd.to_datetime(df['Fecha Analisis'])
    df['Fecha Nac.'] = pd.to_datetime(df['Fecha Nac.'])
    df = df.drop(columns=["Nombre", "Apellido"], errors='ignore')
    df = df.dropna()

    today = datetime.today()
    df["Edad"] = today.year - df["Fecha Nac."].dt.year

    return df


def concat_data(dfs):
    """
    Concatena múltiples DataFrames en uno solo y coloca 'Fecha Analisis' y 'Edad' al final.
    """
    combined_df = pd.concat(dfs, ignore_index=True)

    # Reorganizar columnas para que 'Fecha Analisis' y 'Edad' sean las últimas
    cols = [col for col in combined_df.columns if col not in [
        "Fecha Analisis", "Edad"]] + ["Fecha Analisis", "Edad"]
    combined_df = combined_df[cols]

    return combined_df


def exploratory_analysis(df_combined, output_dir):
    """
    Realiza un análisis exploratorio de datos sobre el DataFrame combinado y guarda los gráficos en el directorio especificado.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Añadir líneas divisorias y saltos de línea en los prints
    separator = "-" * 40
    print(f"\n{separator}\nINFO\n{separator}")
    print(df_combined.info())

    print(f"\n{separator}\nDESCRIBE\n{separator}")
    print(df_combined.describe())

    print(f"\n{separator}\nDTYPES\n{separator}")
    print(df_combined.dtypes)

    print(f"\n{separator}\nNULL VALUES\n{separator}")
    print(df_combined.isna().sum())

# Estilo visual para los gráficos
    style_params = {
        'marker': '*',
        'linestyle': '--',
        'grid_color': 'tab:grey',
    }

    # Gráfico de barras para la distribución por género
    plt.figure(figsize=(8, 6))
    df_combined['Género'].value_counts().plot(
        kind='bar', color='pink', edgecolor='black')
    plt.title('Distribución por Género')
    plt.xlabel('Género')
    plt.ylabel('Cantidad de Pacientes')
    plt.grid(color=style_params['grid_color'],
             linestyle=style_params['linestyle'], alpha=0.6)
    plt.savefig(os.path.join(output_dir, 'distribucion_genero.png'))
    plt.close()

    # Gráfico de barras para la cantidad de pacientes con cada tipo de análisis
    plt.figure(figsize=(8, 6))
    df_combined[['Analisis Influenza', 'Analisis Dengue', 'Analisis Covid']].sum(
    ).plot(kind='bar', color=['violet', 'orange', 'pink'], edgecolor='black')
    plt.title('Cantidad de Pacientes por Tipo de Análisis')
    plt.xlabel('Tipo de Análisis')
    plt.ylabel('Cantidad de Pacientes')
    plt.grid(color=style_params['grid_color'],
             linestyle=style_params['linestyle'], alpha=0.6)
    plt.savefig(os.path.join(output_dir, 'cantidad_pacientes.png'))
    plt.close()

    # Histograma de edades
    plt.figure(figsize=(8, 6))
    plt.hist(df_combined['Edad'], bins=10, edgecolor='black', color='purple')
    plt.title('Distribución de Edades')
    plt.xlabel('Edad')
    plt.ylabel('Cantidad de Pacientes')
    plt.grid(color=style_params['grid_color'],
             linestyle=style_params['linestyle'], alpha=0.6)
    plt.savefig(os.path.join(output_dir, 'distribucion_edades.png'))
    plt.close()


def load_processed_data(df, output_path):
    """
    Guarda el DataFrame procesado en un archivo CSV.
    """
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))
    df.to_csv(output_path, index=False)


# Rutas de archivos
file_paths = {
    "covid": "raw_data/covid.csv",
    "dengue": "raw_data/dengue.csv",
    "influenza": "raw_data/influenza.csv"
}

# Leer datos
dataframes = read_data(file_paths)

# Transformación de datos
transformed_dataframes = {name: transform_data(
    df) for name, df in dataframes.items()}

# Concatenar DataFrames transformados
df_combined = concat_data(transformed_dataframes.values())
print(df_combined)

# EDA: Análisis exploratorio de datos combinados y guardar gráficos
exploratory_analysis(df_combined, "dataviz")

# Guardar datos procesados
load_processed_data(df_combined, "processed_data/combined_data.csv")
