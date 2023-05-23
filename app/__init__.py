from flask import Flask, render_template, redirect, url_for, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Check if the SQLite database file exists
if not os.path.exists(app.config['SQLALCHEMY_DATABASE_URI']):
    with app.app_context():
        db.create_all()

from app import routes, models


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.sb'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Falses