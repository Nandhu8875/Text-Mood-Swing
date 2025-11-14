import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("chat.db")

# Read tables into DataFrames
messages_df = pd.read_sql_query("SELECT * FROM messages", conn)
emojis_df = pd.read_sql_query("SELECT * FROM emojis", conn)
sentiment_df = pd.read_sql_query("SELECT * FROM sentiment", conn)
stats_df = pd.read_sql_query("SELECT * FROM stats", conn)

# Write to Excel file
with pd.ExcelWriter("whatsapp_analysis.xlsx") as writer:
    messages_df.to_excel(writer, sheet_name="Messages", index=False)
    emojis_df.to_excel(writer, sheet_name="Emojis", index=False)
    sentiment_df.to_excel(writer, sheet_name="Sentiment", index=False)
    stats_df.to_excel(writer, sheet_name="Stats", index=False)

print("Export complete! File saved as whatsapp_analysis.xlsx")
