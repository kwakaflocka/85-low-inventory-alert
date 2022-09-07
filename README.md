# inventory-alert-85
Restaurants are able to request data exports from Toast which exports a summary of sales to an Amazon S3 bucket every night. 
By creating an inventory/recipe database you can use this program to download these reports to your desktop to calculate how much inventory has been gone through at the end of every night. 

"85" because it's before something is "86'd" :-)


-main.py downloads sales summary AllItemsReport.csv from Toast

 -example of Toast's AllItemsReport.csv is included (lives in the YYYYMMDD folder in Toast's Amazon S3 bucket)

-'NewInventoryDb_LogBackup_2022-09-01_23-50-56.bak' an example of the SQL inventory database. I've only filled out the quantities and recipes for drinks but it does have  the full menu with placeholder variables

-database.py connects to local desktop NewInventoryDb, executes stored procedures to load AllItemsReport.csv data into the database, calculate ingredients used according to the report, and updates the inventory quantities and checks for ingredients falling below a minimum threshold

-sendsms.py is called to send an SMS if any ingredient in the "Ingredient" table in InventoryDb falls below a minimum threshold value
