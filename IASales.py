# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 14:21:40 2023

@author: gauquebauz001
"""

import pandas as pd
import numpy as np

# Define variables
estado_final_values = ["Perdido","Ganado","Abierto"]
gerente_values = ["Alice","Bob","Charlie"]
bu_values = ["BU1","BU2","BU3"]
producto_values = ["Producto1","Producto2","Producto3"]

# Define win rate calculation function
def win_rate_calculation(df):

    # Convert date variables to pandas datetime format

    df["Date of creation"] = pd.to_datetime(df["Date of creation"])

    df["Date of Completion"] = pd.to_datetime(df["Date of Completion"])

 

    # Group by distinct combinations of "Gerente", "BU", "Producto", and year of "Date of creation"

    group_df = df.groupby([pd.Grouper(key="Date of creation", freq="YS"), "Gerente", "BU", "Producto", pd.Grouper(key="Date of Completion", freq="YS"), "Estado Final"])

 

    # Calculate sum of "Valor" for each group

    group_df = group_df.agg({"Valor": "sum"})

 

    # Calculate count of "Estado Final" for each group

    count_df = df.groupby([pd.Grouper(key="Date of creation", freq="YS"), "Gerente", "BU", "Producto", pd.Grouper(key="Date of Completion", freq="YS"), "Estado Final"]).count()

    count_df = count_df["Valor"]

    count_df.name = "Estado Final Count"

 

    # Merge the sum and count dataframes

    merge_df = pd.merge(group_df, count_df, on=["Date of creation", "Gerente", "BU", "Producto", "Date of Completion", "Estado Final"], how="left")

 

    # Pivot the table to make "Estado Final" values as columns

    pivot_df = pd.pivot_table(merge_df, values=["Valor", "Estado Final Count"], index=["Date of creation", "Gerente", "BU", "Producto", "Date of Completion"], columns=["Estado Final"], fill_value=0)

 

    # Calculate win rate as the division between the sum of "Valor" for "Estado Final"=="Ganado" and the sum of "Valor" for "Estado Final"=="Ganado" or "Estado Final"=="Perdido"

    win_rate_df = pd.DataFrame()

    win_rate_df["Win Rate Valor"] = pivot_df[("Valor", "Ganado")]/(pivot_df[("Valor", "Ganado")]+pivot_df[("Valor", "Perdido")])

    win_rate_df["Win Rate Numero"] = pivot_df[("Estado Final Count", "Ganado")]/(pivot_df[("Estado Final Count", "Ganado")]+pivot_df[("Estado Final Count", "Perdido")])

 

    # Reset index to convert grouped columns into individual columns

    win_rate_df = win_rate_df.reset_index()

 

    return win_rate_df


# Generate mock dataframe
n_rows = 1000
np.random.seed(1)
df = pd.DataFrame({
    "Estado Final": np.random.choice(estado_final_values, size=n_rows),
    "Valor": np.random.uniform(low=0.0, high=1000.0, size=n_rows),
    "Gerente": np.random.choice(gerente_values, size=n_rows),
    "BU": np.random.choice(bu_values, size=n_rows),
    "Producto": np.random.choice(producto_values, size=n_rows),
    "Date of creation": pd.date_range(start="2020-01-01", end="2022-12-31", periods=n_rows),
    "Date of Completion": pd.date_range(start="2020-01-01", end="2022-12-31", periods=n_rows) + pd.to_timedelta(np.random.uniform(low=0, high=365*2, size=n_rows)), #Modified to inclued Date of completio
    })

win_rate_df=win_rate_calculation(df)

