########################
# PRECISAREI FAZER UMAS ADEQUACOES NO MAIN.PY, POR ISSO VOU CRIAR UMA COPIA DELE PARA MANTER DE BACKUP
########################
# precisamos sair de um ponto de partida (uma imagem de partida)
# vamos partir de uma imagem do python
# slim indica que é uma imagem mais leve
FROM python:3.7-slim

# vamos criar as variaveis de ambiente para salvar as senhas
# para que o usuario e senha nao fiquem e expostos, vamos usar o comando ARG
# esse comando vai permitir passar argumentos ao dockerfile ao iniciar o container
ARG BASIC_AUTH_USERNAME_ARG
ARG BASIC_AUTH_PASSWORD_ARG

# Agora, irei criar as variaveis de ambiente
# as variaveis vao ficar disponiveis dentro de um container docker
ENV BASIC_AUTH_USERNAME=BASIC_AUTH_USERNAME_ARG
ENV BASIC_AUTH_PASSWORD=BASIC_AUTH_PASSWORD_ARG

# Aqui estamos copiando os requerimentos da pasta atual
# e estamos criando e colando os requerimentos na pasta usr dentro do container docker
COPY ./requirements.txt /usr/requirements.txt

# vamos setar o diretorio de trabalho dentro da máquina do container
WORKDIR /usr

# agora, precisamos instalar as dependencias
RUN pip3 install -r requirements.txt

# vamos levar so os arquivos essencias para o funcionamento da API
# aqui, estamos levando as pastas inteiras
COPY ./src /usr/src
COPY ./models /usr/models

# vamos definir o entrypoint do container
# qual TIPO de comando o container vai executar ao ser iniciado
ENTRYPOINT [ "python" ]

# e agora vamos definir qual o comando exatamente sera executado
CMD [ "src/app/main_bck.py" ]