#!/usr/bin/env python3

### */5 * * * * /usr/bin/python3 /home/gubit/docker-oxidized/zabbix-sync.py ##
#./zabbix-sync.py > /dev/null 2>&1

#import time
from pyzabbix import ZabbixAPI

# Configurações
ZABBIX_API_URL = "http://URL/api_jsonrpc.php"
API_TOKEN = ""
ROUTER_DB_PATH = "/home/gubit/docker-oxidized/oxidized/router.db"

# Conexão com a API do Zabbix usando o token
zapi = ZabbixAPI(ZABBIX_API_URL)
zapi.session.headers.update({'Authorization': f'Bearer {API_TOKEN}'})

# Função para buscar hosts com a tag 'oxidized', as macros e retornar as informações formatadas
def get_hosts_with_tag_and_macros(tag, macro_names):
    hosts = zapi.host.get(
        output=['hostid', 'host'],
        selectTags='extend',
        selectInterfaces=['ip'],
        selectMacros='extend',
        tags=[{'tag': tag}]
    )

    host_info = []
    for host in hosts:
        # Filtra a tag oxidized
        for host_tag in host['tags']:
            if host_tag['tag'] == tag:
                ip = host['interfaces'][0]['ip'] if host['interfaces'] else 'IP não encontrado'
                macros = {macro['macro']: macro['value'] for macro in host['macros'] if macro['macro'] in macro_names}
                user = macros.get('{$BACKUP.USUARIO}', 'N/A')
                senha = macros.get('{$BACKUP.SENHA}', 'N/A')
                porta = macros.get('{$BACKUP.PORTA}', 'N/A')
                host_info.append(f"{host['host']}:{ip}:{host_tag['value']}:{user}:{senha}:{porta}")
    return host_info

# Função para escrever as informações no arquivo router.db
def write_to_router_db(data, file_path):
    with open(file_path, 'w') as file:
        for line in data:
            file.write(line + '\n')

# Nomes das macros a buscar
macro_names = ['{$BACKUP.USUARIO}', '{$BACKUP.SENHA}', '{$BACKUP.PORTA}']

# Loop contínuo para atualização do arquivo router.db
try:
    while True:
        hosts = get_hosts_with_tag_and_macros('backup', macro_names)
        if hosts:
            write_to_router_db(hosts, ROUTER_DB_PATH)
            print("Arquivo router.db atualizado.")
        else:
            print("Nenhum host encontrado com a tag 'oxidized'.")

        time.sleep(60)  # Espera 5 minutos antes de atualizar novamente
except Exception as e:
    print(f"Erro: {e}")
