# encoding=utf-8
from flask import Flask, url_for, render_template, request, session, redirect, flash, g, session, jsonify
import  os
from flask_sqlalchemy import SQLAlchemy
import config
import sqlite3
from flask import g
from flask_mail import Mail, Message
import folium
import geocoder

mail = Mail()
app = Flask(__name__)
app.config.from_object(config)


DATABASE = 'user_feature.db'
mail.init_app(app)


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
    # msg = Message("Hello, this for test",
    #               sender=app.config["MAIL_USERNAME"],
    #               recipients=["b.ben.hjy@gmail.com"])
    # mail.send(msg)
    return "hello world"


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "GET":
        return render_template("registration.html")
    else:
        username = request.form.get("username")
        email = request.form.get("email")
        cur = get_db()
        cur.execute("delete from user_email where username='{}'".format(username))
        sql_command = "INSERT INTO user_email VALUES ('{}', '{}')".format(username, email)
        cur.execute(sql_command)
        cur.commit()
        # close db
        if cur is not None:
            cur.close()
        return "Sign up successfully"




@app.route("/send/<info>")
def send(info):
    # data should be seperate by "-"
    # username text, latitude  real, Longitude real, temperature real, pressure real, humidity real
    info = info.split("-")
    print(info)
    db = get_db()
    # cur.execute("delete from user_feature where username='{}'".format(info[0]))
    # sql_command = "INSERT INTO user_feature VALUES ('{}',{},{},{},{},{})".format(info[0], info[1], info[2], info[3], info[4], info[5])
    # cur.execute(sql_command)
    # cur.commit()
    cur = db.cursor()
    print(info[0])
    cur.execute("select * from user_email where username='{}'".format(info[0]))
    to_email = cur.fetchall()[0][1]
    msg = Message("Help!!! {} is in danger. The location is {}".format(info[0], info[1]),
                  sender=app.config["MAIL_USERNAME"],
                  recipients=[to_email])
    mail.send(msg)
    # close db
    if db is not None:
        db.close()
    return "Successfully send"

@app.route("/save_data/<info>")
def save_data(info):
    # username-lon-lat-risk
    info = info.split("&")
    print(info)
    username = info[0]
    cur = get_db()
    cur.execute("delete from user_info where username='{}'".format(username))
    sql_command = "INSERT INTO user_info VALUES ('{}', {}, {}, {})".format(username, info[1], info[2], info[3])
    cur.execute(sql_command)
    cur.commit()
    # close db
    if cur is not None:
        cur.close()
    return "save successfully"


@app.route("/get_heatmap/<username>")
def get_heatmap(username):

    check_dict = dict()
    db = get_db()
    cur = db.cursor()
    # cur.execute("select * from user_info where username='{}'".format(username))
    cur.execute("select * from user_info")
    user_info = cur.fetchall()
    cur.execute("select * from user_email")
    user_email = cur.fetchall()
    target_lon = 0
    target_lat = 0
    for i in range(len(user_info)):
        username1 = user_info[i][0]
        username2 = user_email[i][0]
        email = user_email[i][1]
        lon = user_info[i][1]
        lat = user_info[i][2]
        risk = user_info[i][3]
        if not username1 in check_dict:
            check_dict[username1] = {"email":'', "lat":0, "lon":0, "risk":'0'}
        if not username2 in check_dict:
            check_dict[username2] = {"email": '', "lat": 0, "lon": 0, "risk": '0'}
        check_dict[username1]["lon"] = lon
        check_dict[username1]["lat"] = lat
        check_dict[username1]["risk"] = risk
        check_dict[username2]['email'] = email


    folium_map = folium.Map(location=(check_dict[username]['lon'], check_dict[username]['lat']), zoom_start=14)
    for key in check_dict.keys():
        folium.Marker((check_dict[key]["lon"], check_dict[key]['lat']), popup="username: "+key+"\n"+"risk: "+str(check_dict[key]['risk'])+ "\n"+check_dict[key]["email"] ).add_to(folium_map)
    # close db
    if db is not None:
        db.close()
    return folium_map._repr_html_()


@app.route("/get/<username>")
def get(username):
    cur = get_db().cursor()
    cur.execute("select * from user_feature where username='{}'".format(username))
    print(cur.fetchall()[0])
    return "get successfully"


if __name__ == '__main__':
    app.run(port=4999, debug=True, host="0.0.0.0")