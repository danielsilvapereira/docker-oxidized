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
RUN apt-get update && apt install -y python3 python3-pip

# Instalação do pyzabbix
RUN pip3 install pyzabbix

# Copie o script Python para o container
COPY zabbix-sync.py /root/.config/oxidized/

# Defina o diretório de trabalho
WORKDIR /root/.config/oxidized/

# Comando para iniciar o script Python e o Oxidized simultaneamente
CMD ["sh", "-c", "python3 zabbix-sync.py & oxidized"]
