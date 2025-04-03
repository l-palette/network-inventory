import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

class PasswordManager:
    def __init__(self, master):
        self.master = master
        master.title("Менеджер паролей сетевых устройств")

        # Настройка базы данных
        self.init_db()

        # Вкладки
        self.tabs = ttk.Notebook(master)
        self.tabs.pack(fill='both', expand=True)

        self.host_tab = ttk.Frame(self.tabs)
        self.account_tab = ttk.Frame(self.tabs)
        self.group_tab = ttk.Frame(self.tabs)
        self.host_group_tab = ttk.Frame(self.tabs)  
        self.snmp_tab = ttk.Frame(self.tabs)  

        self.tabs.add(self.host_tab, text='Устройства')
        self.tabs.add(self.account_tab, text='Учетные записи')
        self.tabs.add(self.group_tab, text='Группы')  
        self.tabs.add(self.host_group_tab, text='Группа - устройство') 
        self.tabs.add(self.snmp_tab, text='SNMP Community') 

        # Поля для устройств
        self.host_ip_label = tk.Label(self.host_tab, text="Hostname:")
        self.host_ip_label.pack()
        self.host_ip_entry = tk.Entry(self.host_tab)
        self.host_ip_entry.pack()

        self.host_model_label = tk.Label(self.host_tab, text="Модель устройства:")
        self.host_model_label.pack()
        self.host_model_entry = tk.Entry(self.host_tab)
        self.host_model_entry.pack()
        """
        self.host_group_label = tk.Label(self.host_tab, text="Группа устройства:")
        self.host_group_label.pack()
        self.host_group_combobox = ttk.Combobox(self.host_tab, state='readonly')
        self.host_group_combobox.pack()
        """
        self.add_host_button = tk.Button(self.host_tab, text="Добавить устройство", command=self.add_host)
        self.add_host_button.pack()

        self.host_list = ttk.Treeview(self.host_tab, columns=('ID', 'IP', 'Model'), show='headings')
        self.host_list.heading('ID', text='ID')
        self.host_list.heading('IP', text='Hostname')
        self.host_list.heading('Model', text='Модель')
        self.host_list.pack(expand=True, fill='both')
        self.load_hosts()

        #self.update_group_combobox()


########################################################################################################################
        # Поля для учетных записей
        self.username_label = tk.Label(self.account_tab, text="Имя пользователя:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.account_tab)
        self.username_entry.pack()

        self.password_label = tk.Label(self.account_tab, text="Пароль:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.account_tab, show='*')
        self.password_entry.pack()

        self.privilege_label = tk.Label(self.account_tab, text="Уровень привилегий:")
        self.privilege_label.pack()
        self.privilege_entry = tk.Entry(self.account_tab)
        self.privilege_entry.pack()

        self.host_id_label = tk.Label(self.account_tab, text="Hostname:")
        self.host_id_label.pack()
        self.host_id_combobox = ttk.Combobox(self.account_tab, state='readonly')
        self.host_id_combobox.pack()

        self.add_account_button = tk.Button(self.account_tab, text="Добавить учетную запись", command=self.add_account)
        self.add_account_button.pack()

        self.account_list = ttk.Treeview(self.account_tab, columns=('ID', 'Username', 'Password', 'Privilege', 'Host ID'), show='headings')
        self.account_list.heading('ID', text='ID')
        self.account_list.heading('Username', text='Имя пользователя')
        self.account_list.heading('Password', text='Пароль')
        self.account_list.heading('Privilege', text='Уровень привилегий')
        self.account_list.heading('Host ID', text='ID устройства')
        self.account_list.pack(expand=True, fill='both')
        self.load_accounts()

        #загрузка ID устройств в выпадающее поле
        self.update_host_combobox()

########################################################################################################################
        # Вкладка для групп

        self.group_list = ttk.Treeview(self.group_tab, columns=('Group ID', 'Group Name'), show='headings')
        self.group_list.heading('Group ID', text='Group ID')
        self.group_list.heading('Group Name', text='Group Name')
        self.group_list.pack(expand=True, fill='both')

########################################################################################################################
        # Вкладка для SNMP Community

        # Выпадающее меню для ip address
        self.host_id_label = tk.Label(self.snmp_tab, text="ID устройства:")
        self.host_id_label.pack()

        self.host_id_combobox = ttk.Combobox(self.snmp_tab, state='readonly')
        self.host_id_combobox.pack()

        self.snmp_community_label = tk.Label(self.snmp_tab, text="SNMP Community:")
        self.snmp_community_label.pack()
        self.snmp_community_entry = tk.Entry(self.snmp_tab)
        self.snmp_community_entry.pack()

        self.add_snmp_button = tk.Button(self.snmp_tab, text="Добавить SNMP Community", command=self.add_snmp_community)
        self.add_snmp_button.pack()

        self.snmp_list = ttk.Treeview(self.snmp_tab, columns=('Host ID', 'Community'), show='headings')
        self.snmp_list.heading('Host ID', text='Host ID')
        self.snmp_list.heading('Community', text='Community')
        self.snmp_list.pack(expand=True, fill='both')


        self.load_snmp_communities()
        self.load_groups() 

        self.update_host_combobox()
########################################################################################################################
    def init_db(self):
        self.conn = sqlite3.connect('password_manager.db')
        self.cursor = self.conn.cursor()

        # Создание таблиц
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS hosts (
                my_host_id INTEGER PRIMARY KEY AUTOINCREMENT,
                hostid TEXT,
                host TEXT,
                type TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                my_group_id INTEGER PRIMARY KEY AUTOINCREMENT,
                groupid TEXT NOT NULL,
                group_name TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS host_group (
                host_group_id INTEGER PRIMARY KEY AUTOINCREMENT,
                hostid TEXT NOT NULL,
                groupid TEXT NOT NULL,
                FOREIGN KEY (hostid) REFERENCES hosts (hostid),
                FOREIGN KEY (groupid) REFERENCES groups (groupid)   
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                accountid INTEGER PRIMARY KEY AUTOINCREMENT,
                hostid TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                privilege TEXT NOT NULL,
                FOREIGN KEY (hostid) REFERENCES hosts (hostid)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS community (
                communityid INTEGER PRIMARY KEY AUTOINCREMENT,
                hostid TEXT NOT NULL,
                community TEXT NOT NULL,
                FOREIGN KEY (hostid) REFERENCES hosts (hostid)
            )
        ''')
        self.conn.commit()


    def load_hosts(self):
        for row in self.host_list.get_children():
            self.host_list.delete(row)
        self.cursor.execute('SELECT * FROM hosts')
        for host in self.cursor.fetchall():
            self.host_list.insert('', 'end', values=host)

    def load_accounts(self):
        for row in self.account_list.get_children():
            self.account_list.delete(row)
        self.cursor.execute('SELECT * FROM accounts')
        for account in self.cursor.fetchall():
            self.account_list.insert('', 'end', values=account)

    def load_groups(self):
        for row in self.group_list.get_children():
            self.group_list.delete(row)
        self.cursor.execute('SELECT * FROM groups')
        for group in self.cursor.fetchall():
            self.group_list.insert('', 'end', values=group)

    def load_snmp_communities(self):
        for row in self.snmp_list.get_children():
            self.snmp_list.delete(row)
        self.cursor.execute('SELECT * FROM community')
        for community in self.cursor.fetchall():
            self.snmp_list.insert('', 'end', values=community)

    def add_host(self):
        ip_address = self.host_ip_entry.get()
        model = self.host_model_entry.get()
        group = self.host_group_combobox.get()

        if ip_address and model:
            # Создание нового hostid
            hostid = ip_address

            self.cursor.execute('INSERT OR REPLACE INTO hosts (hostid, host, type) VALUES (?, ?, ?)', 
                                (hostid, model, 'unknown'))
            self.cursor.execute('INSERT OR REPLACE INTO host_group (hostid, groupid) VALUES (?, ?)', 
                                (hostid, groupid))
            self.conn.commit()

            # Очистка полей ввода
            self.host_ip_entry.delete(0, tk.END)
            self.host_model_entry.delete(0, tk.END)
            self.host_group_combobox.set('')
            self.load_hosts()
            self.load_groups()
            self.update_host_combobox()
            self.update_group_combobox()
        else:
            messagebox.showwarning("Внимание", "Введите IP-адрес и модель устройства.")

    def add_account(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        privilege_level = self.privilege_entry.get()
        host_id = self.host_id_combobox.get()

        if username and password and privilege_level and host_id:
            self.cursor.execute('INSERT INTO accounts (username, password, privilege_level, hostid) VALUES (?, ?, ?, ?)', 
                                (username, password, privilege_level, host_id))
            self.conn.commit()
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.privilege_entry.delete(0, tk.END)
            self.host_id_combobox.set('')
            self.load_accounts()
        else:
            messagebox.showwarning("Внимание", "Заполните все поля.")

    def add_snmp_community(self):
        host_id = self.snmp_hostid_entry.get()
        community = self.snmp_community_entry.get()

        if host_id and community:
            self.cursor.execute('INSERT INTO snmp_community (hostid, community) VALUES (?, ?)', (host_id, community))
            self.conn.commit()
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.snmp_hostid_entry.delete(0, tk.END)
            self.snmp_community_entry.delete(0, tk.END)
            self.load_snmp_communities()
        else:
            messagebox.showwarning("Внимание", "Введите Host ID и SNMP Community.")

    def update_host_combobox(self):
        self.host_id_combobox['values'] = []
        self.cursor.execute('SELECT host FROM hosts')
        hosts = self.cursor.fetchall()
        self.host_id_combobox['values'] = [host[0] for host in hosts]

    def update_group_combobox(self):
        self.host_group_combobox['values'] = []
        self.cursor.execute('SELECT name FROM hostgroups')
        hostgroups = self.cursor.fetchall()
        self.host_group_combobox['values'] = [group[0] for group in hostgroups]

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManager(root)
    root.mainloop()
