import sqlite3
conn = sqlite3.connect("voting.db")
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS votes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_name TEXT NOT NULL
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS admins(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")

c.execute("SELECT * FROM admins WHERE username = 'admin'")
if not c.fetchone():
    c.execute("INSERT INTO admins(username, password) VALUES(?, ?)", ("admin", "admin123"))
conn.commit()
conn.close()
print("Database initialized successfully with users, votes, and admins tables.")
