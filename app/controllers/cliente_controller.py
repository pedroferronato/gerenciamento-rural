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


@application.route('/cliente/busca')
@login_required
def cliente_busca():
    form = MovimentadorForm()
    page = request.args.get('page', 1, type=int)
    if form.validate_on_submit():
        filtros = []

        if form.contato.data:
            filtros.append(Movimentador.contato.like('%{}%'.format(form.contato.data)))
        filtros.append(Movimentador.nome.like('%{}%'.format(form.endereco.data)))

        resultado = Movimentador.query.filter(*filtros).limit(25).from_self().order_by(Movimentador.nome.asc())

        if len(resultado.all()) <= 0:
            flash('Nenhum cliente encontrado', 'flash-alerta')
            return redirect(url_for('cliente_busca'))

        pages = resultado.paginate(page=page, per_page=5)

        return render_template('cliente_buscar.html', form=form, botao="Buscar cliente", pages=pages)

    return render_template('cliente_buscar.html', form=form, botao="Buscar cliente")


@application.route('/cliente/maiores')
@login_required
def cliente_maiores():
    # clientes = Movimentador.query.filter
    return render_template('cliente_maiores_clientes.html')
