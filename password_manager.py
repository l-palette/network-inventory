import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Создаем базу данных и таблицы
def init_db():
    conn = sqlite3.connect('password_manager.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT NOT NULL,
            model TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            privilege_level TEXT NOT NULL,
            device_id INTEGER NOT NULL,
            FOREIGN KEY (device_id) REFERENCES devices (id)
        )
    ''')
    conn.commit()
    conn.close()

# Класс для менеджера паролей
class PasswordManager:
    def __init__(self, master):
        self.master = master
        master.title("Менеджер паролей сетевых устройств")
      
        # Вкладки
        self.tabs = ttk.Notebook(master)
        self.tabs.pack(fill='both', expand='true')

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

        self.add_device_button = tk.Button(self.device_tab, text="Добавить устройство", command=self.add_device)
        self.add_device_button.pack()

        self.device_list = ttk.Treeview(self.device_tab, columns=('ID', 'IP', 'Model'), show='headings')
        self.device_list.heading('ID', text='ID')
        self.device_list.heading('IP', text='IP-адрес')
        self.device_list.heading('Model', text='Модель')
        self.device_list.pack(expand=True, fill='both')
        self.load_devices()

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

        self.device_id_label = tk.Label(self.account_tab, text="ID устройства:")
        self.device_id_label.pack()
        
        # Выпадающее меню для выбора устройства
        self.device_id_combobox = ttk.Combobox(self.account_tab, state='readonly')
        self.device_id_combobox.pack()
        
        self.add_account_button = tk.Button(self.account_tab, text="Добавить учетную запись", command=self.add_account)
        self.add_account_button.pack()

        self.account_list = ttk.Treeview(self.account_tab, columns=('ID', 'Username', 'Password', 'Privilege', 'Device ID'), show='headings')
        self.account_list.heading('ID', text='ID')
        self.account_list.heading('Username', text='Имя пользователя')
        self.account_list.heading('Password', text='Пароль')
        self.account_list.heading('Privilege', text='Уровень привилегий')
        self.account_list.heading('Device ID', text='ID устройства')
        self.account_list.pack(expand=True, fill='both')
        self.load_accounts()

        # Загрузка ID устройств в выпадающее меню
        self.update_device_combobox()

    def add_device(self):
        ip_address = self.device_ip_entry.get()
        model = self.device_model_entry.get()
        if ip_address and model:
            conn = sqlite3.connect('password_manager.db')
            c = conn.cursor()
            c.execute('INSERT INTO devices (ip_address, model) VALUES (?, ?)', (ip_address, model))
            conn.commit()
            conn.close()
            self.device_ip_entry.delete(0, tk.END)
            self.device_model_entry.delete(0, tk.END)
            self.load_devices()
            self.update_device_combobox()  # Обновляем выпадающее меню
        else:
            messagebox.showwarning("Внимание", "Введите IP-адрес и модель устройства.")

    def add_account(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        privilege_level = self.privilege_entry.get()
        device_id = self.device_id_combobox.get()
        
        if username and password and privilege_level and device_id:
            conn = sqlite3.connect('password_manager.db')
            c = conn.cursor()
            c.execute('INSERT INTO accounts (username, password, privilege_level, device_id) VALUES (?, ?, ?, ?)', 
                      (username, password, privilege_level, device_id))
            conn.commit()
            conn.close()
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.privilege_entry.delete(0, tk.END)
            self.device_id_combobox.set('')  # Очищаем выбор
            self.load_accounts()
        else:
            messagebox.showwarning("Внимание", "Заполните все поля.")

    def load_devices(self):
        for row in self.device_list.get_children():
            self.device_list.delete(row)
        conn = sqlite3.connect('password_manager.db')
        c = conn.cursor()
        c.execute('SELECT * FROM devices')
        for device in c.fetchall():
            self.device_list.insert('', 'end', values=device)
        conn.close()

    def load_accounts(self):
        for row in self.account_list.get_children():
            self.account_list.delete(row)
        conn = sqlite3.connect('password_manager.db')
        c = conn.cursor()
        c.execute('SELECT * FROM accounts')
        for account in c.fetchall():
            self.account_list.insert('', 'end', values=account)
        conn.close()

    def update_device_combobox(self):
        self.device_id_combobox['values'] = []  # Сбрасываем значения
        conn = sqlite3.connect('password_manager.db')
        c = conn.cursor()
        c.execute('SELECT id FROM devices')
        devices = c.fetchall()
        self.device_id_combobox['values'] = [device[0] for device in devices]  # Добавляем ID устройств
        conn.close()

# Инициализация базы данных
init_db()

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManager(root)
    root.mainloop()
