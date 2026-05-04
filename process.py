import mysql.connector
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index_p.html")

@app.route('/send', methods=['POST'])
def send_data():
    # Databasekobling
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="abdisemed08",
        database="skjema_db"
    )

    cursor = conn.cursor()

    # Hent data fra skjemaet
    navn = request.form['navn']
    epost = request.form['epost']
    melding = request.form['melding']

    # Sett data inn i tabell
    sql = "INSERT INTO kontakter (navn, epost, melding) VALUES (%s, %s, %s)"
    values = (navn, epost, melding)

    try:
        cursor.execute(sql, values)
        conn.commit()
        return "Takk, dataene er lagret!"
    except mysql.connector.Error as err:
        return f"Feil: {err}"

    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)