from flask.helpers import flash, url_for
from flask.templating import render_template
from flask import redirect
from app import application, db
from app.forms.produtor_cadastro_form import ProdutorCadastroForm
from app.models.produtor import Produtor

import bcrypt


@application.route('/produtor/registro', methods=['GET', 'POST'])
def criar_produtor():
    form = ProdutorCadastroForm()
    if form.validate_on_submit():
        verificacao_produtor = Produtor.query.filter_by(login=form.login.data).first()
        if verificacao_produtor:
            flash('Nome de usuário não pode ser utilizado, tente escolher outro.', 'flash-alerta')
            return redirect(url_for('criar_produtor'))
        produtor = Produtor(
            nome = form.nome.data,
            login = form.login.data,
            contato = form.contato.data,
            senha = bcrypt.hashpw(form.senha.data.encode('utf-8'), bcrypt.gensalt())
        )
        try:
            db.session.add(produtor)
            db.session.commit()
        except:
            flash('Falha ao se conectar ao banco de dados', 'flash-falha')
            return redirect(url_for('criar_produtor'))
        flash(f'Usuário {form.login.data} registrado com sucesso, realize o login.', 'flash-sucesso')
        return redirect(url_for('login'))
    return render_template('produtor_cadastro.html', form=form)
