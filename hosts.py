from zabbix_api import ZabbixAPI
import json
import sqlite3

def get_device_type(line):
    if 'eltex' in line and 'mes' in line:
        return 'eltex'
    elif 'eltex' in line and 'esr' in line:
        return 'eltex_esr'
    elif 'eltex' in line:
        return 'eltex'
    elif 'mikrotik' in line:
        return 'mikrotik'
    elif 'linux' in line:
        return 'linux'
    elif 'zyxel' in line:
        return 'zyxel'
    elif 'zte' in line:
        return 'zte_zxros'
    elif 'dell' in line:
        return 'dell_dnos9'
    elif 'cisco' in line or 'asr' in line:
        return 'cisco_ios'
    else:
        return 'generic'

# Загружаем конфигурацию из файла
with open('config.json') as data_file:
    data = json.load(data_file)

# Подключение к базе данных
conn = sqlite3.connect('zabbix_hosts.db')
cursor = conn.cursor()

# Создание таблиц, если они не существуют
cursor.execute('''
    CREATE TABLE IF NOT EXISTS hosts (
        hostid TEXT PRIMARY KEY,
        host TEXT,
        type TEXT NOT NULL
        )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS hostgroups (
        groupid TEXT PRIMARY KEY,
        name TEXT NOT NULL
        )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS host_hostgroup (
        hostid TEXT NOT NULL,
        groupid TEXT NOT NULL,
        PRIMARY KEY (hostid, groupid)
    )
''')

try:
    # Подключение к Zabbix API
    zapi = ZabbixAPI(f"http://{data['address']}")
    zapi.login(data['login']['user'], data['login']['password'])

    # Получение всех хостов
    hosts = zapi.host.get({"output": ["hostid", "host"]})
        

    # Получение всех групп хостов
    host_groups = zapi.hostgroup.get({"output": ["groupid", "name"]})
    
    for group in host_groups:
        cursor.execute('''
            INSERT OR REPLACE INTO hostgroups (groupid, name) VALUES (?, ?)
        ''', (group['groupid'], group['name']))

    # Получение шаблонов для всех хостов
    for host in hosts:
        lines = ''
        host_id = host['hostid']
        
        # Получение шаблонов, связанных с текущим хостом
        templates = zapi.host.get({
            "output": ["hostid"],
            "selectParentTemplates": ["templateid", "name"],
            "hostids": host_id
        })

        # Извлечение и вывод названий шаблонов
        if templates and 'parentTemplates' in templates[0]:
            for template in templates[0]['parentTemplates']:
                line = template['name'].lower()
                lines += line
                #(ID: {template['templateid']})
            host_type = get_device_type(lines)
            cursor.execute('''INSERT OR REPLACE INTO hosts (hostid, host, type) VALUES (?, ?, ?)''', 
                       (host['hostid'], host['host'], host_type))

    conn.commit()
    zapi.logout()

except Exception as e:
    print(f"Ошибка при подключении к Zabbix API или выполнении запроса: {e}")

finally:
    # Закрытие соединения с базой данных
    conn.close()