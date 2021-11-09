from app import application, db
from app.models.insumo import Insumo
from flask import flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user


@application.route('/insumo/detalhe/<insumo_id>')
@login_required
def insumo_detalhe(insumo_id):
    return render_template('insumo_detalhes.html')
