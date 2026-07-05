import sqlite3

def init_db():
    conn = sqlite3.connect("leads.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            author TEXT,
            url TEXT UNIQUE,
            text TEXT,
            is_genuine INTEGER,
            confidence_score REAL,
            summary TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

    # Migrate older databases that only had (id, author, url, text)
    existing_columns = [row[1] for row in cursor.execute("PRAGMA table_info(leads)").fetchall()]
    migrations = {
        "source": "TEXT",
        "is_genuine": "INTEGER",
        "confidence_score": "REAL",
        "summary": "TEXT",
        "created_at": "TEXT"
    }
    for column, col_type in migrations.items():
        if column not in existing_columns:
            cursor.execute(f"ALTER TABLE leads ADD COLUMN {column} {col_type}")
            conn.commit()

    conn.close()


def insert_lead(source, author, url, text, is_genuine, confidence_score, summary):
    conn = sqlite3.connect("leads.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT INTO leads (source, author, url, text, is_genuine, confidence_score, summary)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (source, author, url, text, 1 if is_genuine else 0, confidence_score, summary)
        )
        conn.commit()
        tag = "GENUINE" if is_genuine else "logged (not genuine)"
        print(f"Saved {tag} — {author} ({source})")
    except sqlite3.IntegrityError:
        print(f"Already saved, skipping: {url}")
    finally:
        conn.close()


init_db()
print("Database ready")