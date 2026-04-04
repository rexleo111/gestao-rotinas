from flask import render_template
from . import bp
from ...models import Log

@bp.route("/", methods=["GET"])
def listar():
    logs = Log.query.order_by(Log.data_hora.desc()).all()
    return render_template("logs/lista.html", logs=logs)