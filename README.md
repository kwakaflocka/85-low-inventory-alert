# inventory-alert-85
Restaurants are able to request data exports from Toast which exports a summary of sales to an Amazon S3 bucket every night. 
By creating an inventory/recipe database you can use this program to download these reports to your desktop to calculate how much inventory has been gone through at the end of every night. 
"85" because it's before something is "86'd" :-)
Done:
-main.py downloads sales summary AllItemsReport.csv from Toast
  --example of Toast's AllItemsReport.csv is included (lives in the YYYYMMDD folder in Toast's Amazon S3 bucket)
-structured InventoryDb is included as 'InventoryDbExample.bacpac')
-database.py connects to local desktop InventoryDb, SQL statements to import relevant columns from Toast's reports

TODO:
-database.py implement SQL queries to update ingredient quantities
-Write email_alert.py to be triggered if an ingredient in the "Ingredient" table in InventoryDb falls below a minimum threshold value defined by user
