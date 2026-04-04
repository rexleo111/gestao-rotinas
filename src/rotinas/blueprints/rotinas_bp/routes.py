from flask import render_template, request, redirect, url_for
from . import bp
from ...extensions import db
from ...models import Rotina, Usuario, Log

@bp.route("/", methods=["GET"])
def listar():
    rotinas = Rotina.query.all()
    return render_template("rotinas_bp/lista.html", rotinas=rotinas)

@bp.route("/criar", methods=["GET", "POST"])
def criar():
    if request.method == "POST":
        titulo = request.form.get("titulo")
        descricao = request.form.get("descricao")
        usuario_id = request.form.get("usuario_id")

        nova = Rotina(titulo=titulo, descricao=descricao, usuario_id=usuario_id)
        db.session.add(nova)
        db.session.commit()

        log = Log(acao="CRIAR_ROTINA", descricao=f"Rotina '{titulo}' criada")
        db.session.add(log)
        db.session.commit()

        return redirect(url_for("rotinas_bp.listar"))

    usuarios = Usuario.query.all()
    return render_template("rotinas_bp/criar.html", usuarios=usuarios)

@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    r = Rotina.query.get_or_404(id)
    if request.method == "POST":
        r.titulo = request.form.get("titulo", r.titulo)
        r.descricao = request.form.get("descricao", r.descricao)
        db.session.commit()
        return redirect(url_for("rotinas_bp.listar"))
    return render_template("rotinas_bp/editar.html", rotina=r)

@bp.route("/<int:id>/toggle")
def toggle(id):
    r = Rotina.query.get_or_404(id)
    r.ativa = not r.ativa
    db.session.commit()

    status = "ativada" if r.ativa else "desativada"
    log = Log(acao="TOGGLE_ROTINA", descricao=f"Rotina '{r.titulo}' {status}")
    db.session.add(log)
    db.session.commit()

    return redirect(url_for("rotinas_bp.listar"))

@bp.route("/<int:id>/deletar")
def deletar(id):
    r = Rotina.query.get_or_404(id)
    db.session.delete(r)
    db.session.commit()
    return redirect(url_for("rotinas_bp.listar"))