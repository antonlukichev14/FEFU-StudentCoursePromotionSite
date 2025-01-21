from flask import Flask, abort, flash, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, LoginManager, UserMixin, login_user, login_required, logout_user
from datetime import datetime
from app.models import db, Category, Audience, Course
from app.forms import CourseForm

def create_app():
    app = Flask(__name__)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Конфигурация приложения
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses.db'  # Замена на вашу базу данных
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key'  # Установите секретный ключ

    db.init_app(app)  # Инициализируем базу данных с приложением

    with app.app_context():
        db.create_all()  # Создаем таблицы в базе данных

    return app

app = create_app()

@app.route('/', methods=['GET', 'POST'])
def search():
    categories = Category.query.all()
    audiences = Audience.query.all()
    
    if request.method == 'POST':
        category_id = request.form.get('category')
        audience_id = request.form.get('audience')

        # Начинаем с запроса всех курсов
        courses_query = Course.query
        
        # Если поле категории не пустое, фильтруем по категории
        if category_id:
            courses_query = courses_query.filter_by(category_id=category_id)
        
        # Если поле аудитории не пустое, фильтруем по аудитории
        if audience_id:
            courses_query = courses_query.filter_by(audience_id=audience_id)

        # Получаем отфильтрованные курсы
        courses = courses_query.all()
    else:
        # Если метод GET, то просто показываем все курсы
        courses = Course.query.all()

    return render_template(
        'search.html', 
        courses=courses, 
        categories=categories, 
        audiences=audiences, 
        isUserAdmin=isUserAdmin())

@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if not isUserAdmin():
        abort(403)  # Отказ в доступе, если пользователь не администратор

    form = CourseForm()
    form.graduation_year.choices = get_year_choices()  # Возможно, сделать выбор годов
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]  # Получаем все категории
    form.audience_id.choices = [(a.id, a.type) for a in Audience.query.all()]  # Получаем всех аудитории

    if form.validate_on_submit():
        new_course = Course(
            title=form.title.data,
            description=form.description.data,
            graduation_year=form.graduation_year.data,
            category_id=form.category_id.data,
            audience_id=form.audience_id.data
        )
        db.session.add(new_course)
        db.session.commit()
        flash('Курс успешно добавлен!', 'success')
        return redirect("/")  # Перенаправляем на страницу курсов

    return render_template('add_course.html', form=form)

@app.route('/delete_course/<int:course_id>', methods=['POST'])
def delete_course(course_id):
    if not isUserAdmin():
        abort(403)  # Отказ в доступе, если пользователь не администратор

    course = Course.query.get_or_404(course_id)  # Получаем курс или 404, если не найден
    db.session.delete(course)  # Удаляем курс из сессии
    db.session.commit()  # Сохраняем изменения
    flash('Курс успешно удалён!', 'success')  # Показываем сообщение об успехе
    return redirect("/")  

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Найдите пользователя по имени
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):  # Проверьте правильность пароля
            login_user(user)  # Выполняем вход
            flash('Успешный вход!', 'success')
            return redirect(url_for('dashboard'))  # Перенаправляем на главную страницу или страницу профиля
        else:
            flash('Неправильное имя пользователя или пароль.', 'danger')

    return render_template('login.html')  # Отобразите страницу входа

@app.route('/logout')
@login_required  # Только для зарегистрированных пользователей
def logout():
    logout_user()  # Выполняем выход
    flash('Вы вышли из системы.', 'success')
    return redirect(url_for('login'))  # Перенаправляем на страницу входа

def isUserAdmin():
    return current_user.is_authenticated and current_user.role == 'admin'

def get_year_choices():
    current_year = datetime.now().year
    years = [(str(year), str(year)) for year in range(current_year - 10, current_year + 1)]
    return years

if __name__ == '__main__':
    app.run(debug=True)