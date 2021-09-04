from datetime import timedelta

from app import application, login_manager, db
from flask import session, redirect, render_template, request, flash, redirect, url_for
from flask_login import login_required, login_user, logout_user
import bcrypt

from app.models.produtor import Produtor


@application.before_request
def make_session_permanent():
    session.permanent = True
    application.permanent_session_lifetime = timedelta(minutes=60)
    session.modified = True


@login_manager.unauthorized_handler
def not_allowed():
    return redirect('/login')


@login_manager.user_loader
def get_user(produtor_id):
    return Produtor.query.filter_by(id=produtor_id).first()


@application.route('/')
@login_required
def inicial():
    return render_template('inicial.html')


@application.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        
        login = request.form['login']
        senha = request.form['senha']

        produtor = Produtor.query.filter_by(login=login).first()

        autorizado = False

        if produtor:
            autorizado = bcrypt.checkpw(senha.encode('UTF-8'), produtor.senha.encode('UTF-8'))

        if not produtor or not autorizado:
            flash("Login não autorizado, verificar informações")
            return redirect(url_for('login'))
        else:
            login_user(produtor, remember=False)
            return redirect(url_for('inicial'))


@application.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
