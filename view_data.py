import sqlite3
import pandas as pd

conn = sqlite3.connect("chat.db")
df = pd.read_sql_query("SELECT * FROM whatsapp_chat", conn)
print(df)
conn.close()
