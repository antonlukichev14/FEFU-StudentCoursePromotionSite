from flask import Flask, abort, flash, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, LoginManager, UserMixin, login_user, login_required, logout_user
from datetime import datetime
from app.models import db, Category, Audience, Course, User, Link
from app.forms import CourseForm, SearchForm

def create_app():
    app = Flask(__name__)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get_or_404(int(user_id))

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

    form = SearchForm()

    form.submit.label.text = "Найти"

    form.years.choices = get_year_choices()
    form.categories.choices = [(x.id, x.name) for x in categories]
    form.audiences.choices = [(x.id, x.type) for x in audiences]

    if request.method == 'POST':
        courses_query = Course.query

        if form.title.data:
            courses_query = courses_query.filter(Course.title.contains(form.title.data.lower()))

        if form.categories.data:
            courses_query = (courses_query
                .join(Category)
                .filter(Category.id.in_(form.categories.data))
                .distinct())

        if form.audiences.data:
            courses_query = (courses_query
                .join(Audience)
                .filter(Audience.id.in_(form.audiences.data))
                .distinct())

        if form.years.data:
            courses_query = courses_query.filter(Course.year.in_(form.years.data))

        courses = courses_query.all()

        return render_template(
            'search.html', 
            form=form,
            courses=courses, 
            categories=categories, 
            audiences=audiences, 
            is_user_admin=is_user_admin()
        )        

    courses = Course.query.all()

    return render_template(
        'search.html', 
        form=form,
        courses=courses, 
        categories=categories, 
        audiences=audiences, 
        is_user_admin=is_user_admin()
    )

@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if not is_user_admin():
        abort(403)  # Отказ в доступе, если пользователь не администратор

    form = CourseForm()
    form.submit.label.text = 'Добавить курс'

    form.year.choices = get_year_choices()  # Возможно, сделать выбор годов
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]  # Получаем все категории
    form.audience_id.choices = [(a.id, a.type) for a in Audience.query.all()]  # Получаем всех аудитории
    form.link_id.choices = [(a.id, a.type) for a in Link.query.all()] 

    if form.validate_on_submit():
        new_course = Course(
            title=form.title.data,
            description=form.description.data,
            year=form.year.data,
            category_id=form.category_id.data,
            audience_id=form.audience_id.data,
            link_id=form.link_id.data,
            url=form.url.data,
            authors=form.authors.data
        )
        db.session.add(new_course)
        db.session.commit()
        flash('Курс успешно добавлен!', 'success')
        return redirect("/")  # Перенаправляем на страницу курсов

    return render_template(
        'course.html', 
        title='Добавить курс',
        h1='Добавить новый курс',
        form=form
    )

@app.route('/delete_course/<int:course_id>', methods=['POST'])
def delete_course(course_id):
    if not is_user_admin():
        abort(403)  # Отказ в доступе, если пользователь не администратор

    course = Course.query.get_or_404(course_id)  # Получаем курс или 404, если не найден
    db.session.delete(course)  # Удаляем курс из сессии
    db.session.commit()  # Сохраняем изменения
    flash('Курс успешно удалён!', 'success')  # Показываем сообщение об успехе
    return redirect("/")  

@app.route('/redact_course/<int:course_id>', methods=['GET', 'POST'])
def redact_course(course_id):
    if not is_user_admin():
        abort(403)

    course = Course.query.get_or_404(course_id)

    form = CourseForm(obj=course)

    form.submit.label.text = 'Сохранить изменения'

    form.year.choices = get_year_choices()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()] 
    form.audience_id.choices = [(a.id, a.type) for a in Audience.query.all()]
    form.link_id.choices = [(a.id, a.type) for a in Link.query.all()] 

    if form.validate_on_submit():
        form.populate_obj(course)
        db.session.commit()
        flash('Курс успешно обнавлён!', 'success')

    return render_template(
        'course.html', 
        title='Редактировать курс',
        h1='Редактировать курс',
        form=form
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method != 'POST':
        return render_template('login.html')

    username = request.form.get('username')
    password = request.form.get('password')

    # Найдите пользователя по имени
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('Неправильное имя пользователя или такого пользователя не существует!', 'danger')
        return render_template('login.html')

    if not(user.verify_password(password)):
        flash('Неверный пароль! Проверьте имя пользователя!', 'danger')
        return render_template('login.html')

    login_user(user)  # Выполняем вход
    flash('Успешный вход!', 'success')
    return render_template('login.html')

@app.route('/logout')
@login_required  # Только для зарегистрированных пользователей
def logout():
    logout_user()  # Выполняем выход
    flash('Вы вышли из системы.', 'success')
    return redirect(url_for('login'))  # Перенаправляем на страницу входа

def is_user_admin():
    return current_user.is_authenticated and current_user.role == 'admin'

def get_year_choices():
    years = [(year, f"{year}-{year+1}") for year in range(2023, 2026)]
    return years

if __name__ == '__main__':
    app.run(debug=True)