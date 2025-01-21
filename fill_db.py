from run import create_app
from app.models import db, Category, Audience, Course

def fill_database():
    app = create_app()
    with app.app_context():  # Входим в контекст приложения
        # Удаляем все существующие данные и создаем новую базу
        db.drop_all()
        db.create_all()

        # Добавляем категории
        category1 = Category(name='Программирование')
        category2 = Category(name='Дизайн')
        category3 = Category(name='Маркетинг')

        db.session.add(category1)
        db.session.add(category2)
        db.session.add(category3)
        db.session.commit()  # Обязательно

        # Добавляем аудиторию
        audience1 = Audience(type='Начинающие')
        audience2 = Audience(type='Продвинутые')
        audience3 = Audience(type='Специалисты')

        db.session.add(audience1)
        db.session.add(audience2)
        db.session.add(audience3)
        db.session.commit()  # Обязательно

        # Добавляем курсы
        course1 = Course(title='Введение в Python', 
                         description='Основы программирования на Python.', 
                         category_id=category1.id, 
                         graduation_year=2022, 
                         audience_id=audience1.id)
        
        course2 = Course(title='UX/UI Дизайн', 
                         description='Изучите основы проектирования интерфейсов.', 
                         category_id=category2.id, 
                         graduation_year=2023, 
                         audience_id=audience1.id)
        
        course3 = Course(title='Цифровой маркетинг', 
                         description='Как продвигать товары и услуги в интернете.', 
                         category_id=category3.id, 
                         graduation_year=2023, 
                         audience_id=audience2.id)

        db.session.add(course1)
        db.session.add(course2)
        db.session.add(course3)
        db.session.commit()  # Обязательно

        print('База данных успешно заполнена!')

if __name__ == '__main__':
    fill_database()