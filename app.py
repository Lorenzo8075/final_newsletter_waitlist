import os
from flask import Flask, render_template, request, redirect,url_for, flash
import mysql.connector
from mysql.connector import IntegrityError
from db_config import db_host, db_user, db_password, db_database

app = Flask(__name__, static_folder="static")
app.secret_key = os.urandom(16)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form["email"]

        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_database
        )

        cursor = conn.cursor()
        query = "INSERT INTO email (email) VALUES (%s)"

        try:
            cursor.execute(query, (email,))
            conn.commit()
            return redirect(url_for("thank_you"))
        except IntegrityError:
            conn.rollback()
            flash("Email already exists. Please use a different email address.")
        finally:
            cursor.close()
            conn.close()

    return render_template("index.html",css=url_for('static',filename='styles.css'))

@app.route("/thankyou", methods=["GET","POST"])
def thank_you():
    return render_template("thankyou.html")


if __name__ == "__main__":
    app.run(debug=True)
