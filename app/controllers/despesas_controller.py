from datetime import date
import app
from app.controllers.fornecedor_controller import fornecedor
from app.models.compra import Compra
from app.forms.compra_form import CompraForm
from app import db, application
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
            flash("Você precisa cadastrar sua propriedade para registrar compras")
            return redirect(url_for('despesas_compra'))
        
        finalidade = dict(finalidades).get(int(form.finalidade.data))

        if not finalidade in [f for (i, f) in finalidades]:
            flash("Insira apenas as funcionalidades originais")
            return redirect(url_for('despesas_compra'))

        fornecedor = dict(fornecedores_escolhas).get(int(form.fornecedor.data))

        if not fornecedor in [f for (i, f) in fornecedores_escolhas]:
            flash("Insira apenas as funcionalidades originais")
            return redirect(url_for('despesas_compra'))

        if form.data.data < date(2010, 1, 1):
            flash("Data muito antiga")
            return redirect(url_for('despesas_compra'))

        insumo = Insumo(
            fornecedor_id = int(form.fornecedor.data),
            propriedade_id = propriedade.id,
            nome = form.insumo.data,
            quantidade = form.quantidade.data,
            quantidade_estocada = form.quantidade.data,
            valor_unitario = form.valor_unitario.data,
            valor_total = form.valor_unitario.data,
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
                movimentador_id = int(form.fornecedor.data),
                desconto = form.desconto.data
            )
            db.session.add(compra)
            db.session.commit()
        except Exception as e:
            print(e)
            flash('Falha ao registrar compra, provável falha ao conectar ao banco de dados')
            return redirect(url_for('despesas_compra'))
        
    return render_template('compra_adicionar.html', form=form, botao="Registrar compra")
