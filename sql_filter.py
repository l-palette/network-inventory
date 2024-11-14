import sqlite3
import subprocess
import netmiko
def execute_snmpwalk(ip_address, command):
    try:
        output = subprocess.check_output(command, shell=True)  # Добавлено shell=True для выполнения команды
        return output.decode(errors='ignore').splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error for IP {ip_address}: {e.output.decode(errors='ignore').strip()}")
        return []
    except UnicodeDecodeError as e:
        print(f"Unicode decode error for IP {ip_address}: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred for IP {ip_address}: {e}")
        return []
def get_device_type(device):
    pass
def connect_ssh(ip_address, command):
    try:
        device = {
            "device_type": "generic",
            "ip": ip_address,
            "username": "admin",
            "password": "72HeccrfZ,72"
        }
        ssh_connection = netmiko.ConnectHandler(**device)
        output = ssh_connection.send_command(command)
        ssh_connection.disconnect()
        return output.splitlines()
    except Exception as e:
        print(f"Ошибка подключения к устройству {ip_address}: {e}")
        return []
    
    
    
    
def get_ips(cursor, group_name):
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
        if results:
            print(f"Хосты в группе '{group_name}':")
            for host in results:
                devices.append(host[0])
        else:
            print(f"В группе '{group_name}' нет хостов.")
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении SQL-запроса для группы '{group_name}': {e}")
    return devices

# Подключение к базе данных
conn = sqlite3.connect('zabbix_hosts.db')
cursor = conn.cursor()

try:
    for group_name in ["ДЦ Респ. 55  Коммутаторы", "ДЦ Респ. 55  Маршрутизаторы"]:
        devices = get_ips(cursor, group_name)
        if devices:
            for device in devices:
                command = f"snmpwalk -v 2c -c sysadmin {device} 1.3.6.1.2.1.1.1.0"
                output = execute_snmpwalk(device, command)
                if output:
                    print(output)
                else:
                    command = "show system"
                    output = connect_ssh(device, command)
                    if output:
                        print(output)
                
except Exception as e:
    print(f"Ошибка: {e}")

finally:
    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()