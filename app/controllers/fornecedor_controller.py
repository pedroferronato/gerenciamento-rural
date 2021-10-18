from app.controllers.server_controller import login
from app.models.movimentador import Movimentador
from app.forms.movimentador_form import MovimentadorForm
from app import db, application
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, flash, request


@application.route('/fornecedor')
@login_required
def fornecedor_recepcao():
    return render_template('fornecedor_recepcao.html')


@application.route('/fornecedor/cadastro')
@login_required
def fornecedor_cadastro():
    form = MovimentadorForm()
    if form.validate_on_submit():
        verificacao_fornecedor = Movimentador.query.filter_by(
            nome=form.nome.data,
            tipo="Fornecedor", 
            produtor_id=current_user.id
        ).first()
        if verificacao_fornecedor:
            flash('Você já cadastrou um fornecedor com este nome')
            return redirect(url_for('fornecedor_cadastro'))
        fornecedor = Movimentador(
            produtor_id=current_user.id,
            nome=form.nome.data,
            contato=form.contato.data,
            endereco=form.endereco.data,
            tipo="Fornecedor"
        )
        try:
            db.session.add(fornecedor)
            db.session.commit()
        except:
            flash("Falha ao cadastrar fornecedor")
            return redirect(url_for('fornecedor_cadastro'))
        flash(f'Fornecedor {form.nome.data} registrado com sucesso')
        return redirect(url_for('fornecedor_recepcao'))
    return render_template('fornecedor_cadastro.html', form=form)


@application.route('/fornecedor/busca')
@login_required
def fornecedor_busca():
    form = MovimentadorForm()
    page = request.args.get('page', 1, type=int)
    if form.validate_on_submit():
        filtros = []

        if form.contato.data:
            filtros.append(Movimentador.contato.like('%{}%'.format(form.contato.data)))
        filtros.append(Movimentador.nome.like('%{}%'.format(form.endereco.data)))

        resultado = Movimentador.query.filter(*filtros).limit(25).from_self().order_by(Movimentador.nome.asc())

        if len(resultado.all()) <= 0:
            flash('Nenhum fornecedor encontrado')
            return redirect(url_for('fornecedor_busca'))

        pages = resultado.paginate(page=page, per_page=5)

        return render_template('fornecedor_busca.html', form=form, botao="Buscar fornecedor", pages=pages)

    return render_template('fornecedor_busca.html', form=form, botao="Buscar fornecedor")



