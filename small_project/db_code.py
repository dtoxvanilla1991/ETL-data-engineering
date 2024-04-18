import sqlite3
import pandas as pd

conn = sqlite3.connect('STAFF.db')

table_name = 'INSTRUCTOR'
attribute_list = ['ID', 'FNAME', 'LNAME', 'CITY', 'CCODE']

file_path = '/home/project/INSTRUCTOR.csv'
df = pd.read_csv(file_path, names = attribute_list)
df.to_sql(table_name, conn, if_exists = 'replace', index= False)
print('Table is ready')

query_statement = f"SELECT * FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

query_statement = f"SELECT FNAME FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

query_statement = f"SELECT COUNT(*) FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

data_dict = {
    'ID': [100],
    'FNAME' : ['John'],
    'LNAME' : ['Doe'],
    'CITY' : ['Paris'],
    'CCODE' : ['FR']
}
data_append = pd.DataFrame(data_dict)

data_append.to_sql(table_name, conn, if_exists = 'append', index=False)
query_statement = f"SELECT COUNT(*) FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

department_table = 'Departments'
department_attribute_list = ['DEPT_ID', 'DEP_NAME', 'MANAGER_ID', 'LOC_ID']
file_path='/home/project/Departments.csv'

dep_df=pd.read_csv(file_path, names = department_attribute_list)
dep_df.to_sql(department_table, conn, if_exists='replace', index=False)
print('Department Table is ready')

dep_dict = {
    'DEPT_ID': [9],
    'DEP_NAME': ['Quality Assurance'],
    "MANAGER_ID": [30010],
    "LOC_ID": ['L0010']
}
data_append=pd.DataFrame(dep_dict)
data_append.to_sql(department_table, conn, if_exists='append', index=False)
query_statement=f"SELECT COUNT(*) FROM {department_table}"
query_output=pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

query_statement=f"SELECT * from {department_table}"
query_output=pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

query_statement=f"SELECT DEP_NAME FROM {department_table}"
query_output=pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

conn.close()