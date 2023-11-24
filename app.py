from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:23675@localhost/users'
db = SQLAlchemy(app)

# Модель ребёнка   
class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50))
    secondName = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    password = db.Column(db.String(50))
    age = db.Column(db.Integer)
    sciences = db.Column(db.String(200))
    email = db.Column(db.String(100), unique=True)
    phoneNumber = db.Column(db.String(20))

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    error = request.form.get("error")
    if email == "valid_email" and password == "valid_password":
        return render_template("child.html")
    else:
        return render_template("login.html", email=email, password=password, error=True)

@app.route("/register", methods=["GET"])
def register():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register_post():
    firstName = request.form.get("firstName")
    secondName = request.form.get("secondName")
    surname = request.form.get("surname")
    password = request.form.get("password")
    age = request.form.get("age")
    sciences = request.form.getlist("sciences")
    email = request.form.get("email")
    phoneNumber = request.form.get("phoneNumber")
    error = request.form.get("error")
    existing_child = Child.query.filter_by(email=email).first()
    if existing_child:
        return render_template("register.html", firstName=firstName, secondName=secondName, surname=surname,
                               password=password, age=age, sciences=sciences, email=email, phoneNumber=phoneNumber,
                               error=True)
    else:
        new_child = Child(firstName=firstName, secondName=secondName, surname=surname, password=password, age=age,
                          sciences=sciences, email=email, phoneNumber=phoneNumber)
        db.session.add(new_child)
        db.session.commit()
        return render_template("child.html")

@app.route("/child", methods=["GET"])
def child():
    child_id = request.args.get("id")
    # Извлекаем ребенка из базы данных, используя child_id
    # Отрисовываем дочерний элемент, используя полученные данные
    return render_template("child.hbs", child_id=child_id)

@app.route("/search", methods=["GET"])
def search():
    firstName = request.args.get("firstName")
    secondName = request.args.get("secondName")
    surname = request.args.get("surname")
    sciences = request.args.get("sciences")   
# Поиск детей по предоставленным параметрам в базе данных
    # Отображение результатов поиска с помощью search.hbs
    return render_template("search.hbs")
