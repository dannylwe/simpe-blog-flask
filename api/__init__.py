from api.User.user_model import User
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash

db =  SQLAlchemy()

def create_app():
    """
    Initialises the app and the database
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskdatabase.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    CORS(app)

    db.init_app(app)

    from api.Blog.blog_routes import blogs
    app.register_blueprint(blogs)

    @click.command(name='create_admin')
    @with_appcontext
    def create_admin():
        admin = User(email="admin_email_address", password="admin_password")
        admin.password = generate_password_hash(admin.password, 'sha256', salt_length=12)
        db.session.add(admin)
        db.session.commit()
    app.cli.add_command(create_admin)
    
    return app