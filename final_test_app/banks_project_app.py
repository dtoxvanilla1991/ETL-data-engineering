# Code for ETL operations on Country-GDP data

# Importing the required libraries
import requests
import sqlite3
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

# global consts
url = 'https://web.archive.org/web/20230908091635 /https://en.wikipedia.org/wiki/List_of_largest_banks'
exchange_rate_csv_path = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-PY0221EN-Coursera/labs/v2/exchange_rate.csv'
table_attrs_upon_extraction = ['Name', 'MC_USD_Billion']
table_attrs_finals = ['Name', 'MC_USD_Billion', 'MC_GBP_Billion', 'MC_EUR_Billion', 'MC_INR_Billion']
output_csv_path = './Largest_banks_data.csv'
db_name = 'Banks.db'
table_name = 'Largest_banks'
log_file_name = 'code_log.txt'

def log_progress(message):
    ''' This function logs the mentioned message of a given stage of the
    code execution to a log file. Function returns nothing'''
    now = datetime.now()
    timestamp_format = '%Y-%h-%d-%H:%M:%S'
    timestamp = now.strftime(timestamp_format)
    with open(log_file_name, 'a') as f:
        f.write(timestamp + ' : ' + message + '\n')

def extract(url, table_attribs):
    ''' This function aims to extract the required
    information from the website and save it to a data frame. The
    function returns the data frame for further processing. '''
    html = requests.get(url).text
    data = BeautifulSoup(html, 'html.parser')
    df = pd.DataFrame(columns=table_attrs_upon_extraction)
    tables = data.find_all('tbody')
    rows = tables[0].find_all('tr')
    for row in rows:
        col = row.find_all('td')
        if len(col) != 0:
            bank = col[1].find_all('a')[1]['title']
            MC_USD_Billion = float(col[2].contents[0][:-1])
            data_dict = {
                'Name': bank,
                'MC_USD_Billion': MC_USD_Billion
            }
            df1 = pd.DataFrame(data_dict, index=[0])
            df = pd.concat([df,df1], ignore_index=True)

    return df

def transform(df, csv_path):
    ''' This function accesses the CSV file for exchange rate
    information, and adds three columns to the data frame, each
    containing the transformed version of Market Cap column to
    respective currencies'''
    dataframe = pd.read_csv(csv_path)
    exchange_rate = dataframe.set_index('Currency')['Rate'].to_dict()
    # Add MC_GBP_Billion column
    df['MC_GBP_Billion'] = [np.round(x * exchange_rate['GBP'],2) for x in df['MC_USD_Billion']]
    #Add MC_EUR_Billion column
    df['MC_EUR_Billion'] = [np.round(x * exchange_rate['EUR'],2) for x in df['MC_USD_Billion']]
    # Add MC_INR_Billion column
    df['MC_INR_Billion'] = [np.round(x * exchange_rate['INR'],2) for x in df['MC_USD_Billion']]
    return df

def load_to_csv(df, output_path):
    ''' This function saves the final data frame as a CSV file in
    the provided path. Function returns nothing.'''
    df.to_csv(output_csv_path)

def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final data frame to a database
    table with the provided name. Function returns nothing.'''
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)

def run_query(query_statement, sql_connection):
    ''' This function runs the query on the database table and
    prints the output on the terminal. Function returns nothing. '''
    print(query_statement)
    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_output)

''' Here, you define the required entities and call the relevant
functions in the correct order to complete the project. Note that this
portion is not inside any function.'''
log_progress('Preliminaries complete. Initiating ETL process')

df = extract(url, table_attrs_upon_extraction)
log_progress('Data extraction complete. Initiating Transformation process')

df = transform(df, exchange_rate_csv_path)
log_progress('Data transformation complete. Initiating loading process')

load_to_csv(df, output_csv_path)
log_progress('Data saved to CSV file')

sql_connection = sqlite3.connect(db_name)
log_progress('SQL Connection established')

load_to_db(df, sql_connection, table_name)
log_progress('Data loaded to Database as a table, Executing queries')

query_statement = f"SELECT * FROM Largest_banks"
run_query(query_statement, sql_connection)

query_statement = f"SELECT AVG(MC_GBP_Billion) FROM Largest_banks"
run_query(query_statement, sql_connection)

query_statement = f"SELECT Name from Largest_banks LIMIT 5"
run_query(query_statement, sql_connection)

log_progress('Process Complete!')

sql_connection.close()

log_progress('Server closed!')