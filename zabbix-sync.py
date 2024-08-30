from pyzabbix import ZabbixAPI
import json

# Configurações
ZABBIX_URL = 'http:/sua_url/api_jsonrpc.php'
ZABBIX_TOKEN = ''

# Conectar à API do Zabbix
zapi = ZabbixAPI(ZABBIX_URL)
zapi.login(api_token=ZABBIX_TOKEN)


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
                host_info.append(f"{host['host']}: {ip}: {host_tag['value']}: {user}: {senha}")
    return host_info


# Nomes das macros a buscar
macro_names = ['{$BACKUP.USUARIO}', '{$BACKUP.SENHA}']

# Busca os hosts com a tag 'oxidized' e as macros especificadas
try:
    hosts = get_hosts_with_tag_and_macros('oxidized', macro_names)
    if hosts:
        for info in hosts:
            print(info)
    else:
        print("Nenhum host encontrado com a tag 'oxidized'.")
except Exception as e:
    print(f"Erro: {e}")
