from flask import render_template, request, redirect, url_for
from datetime import date
from . import bp
from ...extensions import db
from ...models import Rotina, Execucao, Log

@bp.route("/", methods=["GET"])
def listar():
    execucoes = Execucao.query.all()
    return render_template("execucoes/lista.html", execucoes=execucoes)

@bp.route("/criar", methods=["GET", "POST"])
def criar():
    erro = None

    if request.method == "POST":
        rotina_id = request.form.get("rotina_id")
        observacao = request.form.get("observacao")
        rotina = Rotina.query.get_or_404(rotina_id)

        # REGRA 1: rotina precisa estar ativa
        if not rotina.ativa:
            erro = "Rotina inativa. Não é possível registrar execução."

        # REGRA 2: só pode executar uma vez por dia
        if not erro:
            hoje = date.today()
            ja_executou = Execucao.query.filter_by(rotina_id=rotina_id, data_execucao=hoje).first()
            if ja_executou:
                erro = "Esta rotina já foi executada hoje."

        if not erro:
            execucao = Execucao(rotina_id=rotina_id, observacao=observacao)
            db.session.add(execucao)
            db.session.commit()

            log = Log(acao="EXECUTAR_ROTINA", descricao=f"Rotina '{rotina.titulo}' executada em {date.today()}")
            db.session.add(log)
            db.session.commit()

            return redirect(url_for("execucoes.listar"))

    rotinas = Rotina.query.all()
    return render_template("execucoes/criar.html", rotinas=rotinas, erro=erro)

@bp.route("/<int:id>/deletar")
def deletar(id):
    e = Execucao.query.get_or_404(id)
    db.session.delete(e)
    db.session.commit()
    return redirect(url_for("execucoes.listar"))