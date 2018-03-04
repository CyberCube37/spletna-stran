from flask import Flask
from flask import render_template, make_response, session
from flask import request
from flask import redirect
import string
import random
import baza

app = Flask(__name__)
app.secret_key = 'kajdsfhg'
baza.ustvari_tabele()

@app.route("/")
def index():
    return render_template("domaca_stran.html")

@app.route("/logout")
def logout():
    session['user']= None
    return redirect("/")

@app.route("/logo")
def logo():
    return render_template("domaca_stran.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        session['user'] = baza.dobi_uporabnika(
            username=request.form["username"],
            password=request.form["password"])
    return render_template("druga_stran.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST" and session['user']==None:
        if baza.dobi_uporabnika(username=request.form["username"]) is None:
            baza.vstavi_novega_uporabnika(
                username=request.form["username"],
                password=request.form["password"])
            session['user'] = baza.dobi_uporabnika(
                username=request.form["username"],
                password=request.form["password"])
            session['registriran'] = 1
        else:
            session['registriran']=None
    return render_template("register.html")

@app.route("/vislice/<znak>")
def ugibaj(znak):
    if len(znak) == 1:
        session['ugibal'] = session['ugibal'] + znak
        if znak not in session['beseda']:
            session['slika'] += 1
    for crka in session['beseda']:
        if crka not in session['ugibal']:
            break
    else:
        return render_template('zmaga.html', session = session)
    return render_template('Vvislice.html', session=session, letters=string.ascii_lowercase)

@app.route("/vislice")
def vislice():
    with open('besede.txt') as f:
        beseda = ''
        while len(beseda) < 5:
            for i in range(random.randint(1,350748)):
                beseda = f.readline()
    session['beseda'] = beseda.strip()
    session['slika'] = 0
    session['ugibal'] = ''
    return render_template('Vvislice.html', session=session, letters=string.ascii_lowercase)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
