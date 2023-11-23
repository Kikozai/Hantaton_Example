from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify, redirect, url_for


# подключение к базе данных
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:23675@localhost/users'
db = SQLAlchemy(app)

# модель ребёнка
class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer)
    talent_area = db.Column(db.String(255))
    contact_info = db.Column(db.String(255))
    
# функция отображения главной страницы
@app.route('/')
def index():
    return render_template('index.html')
   
    
# функция добавления ребёнка 
@app.route('/add', methods=['GET', 'POST'])
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
# получение данных о ребёнке 
@app.route('/get/<int:id>')
def get_child(id):
    child = Child.query.get(id)
    return render_template('get_child.html', child=child)
# функция удаления данных о ребёнке
@app.route('/delete/<int:id>')
def delete_child(id):
    child = Child.query.get(id)
    db.session.delete(child)
    db.session.commit()
    return 'Child deleted successfully!'

# функция поиска ребёнка по имени
@app.route('/search', methods=['GET', 'POST'])
def search_children_by_name():
    if request.method == 'POST':
        name = request.form['name']
        children = Child.query.filter(Child.full_name.ilike(f'%{name}%')).all()
        return render_template('search_results.html', children=children)
    return render_template('search_children.html')

# функция поиска ребёнка по возврасту
@app.route('/search', methods=['GET', 'POST'])
def search_children_by_age():
    if request.method == 'POST':
        age = request.form['age']
        children = Child.query.filter(Child.age == age).all()
        return render_template('search_results.html', children=children)
    return render_template('search_children.html')

# функция поиска ребёнка по таланту
@app.route('/search', methods=['GET', 'POST'])
def search_children_by_talent_area():
    if request.method == 'POST': 
        talent_area = request.form['talent_area']
        children = Child.query.filter(Child.talent_area.ilike(f'%{talent_area}%')).all()
        return render_template('search_results.html', children=children)
    return render_template('search_children.html')

if __name__ == '__main__':  
     app.run(port=8080, debug=True)