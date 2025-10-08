# Construcao das tabelas do Banco de Dados
from comunidade import database, login_manager
from datetime import datetime
from flask_login import UserMixin

# Por conveniência usamos os mesmos nomes dos campos do formulario de criar usuário
# Vamos ter que importar o login_manager para cá para mostrar que a classe Usuario é um objeto capaz de fazer login no site
# Vamos ter que criar uma funcão fora da classe que mostre qual o campo será utilizado para identificar um usuário do nosso Banco de Dados
@login_manager.user_loader # indica para o login_manager qual é a função que ele tem que usar para identificar um usuário no nosso banco pelo seu id e carregá-lo.
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario)) # get é um metodo que busca na coluna da primary key

# Temos que mostrar ao login_manager qual a tabela que tem a estrutura de usuário que ele precisa. Ele precisa que essa classe tenha algumas características específicas.
#  UserMixin -> é um paramêtro que vamos passar para nossa classe Usuario que já vai atribuir e ela todas as características que o login_manager precisa para fazer login e manter pessoa conectada quando sai do site.
class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False) # antes de salvar a senha no banco de dados tenho que codificar para não ter acesso a senha da pessoa
    foto_perfil = database.Column(database.String, default='default.jpg') # vai armazenar o nome do arquivo da foto do usuário. Se não subir foto, vai usar uma foto padrão (silhueta) default.jpg
    posts = database.relationship('Post', backref='autor', lazy=True) # lazy carrega de uma vez todas as informações sobre o autor. É apenas uma relação não é uma coluna
    cursos = database.Column(database.String, default='Não Informado') # temos que passar um valor default, pois qdo se cria uma conta, nao informamos os cursos de imediato. Nao precisa ter uma tabela separada, pois só quero exibir os nomes dos cursos inscritos.
    
    def contar_posts(self):
        return len(self.posts)
    

class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False, unique=True) # quando temos um texto maior, usamos Text
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow) # não pode passar datetime.utcnow(), pois armazenaria um valor fixo, tem que passar o método.
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)






    
    
    
    
