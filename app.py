from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_bcrypt import Bcrypt
import sqlite3
from rag_engine import generate_answer
from auth import User, init_db
from utils.pdf_loader import extract_text_from_pdf
from utils.summarizer import summarize_document
import os


app = Flask(__name__)
app.secret_key = "supersecretkey"
bcrypt = Bcrypt(app)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
login_manager = LoginManager()
login_manager.init_app(app)

init_db()

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = c.fetchone()
    conn.close()
    if user:
        return User(user[0], user[1])
    return None

@app.route("/")
def home():
    return redirect("/login")
@app.route("/upload", methods=["GET","POST"])
@login_required
def upload():
    summary = None
    if request.method == "POST":
        file = request.files["pdf_file"]
        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            text = extract_text_from_pdf(filepath)
            summary = summarize_document(text)

    return render_template("upload.html", summary=summary)

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("INSERT INTO users (username,password) VALUES (?,?)",(username,password))
        conn.commit()
        conn.close()
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user[2], password):
            login_user(User(user[0], user[1]))
            return redirect("/dashboard")

    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/ask", methods=["GET","POST"])
@login_required
def ask():
    answer = None
    confidence = None
    if request.method == "POST":
        question = request.form["question"]
        answer, confidence = generate_answer(question)

    return render_template("ask.html", answer=answer, confidence=confidence)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
