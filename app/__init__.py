from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv
import os

load_dotenv()

application = Flask(__name__)

application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+ os.getenv("DB_USUARIO") +':'+ os.getenv("DB_SENHA") +'@'+ os.getenv("DB_LOCAL") + '/' + os.getenv("DB_BASEDEDADOS")
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SECRET_KEY'] = os.getenv("SECRET")
application.config['JSON_AS_ASCII'] = False

db = SQLAlchemy(application)
migrate = Migrate(application, db, compare_type=True)

login_manager = LoginManager(application)
login_manager.init_app(application)

import app.models.produtor
import app.models.movimentador
import app.models.propriedade
import app.models.produto
import app.models.insumo
import app.models.producao
import app.models.producao_insumo
import app.models.producao_produto
import app.models.venda
import app.models.compra

import app.controllers.server_controller
import app.controllers.produtor_controller
import app.controllers.propriedades_controller
import app.controllers.cliente_controller
import app.controllers.producao_controller
import app.controllers.fornecedor_controller
import app.controllers.despesas_controller
import app.controllers.insumo_controller
import app.controllers.vendas_controller
