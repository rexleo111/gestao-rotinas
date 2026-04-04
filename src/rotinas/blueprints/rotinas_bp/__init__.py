from flask import Blueprint

bp = Blueprint("rotinas_bp", __name__)

from . import routes