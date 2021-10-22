from flask import Blueprint, render_template, request
from .models import Condominio, Usuario, Encomenda
from flask_login import current_user, login_required
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/home')
@login_required
def home():
    qtd = Encomenda.query.filter_by(recebimento_porteiro='Não', encomenda_usuario=current_user.id).count()

    return render_template('home.html', usuario=current_user, qtd_encomenda=qtd)

@views.route('/listar/morador_id', methods=['POST'])
def listar_morador_id():
    id = json.loads(request.data)
    id_cond = id['condId']

    morador = Usuario.query.filter_by(tipo_conta='Morador', usuario_condominio=int(id_cond))

    # lista = []
    # dicionario = {}

    # if morador:
    #     for m in morador:
    #         dicionario['nome'] = m.nome
    #         dicionario['id'] = m.id
    #         dicionario['apto'] = m.apto

    #         lista.append(dicionario.copy())
    return morador.__dict__

@views.route('/listar/condominio')
@login_required
def listar_condominio():
    condominio = Condominio.query.all()

    return render_template('listar_condominio.html', usuario=current_user, condominio=condominio)

@views.route('/listar/encomenda', methods=['GET', 'POST'])
@login_required
def listar_encomendas():
    if current_user.tipo_conta == 'Porteiro':
        encomendas = db.session.query(Encomenda)\
            .join(Usuario, Encomenda.encomenda_usuario == Usuario.id)\
            .join(Condominio, Usuario.usuario_condominio == Condominio.id)\
            .filter_by(id=current_user.usuario_condominio).order_by(Encomenda.id)

        return render_template('listar_encomendas.html', 
                                usuario=current_user, 
                                encomendas=encomendas)
    elif current_user.tipo_conta == 'Administrador':
        encomendas_admin = Encomenda.query.all()

        return render_template('listar_encomendas.html', 
                usuario=current_user, encomendas=encomendas_admin)

@views.route('/listar/encomenda_morador', methods=['GET'])
@login_required
def listar_encomendas_morador():
    encomendas_morador = Encomenda.query.filter_by(encomenda_usuario=current_user.id, recebimento_porteiro='Sim')

    return render_template('listar_encomenda_morador.html', usuario=current_user, encomendas=encomendas_morador)

@views.route('/listar/usuario', methods=['GET', 'POST'])
@login_required
def listar_usuario():
    usuarios = Usuario.query.all()

    return render_template('listar_usuario.html',
                            usuario=current_user, 
                            usuarios=usuarios)

@views.route('/perfil', methods=['GET'])
@login_required
def perfil():
    return render_template('perfil.html', usuario=current_user)
