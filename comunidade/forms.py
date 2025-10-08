''' 
* Formulário no python - FlaskForm é um formulário web

* Tudo que tem no site que não é texto proprimamente, é um objeto no python: postos, usuários, forms

* Segurança dos formulários: Os forms de um site tem por padrão um token de segurança (crsf token), para previnir ataques maliciosos. Formulario é uma porta entre o front do seu site e
o seu backend, permite trocar informações com o banco de dados do seu site. 

'''

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed # FileAllowed é uma validador que definimos as extensões permitidas
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidade.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):
    # Nao precisamos definir o init, pois já herda da classe FlaskForm
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criar_conta = SubmitField('Criar Conta')

    # a método validate_on_submit() do objeto FlaskForm é quem faz todos os validators definidos nos formulários e execeuta todas as funções que tem "validate" no nome.
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first() # email.data é o que o usuario preencheu, email é o campo do form.
        if usuario:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar')


class FormCriarLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Permanecer conectado')
    botao_submit_login = SubmitField('Login')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()]) # Campo = Tipo(Label, Validador)
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Foto de Perfil', validators=[FileAllowed(['jpg', 'png'])])
    int_arte = BooleanField('Arte')
    int_negocios = BooleanField('Negócios')
    int_moda = BooleanField('Moda')
    int_musica = BooleanField('Música')
    int_livros = BooleanField('Livros')
    int_tech = BooleanField('Tech')
    int_esportes = BooleanField('Esportes')
    int_games = BooleanField('Games')
    int_viagem = BooleanField('Viagem')
    int_comida = BooleanField('Comida')
    int_saude = BooleanField('Saúde')
    int_fitness = BooleanField('Fitness')
    botao_submit_editar_perfil = SubmitField('Salvar')

    def validate_email(self, email):
        if email.data != current_user.email:
            usuario = Usuario.query.filter_by(email=email.data).first() # email.data é o que o usuario preencheu, email é o campo do form.
            if usuario:
                raise ValidationError('E-mail já cadastrado. Escolha outro e-mail válido')
            

class FormCriarPost(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(2, 100)])
    corpo = TextAreaField('O que está acontecendo?', validators=[DataRequired(), Length(6, 240)])
    botao_submit_postar = SubmitField('Postar')


class FormEditarPost(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(2, 100)])
    corpo = TextAreaField('O que está acontecendo?', validators=[DataRequired(), Length(6, 240)])
    botao_submit_salvar = SubmitField('Salvar')
    botao_editar = SubmitField('Editar')
    botao_excluir = SubmitField('Excluir')