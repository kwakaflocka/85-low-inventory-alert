import pandas as pd
from mssql_dataframe import SQLServer

import main
import sendsms

server = 'LOCALHOST\SQLEXPRESS'
database = 'NewInventoryDb'
username='sa'
password='123456'
sql = SQLServer(database=database, server=server, username=username, password=password, driver='ODBC Driver 17 for SQL Server')
data=""
Yesterday=main.yesterday
#import AllItemsReport csv into a dataframe
def csvtodf():
    path=fr'C:\Users\sabri\Desktop\Toast\{Yesterday}\AllItemsReport.csv'
    df=pd.read_csv(path)
    print(df)
    return df

def loadsqlfromcsv():
    dailyreports_df = csvtodf()
    #add date column to data frame
    dailyreports_df['Date'] = Yesterday
    #delete yesterday's dataloadfromcsv table
    try:
        cursor = sql.connection.cursor()
        sqlstr='exec spDel_dataloadfromcsv'
        cursor.execute(sqlstr)
        print(f"Deleted {Yesterday} dataloadfromcsv")
    except:
        print(f'Try: delete {Yesterday} dataloadfromcsv but did not exist. Creating new dataloadfromcsv')
        pass
    print(f"Creating 'dataloadfromcsv' SQL table with {Yesterday}")

#dataloadfromcsv is a temporary table and is inserted into history_dataloadfromcsv to keep an archive
#of report information
    sql.create.table_from_dataframe(table_name='dataloadfromcsv', dataframe=dailyreports_df)
    print(dailyreports_df)
    sql.write.insert(table_name='history_dataloadfromcsv', dataframe=dailyreports_df)

#execute the stored procedures to perform the calculations and update/check the inventory
def sqlstoredprocedure(sp):
    cursor=sql.connection.cursor()
    sqlstr=f'exec {sp}'
    cursor.execute(sqlstr)
    if sp == 'spCheckMin': #this calls sendsms.py to send a text alerting what items need to be ordered
        data=cursor.fetchval()
        if data:
            print(f"{data}: Order more")
            sendsms.inventorySMS(data)
            return data
        else:
            print("Inventory quantities sufficient. No ordering necessary")


loadsqlfromcsv()

#Execute stored procedures
#'ReportItemsUsed' uses the Toast sales report and inventory quantities in the database to calculate quantity of ingredients used according to each report
#'spUpdateIngredient' updates the inventory quantities by subtracting quantities from 'ReportItemsUsed'
#'spCheckMin' checks current inventory quantity against minimum threshold
sqlstoredprocedure('ReportItemsUsed')
sqlstoredprocedure('spUpdateIngredient')
sqlstoredprocedure('spCheckMin')

