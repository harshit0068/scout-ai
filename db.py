import sqlite3

def init_db():
    conn = sqlite3.connect("leads.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT,
            url TEXT UNIQUE,
            text TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()
print("Database ready")
def insert_lead(author, url, text):
    conn = sqlite3.connect("leads.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO leads (author, url, text) VALUES (?, ?, ?)",
            (author, url, text)
        )
        conn.commit()
        print(f"Saved lead from {author}")
    except sqlite3.IntegrityError:
        print(f"Already saved, skipping: {url}")
    finally:
        conn.close()