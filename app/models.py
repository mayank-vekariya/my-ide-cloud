from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()
class Project(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    github_url = db.Column(db.String(255), nullable=False)
    s3_url = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), nullable=False)
    url = db.Column(db.String(255), nullable=True)
    project_name = db.Column(db.String(100), nullable=False)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


