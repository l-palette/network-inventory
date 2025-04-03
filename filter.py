from zabbix_api import ZabbixAPI
import json

def get_hosts(zapi, group_name):
    group_response = zapi.hostgroup.get({
        "output": ["groupid", "name"],
        "filter": {
            "name": [group_name]
        }
    })

    if group_response:
        group_id = group_response[0]['groupid']

        hosts_response = zapi.host.get({
            "output": ["hostid", "host"],
            "groupids": group_id
        })


        if hosts_response:
            print(f"Устройства в группе '{group_name}':")
            for host in hosts_response:
                print(f"- Host ID: {host['hostid']}, Hostname: {host['host']}")
        else:
            print(f"В группе '{group_name}' нет устройств.")
    else:
        print(f"Хостгруппа '{group_name}' не найдена.")



with open('config.json') as data_file:
    data = json.load(data_file)

try:
    # Подключение к Zabbix API
    zapi = ZabbixAPI(f"http://{data['address']}")
    zapi.login(data['login']['user'], data['login']['password'])
    get_hosts(zapi, "Коммутаторы")
    get_hosts(zapi, "Маршрутизаторы")

   

except Exception as e:
    print(f"Ошибка: {e}")

finally:
    # Выход из Zabbix API
    zapi.logout()
