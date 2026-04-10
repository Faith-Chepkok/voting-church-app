import sqlite3
import random
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "church_ballot_999"

def get_db():
    db = sqlite3.connect('database.db')
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, password TEXT)')
    db.execute('CREATE TABLE IF NOT EXISTS votes (id INTEGER PRIMARY KEY AUTOINCREMENT, member_email TEXT, group_name TEXT)')
    db.commit()
    db.close()

init_db()

@app.route("/")
def main_home():
    return render_template("index.html")
@app.route("/register", methods=["GET", "POST"])
def member_reg():
    if request.method == "POST":
        email = request.form.get("email")
        pw = request.form.get("password")
        db = get_db()
        db.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        db.commit()
        db.close()
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def member_login():
    if request.method == "POST":
        email = request.form.get("email")
        pw = request.form.get("password")
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password)).fetchone()
        db.close()
        if user:
            session["user_email"] = email
            return redirect("/vote_panel")
        return "Login Failed", 401
    return render_template("login.html")

@app.route("/vote_panel")
def vote_panel():
    if "user_email" not in session:
        return redirect("/login")
    return render_template("vote.html")
@app.route("/cast_vote", methods=["POST"])
def cast_vote():
    groups = [
        "Beryl", "Chrystolite", "Coral", "Amber", "Lapiz Lazuli", "Ruby", "Carnelian", 
        "Topaz", "Pearl", "Sardonyx", "Sapphire", "Amethyst", "Jacinth", "Turquoise", 
        "Garnet", "Crystal", "Onyx", "Jasper", "Leshem", "Agate", "Emerald", "Chalcedony", 
        "Peridot", "Sardius", "Chrysoprase", "Ligure", "Jade", "Helecidoni", "lulu", 
        "Akiki", "Jasi", "Zumaradi", "Taluku", "Yakuti", "Almasi"
    ]
    assigned = random.choice(groups)
    email = session.get("user_email")
    db = get_db()
    db.execute("INSERT INTO votes (member_email, group_name) VALUES (?, ?)", (email, assigned))
    db.commit()
    db.close()
    return redirect("/results")

@app.route("/results")
def view_results():
    db = get_db()
    data = db.execute("SELECT group_name, COUNT(*) as total FROM votes GROUP BY group_name ORDER BY total DESC").fetchall()
    db.close()
    return render_template("results.html", results=data)

if __name__ == "__main__":
    app.run(debug=True)






