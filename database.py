import pyodbc

#Connect
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = 'DESKTOP\SQLEXPRESS'
database = 'NewInventoryDb'
username = 'DESKTOP\sabri'
password = '1900'
tcon='y'
cnxn = pyodbc.connect(driver='{SQL Server}', host=server, database=database,
                      trusted_connection=tcon, user=username, password=password)
cursor = cnxn.cursor()



sql= """("update Ingredient"
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
""""
#Run query
cursor.execute()
"""
print(cursor.execute("SELECT Name FROM Ingredient"))

rows = cursor.fetchall()
for row in rows:
    print(row)