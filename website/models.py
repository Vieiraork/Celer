from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200))
    login = db.Column(db.String(200), unique=True)
    senha = db.Column(db.String(200))
    apto = db.Column(db.String(100))
    tipo_conta = db.Column(db.String(100))
    usuario_condominio = db.Column(db.Integer, db.ForeignKey('condominio.id'))
    encomenda = db.relationship('Encomenda', backref='usuario')

class Condominio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200))
    endereco = db.Column(db.String(200))
    estado = db.Column(db.String(10))
    usuario = db.relationship('Usuario', backref='condominio')

class Encomenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200))
    data = db.Column(db.DateTime(timezone=True), default=func.now())
    qtd = db.Column(db.Integer)
    recebimento_porteiro = db.Column(db.String(200))
    recebimento_morador = db.Column(db.String(200))
    encomenda_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
