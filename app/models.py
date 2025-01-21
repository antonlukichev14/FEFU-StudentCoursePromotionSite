from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')  # 'admin' or 'user'

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Category {self.name}>'

class Audience(db.Model):
    __tablename__ = 'audiences'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Audience {self.type}>'

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    graduation_year = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    audience_id = db.Column(db.Integer, db.ForeignKey('audiences.id'))

    category = db.relationship('Category', backref=db.backref('courses', lazy=True))
    audience = db.relationship('Audience', backref=db.backref('courses', lazy=True))

    def __repr__(self):
        return f'<Course {self.title}>'