from flask import redirect, url_for, session

from functools import wraps


def usuario_conectado(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'usuario_conectado' in session:
            return f(*args, *kwargs)
        else:
            return redirect(url_for('autorizar.entrar'))

    return wrap


def usuario_nao_conectado(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'usuario_conectado' in session:
            return redirect(url_for('inicio.inicio'))
        else:
            return f(*args, *kwargs)

    return wrap


def admin_conectado(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_conectado' in session:
            return f(*args, *kwargs)
        else:
            return redirect(url_for('admin.admin_entrar'))

    return wrap


def admin_nao_conectado(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_conectado' in session:
            return redirect(url_for('admin.admin'))
        else:
            return f(*args, *kwargs)

    return wrap


def wrappers(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)

    return wrapped

