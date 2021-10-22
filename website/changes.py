from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from .models import Condominio, Usuario, Encomenda
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import json

changes = Blueprint('changes', __name__)

@changes.route('/registrar/condominio', methods=['GET', 'POST'])
@login_required
def registrar_condominio():
    if request.method == 'POST':
        nome_condominio = request.form['nome_condominio']
        endereco = request.form['endereco']
        estado = request.form['estado']

        condominio = Condominio.query.filter_by(endereco=endereco).first()
        if condominio:
            flash('O endereço já está registrado em outro condomínio.', category='erro')
        if len(nome_condominio) < 3:
            flash('Nome do condomínio muito curto.', category='erro')
        else:
            novo_condominio = Condominio(nome=nome_condominio, endereco=endereco, estado=estado)
            db.session.add(novo_condominio)
            db.session.commit()
            flash('Condomínio cadastrado com sucesso!', category='sucesso')
            
    return render_template('registrar_condominio.html', usuario=current_user)

@changes.route('/registrar/usuario', methods=['GET', 'POST'])
@login_required
def registrar_usuario():
    cond = Condominio.query.all()

    if request.method == 'POST':
        nome = request.form['nome']
        login = request.form['login']
        senha = request.form['senha']
        tipo_conta = request.form['tipo_conta']
        

        if tipo_conta == 'Morador':
            usuario = Usuario.query.filter_by(login=login).first()

            usuario_condominio = request.form['usuario_condominio']
            apartamento = request.form['apartamento']

            if usuario:
                flash('O login informado já está cadastrado.', category='erro')
            else:
                novo_usuario = Usuario(nome=nome, login=login, senha=generate_password_hash(senha, method='sha256'), apto=apartamento, tipo_conta=tipo_conta, usuario_condominio=int(usuario_condominio))
                db.session.add(novo_usuario)
                db.session.commit()
                flash('Usuario cadastrado com sucesso.', category='sucesso')

        elif tipo_conta == 'Porteiro':
            usuario = Usuario.query.filter_by(login=login).first()

            usuario_condominio = request.form['usuario_condominio']

            if usuario:
                flash('O login informado já está cadastrado.', category='erro')
            else:
                novo_usuario = Usuario(nome=nome, login=login, senha=generate_password_hash(senha, method='sha256'), tipo_conta=tipo_conta, usuario_condominio=int(usuario_condominio))

                db.session.add(novo_usuario)
                db.session.commit() 
                flash('Usuario cadastrado com sucesso.', category='sucesso')       

        elif tipo_conta == 'Administrador':
            usuario = Usuario.query.filter_by(login=login).first()

            if usuario:
                flash('O login informado já está cadastrado.', category='erro')
            else:
                novo_usuario = Usuario(nome=nome, login=login, senha=generate_password_hash(senha, method='sha256'), tipo_conta=tipo_conta)
                db.session.add(novo_usuario)
                db.session.commit()
                flash('Usuario cadastrado com sucesso.', category='sucesso')    

    return render_template('registrar_usuario.html', condominio=cond, usuario=current_user)

@changes.route('/registrar/encomenda', methods=['GET', 'POST'])
@login_required
def registrar_encomenda():
    morador = Usuario.query.filter_by(usuario_condominio=current_user.usuario_condominio, 
    tipo_conta='Morador')

    if request.method == 'POST':
        if current_user.tipo_conta == "Porteiro":
            descricao = request.form['descricao']
            qtd = request.form['qtd']
            recebimento_porteiro = request.form['recebimento_porteiro']
            morador_id = request.form['morador_id']
            recebimento_morador = 'Não'

            nova_encomenda = Encomenda(descricao=descricao, 
                                        qtd=qtd, 
                                        recebimento_porteiro=recebimento_porteiro,
                                        encomenda_usuario=int(morador_id),
                                        recebimento_morador=recebimento_morador)

            db.session.add(nova_encomenda)
            db.session.commit()

            flash('Encomenda cadastrada com sucesso.', category='sucesso')

    return render_template('registrar_encomenda_porteiro.html', 
                            usuario=current_user, 
                            morador=morador)

@changes.route('/registrar/encomenda_admin', methods=['GET', 'POST'])
@login_required
def registrar_encomenda_admin():
    condominio = Condominio.query.all()

    if request.method == 'POST':
        descricao = request.form['descricao']
        qtd = request.form['qtd']
        recebimento_porteiro = 'Não'
        morador_id = request.form['morador_id']

        nova_encomenda = Encomenda(descricao=descricao, qtd=qtd, recebimento_porteiro=recebimento_porteiro, encomenda_usuario=int(morador_id), recebimento_morador='Não')

        db.session.add(nova_encomenda)
        db.session.commit()
        flash('Encomenda cadastrada com sucesso.', category='sucesso')
        print('Chegou aqui')

    return render_template('registrar_encomenda_admin.html', usuario=current_user, condominio=condominio)

@changes.route('/alterar/recebimento_porteiro', methods=['POST'])
def alterar_recebimento():
    dado = json.loads(request.data)
    id = dado['Id']

    encomenda = Encomenda.query.filter_by(id=id, recebimento_porteiro='Não').update(dict(recebimento_porteiro='Sim'))
    db.session.commit()
    flash('Encomenda liberada para o recebimento.', category='sucesso')

    return jsonify({})

@changes.route('/alterar/recebimento_morador', methods=['POST'])
def alterar_recebimento_morador():
    dado = json.loads(request.data)
    id = dado['Id']

    encomenda = Encomenda.query.filter_by(id=id, recebimento_morador='Não').update(dict(recebimento_morador='Sim'))
    db.session.commit()
    flash('Encomenda recebida com sucesso.', category='sucesso')

    return jsonify({})

@changes.route('/alterar/login', methods=['POST'])
def alterar_login():
    if request.method == 'POST':
        usuario_id = request.form['usuario_id']
        login = request.form['login']

        Usuario.query.filter_by(id=usuario_id).update(dict(login=login))
        db.session.commit()
        flash('Login alterado com sucesso, você foi redireciona para a página de login para entrar novamente com sua nova credencial.', category='sucesso')
        return redirect(url_for('auth.logout'))

@changes.route('/alterar/nome', methods=['POST'])
def alterar_nome():
    if request.method == 'POST':
        nome_usuario = request.form['nome_usuario']
        usuario_id = request.form['usuario_id']

        Usuario.query.filter_by(id=usuario_id).update(dict(nome=nome_usuario))
        db.session.commit()
        flash('Nome alterado com sucesso.', category='sucesso')
        return redirect(url_for('views.home'))

@changes.route('/alterar/senha', methods=['POST'])
def alterar_senha():
    if request.method == 'POST':
        usuario_id = request.form['usuario_id']
        senha_antiga = request.form['senha_antiga']
        senha_nova = request.form['senha_nova']

        checar = Usuario.query.filter_by(id=usuario_id).first()

        if checar:
            if check_password_hash(checar.senha, senha_antiga):
                Usuario.query.filter_by(id=usuario_id).update(dict(senha=generate_password_hash(senha_nova, method='sha256')))
                db.session.commit()
                flash('Senha alterada com sucesso, você foi redirecionado para o login entre com sua nova senha.', category='sucesso')
                return redirect(url_for('auth.logout'))
            else:
                flash('Você deve digitar a senha atual corretamente para que a alteração tenha efeito.', category='erro')           
    return
