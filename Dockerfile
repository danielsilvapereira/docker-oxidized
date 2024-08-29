FROM oxidized/oxidized:latest

# Instalar Git
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Script de inicialização para o Git
COPY init_git.sh /usr/local/bin/init_git.sh
RUN chmod +x /usr/local/bin/init_git.sh

# Comando de inicialização do Oxidized
ENTRYPOINT ["/usr/local/bin/init_git.sh"]
CMD ["oxidized"]
