FROM oxidized/oxidized:latest

# Instalar Git
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Script de inicialização para o Git
COPY init_git.sh /usr/local/bin/init_git.sh
RUN chmod +x /usr/local/bin/init_git.sh

# Comando de inicialização do Oxidized
ENTRYPOINT ["/usr/local/bin/init_git.sh"]
CMD ["oxidized"]

###############################
######## ZABBIX SYNC ##########
###############################
# Instalação de pacotes necessários
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

# Criação de um ambiente virtual Python
RUN python3 -m venv /root/venv

# Ativação do ambiente virtual e instalação do pyzabbix
RUN /root/venv/bin/pip install pyzabbix

# Copie o script Python para o container
#COPY ./zabbix-sync.py /root/.config/oxidized/

# Defina o diretório de trabalho
WORKDIR /root/.config/oxidized/

# Use o script entrypoint.sh como ponto de entrada
#ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
