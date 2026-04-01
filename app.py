from flask import Flask,render_template,request,redirect,session
import sqlite3
import random

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("voting.db")
    conn.row_factory = sqlite3.Row
    return conn
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        db = get_db()
        db.execute("INSERT INTO users(name,email,password) VALUES(?,?,?)", (name,email,password))
        db.commit()
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email=? AND password=?", (email,password)).fetchone()
        if user:
            return redirect("/vote")
    return render_template("login.html")
@app.route("/vote", methods=["GET","POST"])
def vote():
    db=get_db()
    email=session.get("user")
    if not email:
        return redirect("/login")
    existing=db.execute("SELECT*FROM votes WHERE member_email=?",(email,)).fetchone
    if existing:
        return "You have already voted."
    if request.method=="POST":
        group=request.form["group"]
        db.execute("INSERT INTO votes9member_email,group_name)VALUES(?,?)"(email,group))
        db.commit()
        return redirect("/results")
    random_group=random.choice(groups)
    return render_template("vote.html",group=groups,random_group=random_group)
    groups = [
        "Beryl","Chrystolite","Coral","Amber","Lapiz Lazuli",
        "Ruby","Carnelian","Topaz","Pearl","Sardonyx",
        "Sapphire","Amethyst","Jacinth","Turquoise","Garnet",
        "Crystal","Onyx","Jasper","Leshem","Agate",
        "Emerald","Chalcedony","Peridot","Sardius","Chrysoprase",
        "Ligure","Jade","Helecidoni","Lulu","Akiki",
        "Jasi","Zumaradi","Taluku","Yakuti","Almasi"
    ]
@app.route("/admin", methods=["GET","POST"])         
def admin():
    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]
        if username=="admin" and password=="admin123":
            return redirect("/admin_dashboard")
    return render_template("admin_login.html")
@app.route("/admin_dashboard")
def admin_dashboard():
    db = get_db()
    users_row =db.execute("SELECT COUNT(*)FROM users").fetchone()
    users_count = users_row[0]if users_row else 0
    votes_row = db.execute("SELECT COUNT(*)FROM votes").fetchone()
    votes_count = votes_row[0]if votes_row else 0
    return render_template("admin_dashboard.html",total_users=users_count, total_votes=votes_count)
@app.route("/results")
def results():
    db = get_db()
    results = db.execute("SELECT group_name, COUNT(*) as total FROM votes GROUP BY group_name").fetchall()
    return render_template("results.html", results=results)

if __name__=="__main__":
    app.run(debug=True)
