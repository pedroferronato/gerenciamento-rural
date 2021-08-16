from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
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
manager = Manager(application)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager(application)
login_manager.init_app(application)

import app.models.produtor
import app.models.movimentador
import app.models.propriedade
import app.models.movimentacaoFinanceira
import app.models.item
import app.models.producao
import app.models.producaoInsumo
import app.models.movimentacaoFinanceira
import app.models.movimentacaoFinanceiraItem
