# Импорт библиотек
from zabbix_api import ZabbixAPI
import json
import sqlite3

# Функция определения типа устройства
def get_device_type(lines):
    lines = lines.lower()
    if 'accedian' in lines:
        return 'accedian'
    
    elif 'adtran_os' in lines:
        return 'adtran_os'
    
    elif 'adva_fsp150f2' in lines:
        return 'adva_fsp150f2'
    elif 'adva_fsp150f3' in lines:
        return 'adva_fsp150f3'
    
    elif 'alcatel_aos' in lines:
        return 'alcatel_aos'
    elif 'alcatel_sros' in lines:
        return 'alcatel_sros'
    
    elif 'allied_telesis_awplus' in lines:
        return 'allied_telesis_awplus'
    
    elif 'apresia_aeos' in lines:
        return 'apresia_aeos'
    
    elif 'arista_eos' in lines:
        return 'arista_eos'
    
    elif 'arris_cer' in lines:
        return 'arris_cer'
    
    elif 'aruba_os' in lines:
        return 'aruba_os'
    elif 'aruba_osswitch' in lines:
        return 'aruba_osswitch'
    elif 'aruba_procurve' in lines:
        return 'aruba_procurve'
    
    elif 'audiocode_66' in lines:
        return 'audiocode_66'
    elif 'audiocode_72' in lines:
        return 'audiocode_72'
    elif 'audiocode_shell' in lines:
        return 'audiocode_shell'
    
    elif 'avaya_ers' in lines:
        return 'avaya_ers'
    elif 'avaya_vsp' in lines:
        return 'avaya_vsp'
    
    elif 'broacom_icos' in lines:
        return 'broacom_icos'
    
    elif 'brocade_fastiron' in lines:
        return 'brocade_fastiron'
    elif 'brocade_fos' in lines:
        return 'brocade_fos'
    elif 'brocade_netiron' in lines:
        return 'brocade_netiron'
    elif 'brocade_nos' in lines:
        return 'brocade_nos'
    elif 'brocade_vdx' in lines:
        return 'brocade_vdx'
    elif 'brocade_vyos' in lines:
        return 'brocade_vyos'
    
    elif 'calix_b6' in lines:
        return 'calix_b6'
    
    elif 'casa_cmts' in lines:
        return 'casa_cmts'
    
    elif 'cdot_cros' in lines:
        return 'cdot_cros'
    
    elif 'centec_os' in lines:
        return 'centec_os'
    
    elif 'checkpoint_gaia' in lines:
        return 'checkpoint_gaia'
    
    elif'ciena_saos' in lines:
        return 'ciena_saos'
    
    elif 'cisco_asa' in lines:
        return 'cisco_asa'
    elif 'cisco_ftd' in lines:
        return 'cisco_ftd'
    elif 'cisco_nxos' in lines:
        return 'cisco_nxos'
    elif 'cisco_s200' in lines:
        return 'cisco_s200'
    elif 'cisco_s300' in lines:
        return 'cisco_s300'
    elif 'cisco_tp' in lines:
        return 'cisco_tp'
    elif 'cisco_viptela' in lines:
        return 'cisco_viptela'
    elif 'cisco_wlc' in lines:
        return 'cisco_wlc'
    elif 'cisco_xe' in lines:
        return 'cisco_xe'
    elif 'cisco_xr' in lines:
        return 'cisco_xr'
    elif  'cisco' in lines:
        return 'cisco_ios'
    
    elif 'cloudgenix_ion' in lines:
        return 'cloudgenix_ion'
    elif 'coriant' in lines:
        return 'coriant'
    elif 'dell_dnos9' in lines:
        return 'dell_dnos9'
    elif 'dell_force10' in lines:
        return 'dell_force10'
    elif 'dell_isilon' in lines:
        return 'dell_isilon'
    elif 'dell_os10' in lines:
        return 'dell_os10'
    elif 'dell_os6' in lines:
        return 'dell_os6'
    elif 'dell_os9' in lines:
        return 'dell_os9'
    elif 'dell_powerconnect' in lines:
        return 'dell_powerconnect'
    elif 'dell_sonic' in lines:
        return 'dell_sonic'
    elif 'digi_transport' in lines:
        return 'digi_transport'
    
    elif 'dlink' in lines:
        return 'dlink_ds'
    
    elif 'eltex_esr' in lines:
        return 'eltex_esr'
    elif 'eltex' in lines:
        return 'eltex'

    elif 'endace' in lines:
        return 'endace'
    
    elif 'enterasys' in lines:
        return 'enterasys'
    
    elif 'ericsson_ipos' in lines:
        return 'ericsson_ipos'
    elif 'ericsson_mltn63' in lines:
        return 'ericsson_mltn63'
    elif 'ericsson_mltn66' in lines:
        return 'ericsson_mltn66'
    
    elif 'extreme_ers' in lines:
        return 'extreme_ers'
    elif 'extreme_exos' in lines:
        return 'extreme_exos'
    elif 'extreme_netiron' in lines:
        return 'extreme_netiron'
    elif 'extreme_nos' in lines:
        return 'extreme_nos'
    elif 'extreme_slx' in lines:
        return 'extreme_slx'
    elif 'extreme_tierra' in lines:
        return 'extreme_tierra'
    elif 'extreme_vdx' in lines:
        return 'extreme_vdx'
    elif 'extreme_vsp' in lines:
        return 'extreme_vsp'
    elif 'extreme_wing' in lines:
        return 'extreme_wing'
    elif 'extreme' in lines:
        return 'extreme'
    
    elif 'f5_linux' in lines:
        return 'f5_linux'
    elif 'f5_ltm' in lines:
        return 'f5_ltm'
    elif 'f5_tmsh' in lines:
        return 'f5_tmsh'
    elif 'fiberstore_fsos' in lines:
        return 'fiberstore_fsos'
    elif 'flexvnf' in lines:
        return 'flexvnf'
    elif 'fortinet' in lines:
        return 'fortinet'
    elif 'generic_termserver' in lines:
        return 'generic_termserver'
    elif 'hillstone_stoneos' in lines:
        return 'hillstone_stoneos'
    
    elif 'hp_comware' in lines:
        return 'hp_comware'
    elif 'hp_procurve' in lines:
        return 'hp_procurve'
    

    elif 'huawei_olt' in lines:
        return 'huawei_olt'
    elif 'huawei_smartax' in lines:
        return 'huawei_smartax'
    elif 'huawei_vrp' in lines:
        return 'huawei_vrp'
    elif 'huawei_vrpv8' in lines:
        return 'huawei_vrpv8'
    elif 'huawei' in lines:
        return 'huawei'
    
    elif 'ipinfusion_ocnos' in lines:
        return 'ipinfusion_ocnos'
    

    elif 'juniper_junos' in lines:
        return 'juniper_junos'
    elif 'juniper_screenos' in lines:
        return 'juniper_screenos'
    elif 'juniper' in lines:
        return 'juniper'
    

    elif 'keymile_nos' in lines:
        return 'keymile_nos'
    elif 'keymile' in lines:
        return 'keymile'
    
    elif 'linux' in lines:
        return 'linux'
    elif 'maipu' in lines:
        return'maipu'
    elif 'mellanox' in lines:
        return'mellanox'
    elif 'mellanox_mlnxos' in lines:
        return'mellanox_mlnxos'
    
    elif 'mikrotik_switchos' in lines:
        return'mikrotik_switchos'
    elif'mikrotik' in lines:
        return'mikrotik_routeros'
    
    elif 'mrv_lx' in lines:
        return'mrv_lx'
    elif 'mrv_optiswitch' in lines:
        return'mrv_optiswitch'
    elif 'netapp_cdot' in lines:
        return 'netapp_cdot'
    
    elif 'netgear' in lines:
        return 'netgear_prosafe'
    
    elif 'netscaler' in lines:
        return 'netscaler'
    
    elif 'nokia_srl' in lines:
        return 'nokia_srl'
    elif 'nokia' in lines:
        return 'nokia_sros'
    
    
    elif 'oneaccess_oneos' in lines:
        return 'oneaccess_oneos'
    elif 'ovs_linux' in lines:
        return 'ovs_linux'
    elif 'paloalto_panos' in lines:
        return 'paloalto_panos'
    elif 'pluribus' in lines:
        return 'pluribus'
    elif 'quanta_mesh' in lines:
        return 'quanta_mesh'
    elif 'rad_etx' in lines:
        return 'rad_etx'
    elif 'raisecom_roap' in lines:
        return 'raisecom_roap'
    elif 'ruckus_fastiron' in lines:
        return 'ruckus_fastiron'
    elif 'ruijie_os' in lines:
        return 'ruijie_os'
    elif 'sixwind_os' in lines:
        return'sixwind_os'
    elif'sophos_sfos' in lines:
        return'sophos_sfos'
    elif'supermicro_smis' in lines:
        return'supermicro_smis'
    elif 'teldat_cit' in lines:
        return 'teldat_cit'
    
    elif 'tplink' in lines:
        return 'tplink_jetstream'
    

    elif 'ubiquiti_edgerouter' in lines:
        return 'ubiquiti_edgerouter'
    elif 'ubiquiti_edgeswitch' in lines:
        return 'ubiquiti_edgeswitch'
    elif 'ubiquiti_unifiswitch' in lines:
        return 'ubiquiti_unifiswitch'
    elif 'ubiquiti' in lines:
        return 'ubiquiti_edge'
    
    elif 'vyatta_vyos' in lines:
        return 'vyatta_vyos'
    elif 'vyos' in lines:
        return 'vyos'
    elif 'watchguard_fireware' in lines:
        return 'watchguard_fireware'
    elif 'yamaha' in lines:
        return 'yamaha'
    
    elif 'zyxel' in lines:
        return 'zyxel'
    elif 'zte' in lines:
        return 'zte_zxros'
    else:
        return 'generic'


# Основной код
with open('config.json') as data_file:
    data = json.load(data_file)

conn = sqlite3.connect('zabbix_hosts.db')
cursor = conn.cursor()

# Создание таблиц
cursor.execute('''
    CREATE TABLE IF NOT EXISTS hosts (
        my_host_id INTEGER PRIMARY KEY AUTOINCREMENT,
        hostid TEXT,
        host TEXT,
        type TEXT 
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS groups (
        my_group_id INTEGER PRIMARY KEY AUTOINCREMENT,
        groupid TEXT NOT NULL,
        group_name TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS host_group (
        host_group_id INTEGER PRIMARY KEY AUTOINCREMENT,
        hostid TEXT NOT NULL,
        groupid TEXT NOT NULL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        accountid INTEGER PRIMARY KEY AUTOINCREMENT,
        hostid TEXT NOT NULL,
        username TEXT,
        password TEXT,
        privilege TEXT,
        FOREIGN KEY (hostid) REFERENCES hosts(hostid)
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS community (
        communityid INTEGER PRIMARY KEY AUTOINCREMENT,
        hostid TEXT NOT NULL,
        community TEXT NOT NULL,
        FOREIGN KEY (hostid) REFERENCES hosts(hostid)
    )
''')

try:
    # Подключение к Zabbix API
    zapi = ZabbixAPI(f"http://{data['address']}")
    zapi.login(data['login']['user'], data['login']['password'])

    hosts = zapi.host.get({"output": ["hostid", "host"]})
    groups = zapi.hostgroup.get({"output": ["groupid", "name"]})

    for group in groups:
        cursor.execute('''
            INSERT OR REPLACE INTO groups (groupid, group_name) VALUES (?, ?)
        ''', (group['groupid'], group['name']))
        print("!")

    conn.commit()

    for host in hosts:
        lines = ''
        host_id = host['hostid']
        templates = zapi.host.get({
            "output": ["hostid"],
            "selectParentTemplates": ["templateid", "name"],
            "hostids": host_id
        })
        if templates and 'parentTemplates' in templates[0]:
            for template in templates[0]['parentTemplates']:
                line = template['name'].lower()
                lines += line
            print(lines)
            host_type = get_device_type(lines)
            print("         ", host_type)
            print(f"Host ID: {host_id}, Hostname: {host['host']}, Type: {host_type}")
            cursor.execute('''
                INSERT OR REPLACE INTO hosts (hostid, host, type) VALUES (?, ?, ?)
            ''', (host['hostid'], host['host'], host_type))
    conn.commit()
    zapi.logout()

except Exception as e:
    print(f"Ошибка при подключении к Zabbix API или выполнении запроса: {e}")

finally:
    conn.close()