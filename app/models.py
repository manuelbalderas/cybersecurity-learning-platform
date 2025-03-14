from app import db, login

from datetime import datetime

from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow) 

    def __repr__(self):
        return '<Username %r>' % self.username

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    alias = db.Column(db.String(25), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))

    challenges = db.relationship('Challenge', back_populates='course')

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    alias = db.Column(db.String(25), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))

    challenges = db.relationship('Challenge', back_populates='category')

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    alias = db.Column(db.String(25), nullable=False)
    description = db.Column(db.Text)
    files = db.Column(db.String(255))
    resources = db.Column(db.String(255))
    flag = db.Column(db.String(30), nullable=False)

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    course = db.relationship('Course', back_populates='challenges')
    category = db.relationship('Category', back_populates='challenges')