import os
from flask import Flask, render_template, request, redirect,url_for, flash
import mysql.connector
from mysql.connector import IntegrityError
from db import get_db
import configparser
from flask_mail import Mail, Message


app = Flask(__name__, static_folder="static")
app.secret_key = os.urandom(16)

config = configparser.ConfigParser()
config.read('email_config.ini')


app.config.update(
    MAIL_SERVER=config.get('mail', 'MAIL_SERVER'),
    MAIL_PORT=config.getint('mail', 'MAIL_PORT'),
    MAIL_USE_SSL=config.getboolean('mail', 'MAIL_USE_SSL'),
    MAIL_USERNAME=config.get('mail', 'MAIL_USERNAME'),
    MAIL_PASSWORD=config.get('mail', 'MAIL_PASSWORD'),
)
mail = Mail(app)

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form["email"]

        db = get_db()

        cursor = db.cursor()
        query = "INSERT INTO email (email) VALUES (%s)"

        try:
            cursor.execute(query, (email,))
            db.commit()
            # Send email for suscribing (Disabled)
            # msg = Message("Hello", sender="lorenzo.jiang8075@gmail.com", recipients=[email])
            # msg.html = render_template('email.html')  # assuming 'email.html' is your email template and 'User' is the name of the user
            # mail.send(msg)
            
            # Send email for suscribing (Disabled)
            msg = Message("New subscriber!!", sender="lorenzo.jiang8075@gmail.com", recipients=["lorenzo.jiang8075@gmail.com"])
            msg.body = f"New subscription from {email}"
            mail.send(msg)

            return redirect(url_for("thank_you"))
        except IntegrityError:
            db.rollback()
            flash("Email already exists. Please use a different email address.")
        finally:
            cursor.close()
            db.close()

    return render_template("index.html",css=url_for('static',filename='styles.css'))

@app.route("/thankyou", methods=["GET", "POST"])
def thank_you():
    return render_template("thankyou.html")


if __name__ == "__main__":
    app.run(debug=True)
