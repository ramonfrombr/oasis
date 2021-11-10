from flask import (
    Flask,
    render_template,
    flash,
    redirect,
    url_for,
    session,
    request,
    logging
)

from flask_mysqldb import MySQL



app = Flask(__name__)








app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'oasisadmin'
app.config['MYSQL_PASSWORD'] = 'senha'
app.config['MYSQL_DB'] = 'OasisDB'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'




if __name__ == '__main__':
    app.run(debug=True)
