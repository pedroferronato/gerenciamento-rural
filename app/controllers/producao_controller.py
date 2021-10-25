import datetime
from app import application, db
from app.forms.producao_form import ProducaoForm
from app.forms.estoque_form import EstoqueForm
from app.forms.producao_finalizada_form import ProducaoFinalizadasForm
from app.models.producao import Producao
from app.models.producao_insumo import ProducaoInsumo
from app.models.propriedade import Propriedade
from app.models.insumo import Insumo
from app.models.produto import Produto
from flask import flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user


@application.route('/producao')
@login_required
def producao():
    return render_template('producao_recepcao.html')


@application.route('/producao/atuais')
@login_required
def producoes_atuais():
    page = request.args.get('page', 1, type=int)

    propriedade = Propriedade.query.filter_by(produtor_id=current_user.id).first()
    filtros = [
        Producao.propriedade_id == propriedade.id,
        Producao.ativa == True,
    ]
    producoes = Producao.query.filter(*filtros).order_by(Producao.data.asc())

    if len(producoes.all()) == 0:
        flash('Nenhuma produção ativa encontrada', 'flash-alerta')
        return render_template('producao_atuais.html')

    if len(producoes.all()) > 10:
        producoes = producoes.paginate(page=page, per_page=10)
        return render_template('producao_atuais.html', pages=producoes)
    
    producoes = producoes.all()

    return render_template('producao_atuais.html', producoes=producoes)


@application.route('/producao/estoque')
@login_required
def producoes_estoque():
    form = EstoqueForm()

    page = request.args.get('page', 1, type=int)
    propriedade_id = Propriedade.query.filter_by(produtor_id=current_user.id).first().id

    filtros = [
        Produto.propriedade_id == propriedade_id,
        Produto.quantidade > 0
    ]

    if form.nome.data:
        filtros.append(Produto.nome == form.nome.data)

    if form.validade.data:
        filtros.append(Produto.validade == form.validade.data)

    produtos_em_estoque = Produto.query.filter(*filtros).order_by(Produto.quantidade.asc())

    if len(produtos_em_estoque.all()) == 0:
        flash('Nenhuma produção ativa encontrada', 'flash-alerta')
        return render_template('producao_estoque.html', form=form)

    if len(produtos_em_estoque.all()) > 10:
        produtos = produtos_em_estoque.paginate(page=page, per_page=10)
        return render_template('producao_estoque.html', pages=produtos, form=form)
    
    produtos = produtos_em_estoque.all()

    return render_template('producao_estoque.html', produto=produtos, form=form)    


@application.route('/producao/finalizadas')
@login_required
def producoes_finalizadas():
    page = request.args.get('page', 1, type=int)
    form = ProducaoFinalizadasForm()

    propriedade_id = Propriedade.query.filter_by(produtor_id=current_user.id).first().id

    filtros = [
        Producao.propriedade_id == propriedade_id,
        Producao.ativa == False
    ]
    
    if form.nome.data:
        filtros.append(Producao.nome == form.nome.data)

    if form.data_comeco.data:
        filtros.append(Producao.data == form.data_comeco.data)

    if form.data_coleta.data:
        filtros.append(Producao.data_coleta == form.data_coleta.data)

    producoes = Producao.query.filter(*filtros).order_by(Producao.data.asc())

    if len(producoes.all()) == 0:
        flash('Nenhuma produção finalizada encontrada', 'flash-alerta')
        return render_template('producao_finalizadas.html')

    if len(producoes.all()) > 10:
        producoes = producoes.paginate(page=page, per_page=10)
        return render_template('producao_finalizadas.html', pages=producoes)
    
    producoes = producoes.all()

    return render_template('producao_finalizadas.html', producoes=producoes, form=form, botao="Buscar")


@application.route('/producao/adicionar', methods=['GET', 'POST'])
@login_required
def producoes_adicionar():
    form = ProducaoForm()
    filtros = [
        Insumo.utilidade == "Criação",
        Insumo.quantidade > 0
    ]
    insumos = Insumo.query.filter(*filtros).order_by(Insumo.nome.asc()).all()
    form.produto.choices = [(insumo.id, insumo.nome) for insumo in insumos]

    if form.validate_on_submit():
        propriedade = Propriedade.query.filter_by(produtor_id=current_user.id).first()
        if not propriedade:
            flash("Você precisa cadastrar sua propriedade para registrar produções", 'flash-alerta')
            return redirect(url_for('producoes_adicionar'))

        if form.data.data < datetime.date(2018, 1, 1):
            flash("Você está inserindo uma prodção muito antiga", 'flash-alerta')
            return redirect(url_for('producoes_adicionar'))
        
        producao = Producao(
            propriedade_id = propriedade.id,
            nome = form.nome.data,
            quantidade = form.quantidade.data,
            ativa = True,
            data = form.data.data
        )

        try:
            db.session.add(producao)
            db.session.flush()
            db.session.refresh(producao)
            insumo_base = ProducaoInsumo(
                producao_id = producao.id,
                insumo_id = form.produto.data,
                base = True
            )
            db.session.add(insumo_base)
            db.session.commit()
        except:
            flash("Falha ao criar produção", 'flash-falha')
            return redirect(url_for('producoes_adicionar'))
        flash("Produção criada com sucesso", 'falha-sucesso')
        return redirect(url_for("producoes_atuais"))
    return render_template('producao_cadastro.html', form=form, botao="Criar produção")
