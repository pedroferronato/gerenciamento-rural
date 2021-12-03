from app.forms.propriedade_cadastro_form import PropriedadeCadastroForm
from flask.templating import render_template
from flask import redirect, flash, url_for, request
from sqlalchemy import and_
from app import application, db
from app.models.propriedade import Propriedade
from flask_login import login_required, current_user


@application.route('/propriedades')
@login_required
def propriedades():
    propriedades = Propriedade.query.filter_by(produtor_id=current_user.id).all()
    return render_template('recepcao_propriedades.html', propriedades=propriedades)


@application.route('/propriedades/cadastro', methods=['GET', 'POST'])
@login_required
def propriedades_cadastro():
    form = PropriedadeCadastroForm()
    if form.validate_on_submit():
    
        filtros = [
            Propriedade.nome == form.nome.data,
            Propriedade.produtor_id == current_user.id
        ]

        verificacao_propriedade_produtor = Propriedade.query.filter(*filtros).first()
        print(verificacao_propriedade_produtor)
        if verificacao_propriedade_produtor:
            flash('Você já registrou esta propriedade', 'flash-alerta')
            return redirect(url_for('propriedades_cadastro'))

        if not form.contato.data:
            form.contato.data = current_user.contato

        nova_propriedade = Propriedade(
            produtor_id = current_user.id,
            nome = form.nome.data,
            endereco = form.endereco.data,
            area = form.area.data,
            contato = form.contato.data,
            ativa = True
        )

        try:
            db.session.add(nova_propriedade)
            db.session.commit()
        except:
            flash('Falha ao salvar no banco de dados', 'flash-falha')
            return redirect(url_for('propriedades_cadastro'))
        
        return redirect(url_for('propriedades'))

    return render_template('propriedade_cadastro.html', form=form, botao="Cadastrar")


@application.route('/propriedades/detalhes/<propriedade_id>')
@login_required
def propriedades_detalhes(propriedade_id):
    propriedade = Propriedade.query.filter(
        Propriedade.ativa == True,
        Propriedade.id == propriedade_id
    ).first()
    return render_template('propriedade_detalhes.html', propriedade=propriedade)


@application.route('/propriedades/alterar/<propriedade_id>', methods=["GET", "POST"])
@login_required
def propriedades_atualizar(propriedade_id):
    propriedade = Propriedade.query.filter(
        Propriedade.ativa == True,
        Propriedade.id == propriedade_id
    ).first()
    form = PropriedadeCadastroForm()
    if request.method == "GET":
        form.nome.data = propriedade.nome
        form.endereco.data = propriedade.endereco
        form.area.data = propriedade.area
        form.contato.data = propriedade.contato
    if request.method == "POST":
        if form.validate_on_submit():
            if not form.contato.data:
                form.contato.data = current_user.contato

            propriedade.nome = form.nome.data
            propriedade.endereco = form.endereco.data
            propriedade.area = form.area.data
            propriedade.contato = form.contato.data

            try:
                db.session.add(propriedade)
                db.session.commit()
            except Exception as ex:
                flash('Falha ao alterar no banco de dados', 'flash-falha')
                return redirect(url_for('propriedades_atualizar', propriedade_id=propriedade_id))
            flash('Propriedade atualizada com sucesso', 'flash-sucesso')
            return redirect(url_for('propriedades_detalhes', propriedade_id=propriedade_id))

    return render_template('propriedade_editar.html', form=form, propriedade=propriedade, botao="Atualizar")


@application.route('/propriedades/excluir/<propriedade_id>')
@login_required
def propriedades_excluir(propriedade_id):
    propriedade = Propriedade.query.filter(
        Propriedade.ativa == True,
        Propriedade.id == propriedade_id
    ).first()
    try:
        propriedade.ativa == False
        db.session.add(propriedade)
        db.session.commit()
    except:
        flash("Falha ao excluir da base de dados", 'flash-falha')
        return redirect(url_for('propriedades_detalhes', propriedade_id=propriedade_id))
    flash("Propriedade removida com sucesso", 'flash-sucesso')
    return redirect(url_for('propriedades'))
