from comunidade import  app, database
from comunidade import models

with app.app_context(): # todo comando de criacao e leitura no banco de dados tem que estar dentro desse app_context()
    database.drop_all()
    database.create_all()
# Tudo que você vai fazendo no seu banco de dados, ele vai armazenando numa sessão temporária, depois de fazer todas as ediçoes comitamos no banco.
    # usuario1 = Usuario(username='nobrumorais', email='nobrumorais@gmail.com', senha='nobru2310')
    # usuario2 = Usuario(username='luisaveiga', email='luisaveiga@gmail.com', senha='luisa1709')
    # database.session.add(usuario1)
    # database.session.add(usuario2)
    # database.session.commit()

    # usuarios = Usuario.query.filter(Usuario.id==1).first()
    
    # post = Post(id_usuario=1, titulo='Primeiro Post', corpo='Fazendo um teste para ver se está tudo funcionando')
    # database.session.add(post)
    # database.session.commit()

    # post = Post.query.filter(Post.id==1).first()
    # print(post.autor.username)