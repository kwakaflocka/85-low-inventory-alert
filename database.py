from datetime import datetime, timedelta
import pyodbc
import pandas as pd
from pandasql import sqldf
pysqldf = lambda q: sqldf(q, globals())

def Yesterday(frmt='%Y-%m-%d', string=True):
    yesterday=datetime.now()-timedelta(1)
    if string:
        return yesterday.strftime(frmt)
    return yesterday
## convert to YYYYMMDD
yesterday=Yesterday()
def remove_hyphens(string):
    string=string.replace('-', '')
    return string
yesterday=remove_hyphens(yesterday)

#either set date=yesterday or provide a date in YYYYMMDD if you have a specific date you want to download. Toast stores up to 3 weeks worth of files
date=yesterday

server = 'DESKTOP\SQLEXPRESS'
database = 'NewInventoryDb'
username = 'DESKTOP\sabri'
password = 'itsasecret'
tcon='y'
cnxn = pyodbc.connect(driver='{SQL Server}', host=server, database=database,
                      trusted_connection=tcon, user=username, password=password)

if cnxn:
    print('True')
cursor = cnxn.cursor()

def Read(cnxn):
    table_name=str(input("What table do you want to read from?"))
    print('Read')
    cursor.execute(f'SELECT * FROM {table_name}')
    for row in cursor:
        print(row)
    cnxn.commit()

def Insert(cnxn):
    print('Write')
    table_name=input('What table do you want to write to?')
    column_name=input('What column do you want to write to?')
    entry= input('What do you want to insert?')
    insert_stmt = (
        f"INSERT INTO {table_name} ({column_name}) VALUES ({entry})"
    )
    cursor.execute(insert_stmt)

    #preview insert statement
    print('Read')
    cursor.execute(f'SELECT * FROM {table_name}')
    for row in cursor:
        print(row)

    cnxn.commit()


#SQL statement to update Ingredient table with new QuantityAvailable with # Orders from AllItemsReport (downloaded from Toast AWS bucket)
sqlUpdateIngredient= """("update Ingredient"
      "set"
      "QuantityAvailable = ISNULL(QuantityAvailable - (select sum(mii.Quantity * a.[  # Orders]) as QtyOfIngUsed)"
      "from MenuItem m"
      "inner join AllItemsReport1 a"
      "on m.Name = a.[Menu Item]"
      "inner join MenuItemIngredient mii"
      "on mii.MenuItemId = m.MenuItemId"
      "inner join Ingredient i"
      "on mii.IngredientId = i.IngredientId"
      "where i.IngredientId = ix.IngredientId"
      "group by m.MenuItemId, m.Name, i.Name, mii.IngredientId), ix.QuantityAvailable)"
      "from Ingredient ix")
"""

#Created DailyReport table in NewInventoryDb to be updated daily:
# cursor.execute('''
# 		CREATE TABLE DailyReport (
# 			MasterID int primary key,
# 			MenuItem nvarchar(50),
# 			ItemQty int
# 			)
#                ''')
# cnxn.commit()

# 2) Import AllItemsReport.csv into a DataFrame TODO:change path to Toast\{date}\AllItemsReport after everything else works
data= pd.read_csv(rf'C:\Users\sabri\Desktop\Toast\20220801\AllItemsReport.csv')
df=pd.DataFrame(data)
df.columns = df.columns.str.replace(' ','')
df = df.fillna(value=0)

# 3) Create a df Table for AllItemsReport.csv with columns Master ID, Menu Item, Item Qty
select = """SELECT MenuItem, SUM(ItemQty) as ItemQty
FROM df
GROUP BY MenuItem;"""
report = pysqldf(select)
report=report.fillna(value=0)
# print({date})
print(report)


# 4) Insert DataFrame Data into the Table TODO: how to handle duplicate MenuItem records

#Start here: Fix Error for sqlInsert: Violation of PRIMARY KEY constraint 'PK__AllItems__F6B782C4E21BCAD4'. Cannot insert duplicate key in object 'dbo.DailyReport'. The duplicate key value is (HH Buffalo Wings).
#https://www.tutorialspoint.com/sql/sql-check.htm 1) Use constraints to avoid duplicate insertion and 2) if duplicate, add ItemQty to existing column
sqlInsert="""
INSERT INTO [DailyReport] (MenuItem,ItemQty) values(?,?)
"""

testsql="""
ALTER TABLE DAILY REPORT
    INSERT INTO (MenuItem,ItemQty) values(?,?) UNIQUE(MenuItem) 
"""

for index,row in report.iterrows():
    newVals = row['MenuItem'], row['ItemQty']

    cursor.execute(testsql,newVals)

df.to_sql('AllItemsReport', con=cnxn, if_exists='replace')


cnxn.execute(sql)
cnxn.commit()
cursor.close()
