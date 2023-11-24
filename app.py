from flask import Flask, redirect, render_template, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:23675@localhost/child'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)


# Модель ребёнка
class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(100), nullable=False)
    secondName = db.Column(db.String(100))
    surname = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sciences = db.Column(db.String(100))
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phoneNumber = db.Column(db.String(20))

    def __init__(self, firstName, secondName, surname, age, sciences, password, email, phoneNumber):
        self.firstName = firstName
        self.secondName = secondName
        self.surname = surname
        self.age = age
        self.sciences = sciences
        self.password = password
        self.email = email
        self.phoneNumber = phoneNumber


@app.route("/", methods=["GET"])
def index():
    if 'child_id' in session:
        id = session['child_id']
        return render_template("index.html", id=id)
    else:
        return render_template("index.html")
    
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        # Проверка, существует ли ребенок с указанным email и паролем
        child = Child.query.filter_by(email=email, password=password).first()

        if child:
            # Сохранение ID ребенка в сессии
            session['child_id'] = child.id
            return redirect(url_for('child'))
        else:
            return render_template('login.html', error=True, email=email)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        first_name = request.form.get('firstName')
        second_name = request.form.get('secondName')
        surname = request.form.get('surname')
        password = request.form.get('password')
        age = request.form.get('age')
        sciences = request.form.getlist('sciences')
        email = request.form.get('email')
        phone_number = request.form.get('phoneNumber')

        existing_child = Child.query.filter_by(email=email).first()

        if existing_child:
            return render_template('register.html', error=True, firstName=first_name, secondName=second_name,
                                   surname=surname, password=password, age=age, sciences=sciences,
                                   email=email, phoneNumber=phone_number)
        else:
            new_child = Child(first_name, second_name, surname, age, sciences, password, email, phone_number)
            db.session.add(new_child)
            db.session.commit()
            return redirect(url_for('login'))

@app.route("/child")
def child():
    if 'child_id' in session:
        id = session['child_id']
        return render_template("child.html", id=id, main=True)
    else:
        return render_template("child.html", main=False)

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")
    elif request.method == "POST":
        firstName = request.form.get('firstName')
        secondName = request.form.get('secondName')
        surname = request.form.get('surname')
        sciences = request.form.get('sciences')
        minAge = request.form.get('minAge')
        maxAge = request.form.get('maxAge')

        # Логика поиска ребенка по указанным параметрам

        return render_template("search.html", firstName=firstName, secondName=secondName,
                               surname=surname, sciences=sciences, minAge=minAge, maxAge=maxAge, child=child)

@app.route("/achievement", methods=["POST"])
def achievement():
    science = request.form.get('science')
    category = request.form.get('category')
    title = request.form.get('title')
    place = request.form.get('place')
    child_id = request.form.get('id')

    # Логика добавления нового достижения для ребенка с указанным ID

    return redirect(url_for('child'))

if __name__ == "__main__":
    app.run()


