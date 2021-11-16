import datetime

from app import application, db
from app.forms.producao_form import ProducaoForm
from app.forms.estoque_form import EstoqueForm
from app.forms.producao_finalizada_form import ProducaoFinalizadasForm
from app.models.producao import Producao
from app.models.producao_insumo import ProducaoInsumo
from app.models.producao_produto import Coleta
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
        return render_template('producao_finalizadas.html', form=form)

    if len(producoes.all()) > 10:
        producoes = producoes.paginate(page=page, per_page=10)
        return render_template('producao_finalizadas.html', pages=producoes, form=form)
    
    producoes = producoes.all()

    return render_template('producao_finalizadas.html', producoes=producoes, form=form, botao="Buscar")


@application.route('/producao/adicionar', methods=['GET', 'POST'])
@login_required
def producoes_adicionar():
    propriedade = Propriedade.query.filter_by(produtor_id=current_user.id).first()
    if not propriedade:
        flash("Você precisa cadastrar sua propriedade para registrar produções", 'flash-alerta')
        return redirect(url_for('producoes_adicionar'))

    form = ProducaoForm()
    filtros = [
        Insumo.utilidade == "Cultivo",
        Insumo.quantidade > 0,
        Insumo.propriedade_id == propriedade.id
    ]
    insumos = Insumo.query.filter(*filtros).order_by(Insumo.nome.asc()).all()
    
    if form.validate_on_submit():

        if form.data.data < datetime.date(2018, 1, 1):
            flash("Você está inserindo uma produção muito antiga", 'flash-alerta')
            return redirect(url_for('producoes_adicionar'))

        filtros_produto = filtros + [
            Insumo.id == request.form['data-insumo'].split(' - ')[0],
            Insumo.nome == request.form['data-insumo'].split(' - ')[1]
        ]
        produto_id = Insumo.query.filter(*filtros_produto).first().id
        
        if not produto_id:
            flash("Produto não encontrado", 'flash-falha')
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
                insumo_id = produto_id,
                base = True
            )
            db.session.add(insumo_base)
            db.session.flush()
            insumo_estoque = Insumo.query.filter_by(id = produto_id, propriedade_id=propriedade.id).first()
            if insumo_estoque.quantidade_estocada < producao.quantidade:
                flash("Falta de insumo, verifique o valor inserido", 'flash-falha')
                return redirect(url_for('producoes_adicionar'))
            insumo_estoque.quantidade_estocada -= producao.quantidade
            db.session.add(insumo_estoque)
            db.session.commit()
        except Exception as e:
            flash("Falha ao criar produção", 'flash-falha')
            return redirect(url_for('producoes_adicionar'))
        flash("Produção criada com sucesso", 'flash-sucesso')
        return redirect(url_for("producoes_atuais"))
    return render_template('producao_cadastro.html', form=form, botao="Criar produção", insumos=insumos)


@application.route('/producoes/detalhes/<producao_id>')
@login_required
def producao_detalhes(producao_id):
    producao = Producao.query.filter_by(id=producao_id).first()

    if not producao:
        flash("A produção que você buscou não existe", 'flash-alerta')
        return redirect(url_for('producoes_atuais'))

    producao_custo = producao.get_custos()
    
    custos = "{} {}".format("R$", producao_custo)

    custo_unitario = producao_custo / producao.quantidade

    custo_unitario_formatado = "{} {}".format("R$", custo_unitario)

    return render_template('producao_detalhes.html', producao=producao, custos=custos, custo_unitario=custo_unitario_formatado)


@application.route('/producoes/adicionar/custeio/<producao_id>', methods=['GET', 'POST'])
@login_required
def producao_adicionar_custeio(producao_id):
    propriedade = Propriedade.query.filter_by(produtor_id=current_user.id).first()
    if not propriedade:
        flash("Você precisa cadastrar sua propriedade para registrar produções", 'flash-alerta')
        return redirect(url_for('producao_adicionar_custeio'))
    producao = Producao.query.filter_by(id=producao_id).first()
    if not producao:
        flash("A produção que você buscou não existe", 'flash-alerta')
        return redirect(url_for('producoes_atuais'))
    filtros = [
        Insumo.quantidade > 0,
        Insumo.propriedade_id == propriedade.id
    ]
    insumos = Insumo.query.filter(*filtros).all()
    if request.method == 'POST':
        filtros_produto = filtros + [
            Insumo.id == request.form['data-insumo'].split(' - ')[0],
            Insumo.nome == request.form['data-insumo'].split(' - ')[1]
        ]
        insumo = Insumo.query.filter(*filtros_produto).first()
        custeio = ProducaoInsumo(
            producao_id = producao_id,
            insumo_id = insumo.id,
            quantidade_aplicada = request.form['quantidade'],
            data = datetime.datetime.strptime(request.form['data'], '%d/%m/%Y').date(),
            base = False
        )

        try:
            db.session.add(custeio)
            db.session.commit()
        except:
            flash("Falha ao criar produção", 'flash-falha')
            return redirect(url_for('producoes_adicionar'))
        flash("Custeio adicionado com sucesso", 'flash-sucesso')
        return redirect(url_for("producao_detalhes", producao_id=producao_id))
    return render_template('producao_adicionar_custeio.html', producao_id=producao_id, insumos=insumos, producao=producao, botao="Adicionar custeio")


@application.route('/producao/<producao_id>/confirmar-finalizar')
@login_required
def producao_confirmar_finalizar(producao_id):
    producao = Producao.query.filter_by(id=producao_id).first()
    if not producao:
        flash("Produção não encontrada", 'flash-falha')
        return redirect(url_for('producoes_atuais'))
    if not producao.ativa:
        flash("Produção já foi finalizada", 'flash-falha')
        return redirect(url_for('producoes_finalizadas'))
    return render_template('producao_finalizar.html', producao=producao, botao="Finalizar produção", data=datetime.date.today())


@application.route('/producao/<producao_id>/finalizar')
@login_required
def producao_finalizar(producao_id):
    producao = Producao.query.filter_by(id=producao_id).first()

    produto = Produto.query.filter_by(producao_id=producao.id).first()

    if produto:
        produto.quantidade += float(producao.quantidade_atual)
    else:
        propriedade = Propriedade.query.filter_by(produtor_id=current_user.id).first()

        produto = Produto(
            producao_id = producao.id,
            propriedade_id = propriedade.id,
            nome = producao.get_insumo_base().nome,
            quantidade = float(producao.quantidade_atual),
            valor_unitario = request.form['unitario'],
            validade = request.form['validade'],
            unidade_medida = request.form['medida']
        )

    producao.quantidade_atual = 0
    producao.data_coleta = datetime.datetime.strptime(str(request.form['data']), "%d/%m/%Y").date() 

    try:
        db.session.add(produto)
        db.session.add(producao)
        db.session.commit(producao)
    except:
        flash("Falha ao criar produção", 'flash-falha')
        return redirect(url_for('producoes_atuais'))
    flash("Produção finalizada", 'flash-sucesso')
    return redirect(url_for('producoes_finalizadas'))


@application.route('/producao/<producao_id>/coleta', methods=['GET', 'POST'])
@login_required
def producao_coleta(producao_id):
    producao = Producao.query.filter_by(id=producao_id).first()
    if not producao:
        flash("Produção não encontrada", 'flash-falha')
        return redirect(url_for('producoes_atuais'))
    if not producao.ativa:
        flash("Produção já foi finalizada", 'flash-falha')
        return redirect(url_for('producoes_finalizadas'))
    
    if request.method == 'POST':
        quantidade = float(request.form['quantidade'])
        if producao.quantidade_atual < quantidade:
            flash("Quantidade superor à atual", 'flash-falha')
            return redirect(url_for('producoes_atuais'))

        produto = Produto.query.filter_by(producao_id=producao.id).first()

        if produto:
            produto.quantidade += float(producao.quantidade_atual)
        else:
            propriedade = Propriedade.query.filter_by(produtor_id=current_user.id).first()

            produto = Produto(
                producao_id = producao.id,
                propriedade_id = propriedade.id,
                nome = producao.get_insumo_base().nome,
                quantidade = float(producao.quantidade_atual),
                valor_unitario = request.form['unitario'],
                validade = request.form['validade'],
                unidade_medida = request.form['medida']
            )
    
        producao.quantidade_atual -= quantidade

        coleta = Coleta(
            data_coleta = datetime.datetime.strptime(str(request.form['data']), "%d/%m/%Y").date(),
            producao_id = producao_id,
            quantidade = quantidade,
            unidade_especifica = request.form['unidade']
        )

        try:
            db.session.add(produto)
            db.session.add(producao)
            db.session.add(coleta)
            db.session.commit()
        except:
            flash("Falha ao registrar coleta", 'flash-falha')
            return redirect(url_for('producao_detalhes', producao_id=producao_id))
        flash(f"Coleta na produção {producao.nome} reistrada", 'flash-sucesso')
        return redirect(url_for('producoes_atuais'))

    return render_template('producao_coleta.html', botao="Registrar coleta", producao=producao, data=datetime.date.today())
