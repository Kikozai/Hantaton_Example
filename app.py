from flask import Flask, redirect, render_template, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:23675@localhost/child'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)



# Модель ребёнка
class Child(db.Model):
    __tablename__ = 'child'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    second_name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    age = db.Column(db.Integer)
    sciences = db.Column(db.String(100))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(100))
    achievements = db.relationship('Achievement', backref='child', lazy=True)

    def __init__(self, first_name, second_name, surname, age, sciences, password, email, phone_number):
        self.first_name = first_name
        self.second_name = second_name
        self.surname = surname
        self.age = age
        self.sciences = sciences
        self.password = password
        self.email = email
        self.phone_number = phone_number

class Achievement(db.Model):
    __tablename__ = 'achievement'
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))
    title = db.Column(db.String(100))
    description = db.Column(db.String(255))
    date_achieved = db.Column(db.Date)
    
    def __init__(self, child_id, title, description, date_achieved):
        self.child_id = child_id
        self.title = title
        self.description = description
        self.date_achieved = date_achieved


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
        try:
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
                new_child = Child(
                    first_name=first_name,
                    second_name=second_name,
                    surname=surname,
                    age=age,
                    sciences=sciences,
                    password=password,
                    email=email,
                    phone_number=phone_number
                )
                db.session.add(new_child)
                db.session.commit()
                return redirect(url_for('login'))
        except Exception as e:
            return f"Database error: {str(e)}"

@app.route("/child")
def child():
    if 'child_id' in session:
        id = session['child_id']
        return render_template("child.html", id=id, main=True)
    else:
        return render_template("child.html", main=False)
    
app.route("/search", methods=["GET"])
def search():
    if 'child_id' in session:
        id = session['child_id']
    else:
        id = None

    # Получаем параметры поиска из query запросов
    first_name = request.args.get('first_name')
    second_name = request.args.get('second_name')
    surname = request.args.get('surname')
    sciences = request.args.getlist('sciences')  # Get as a list
    min_age = int(request.args.get('minAge') or 4)
    max_age = int(request.args.get('maxAge') or 25)

    # Check if data is present for sciences
    if not sciences:  # If no data is provided, set sciences as an empty list
        sciences = []

    # Обработка логики поиска
    children = Child.query.filter(
        Child.first_name.ilike(f'%{first_name}%'),
        Child.second_name.ilike(f'%{second_name}%'),
        Child.surname.ilike(f'%{surname}%'),
        Child.age.between(min_age, max_age),
        Child.sciences.ilike(f'%{", ".join(sciences)}%')  # Join sciences as a comma-separated string
    ).all()

    # Возвращаем выражение
    return render_template("search.html", first_name=first_name, second_name=second_name, surname=surname,
                           sciences=sciences, minAge=min_age, maxAge=max_age, children=children, id=id)

@app.route("/achievement", methods=["POST"])
def achievement():
    id = request.args.get('id')
    science = request.form.get('science')
    category = request.form.get('category')
    title = request.form.get('title')
    place = request.form.get('place')

    # Логика добавления нового достижения для ребенка с указанным ID
    child = Child.query.filter_by(child_id=id).first()
    if child:
        new_achievement = Achievement(science=science, category=category, title=title, place=place)
        child.achievements.append(new_achievement)
        db.session.commit()

    return redirect(url_for('child'))

if __name__ == "__main__":
    app.run()
