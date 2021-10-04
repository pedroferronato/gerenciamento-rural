from app.forms.cliente_form import ClienteForm
from app import application, db
from app.models.movimentador import Movimentador
from flask import flash, redirect, url_for, render_template
from flask_login import login_required


@application.route('/cliente')
@login_required
def cliente():
    return render_template('cliente_recepcao.html')


@application.route('/cliente/cadastro', methods=['GET','POST'])
@login_required
def cliente_cadastro():
    form = ClienteForm()
    return render_template('cliente_cadastro.html', form=form, botao="Cadastrar novo cliente")


@application.route('/cliente/busca', methods=['GET','POST'])
@login_required
def cliente_busca():
    form = ClienteForm()
    return render_template('cliente_buscar.html', form=form, botao="Buscar cliente")


@application.route('/cliente/maiores')
@login_required
def cliente_maiores():
    return render_template('cliente_maiores_clientes.html')
