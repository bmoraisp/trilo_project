from comunidade import app
# app está dentro do arquivo init da pasta comunidade que é executado sempre que chama a pasta comunidade
# from models import Usuario, Post -> Isso aqui da problema, pois o arquivo main precisa do arquivo models para funcionar e o arquivo models precisa do arquivo main. (Circular Import)

if __name__ == '__main__': # código abaixo só rodará se estiver executando esse arquivo
    app.run(debug=True)
