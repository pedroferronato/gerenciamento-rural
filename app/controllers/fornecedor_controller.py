from app.models.movimentador import Movimentador
from app.forms.movimentador_form import MovimentadorForm
from app import db, application
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, flash, request


@application.route('/fornecedor')
@login_required
def fornecedor():
    return render_template('fornecedor_recepcao.html')


@application.route('/fornecedor/cadastro', methods=['GET', 'POST'])
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
            flash('Você já cadastrou um fornecedor com este nome', 'flash-alerta')
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
            flash("Falha ao cadastrar fornecedor", 'flash-falha')
            return redirect(url_for('fornecedor_cadastro'))
        flash(f'Fornecedor {form.nome.data} registrado com sucesso', 'flash-sucesso')
        return redirect(url_for('fornecedor'))
    return render_template('fornecedor_cadastro.html', form=form, botao="Cadastrar fornecedor")


@application.route('/fornecedor/busca')
@login_required
def fornecedor_busca():
    return render_template('fornecedor_busca.html', botao="Buscar fornecedor")


@application.route('/fornecedor/busca/resultado')
@login_required
def fornecedor_busca_resultado():
    page = request.args.get('page', 1, type=int)
    nome = request.args.get('nome', '')
    contato = request.args.get('contato', '')
    filtros = [
        Movimentador.tipo == "Fornecedor"
    ]
    if not nome and not contato:
        flash('Insira pelo menos uma informação para a busca', 'flash-alerta')
        return redirect(url_for('fornecedor_busca'))

    if nome:
        filtros.append(Movimentador.nome.like('%{}%'.format(nome)))
    if contato:
        filtros.append(Movimentador.contato.like('%{}%'.format(contato)))

    resultado = Movimentador.query.filter(*filtros).order_by(Movimentador.nome.asc())

    if len(resultado.all()) <= 0:
        flash('Nenhum fornecedor encontrado', 'flash-alerta')
        return redirect(url_for('fornecedor_busca'))

    if len(resultado.all()) < 10:
        return render_template('fornecedor_busca.html', botao="Buscar fornecedor", fornecedores=resultado.all())

    pages = resultado.paginate(page=page, per_page=5)
    return render_template('fornecedor_busca.html', botao="Buscar fornecedor", pages=pages)
