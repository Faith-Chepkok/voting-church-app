import sqlite3 
from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = "super_secret_key" 
@app.route("/")
def home():
    return redirect("/vote")


@app.route("/vote", methods=["GET", "POST"])
def vote():
    db = get_db()
    import sqlite3

def get_db():
    
    db = sqlite3.connect('database.db')
    db.row_factory = sqlite3.Row
    return db

    
    existing = False 

    if request.method == "POST":
        if existing:
            return "You have already voted."

        groups = ["Group A", "Group B"] 
        email = "test@example.com"     
        
        random_name = random.choice(groups)
        db.execute("INSERT INTO votes (member_email, group_name) VALUES (?, ?)", (email, random_name))
        db.commit()
        return redirect("/results")

    return render_template("vote.html", existing=existing)


@app.route("/admin", methods=["GET", "POST"])         
def admin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
    if username == "admin" and password == "admin123":
            session["admin"] = True
            return redirect("/admin_dashboard")
            
    return render_template("admin_login.html")

@app.route("/admin_dashboard")
def admin_dashboard():
    db = get_db()
    
    users_row = db.execute("SELECT COUNT(*) FROM users").fetchone()
    users_count = users_row[0] if users_row else 0
    
    votes_row = db.execute("SELECT COUNT(*) FROM votes").fetchone()
    votes_count = votes_row[0] if votes_row else 0
    
    return render_template("admin_dashboard.html", total_users=users_count, total_votes=votes_count)

@app.route("/results")
def results():
    db = get_db()
    
    query = "SELECT group_name, COUNT(*) as total FROM votes GROUP BY group_name"
    results = db.execute(query).fetchall()
    return render_template("results.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)


