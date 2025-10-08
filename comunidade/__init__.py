# Sempre que eu chamar a pasta comunidade vai rodar esse arquivo __init__.py como se fosse uma classe.
# Dentro do __init__ vamos ter apenas as estrutura do nosso site: o app e banco de dados.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
# Token estará apenas no seu código e não aparece mais em nenhum lugar.
app.config['SECRET_KEY'] = '88da79784728e3aaa3156a182dec3419'

# URI é o caminho no meu computador onde vai estar esse banco de dados. /// indica que o banco será criado em relação ao CWD.
BASE_DIR = Path(__file__).resolve().parent # .../site_flask/comunidade
DB_PATH  = BASE_DIR / "comunidade.db"
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH.as_posix()}"
# vai criar o banco de dados de acordo com as configurações do nosso app.
database = SQLAlchemy(app)

# Utilizado para salvar senha criptografada
bcrypt = Bcrypt(app) # só nosso site será capaz de descriptografar essa senha

# Criando o LoginManager do nosso site
login_manager = LoginManager(app) 
login_manager.login_view = 'login' # página que será redirecionado o usuário, se tentar acessar sem login onde o login é requerido
login_manager.login_message_category = 'alert-info' # caixa azul

# executa o arquivo route.py
from comunidade import routes 

