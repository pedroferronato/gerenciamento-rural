from app.forms.login_form import LoginForm
from datetime import date, timedelta

from app import application, login_manager
from flask import session, redirect, render_template, flash, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt

from app.models.produtor import Produtor
from app.models.compra import Compra
from app.models.venda import Venda
from app.models.propriedade import Propriedade


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
    propriedade = Propriedade.query.filter(
        Propriedade.produtor_id == current_user.id,
        Propriedade.ativa == True
    ).first()
    if not propriedade:
        return render_template('inicial.html', propriedade=False)
    propriedade_id = propriedade.id

    hoje = date.today()
    diasDoMes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    lista_despesas = Compra.query.filter_by(propriedade_id = propriedade_id).order_by(Compra.data.desc()).limit(4).all()

    lista_lucros = Venda.query.filter(
        Venda.propriedade_id == propriedade_id,
        Venda.data.between(str(hoje.year)+'-'+str(hoje.month)+'-01', str(hoje.year)+'-'+str(hoje.month)+'-'+str(diasDoMes[hoje.month - 1]))
    ).order_by(Venda.data.desc()).limit(4).all()

    lista_despesas_mes = Compra.query.filter(
        Compra.propriedade_id == propriedade_id,
        Compra.data.between(str(hoje.year)+'-'+str(hoje.month)+'-01', str(hoje.year)+'-'+str(hoje.month)+'-'+str(diasDoMes[hoje.month - 1]))
    ).all()

    lista_lucros_mes = Venda.query.filter(
        Venda.propriedade_id == propriedade_id,
        Venda.data.between(str(hoje.year)+'-'+str(hoje.month)+'-01', str(hoje.year)+'-'+str(hoje.month)+'-'+str(diasDoMes[hoje.month - 1]))
    ).all()

    lista_despesas_mes_anterior = Compra.query.filter(
        Compra.propriedade_id == propriedade_id,
        Compra.data.between(str(hoje.year)+'-'+str(hoje.month - 1)+'-01', str(hoje.year)+'-'+str(hoje.month - 1)+'-'+str(diasDoMes[hoje.month - 2]))
    ).all()

    lista_lucros_mes_anterior = Venda.query.filter(
        Venda.propriedade_id == propriedade_id,
        Venda.data.between(str(hoje.year)+'-'+str(hoje.month - 1)+'-01', str(hoje.year)+'-'+str(hoje.month - 1)+'-'+str(diasDoMes[hoje.month - 2]))
    ).all()

    despesa_mes = 0
    for despesa in lista_despesas_mes:
        despesa_mes += despesa.get_insumo().valor_total
    despesa_mes *= -1

    lucro_mes = 0
    for lucro in lista_lucros_mes:
        lucro_mes += lucro.valor_total

    despesa_mes_anterior = 0
    for despesa in lista_despesas_mes_anterior:
        despesa_mes_anterior += despesa.get_insumo().valor_total
    despesa_mes_anterior *= -1

    lucro_mes_anterior = 0
    for lucro in lista_lucros_mes_anterior:
        lucro_mes_anterior += lucro.valor_total

    caixa_mes = despesa_mes + lucro_mes
    caixa_mes_anterior = despesa_mes_anterior + lucro_mes_anterior

    return render_template('inicial.html', 
    propriedade=True,
    despesa_mes='{:.2f}'.format(despesa_mes).replace('.', ','), 
    lucro_mes='{:.2f}'.format(lucro_mes).replace('.', ','), 
    lista_lucros=lista_lucros, lista_despesas=lista_despesas, 
    despesa_mes_anterior='{:.2f}'.format(despesa_mes_anterior).replace('.', ','), 
    lucro_mes_anterior='{:.2f}'.format(lucro_mes_anterior).replace('.', ','),
    caixa_mes=caixa_mes, caixa_mes_anterior='{:.2f}'.format(caixa_mes_anterior).replace('.', ','))


@application.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login = form.usuario.data
        senha = form.senha.data

        produtor = Produtor.query.filter_by(login=login).first()

        autorizado = False

        if produtor:
            autorizado = bcrypt.checkpw(senha.encode('UTF-8'), produtor.senha.encode('UTF-8'))

        if not produtor or not autorizado:
            flash("Login não autorizado, verificar informações", 'flash-falha')
            return redirect(url_for('login'))
        else:
            login_user(produtor, remember=False)
            return redirect(url_for('inicial'))
    return render_template('login.html', form=form)


@application.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
