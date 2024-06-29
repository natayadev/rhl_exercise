import pandas as pd
import numpy as np
from datetime import datetime

import os

file_covid = "raw_data/covid.csv"
file_dengue = "raw_data/dengue.csv"
file_influenza = "raw_data/influenza.csv"

df_covid = pd.read_csv(file_covid)
df_dengue = pd.read_csv(file_dengue)
df_influenza = pd.read_csv(file_influenza)


# EDA: Analisis exploratorio de datos
def exploratory_analysis(dataframes):
    """ Esta función realiza el análisis de datos """
    print("------INFO------")
    print(dataframes.info())
    print("------DESCRIBE------")
    print(dataframes.describe())
    print("------DTYPES------")
    print(dataframes.dtypes)

    # Valores atípicos
    valores_nulos = dataframes.isna().sum()
    print("Valores atípicos", valores_nulos)

    # Estadísticas descriptivas
    media = np.mean(dataframes["Edad"])
    print("media: ", media)
    mediana = np.median(dataframes["Edad"])
    print("mediana: ", mediana)
    desvio_estandar = np.std(dataframes["Edad"])
    print("desvio_estandar: ", desvio_estandar)


def transform_data(dataframes):
    """ Esta función realiza la transformación de datos """

    # Cambiar el índice del df
    dataframes = dataframes.set_index('id')

    # Renombrar los encabezados de las columnas
    diccionario_columnas = {"first_name": "Nombre",
                            "last_name": "Apellido",
                            "email": "Correo",
                            "phone": "Contacto",
                            "gender": "Género",
                            "birth": "Fecha Nac.",
                            "dengue": "Analisis Dengue",
                            "covid": "Analisis Covid",
                            "influenza": "Analisis Influenza",
                            "date": "Fecha Analisis"}
    dataframes = dataframes.rename(columns=diccionario_columnas)

    # Cambiar los tipos de columnas
    dataframes['Fecha Analisis'] = pd.to_datetime(dataframes['Fecha Analisis'])
    dataframes['Fecha Nac.'] = pd.to_datetime(dataframes['Fecha Nac.'])

    # Eliminar las columnas que no vamos a utilizar
    lista_cols_a_eliminar = ["Nombre", "Apellido"]
    dataframes = dataframes.drop(columns=lista_cols_a_eliminar)

    # Eliminar los valores nulos
    dataframes = dataframes.dropna()
    print(dataframes.info())

    valores_nulos = dataframes.isna().sum()
    print("Valores atípicos", valores_nulos)

    return dataframes


df_dengue = transform_data(df_dengue)
print(df_dengue.head())
df_influenza = transform_data(df_influenza)
print(df_influenza.head())
df_covid = transform_data(df_covid)
print(df_covid.head())


def concat_data(df_dengue, df_influenza, df_covid):
    dataframe = pd.concat([df_dengue, df_influenza, df_covid])

    return dataframe


dataframe = concat_data(df_dengue, df_influenza, df_covid)


def calcular_edad(dataframe):
    today = datetime.today()

    dataframe["Edad"] = dataframe["Fecha Nac."].apply(
        lambda x: today.year - x.year)
    print(dataframe.sample(25))

    return dataframe


dataframe = calcular_edad(dataframe)

exploratory_analysis(dataframe)


def load_processed_data(dataframe):
    if not os.path.exists("processed_data"):
        os.makedirs("processed_data")

    dataframe.to_csv("processed_data/combined_data.csv")


load_processed_data(dataframe)