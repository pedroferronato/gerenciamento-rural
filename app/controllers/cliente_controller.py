from app.forms.movimentador_form import MovimentadorForm
from app import application, db
from app.models.movimentador import Movimentador
from flask import flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user


@application.route('/cliente')
@login_required
def cliente():
    return render_template('cliente_recepcao.html')


@application.route('/cliente/cadastro', methods=['GET','POST'])
@login_required
def cliente_cadastro():
    form = MovimentadorForm()
    if form.validate_on_submit():
        verificacao_cliente = Movimentador.query.filter_by(
            nome=form.nome.data,
            tipo="Cliente", 
            produtor_id=current_user.id
        ).first()
        if verificacao_cliente:
            flash("Você já cadastrou esse cliente", 'flash-alerta')
            return redirect(url_for('cliente_cadastro'))
        cliente = Movimentador(
            produtor_id=current_user.id,
            nome=form.nome.data,
            contato=form.contato.data,
            endereco=form.endereco.data,
            tipo="Cliente"
        )
        try:
            db.session.add(cliente)
            db.session.commit()
        except:
            flash("Falha ao cadastrar cliente", 'flash-falha')
            return redirect(url_for("cliente_cadastro"))
        flash(f'Cliente {form.nome.data} registrado com sucesso', 'flash-sucesso')
        return redirect(url_for('cliente'))
    return render_template('cliente_cadastro.html', form=form, botao="Cadastrar novo cliente")


@application.route('/cliente/alterar/<cliente_id>', methods=['GET', 'POST'])
@login_required
def cliente_alterar(cliente_id):
    cliente = Movimentador.query.filter(
            Movimentador.tipo == "Cliente",
            Movimentador.id == cliente_id
        ).first()

    form = MovimentadorForm()
    if request.method == "GET":
        form.nome.data = cliente.nome
        form.endereco.data = cliente.endereco
        form.contato.data = cliente.contato
    if request.method == "POST":
        if form.validate_on_submit():
            cliente.nome = form.nome.data
            cliente.endereco = form.endereco.data
            cliente.contato = form.contato.data
            try:
                db.session.add(cliente)
                db.session.commit()
                flash(f'Cliente {cliente.nome} alterado com sucesso', 'flash-sucesso')
                return redirect(url_for('cliente'))
            except:
                flash("Falha ao atualizar cliente", 'flash-falha')
                return redirect(url_for('cliente', cliente_id=cliente_id))
    return render_template('cliente_alterar.html', form=form, cliente_id=cliente_id, botao="Atualizar cadastro")


@application.route('/cliente/excluir/<cliente_id>')
@login_required
def cliente_deletar(cliente_id):
    cliente = Movimentador.query.filter(
        Movimentador.tipo == "Cliente",
        Movimentador.id == cliente_id
    ).first()
    try:
        db.session.delete(cliente)
        db.session.commit()
    except:
        flash("Falha ao remover cliente", 'flash-falha')
        return redirect(url_for('cliente'))
    flash("Cliente removido com sucesso", 'flash-sucesso')
    return redirect(url_for('cliente'))


@application.route('/cliente/detalhes/<cliente_id>')
@login_required
def cliente_detalhes(cliente_id):
    cliente = Movimentador.query.filter_by(id=cliente_id).first()
    return render_template('cliente_detalhes.html', cliente=cliente)


@application.route('/cliente/busca')
@login_required
def cliente_busca():
    return render_template('cliente_buscar.html', botao="Buscar cliente")


@application.route('/cliente/busca/resultado')
@login_required
def cliente_busca_resultado():
    nome = request.args.get('nome')
    contato = request.args.get('contato')
    page = request.args.get('page', 1, type=int)
    
    filtros = [
        Movimentador.tipo == "Cliente"
    ]
    if contato:
        filtros.append(Movimentador.contato.like('%{}%'.format(contato)))
    filtros.append(Movimentador.nome.like('%{}%'.format(nome)))

    resultado = Movimentador.query.filter(*filtros).limit(25).from_self().order_by(Movimentador.nome.asc())

    print(resultado.all())
    if len(resultado.all()) <= 0:
        flash('Nenhum cliente encontrado', 'flash-alerta')
        return redirect(url_for('cliente_busca'))

    if len(resultado.all()) < 10:
        return render_template('cliente_buscar.html', botao="Buscar cliente", clientes=resultado.all())
    
    pages = resultado.paginate(page=page, per_page=5)

    return render_template('cliente_buscar.html', botao="Buscar cliente", pages=pages, nome=nome, contato=contato)
