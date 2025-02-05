from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')  # 'admin' or 'user'

    @property
    def password(self):
        raise AttributeError()

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return self.name

class Audience(db.Model):
    __tablename__ = 'audiences'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return self.type

class Link(db.Model):
    __tablename__ = 'links'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False) 

    def __repr__(self):
        return self.type

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    year = db.Column(db.Integer)
    authors = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200), nullable=False)

    link_id = db.Column(db.Integer, db.ForeignKey('links.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    audience_id = db.Column(db.Integer, db.ForeignKey('audiences.id'))

    link = db.relationship('Link', backref=db.backref('courses', lazy=True))
    category = db.relationship('Category', backref=db.backref('courses', lazy=True))
    audience = db.relationship('Audience', backref=db.backref('courses', lazy=True))

    def get_authors(self):
        return self.authors.split(';')

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)