from datetime import date, datetime
from app.models.compra import Compra
from app.forms.compra_form import CompraForm
from app.forms.compra_historico_form import CompraHistoricoForm
from app import db, application
from sqlalchemy import and_
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, flash, request

from app.models.insumo import Insumo
from app.models.movimentador import Movimentador
from app.models.propriedade import Propriedade


@application.route('/despesas')
@login_required
def despesa():
    return render_template('compra_recepcao.html')


@application.route('/despesas/compra', methods=['GET', 'POST'])
@login_required
def despesas_compra():
    form = CompraForm()

    selecione = [(0, "Selecione")]

    fornecedores = Movimentador.query.filter_by(produtor_id=current_user.id, tipo="Fornecedor").all()
    fornecedores_escolhas = selecione + [(fornecedor.id, fornecedor.nome) for fornecedor in fornecedores]
    form.fornecedor.choices = fornecedores_escolhas

    finalidades = selecione + [(1, "Cultivo"), (2, "Fertilização"), (3, "Defensivo"), (4, "Manutenção")]
    form.finalidade.choices = finalidades

    if form.validate_on_submit():
        propriedade = Propriedade.query.filter_by(produtor_id=current_user.id).first()
        if not propriedade:
            flash("Você precisa cadastrar sua propriedade para registrar compras", 'flash-alerta')
            return redirect(url_for('despesas_compra'))
        
        finalidade = dict(finalidades).get(int(form.finalidade.data))

        if not finalidade in [f for (i, f) in finalidades]:
            flash("Insira apenas as funcionalidades originais", 'flash-falha')
            return redirect(url_for('despesas_compra'))

        fornecedor_selecionado = request.form['data-fornecedor']
        filtros = [
            Movimentador.tipo == "Fornecedor",
            Movimentador.nome == fornecedor_selecionado,
            Movimentador.produtor_id == current_user.id
        ]
        fornecedor_id = Movimentador.query.filter(*filtros).first().id
        
        if not fornecedor_id:
            flash("Fornecedor não encontrado", 'flash-falha')
            return redirect(url_for('despesas_compra'))

        if form.data.data < date(2010, 1, 1):
            flash("Data muito antiga", 'flash-falha')
            return redirect(url_for('despesas_compra'))

        insumo = Insumo(
            fornecedor_id = fornecedor_id,
            propriedade_id = propriedade.id,
            nome = form.insumo.data,
            quantidade = form.quantidade.data,
            quantidade_estocada = form.quantidade.data,
            valor_unitario = form.valor_unitario.data,
            valor_total = form.valor_total.data,
            utilidade = finalidade,
            unidade_medida = form.unidade.data
        )

        try:
            db.session.add(insumo)
            db.session.flush()
            db.session.refresh(insumo)
            compra = Compra(
                propriedade_id = propriedade.id,
                data = form.data.data,
                insumo_id = insumo.id,
                movimentador_id = fornecedor_id,
                desconto = form.desconto.data
            )
            db.session.add(compra)
            db.session.commit()
        except Exception as e:
            print(e)
            flash('Falha ao registrar compra, falha ao conectar ao banco de dados', 'flash-falha')
            return redirect(url_for('despesas_compra'))
        
        flash('Compra registrada com sucesso', 'flash-sucesso')
        return redirect(url_for('despesa'))
        
    return render_template('compra_adicionar.html', form=form, botao="Registrar compra", fornecedores=fornecedores)


def setup_formulario_buscar():
    return Movimentador.query.filter_by(produtor_id=current_user.id, tipo="Fornecedor").all()


@application.route('/despesas/compra/historico')
@login_required
def despesas_compra_historico():
    form = CompraHistoricoForm()
    return render_template('compras_historico.html', form=form, botao="Buscar no histórico", fornecedores=setup_formulario_buscar())


@application.route('/despesas/compra/historico/resultado')
@login_required
def despesas_compra_historico_resultado():
    form = CompraHistoricoForm()

    data_inicio = request.args.get('data_inicio')
    data_final = request.args.get('data_final')
    fornecedor = request.args.get('data-fornecedor')
    filtros_forn = [
            Movimentador.tipo == "Fornecedor",
            Movimentador.nome == fornecedor ,
            Movimentador.produtor_id == current_user.id
        ]
    fornecedor = Movimentador.query.filter(*filtros_forn).first().id

    page = request.args.get('page', 1, type=int)

    filtros = []

    if fornecedor != 0 and fornecedor:
        filtros.append(Compra.movimentador_id == fornecedor)

    if data_inicio and not data_final :
        data = datetime.strptime(str(data_inicio), "%d/%m/%Y").date()
        filtros.append(Compra.data == data)

    if data_final and not data_inicio:
        data = datetime.strptime(str(data_final), "%d/%m/%Y").date()
        filtros.append(Compra.data == data)

    if data_final and data_inicio:
        data_inicial = datetime.strptime(str(data_inicio), "%d/%m/%Y").date()
        data_fim = datetime.strptime(str(data_final), "%d/%m/%Y").date()
        filtros.append(and_(Compra.data >= data_inicial, Compra.data <= data_fim))

    if len(filtros) <= 0:
        flash('Insira valores para a busca', 'flash-alerta')
        return redirect(url_for('despesas_compra_historico'))

    compras = Compra.query.filter(*filtros).order_by(Compra.data.desc())

    if len(compras.all()) <= 0:
        flash('Nenhuma compra encontrada', 'flash-alerta')
        return redirect(url_for('despesas_compra_historico'))

    if len(compras.all()) <= 10:
        return render_template('compras_historico.html', form=form, botao="Buscar no histórico", compras=compras.all(), fornecedores=setup_formulario_buscar())

    pages = compras.paginate(page=page, per_page=5)

    return render_template('compras_historico.html', form=form, botao="Buscar no histórico", pages=pages, fornecedores=setup_formulario_buscar())


@application.route('/compra/<compra_id>')
@login_required
def compra_detalhe(compra_id):
    compra = Compra.query.filter_by(id=compra_id).first()
    return render_template('compra_detalhes.html', compra=compra)
