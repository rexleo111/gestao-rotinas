from flask import Blueprint

bp = Blueprint("execucoes", __name__)

from . import routes