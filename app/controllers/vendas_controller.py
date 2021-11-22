from datetime import date, datetime

from app import application, db
from app.models.venda import Venda
from app.models.propriedade import Propriedade
from app.models.movimentador import Movimentador
from app.models.produto import Produto
from app.forms.venda_form import VendaForm
from flask import flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import and_


@application.route('/venda')
@login_required
def venda():
    return render_template('vendas_recepcao.html')


@application.route('/venda/adicinar', methods=['GET', 'POST'])
@login_required
def venda_adicionar():
    form = VendaForm()

    filtros_clientes = [
        Movimentador.tipo == "Cliente",
        Movimentador.produtor_id == current_user.id
    ]
    clientes = Movimentador.query.filter(*filtros_clientes).order_by(Movimentador.nome.asc()).all()

    propriedade = Propriedade.query.filter_by(produtor_id=current_user.id).first()
    filtros_produtos = [
        Produto.propriedade_id == propriedade.id,
        Produto.quantidade > 0
    ]

    produtos = Produto.query.filter(*filtros_produtos).order_by(Produto.nome.asc()).all()

    if form.validate_on_submit():
        if form.data.data < datetime.date(2018, 1, 1):
            flash("Você está inserindo uma produção muito antiga", 'flash-alerta')
            return redirect(url_for('venda_adicionar'))

        produto = Produto.query.filter_by(id=int(request.form['data-insumo'].split(' - ')[0])).first()

        produto.quantidade -= float(form.quantidade.data)

        if produto.quantidade < float(form.quantidade.data):
            flash("Quantidade vendida não está em estoque", 'flash-alerta')
            return redirect(url_for('venda_adicionar'))

        venda = Venda(
            propriedade_id = propriedade.id,
            data = form.data.data,
            valor_total = form.valor_total.data,
            quantidade = form.quantidade.data,
            valor_unitario = form.valor_unitario.data,
            produto_id = int(request.form['data-insumo'].split(' - ')[0]),
            movimentador_id = int(request.form['data-produto'].split(' - ')[0])
        )

        try:
            db.session.add(produto)
            db.session.add(venda)
            db.session.commit()
        except:
            flash("Falha ao criar venda", 'flash-falha')
            return redirect(url_for('venda_adicionar'))
        flash("Venda criada com sucesso", 'flash-sucesso')
        return redirect(url_for("vendas"))
    return render_template('vendas_adicionar.html', produtos=produtos, clientes=clientes, form=form)


@application.route('/venda/historico')
@login_required
def venda_historico():
    vendas = Venda.query.order_by(Venda.data.desc()).limit(10).all()
    return render_template('vendas_historico.html', vendas=vendas, botao="Buscar vendas")


@application.route('/venda/historico/busca')
@login_required
def venda_historico_busca():
    propriedade = Propriedade.query.filter_by(produtor_id=current_user.id).first()

    page = request.args.get('page', 1, type=int)

    data_inicio = request.args.get('data_inicio')
    data_final = request.args.get('data_final')

    filtros = [
        Venda.propriedade_id == propriedade.id
    ]

    if data_inicio and not data_final :
        data = datetime.strptime(str(data_inicio), "%d/%m/%Y").date()
        filtros.append(Venda.data == data)

    if data_final and not data_inicio:
        data = datetime.strptime(str(data_final), "%d/%m/%Y").date()
        filtros.append(Venda.data == data)

    if data_final and data_inicio:
        data_inicial = datetime.strptime(str(data_inicio), "%d/%m/%Y").date()
        data_fim = datetime.strptime(str(data_final), "%d/%m/%Y").date()
        filtros.append(and_(Venda.data >= data_inicial, Venda.data <= data_fim))

    if len(filtros) <= 1:
        flash('Insira valores para a busca', 'flash-alerta')
        return redirect(url_for('venda_historico'))

    vendas = Venda.query.filter(*filtros).order_by(Venda.data.desc())

    if len(vendas.all()) <= 0:
        flash('Nenhuma venda encontrada', 'flash-alerta')
        return redirect(url_for('venda_historico'))

    if len(vendas.all()) <= 10:
        return render_template('vendas_historico.html', botao="Buscar vendas", vendas=vendas.all())

    pages = vendas.paginate(page=page, per_page=5)
    
    return render_template('vendas_historico.html', pages=pages)


@application.route('/venda/<venda_id>')
@login_required
def venda_detalhes(venda_id):
    venda = Venda.queri.filter_by(id=venda_id).first()

    if not venda:
        flash("Venda não encontrada", 'flash-alerta')
        return redirect(url_for('venda'))

    return render_template('vendas_historico.html', venda=venda)
