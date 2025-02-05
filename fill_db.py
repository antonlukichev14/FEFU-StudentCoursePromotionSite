from run import create_app
from app.models import db, Category, Audience, Course, Link
import pandas as pd

def fill_database():
    app = create_app()

    with app.app_context(): 
        Course.query.delete()
        Category.query.delete()
        Audience.query.delete()
        Link.query.delete()

        df = pd.read_excel("Курсы.xlsx")
        
        for index, row in df.iterrows():
            title = row["Название"]
            description = row["Описание"]
            category_name = row["Категория"]
            year = row["Дата"].year
            audience_type = row["Подходит для"]
            authors = row["Авторы"].replace(", ", ";")
            link_type = row["Платформа"]
            url = row["Ссылка"]

            category = Category.query.filter_by(name=category_name).first()
            if not category:
                category = Category(name=category_name)
                db.session.add(category)
                db.session.commit()
            category_id = category.id

            audience = Audience.query.filter_by(type=audience_type).first()
            if not audience:
                audience = Audience(type=audience_type)
                db.session.add(audience)
                db.session.commit()
            audience_id = audience.id

            link = Link.query.filter_by(type=link_type).first()
            if not link:
                link = Link(type=link_type)
                db.session.add(link)
                db.session.commit()
            link_id = link.id

            course = Course(
                title=title,
                description=description,
                year=year,
                category_id=category_id,
                audience_id=audience_id,
                link_id=link_id,
                url=url,
                authors=authors
            )
            db.session.add(course)
            db.session.commit()

if __name__ == '__main__':
    fill_database()