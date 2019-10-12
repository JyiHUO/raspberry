# encoding=utf-8
from flask import Flask, url_for, render_template, request, session, redirect, flash, g, session, jsonify
import  os
from flask_sqlalchemy import SQLAlchemy
import config
import sqlite3
from flask import g

app = Flask(__name__)
app.config.from_object(config)
DATABASE = 'user_location.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    return "hello world"


@app.route("/send/<info>")
def send(info):
    # data should be seperate by "-"
    # username text, latitude  real, Longitude real, temperature real, pressure real, humidity real
    info = info.split("-")
    print(info)
    cur = get_db()
    cur.execute("delete from user_feature where username='{}'".format(info[0]))
    sql_command = "INSERT INTO user_feature VALUES ('{}',{},{},{})".format(info[0], info[1], info[2], info[3], info[4], info[5])
    cur.execute(sql_command)
    cur.commit()
    return "Successfully send"


@app.route("/get/<username>")
def get(username):
    cur = get_db().cursor()
    cur.execute("select * from user_feature where username='{}'".format(username))
    print(cur.fetchall()[0])
    return "get successfully"


if __name__ == '__main__':
    app.run(port=4999, debug=True)