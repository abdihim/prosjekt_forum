from flask import Flask, render_template, request, redirect, url_for  # importerer Flask og verktøy
import mysql.connector  # kobler til database
from dotenv import load_dotenv  # laster .env
import os
from werkzeug.security import generate_password_hash, check_password_hash  # for å hashe passord

load_dotenv()
app = Flask(__name__)

# hjelpefunksjon for å koble til databasen
def db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

@app.route("/")  # forside
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])  # login side
def login():
    if request.method == "POST":
        username = request.form["username"]  # henter brukernavn
        password = request.form["password"]  # henter passord
        conn = db()  # lagrer koblingen
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))  # henter bruker
        result = cursor.fetchone()  # henter bruker fra databasen
        if result and check_password_hash(result[2], password):  # sjekker passord mot hash
            return "Riktig login"
        return "Feil login"
    return render_template("login.html")

@app.route("/registrer", methods=["GET", "POST"])  # registreringsside
def registrer():
    if request.method == "POST":
        username = request.form["username"]  # henter brukernavn
        password = generate_password_hash(request.form["password"])  # hasher passord
        conn = db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))  # setter inn bruker
        conn.commit()  # lagrer i databasen
        return redirect(url_for("login"))  # sender til login siden
    return render_template("registrer.html")

@app.route("/users")  # viser alle brukere
def users():
    conn = db()  # lagrer koblingen
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")  # henter alle brukere
    return render_template("users.html", data=cursor.fetchall())  # sender til HTML

@app.route("/meld_feil", methods=["GET", "POST"])  # meld feil side
def meld_feil():
    return render_template("Meld_feil.html")

@app.route("/faq")  # faq side
def faq():
    return render_template("faq.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)  # starter Flask