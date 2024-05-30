import sqlite3
import pandas as pd

# todo: implement cleaning up columns. manually changed column names to have easier to query db columns
# would be better if original excel can become drop-in

cxn = sqlite3.connect('app/repairdata.sqlite')
wb = pd.read_excel('repairs-en.xlsx',sheet_name = 'repairs-en')
wb.to_sql(name='repairs',con=cxn,if_exists='replace',index=True)
cxn.commit()
cxn.close()
