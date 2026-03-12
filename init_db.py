import sqlite3

# Connect to the database (creates file if it doesn't exist)
conn = sqlite3.connect("voting.db")
c = conn.cursor()

# Create users table
c.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")

# Create votes table
c.execute("""
CREATE TABLE IF NOT EXISTS votes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_name TEXT NOT NULL
)
""")

# Optional: Create admin table (if you want multiple admins)
c.execute("""
CREATE TABLE IF NOT EXISTS admins(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")

# Insert default admin if not exists
c.execute("SELECT * FROM admins WHERE username = 'admin'")
if not c.fetchone():
    c.execute("INSERT INTO admins(username, password) VALUES(?, ?)", ("admin", "admin123"))

conn.commit()
conn.close()
print("Database initialized successfully with users, votes, and admins tables.")