from flask import Blueprint, url_for, redirect, render_template, request, flash
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import check_password_hash
from .models import Usuario

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def login_usuario():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        login = request.form['login']
        senha = request.form['senha']

        usuario = Usuario.query.filter_by(login=login).first()

        if usuario:
            if check_password_hash(usuario.senha, senha):
                flash('Login efetuado com sucesso.', category='sucesso')
                login_user(usuario, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Senha incorreta, tente novamente.', category='erro')
        else:
            flash('Usuario não encontrado, verifique seu login.', category='erro')

    return render_template('login_usuario.html', usuario=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login_usuario'))
