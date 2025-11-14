import re
import sqlite3
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import emoji

# Create / connect to SQLite DB
conn = sqlite3.connect("chat.db")
cur = conn.cursor()

# Create table
cur.execute("""
CREATE TABLE IF NOT EXISTS whatsapp_chat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_date TEXT,
    chat_time TEXT,
    sender TEXT,
    message TEXT,
    sentiment_score FLOAT,
    mood TEXT,
    emoji TEXT
);
""")

# Function to insert data
def insert(row):
    cur.execute(
        "INSERT INTO whatsapp_chat (chat_date, chat_time, sender, message) VALUES (?, ?, ?, ?)",
        row
    )

# WhatsApp chat pattern
pattern = r"(\d{2}/\d{2}/\d{4}), (\d{1,2}:\d{2} [APM]{2}) - (.*?): (.*)"

# Read chat.txt
with open("chat.txt", "r", encoding="utf-8") as f:
    for line in f:
        match = re.match(pattern, line)
        if match:
            insert(match.groups())

conn.commit()

# Sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Fetch messages
rows = cur.execute("SELECT id, message FROM whatsapp_chat").fetchall()

# Update each row with sentiment + mood + emoji
for rid, msg in rows:
    score = sia.polarity_scores(msg)["compound"]

    if score > 0.4:
        mood = "Happy"
    elif score < -0.4:
        mood = "Angry/Sad"
    else:
        mood = "Neutral"

    extracted_emoji = ''.join(c for c in msg if c in emoji.EMOJI_DATA)

    cur.execute(
        "UPDATE whatsapp_chat SET sentiment_score=?, mood=?, emoji=? WHERE id=?",
        (score, mood, extracted_emoji, rid)
    )

conn.commit()
conn.close()

print("Processing complete! Check chat.db for results.")
