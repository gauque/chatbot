def new_func():
    pip3 install pandas - -upgrade

new_func()


import pandas as pd

 

# Create mock data frame

data = {

    'Gerente': ['Gerente A', 'Gerente B', 'Gerente A', 'Gerente B', 'Gerente A'],

    'BU': ['BU1', 'BU1', 'BU2', 'BU2', 'BU3'],

    'Producto': ['Producto 1', 'Producto 2', 'Producto 3', 'Producto 4', 'Producto 5'],

    'Estado Final': ['Ganado', 'Perdido', 'Ganado', 'Ganado', 'Perdido'],

    'Valor': [1000.0, 2000.0, 3000.0, 4000.0, 5000.0],

    'Date of creation': ['2020-01-01', '2020-02-01', '2020-01-01', '2021-02-01', '2022-01-01'],

    'Date of Completion': ['2020-06-01', '2020-04-01', '2020-05-01', '2021-04-01', '2022-02-01']

}

df = pd.DataFrame(data)

 

# Define the win rate calculation function

def win_rate_calculation(df, start_date, end_date):

    df = df.loc[(df['Date of creation'] >= start_date) & (df['Date of creation'] <= end_date)]

    df['Year'] = pd.DatetimeIndex(df['Date of creation']).year

    win_count = df.loc[df['Estado Final'] == 'Ganado'].groupby(['Year', 'Gerente', 'BU', 'Producto'])['Valor'].sum()

    total_count = df.loc[df['Estado Final'].isin(['Ganado', 'Perdido'])].groupby(['Year', 'Gerente', 'BU', 'Producto'])['Valor'].sum()

    win_rate_valor = win_count.div(total_count, level=['Year', 'Gerente', 'BU', 'Producto']).reset_index(name='Win rate valor')

    win_count2 = df.loc[df['Estado Final'] == 'Ganado'].groupby(['Year', 'Gerente', 'BU', 'Producto'])['Estado Final'].count()

    total_count2 = df.loc[df['Estado Final'].isin(['Ganado', 'Perdido'])].groupby(['Year', 'Gerente', 'BU', 'Producto'])['Estado Final'].count()

    win_rate_numero = win_count2.div(total_count2, level=['Year', 'Gerente', 'BU', 'Producto']).reset_index(name='Win rate numero')

    return pd.merge(win_rate_valor, win_rate_numero, on=['Year', 'Gerente', 'BU', 'Producto'])

 

# Call the win rate calculation function

results = win_rate_calculation(df, '2019-01-01', '2022-12-31')

 

# Print the results

print(results)