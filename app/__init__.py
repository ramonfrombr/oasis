import os
from flask import Flask
from flask_mysqldb import MySQL
from flask_uploads import configure_uploads


"""
    Outras bibliotecas usadas no projeto

    from flask import Flask, render_template, flash, redirect, url_for, session, request, logging

    from flask_mysqldb import MySQL

    from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField

    from passlib.hash import sha256_crypt

    from functools import wraps

    from flask_uploads import UploadSet, configure_uploads, IMAGES

    import timeit

    import datetime

    from flask_mail import Mail, Message

    import os

    from wtforms.fields.html5 import EmailField
"""





# Globally accessible libraries
mysql = MySQL()

from app.admin.rotas import fotos as photos


def create_app(test_config=None):

    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    app.config['TEMPLATES_AUTO_RELOAD'] = True

    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'oasisadmin'
    app.config['MYSQL_PASSWORD'] = 'senha'
    app.config['MYSQL_DB'] = 'oasisDB'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

    app.config['UPLOADED_PHOTOS_DEST'] = 'app/static/image/produto'


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)


    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass



    configure_uploads(app, photos)


    mysql.init_app(app)


    # REGISTRANDO ROTAS
    
    from .inicio import inicio as inicio_blueprint
    app.register_blueprint(inicio_blueprint, url_prefix='/')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .autorizar import autorizar as autorizar_blueprint
    app.register_blueprint(autorizar_blueprint, url_prefix='/autorizar')

    from .mensagens import mensagens as mensagens_blueprint
    app.register_blueprint(mensagens_blueprint, url_prefix='/mensagens')

    from .secao import secao as secao_blueprint
    app.register_blueprint(secao_blueprint, url_prefix='/secao')

    return app