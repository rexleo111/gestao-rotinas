from .extensions import db
from datetime import datetime, date

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    rotinas = db.relationship("Rotina", backref="usuario", lazy=True, cascade="all, delete-orphan")

class Rotina(db.Model):
    __tablename__ = "rotinas"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255))
    ativa = db.Column(db.Boolean, default=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    criada_em = db.Column(db.DateTime, default=datetime.utcnow)

    execucoes = db.relationship("Execucao", backref="rotina", lazy=True, cascade="all, delete-orphan")

class Execucao(db.Model):
    __tablename__ = "execucoes"

    id = db.Column(db.Integer, primary_key=True)
    rotina_id = db.Column(db.Integer, db.ForeignKey("rotinas.id"), nullable=False)
    data_execucao = db.Column(db.Date, default=date.today)
    observacao = db.Column(db.String(255))

class Log(db.Model):
    __tablename__ = "logs"

    id = db.Column(db.Integer, primary_key=True)
    acao = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255))
    data_hora = db.Column(db.DateTime, default=datetime.utcnow)