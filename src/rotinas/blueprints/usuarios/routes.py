from flask import render_template, request, redirect, url_for
from . import bp
from ...extensions import db
from ...models import Usuario, Log

@bp.route("/", methods=["GET"])
def listar():
    usuarios = Usuario.query.all()
    return render_template("usuarios/lista.html", usuarios=usuarios)

@bp.route("/criar", methods=["GET", "POST"])
def criar():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")

        novo = Usuario(nome=nome, email=email)
        db.session.add(novo)
        db.session.commit()

        log = Log(acao="CRIAR_USUARIO", descricao=f"Usuário '{nome}' criado")
        db.session.add(log)
        db.session.commit()

        return redirect(url_for("usuarios.listar"))

    return render_template("usuarios/criar.html")

@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    u = Usuario.query.get_or_404(id)
    if request.method == "POST":
        u.nome = request.form.get("nome", u.nome)
        u.email = request.form.get("email", u.email)
        db.session.commit()
        return redirect(url_for("usuarios.listar"))
    return render_template("usuarios/criar.html", usuario=u)

@bp.route("/<int:id>/deletar")
def deletar(id):
    u = Usuario.query.get_or_404(id)
    db.session.delete(u)
    db.session.commit()
    return redirect(url_for("usuarios.listar"))