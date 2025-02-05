from run import create_app
from app.models import db, Category, Audience, Course, Link

def fill_database():
    app = create_app()

    with app.app_context():  # Входим в контекст приложения
        # Удаляем все существующие данные и создаем новую базу
        Course.query.delete()
        Category.query.delete()
        Audience.query.delete()
        Link.query.delete()

        # Добавляем категории
        category1 = Category(name='Математика')
        category2 = Category(name='Информатика')

        db.session.add(category1)
        db.session.add(category2)
        db.session.commit()  # Обязательно

        # Добавляем аудиторию
        audience1 = Audience(type='Школьников')
        audience2 = Audience(type='Студентов')
        audience3 = Audience(type='Взрослых')

        db.session.add(audience1)
        db.session.add(audience2)
        db.session.add(audience3)
        db.session.commit()  # Обязательно

        link1 = Link(type='STEPIK')

        db.session.add(link1)
        db.session.commit() 

        # Добавляем курсы
        course1 = Course(title='Дифференциальные уравнения первого порядка', 
                         description='Запишитесь на наш курс и откройте для себя увлекательный мир дифференциальных уравнений! Доступ к полезным материалам и возможность учиться в удобном для вас темпе — всё это поможет вам достичь успеха в изучении математики. Не упустите шанс стать мастером в решении дифференциальных уравнений!',
                         year=2023, 
                         url='https://stepik.org/course/225581',
                         authors='Михайлова А.;Им М;Тесля Н.;Сакамаркин В.;Давидчук В.',
                         link_id=link1.id,
                         category_id=category1.id,
                         audience_id=audience2.id)
        
        course2 = Course(title='Тригонометрия', 
                         description='Тригонометрия – это основа, без которой невозможно представить современную науку, архитектуру и даже компьютерные технологии. Наш курс создан, чтобы сделать этот путь понятным, интересным и доступным каждому.',
                         year=2024, 
                         url='https://stepik.org/course/225581',
                         authors='Олейник В.В.;Козырев Д.В.;Трякшин А.А.',
                         link_id=link1.id,
                         category_id=category2.id,
                         audience_id=audience1.id)

        db.session.add(course1)
        db.session.add(course2)
        db.session.commit()  # Обязательно

        print('База данных успешно заполнена!')

if __name__ == '__main__':
    fill_database()