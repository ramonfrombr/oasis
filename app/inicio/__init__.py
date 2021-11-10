from flask import Blueprint

# 'autorizar' é o nome do Blueprint, e __name__ é o nome do módulo/pacote onde o blueprint está localizado
inicio = Blueprint('inicio', __name__)

from . import rotas
