from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from comunidade import app, database, bcrypt
from comunidade.forms import FormCriarLogin, FormCriarConta, FormEditarPerfil, FormCriarPost, FormEditarPost
from comunidade.models import Usuario, Post
import secrets
import os
from PIL import Image

@app.route('/')
# Decorador @: atribui a função home uma nova funcionalidade: executar a função home quando a rota definida for chamada
# Link da página pode ser necessário mudar, rankeamento do google, de organização do site
# Temos que evitar que mudança no link comprometa os links de dentro dos htmls.
# As funções nao devemos mudar os nomes
# Para evitar quebras de links entre codigo e html usamos url_for -> pega o link que tem a funcão X.
def home(): 
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    # Atenção: o parâmetro lista_usuarios recebe a variável lista_usuários. O parâmetro irá representar a variável dentro do template html
    # Por padrão parâmetro e variável são usado com o mesmo nome
    # No template html o parâmetro é acessado utilizando {{ paramêtro }}
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)

@app.route('/login', methods=['GET', 'POST'])
# Todas as páginas que tiverem formulário tem que explicitar o método POST
def login ():
    form_login = FormCriarLogin()
    form_criar_conta = FormCriarConta()
    # quando clico num botao de um formulario e tem mais de um na mesma página, o python não sabe em qual form foi o clique, tenho que identificar qual foi o botao na função
    # form_login.email.data: o .data refere ao resultado do que foi preenchido no formulário. form_login.email é apenas o campo do formulário
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data) # tem uma parametro Remember que pode ser True or False
            flash(f'Login realizado com sucesso no email: {form_login.email.data}', category='alert-success')
            param_next = request.args.get('next') # dicionário com todos os paramêtros do link (após /rota?)
            if param_next:
                return redirect(param_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Falha no login. E-mail ou Senha incorretos', category='alert-danger')
    if form_criar_conta.validate_on_submit() and 'botao_submit_criar_conta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_login.senha.data).decode('utf-8')
        usuario = Usuario(username=form_criar_conta.username.data, email=form_criar_conta.email.data, senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta criada com sucesso. Realize o seu login para começar: {form_criar_conta.email.data}', category='alert-success')
        return redirect(url_for('login'))
    return render_template('login.html', form_login = form_login, form_criar_conta=form_criar_conta )

@app.route('/sair')
@login_required
def sair():
    logout_user()
    return redirect(url_for('login'))

@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename = f'fotos_perfil/{current_user.foto_perfil}')

    return render_template('perfil.html', foto_perfil=foto_perfil)

def salvar_imagem(imagem):
    codigo = secrets.token_hex(8) # gera um toke de 8bits
    nome, extensao = os.path.splitext(imagem.filename)
    arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, f'static/fotos_perfil/{arquivo}')
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return arquivo

def listar_interesses(form):
    interesses = [campo.label.text for campo in form if 'int_' in campo.name and campo.data]        
    interesses = ';'.join(interesses)
    return interesses

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form_editar_perfil = FormEditarPerfil()
    foto_perfil = url_for('static', filename = f'fotos_perfil/{current_user.foto_perfil}')
    if form_editar_perfil.validate_on_submit():
        current_user.username = form_editar_perfil.username.data
        current_user.email = form_editar_perfil.email.data
        if form_editar_perfil.foto_perfil.data:
            current_user.foto_perfil = salvar_imagem(form_editar_perfil.foto_perfil.data)
        current_user.cursos = listar_interesses(form_editar_perfil)
        database.session.commit()
        flash(f'Perfil editado com sucesso!', category='alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form_editar_perfil.username.data = current_user.username
        form_editar_perfil.email.data  = current_user.email
        for campo in form_editar_perfil:
            if 'int_' in campo.name and campo.label.text in current_user.cursos:
                campo.data = True
        return render_template('editarperfil.html', foto_perfil=foto_perfil, form_editar_perfil=form_editar_perfil)
    
@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form_criar_post = FormCriarPost()
    if form_criar_post.validate_on_submit():
        post = Post(titulo=form_criar_post.titulo.data, corpo=form_criar_post.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash(f'Post criado com sucesso!', category='alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form_criar_post=form_criar_post)

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get_or_404(post_id)
    form_editar_post = FormEditarPost()
    modo_edicao = False
    if request.method == 'POST':    
        if 'botao_editar' in request.form:
            modo_edicao = True
            form_editar_post.process(obj=post)
        elif 'botao_submit_salvar' in request.form:
            modo_edicao = True
            if form_editar_post.validate_on_submit():
                post.titulo = form_editar_post.titulo.data
                post.corpo = form_editar_post.corpo.data
                database.session.commit()
                flash('Post atualizado com sucesso!', category='alert-success')
                return redirect(url_for('exibir_post', post_id=post.id))
        elif 'botao_excluir' in request.form:
            database.session.delete(post)
            database.session.commit()
            flash('Post excluído.', category='alert-success')
            return redirect(url_for('home'))
    else:
        form_editar_post.process(obj=post)
    if modo_edicao and request.method != 'POST':
        form_editar_post.process(obj=post)
    return render_template('post.html', post=post, form_editar_post=form_editar_post, modo_edicao=modo_edicao)




    

