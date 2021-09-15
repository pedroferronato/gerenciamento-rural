from app.forms.propriedade_cadastro_form import PropriedadeCadastroForm
from flask.templating import render_template
from app import application
from flask_login import login_required


@application.route('/propriedades')
@login_required
def propriedades():
    return render_template('recepcao_propriedades.html')


@application.route('/propriedades/cadastro', methods=['GET', 'POST'])
@login_required
def propriedades_cadastro():
    form = PropriedadeCadastroForm()
    return render_template('propriedade_cadastro.html', form=form)


@application.route('/propriedades/detalhes')
@login_required
def propriedades_detalhes():
    return render_template('propriedade_detalhes.html')
