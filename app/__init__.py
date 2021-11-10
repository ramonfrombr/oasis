import os

from flask import Flask

from flask_mysqldb import MySQL

#from flask_uploads import UploadSet, configure_uploads, IMAGES


# Globally accessible libraries
mysql = MySQL()



def create_app(test_config=None):


    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    app.config['TEMPLATES_AUTO_RELOAD'] = True

    app.config['MYSQL_HOST'] = 'sql10.freesqldatabase.com'
    app.config['MYSQL_USER'] = 'sql10449991'
    app.config['MYSQL_PASSWORD'] = '6lbNDRv4D8'
    app.config['MYSQL_DB'] = 'sql10449991'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

    #app.config['UPLOADED_PHOTOS_DEST'] = 'static/image/produto'

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

    #photos = UploadSet('photos', IMAGES)

    #configure_uploads(app, photos)

    mysql.init_app(app)


    # REGISTRANDO ROTAS

    from .autorizar import autorizar as autorizar_blueprint
    app.register_blueprint(autorizar_blueprint, url_prefix='/autorizar')

    from .inicio import inicio as inicio_blueprint
    app.register_blueprint(inicio_blueprint, url_prefix='/')
    
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .mensagens import mensagens as mensagens_blueprint
    app.register_blueprint(mensagens_blueprint, url_prefix='/mensagens')

    from .secao import secao as secao_blueprint
    app.register_blueprint(secao_blueprint, url_prefix='/secao')


    # a simple page that says hello

    return app