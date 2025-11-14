CREATE TABLE whatsapp_chat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_date TEXT,
    chat_time TEXT,
    sender TEXT,
    message TEXT,
    sentiment_score FLOAT,
    mood TEXT,
    emoji TEXT
);
