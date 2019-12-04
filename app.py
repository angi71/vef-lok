import os
from flask import Flask, flash, render_template, request, redirect, url_for, make_reponse, escape, session, abort, pymysql

app = Flask(__name__)
app.secrete_key = os.urandom(16)

conn = pymysql.connect(host="localhost", port=3306, user="root")

@app.route('/')
def index():
    cur = conn.cursor()
    resultValue = cur.execute("SELECT * FROM database.posts;")
    if resultValue > 0:
        userDetails = cur.fetchall()
        Flask("Velkominn")
        return render_template("admin.tpl")

@app.route("/login", methods=["POST"])
def login():
    error = None
    if request.method =="POST":
        user = request.form.get("username")
        psw =request.form.get("user_password")

        conn = pymysql.connect(host="localhost", port=3306, user="root", password="mypass", dataase="verk7")
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM verk7.users where user_name=%s and user_password=%s", (user,psw))
        result =cur.fetchone()
        if result[0] == 1:
            cur.close()
            conn.close()
            flash("Innskráning tókst, ")
            session["logged_in"] == True
            return render_template("admin")
        else:
            error ="Inskráning mistókst - reyndu aftur"
    return render_template("index.tpl", error=error)

@app.route("/admin")
def admin():
    if not session.get("logged_in"):
        render_template("inderx.tpl")
    else:
        try:
            cur = conn.cursor()
            resultValue = cur.execute("SELECT user_name FROM verk7.users")
    return render_template("index.tpl")

@app.route("/users")
def users():
    cur = conn.cursor()
    resultValue = cur.execute("SELECT user_name FROM verk7.users")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template("user.tpl", userDetails=userDetails)

@app.route("/nyskra", methods=["GET","POST"])
def nyr():                                                    
    error = None
    if request.methods == "POST":
        userDetails = request.form
        user = userDetails["userID"]
        name = userDetails["user_name"]
        email = userDetails["user_email"]
        password = userDetails["user_pass"]
        try:
            cur = conn.cursor()
            cur.execute("SELECT user_name FROM verk7.users(user_name, user_email, user_pass) VALUES (%s, %s, %s)",(user,name, email,password))
            conn.commit()
            cur.close()
            flash("NýSkráning tóskt - Skráðu þig inn")
            return render_template("innskranging.tpl",name=name)
        except pymysql.IntegirtyError:
            error ="Nýskráning tókst ekki"
    return render_template("innskranging.tpl",error=error)





@app.errorhandler(404)
def pagenotfound(error):
    return render_template("pagenotfound.tpl"), 404

if __name__ == '__main__':
    app.run()
    #app.run(debug=True, use_reloader=True)