import sqlite3
import random
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "super_secret_key" 
def get_db():
    db = sqlite3.connect('database.db')
    db.row_factory = sqlite3.Row
    return db
    def init_db():
      db = get_db()
      db.execute('''CREATE TABLE IF NOT EXISTS votes 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   member_email TEXT, 
                   group_name TEXT)''')
    db.execute('''CREATE TABLE IF NOT EXISTS users 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   email TEXT, 
                   password TEXT)''')
    db.commit()
    db.close()
init_db()

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password)).fetchone()
        db.close()
        
        if user:
            session["user_id"] = user[0] 
            return redirect("/") 
        else:
            return "Invalid email or password", 401
            
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        return redirect("/")
    return render_template("register.html")


@app.route("/vote", methods=["GET", "POST"])
def vote():
    db = get_db()
    existing = False 

    if request.method == "POST":
        if existing:
            return "You have already voted."

        groups = ["Group A", "Group B"] 
        email = "test@example.com"     
        
        random_name = random.choice(groups)
        db.execute("INSERT INTO votes (member_email, group_name) VALUES (?, ?)", (email, random_name))
        db.commit()
        db.close()
        return redirect("/results")

    return render_template("vote.html", existing=existing)
@app.route("/")
def home():
    return render_template("index.html") 
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
    db.close()
    
    return render_template("admin_dashboard.html", total_users=users_count, total_votes=votes_count)

@app.route("/results")  
def results():
    db = get_db() 
    query = "SELECT group_name, COUNT(*) as total FROM votes GROUP BY group_name"
    results = db.execute(query).fetchall()
    db.close()
    return render_template("results.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)



