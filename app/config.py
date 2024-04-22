# app/config.py
import os

class Config:
    SECRET_KEY = '94724552428d304772ad89fdb6df9a21'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
