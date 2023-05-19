import mysql.connector

from flask import current_app, g
import configparser

config = configparser.ConfigParser()
config.read('my_config.ini')

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(user=config.get('database', 'username'), password=config.get('database', 'password'),
                              host=config.get('database', 'host'),
                              database=config.get('database', 'database'))
    
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)