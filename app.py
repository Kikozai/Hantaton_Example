from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:23675@localhost/child'  
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
    email = db.Column(db.String(100), nullable=False)
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
# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        # Get the registration data from the request
        first_name = request.form.get('firstName')
        second_name = request.form.get('secondName')
        surname = request.form.get('surname')
        password = request.form.get('password')
        age = request.form.get('age')
        sciences = request.form.getlist('sciences')
        email = request.form.get('email')
        phone_number = request.form.get('phoneNumber')

        # Check if a child with the given email already exists
        existing_child = Child.query.filter_by(email=email).first()

        if existing_child:
            # Child with the given email already exists
            return render_template('register.html', error=True, firstName=first_name, secondName=second_name,
                                   surname=surname, password=password, age=age, sciences=sciences,
                                   email=email, phoneNumber=phone_number)
        else:
            # Create a new child object
            new_child = Child(first_name, second_name, surname, age, sciences, password, email, phone_number)

            # Add the new child to the database
            db.session.add(new_child)
            db.session.commit()

            # Redirect to the child's dashboard
            return redirect(url_for('child'))

@app.route('/child')
def child():
    # Render the child's dashboard
    return render_template('child.html')

@app.route("/search", methods=["GET"])
def search():
    firstName = request.args.get("firstName")
    secondName = request.args.get("secondName")
    surname = request.args.get("surname")
    sciences = request.args.get("sciences")   
# Поиск детей по предоставленным параметрам в базе данных
    # Отображение результатов поиска с помощью search.hbs
    return render_template("search.hbs")

if __name__ == '__main__':
    app.run()