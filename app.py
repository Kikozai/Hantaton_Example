from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:23675@localhost/users'
db = SQLAlchemy(app)

class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer)
    talent_area = db.Column(db.String(255))
    contact_info = db.Column(db.String(255))

# основная страница
@app.route('/')
def index():
    return render_template('index.html')
# функция добавления ребенка
@app.route('/add_child', methods=['GET', 'POST'])
def add_child():
    if request.method == 'POST':
        full_name = request.form['full_name']
        age = request.form['age']
        talent_area = request.form['talent_area']
        contact_info = request.form['contact_info']

        child = Child(full_name=full_name, age=age, talent_area=talent_area, contact_info=contact_info)
        db.session.add(child)
        db.session.commit()
        return 'Child added successfully!'
    return render_template('add_child.html')

# функция удаления ребенка
@app.route('/delete_child', methods=['POST'])
def delete_child():
    child_id = request.form['child_id']
    child = Child.query.get(child_id)
    if child:
        db.session.delete(child)
        db.session.commit()
        return 'Child deleted successfully!'
    else:
        return 'Child not found!'
    
# функция поиска ребенка по имени
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        full_name = request.form['full_name']
        child = Child.query.filter_by(full_name=full_name).first()
        if child:
            return render_template('search_result.html', child=child)
        else:
            return 'Child not found!'
    return render_template('search_child.html')

# функция поиска ребенка по таланту
@app.route('/search_talent', methods=['GET', 'POST'])
def search_talent():
    if request.method == 'POST':
        talent_area = request.form['talent_area']
        child = Child.query.filter_by(talent_area=talent_area).first()
        if child:
            return render_template('search_result.html', child=child)
        else:
            return 'Child not found!'
    return render_template('search_child.html')

# функция поиска ребенка по возрасту
@app.route('/search_age', methods=['GET', 'POST'])
def search_age():
    if request.method == 'POST':
        age = request.form['age']
        children = Child.query.filter_by(age=age).all()
        if children:
            return render_template('search_result.html', children=children)
        else:
            return 'No children found!'
    return render_template('search_child.html')

# функция поиска ребенка по контактной информации
@app.route('/search_contact', methods=['GET', 'POST'])
def search_contact():
    if request.method == 'POST':
        contact_info = request.form['contact_info']
        child = Child.query.filter_by(contact_info=contact_info).first()
        if child:
            return render_template('search_result.html', child=child)
        else:
            return 'Child not found!'
    return render_template('search_child.html')


if __name__ == '__main__':
    app.run()