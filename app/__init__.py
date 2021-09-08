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
import app.models.movimentacao_financeira
import app.models.item
import app.models.producao
import app.models.producao_insumo
import app.models.movimentacao_financeira_item

import app.controllers.server_controller