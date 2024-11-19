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

        self.device_tab = ttk.Frame(self.tabs)
        self.account_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.device_tab, text='Устройства')
        self.tabs.add(self.account_tab, text='Учетные записи')

        # Поля для устройств
        self.device_ip_label = tk.Label(self.device_tab, text="IP-адрес устройства:")
        self.device_ip_label.pack()
        self.device_ip_entry = tk.Entry(self.device_tab)
        self.device_ip_entry.pack()

        self.device_model_label = tk.Label(self.device_tab, text="Модель устройства:")
        self.device_model_label.pack()
        self.device_model_entry = tk.Entry(self.device_tab)
        self.device_model_entry.pack()

        self.device_group_label = tk.Label(self.device_tab, text="Группа устройства:")
        self.device_group_label.pack()
        self.device_group_entry = tk.Entry(self.device_tab)
        self.device_group_entry.pack()

        self.add_device_button = tk.Button(self.device_tab, text="Добавить устройство", command=self.add_device)
        self.add_device_button.pack()

        self.device_list = ttk.Treeview(self.device_tab, columns=('ID', 'IP', 'Model', 'Group'), show='headings')
        self.device_list.heading('ID', text='ID')
        self.device_list.heading('IP', text='IP-адрес')
        self.device_list.heading('Model', text='Модель')
        self.device_list.heading('Group', text='Группа')
        self.device_list.pack(expand=True, fill='both')

        self.load_devices()

        # Поля для учетных записей
        self.username_label = tk.Label(self.account_tab, text="Имя пользователя:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.account_tab)
        self.username_entry.pack()

        self.password_label = tk.Label(self.account_tab, text="Пароль:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.account_tab, show='')
        self.password_entry.pack()

        self.privilege_label = tk.Label(self.account_tab, text="Уровень привилегий:")
        self.privilege_label.pack()
        self.privilege_entry = tk.Entry(self.account_tab)
        self.privilege_entry.pack()

        self.host_id_label = tk.Label(self.account_tab, text="ID устройства:")
        self.host_id_label.pack()

        # Выпадающее меню для выбора устройства
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
        self.update_host_combobox()

    def init_db(self):
        self.conn = sqlite3.connect('password_manager.db')
        self.cursor = self.conn.cursor()

        # Создание таблиц
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS hosts (
                hostid TEXT PRIMARY KEY,
                host TEXT,
                type TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS hostgroups (
                groupid TEXT PRIMARY KEY,
                name TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS host_hostgroup (
                hostid TEXT NOT NULL,
                groupid TEXT NOT NULL,
                PRIMARY KEY (hostid, groupid)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                privilege_level TEXT NOT NULL,
                hostid TEXT,
                FOREIGN KEY (hostid) REFERENCES hosts (hostid)
            )
        ''')
        self.conn.commit()

    def add_device(self):
        ip_address = self.device_ip_entry.get()
        model = self.device_model_entry.get()
        group = self.device_group_entry.get()

        if ip_address and model:
            # Создание нового hostid (можно настроить свою логику создания уникальных идентификаторов)
            hostid = ip_address

            self.cursor.execute('INSERT OR REPLACE INTO hosts (hostid, host, type) VALUES (?, ?, ?)', 
                                (hostid, model, 'unknown'))
            self.cursor.execute('INSERT OR REPLACE INTO hostgroups (groupid, name) VALUES (?, ?)', 
                                (group, group))
            self.cursor.execute('INSERT OR REPLACE INTO host_hostgroup (hostid, groupid) VALUES (?, ?)', 
                                (hostid, group))
            
            self.conn.commit()

            self.device_ip_entry.delete(0, tk.END)
            self.device_model_entry.delete(0, tk.END)
            self.device_group_entry.delete(0, tk.END)
            self.load_devices()
            self.update_host_combobox()
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
            self.host_id_combobox.set('')  # Очищаем выбор
            self.load_accounts()
        else:
            messagebox.showwarning("Внимание", "Заполните все поля.")

    def load_devices(self):
        for row in self.device_list.get_children():
            self.device_list.delete(row)
        self.cursor.execute('SELECT * FROM hosts')
        for device in self.cursor.fetchall():
            self.device_list.insert('', 'end', values=device)

    def load_accounts(self):
        for row in self.account_list.get_children():
            self.account_list.delete(row)
        self.cursor.execute('SELECT * FROM accounts')
        for account in self.cursor.fetchall():
            self.account_list.insert('', 'end', values=account)

    def update_host_combobox(self):
        self.host_id_combobox['values'] = []
        self.cursor.execute('SELECT hostid FROM hosts')
        hosts = self.cursor.fetchall()
        self.host_id_combobox['values'] = [host[0] for host in hosts]

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManager(root)
    root.mainloop()
