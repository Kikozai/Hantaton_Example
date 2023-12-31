from flask import Flask, flash, redirect, render_template, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:23675@localhost/child'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
# Модель ребёнка
class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    second_name = db.Column(db.String(100))
    surname = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sciences = db.Column(db.ARRAY(db.String))
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone_number = db.Column(db.String(20))
    def __init__(self, first_name, second_name, surname, age, sciences, password, email, phone_number):
        self.first_name = first_name
        self.second_Name = second_name
        self.surname = surname
        self.age = age
        self.sciences = sciences
        self.password = password
        self.email = email
        self.phone_Number = phone_number
        
class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), nullable=False)
    science = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    place = db.Column(db.String(255), nullable=False)

    # Опционально, вы можете добавить дополнительные поля для даты, описания и т.д.

    def __init__(self, child_id, science, category, title, place):
        self.child_id = child_id
        self.science = science
        self.category = category
        self.title = title
        self.place = place
        
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
        phone_number = request.form.get('phoneNumber') or 'не указан'
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
    # Получить необходимую информацию из тела запроса
    data = request.get_json()
    child_id = data.get('child_id')
    science = data.get('science')
    category = data.get('category')
    title = data.get('title')
    place = data.get('place')

    # Создать экземпляр модели Achievement с предоставленной информацией
    achievement = Achievement(child_id=child_id, science=science, category=category, title=title, place=place)

    try:
        # Сохранить достижение в базе данных
        db.session.add(achievement)
        db.session.commit()

        flash('Достижение успешно добавлено', 'success')
    except Exception as e:
        flash('Ошибка при добавлении достижения: ' + str(e), 'error')

    # Перенаправление на личный кабинет ребенка
    return redirect(url_for('child'))

if __name__ == "__main__":
    app.run()