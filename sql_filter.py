import sqlite3
import subprocess
import netmiko


def execute_snmpwalk(ip_address, community_string):
    """Выполнение SNMP-walk для заданного IP-адреса и строка сообщества"""
    command = ['snmpwalk', '-v2c', f'-c{community_string}', ip_address, '1.3.6.1.2.1.1.1.0']
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        return output.decode(errors='ignore').splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Ошибка для IP {ip_address}: {e.output.decode(errors='ignore').strip()}")
        return []
    except UnicodeDecodeError as e:
        print(f"Ошибка декодирования для IP {ip_address}: {e}")
        return []
    except Exception as e:
        print(f"Неожиданная ошибка для IP {ip_address}: {e}")
        return []


def connect_ssh(ip_address, type, command):
    """Подключение к устройству по SSH и выполнение команды"""
    device = {
        "device_type": type,
        "ip": ip_address,
        "username": "admin",
        "password": "72HeccrfZ,72"
    }
    try:
        with netmiko.ConnectHandler(**device) as ssh_connection:
            return ssh_connection.send_command(command).splitlines()
    except Exception as e:
        print(f"Ошибка подключения к устройству {ip_address}: {e}")
        return []


def get_ips(cursor, group_name):
    """Получение IP-адресов устройств из указанной группы"""
    devices = []
    try:
        cursor.execute('''
        SELECT h.host
        FROM hosts h
        JOIN host_hostgroup hhg ON h.hostid = hhg.hostid
        JOIN hostgroups hg ON hhg.groupid = hg.groupid
        WHERE hg.name = ?;
        ''', (group_name,))

        results = cursor.fetchall()
        devices = [host[0] for host in results]
        if devices:
            print(f"Хосты в группе '{group_name}': {devices}")
        else:
            print(f"В группе '{group_name}' нет хостов.")
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении SQL-запроса для группы '{group_name}': {e}")
    return devices

def get_device_type(cursor, device_name):
    """Получение типа устройства по его имени"""
    device_type = None
    try:
        cursor.execute('''
        SELECT h.type
        FROM hosts h
        WHERE h.host =?;
        ''', (device_name,))

        result = cursor.fetchone()
        if result:
            device_type = result[0]
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении SQL-запроса для устройства '{device_name}': {e}")
    return device_type

def main():
    conn = sqlite3.connect('zabbix_hosts.db')
    cursor = conn.cursor()

    communities = ['sysadmin', 'russcom', 'public']
    
    try:
        group_names = ["ДЦ Респ. 55  Коммутаторы", "ДЦ Респ. 55  Маршрутизаторы"]
        for group_name in group_names:
            devices = get_ips(cursor, group_name)
            for device in devices:
                for community in communities:
                    output = execute_snmpwalk(device, community)
                    if output:
                        print(output)
                        break
                else:
                    type_ = get_device_type(cursor, device)
                    print(type_)
                    if type_ == "mikrotik":
                        type_ = "mikrotik_routeros"
                    command = "show system"
                    output = connect_ssh(device, type_, command)
                    if output:
                        print(output)

    except Exception as e:
        print(f"Ошибка: {e}")

    finally:
        cursor.close()
        conn.close()


main()