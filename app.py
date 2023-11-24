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
        return redirect(url_for('child'))
    else:
        return render_template("index.html")


# Роут для входа в аккаунт
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', error=False)
    elif request.method == 'POST':
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


# Роут для выхода из аккаунта
@app.route('/logout')
def logout():
    # Удаление ID ребенка из сессии
    session.pop('child_id', None)
    return redirect(url_for('index'))

# Роут для регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        # Получение данных для регистрации из запроса
        first_name = request.form.get('firstName')
        second_name = request.form.get('secondName')
        surname = request.form.get('surname')
        password = request.form.get('password')
        age = request.form.get('age')
        sciences = request.form.getlist('sciences')
        email = request.form.get('email')
        phone_number = request.form.get('phoneNumber')

        # Проверка, существует ли ребенок с указанным email
        existing_child = Child.query.filter_by(email=email).first()

        if existing_child:
            # Ребенок с указанным email уже существует
            return render_template('register.html', error=True, firstName=first_name, secondName=second_name,
                                   surname=surname, password=password, age=age, sciences=sciences,
                                   email=email, phoneNumber=phone_number)
        else:
            # Создание нового объекта ребенка
            new_child = Child(first_name, second_name, surname, age, sciences, password, email, phone_number)
            db.session.add(new_child)
            db.session.commit()
            return redirect(url_for('login'))