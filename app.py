

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import cast, String

import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = 'some secret key'
# Конфигурация базы данных SQLite
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'employees.db')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.secret_key = 'your_secret_key' # Замените на реальный секретный ключ


# --- НОВЫЙ КОД (PostgreSQL) ---
# Укажите ваши данные: username, password, hostname (например, localhost), port (5432 по умолчанию), database_name
DB_USER = 'postgres'
DB_PASS = '1111'
DB_HOST = 'localhost' # или IP-адрес сервера БД
DB_PORT = '5432'
DB_NAME = ''

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.secret_key = 'some secret key' # Оставьте ваш секретный ключ

db = SQLAlchemy(app)
# ... (остальной код приложения) ...


# Определение модели сотрудника
class Employee(db.Model):
    __tablename__ = 'employees50'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    employment_date = db.Column(db.Date, nullable=False)
    manager_id = db.Column(db.Integer,  nullable=False)
    #manager_id = db.Column(db.Integer, db.ForeignKey('employees50.id'), nullable=False)


    def __repr__(self):
        return f'<Employee {self.id} {self.name}>'

# ... (далее будут добавлены маршруты)
# ... (код из Шага 3 выше) ...

# Маршрут для отображения всех сотрудников и поиска
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form.get('search')
        # Поиск по всем полям
        employees = Employee.query.filter(
            (cast(Employee.id,String).ilike(f'%{search_query}%')) |
            (Employee.name.ilike(f'%{search_query}%')) |
            (Employee.role.ilike(f'%{search_query}%')) |
            (cast(Employee.salary,String).ilike(f'%{search_query}%'))|
            (cast(Employee.employment_date,String).ilike(f'%{search_query}%'))|
            (cast(Employee.manager_id,String).ilike(f'%{search_query}%'))
        ).all()
        return render_template('index.html', employees=employees, search_query=search_query)
    else:
        employees = Employee.query.all()
        return render_template('index.html', employees=employees, search_query='')

# Маршрут для обновления данных сотрудника
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    employee = Employee.query.get_or_404(id)
    if request.method == 'POST':
        employee.id = request.form['id']
        employee.name = request.form['name']
        employee.role = request.form['role']
        employee.salary = request.form['salary']
        employee.employment_date = request.form['employment_date']
        employee.manager_id = request.form['manager_id']
        try:
            db.session.commit()
            flash('Данные сотрудника успешно обновлены!', 'success')
            return redirect(url_for('index'))
        except:
            flash('Произошла ошибка при обновлении данных.', 'danger')
    return render_template('update.html', employee=employee)



# ... (Существующий код импортов и настройки приложения) ...
# ... (Существующий класс Employee) ...

# ... (Существующий маршрут index) ...

# Маршрут для добавления нового сотрудника
@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        role = request.form['role']
        salary = request.form['salary']
        employment_date = request.form['employment_date']
        manager_id = request.form['manager_id']

        if not id or not name or not role or not salary or not employment_date or not manager_id   :
            flash('Все поля обязательны для заполнения!', 'danger')
            return redirect(url_for('index'))

        new_employee = Employee(name=name, role=role, salary=salary, employment_date=employment_date, manager_id=manager_id)
        #db.session.add(new_employee)
        try:
            db.session.add(new_employee)
            db.session.commit()
            flash('Сотрудник успешно добавлен!', 'success')
            return redirect(url_for('index'))
        except:
           flash('Произошла ошибка при добавлении сотрудника.', 'danger')
           return redirect(url_for('index'))






# Маршрут для удаления сотрудника
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    employee = Employee.query.get_or_404(id)
    try:
        db.session.delete(employee)
        db.session.commit()
        flash('Сотрудник успешно удален!', 'success')
        return redirect(url_for('index'))
    except:
        flash('Произошла ошибка при удалении сотрудника.', 'danger')
        return redirect(url_for('index'))


if __name__ == '__main__':
   # app.secret_key = 'some secret key'
    app.run(debug=True)





