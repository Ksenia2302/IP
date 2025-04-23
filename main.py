import platform
import subprocess
import threading
import tkinter as tk
from tkinter import messagebox
import socket
import json
import os


class IPApp:
    def __init__(self, root):
        self.root = root
        self.root.title('IP Mnager')
        self.root.geometry('400x300')

        self.ip_file = 'saved_ips.json'

        self.create_wigets()
        self.show_current_ip()
        self.add_my_ip()


    def create_wigets(self):
        current_ip_frame = tk.Label(self.root, text='Ваш текущий IP', padx=10, pady=10)
        current_ip_frame.pack(padx=10, pady=10, fill='x')

        self.current_ip_label = tk.Label(current_ip_frame, text='Определение...')
        self.current_ip_label.pack()

        add_ip_frame = tk.LabelFrame(self.root, text='Добавить IP', padx=10, pady=10)
        add_ip_frame.pack(pady=10, fill='x', padx=10)

        tk.Label(add_ip_frame, text='Имя/Описание: ').pack(anchor='w')
        self.name_entry = tk.Entry(add_ip_frame, width=40)
        self.name_entry.pack()

        tk.Label(add_ip_frame, text='IP-адрес: ').pack(ancho='w')
        self.ip_entry = tk.Entry(add_ip_frame, width=40)
        self.ip_entry.pack()

        add_button = tk.Button(add_ip_frame, text='Добавить IP', command=self.save_ip)
        add_button.pack(pady=5)


        view_button = tk.Button(self.root, text='Просмотреть сохраненные IP', command=self.view_saved_ip)
        view_button.pack(pady=5)
        self.ping_result = tk.Label(self.root)
        self.ping_result.pack()

        pr_button = tk.Button(self.root, text='Проверть IP', command=self.pr_saved_ip)
        pr_button.pack(pady=5)

    def pr_saved_ip(self):
        ip = self .ip_entry.get().strip()
        self.ping_result.config(text='ПРоверяем', foreground='black')
        self.root.update()

        threading.Thread(target=self.do_ping, args=(ip,), daemon=True).start()

    def do_ping(self, ip):
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        count = 4
        process = subprocess.Popen(
            ['ping', param, count, ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        output, error = process.communicate()

        if process.returncode == 0:
            result = 'Доступен'
            color = 'green'
        else:
            result = 'Недоступен'
            color = 'red'

    def view_saved_ip(self):
        if not os.path.exists(self.ip_file):
            messagebox.showinfo('Информация', 'Нет сохраненных IP-адресов')
            return
        with open(self.ip_file, 'r') as f:
            ips = json.load(f)
        if not ips:
            messagebox.showinfo('Информация', 'Нет сохраненных IP-адресов')
            return
        ip_window = tk.Toplevel(self.root)
        ip_window.title('Сохраненные Ip-адреса')
        text_widget = tk.Text(ip_window, wrap=tk.WORD)
        text_widget.pack(expand=True, fill='both', padx=10, pady=10)

        for item in ips:
            text_widget.insert(tk.END, f'{item['name']}: {item['ip']}\n')

        text_widget.config(state=tk.DISABLED)
    def show_current_ip(self):
        try:
            self.hostname = socket.gethostname()
            self.ip_address = socket.gethostbyname(self.hostname)
            self.current_ip_label.config(text=f'{self.ip_address} (Хост: {self.hostname})')
        except Exception as e:
            self.current_ip_label.config(text=f'Ошибка: {str(e)}')


    def save_ip(self):
        name = self.name_entry.get().strip()
        ip = self.ip_entry.get().strip()
        if not name or not ip:
            messagebox.showerror('Ошибка', 'Пожалуйста, введите имя и IP-адрес')
            return
        try:
            socket.inet_aton(ip)
        except socket.error:
            messagebox.showerror('Ошибка', 'Неверный формат IP-адреса')
            return

        ips = []
        if os.path.exists(self.ip_file):
            try:
                with open(self.ip_file, 'r') as f:
                    ips = json.load(f)
            except:
                pass

        ips.append({'name': name, 'ip': ip})
        with open(self.ip_file, 'w') as f:
            json.dump(ips, f, indent=4)
        messagebox.showinfo('Успех', 'IP-адрес успешно сохранен')
        self.name_entry.delete(0, tk.END)
        self.ip_entry.delete(0, tk.END)

    def add_my_ip(self):
        with open(self.ip_file, 'r') as f:
            ips = json.load(f)
            ips.append({'name': self.hostname, 'ip': self.ip_address})
        with open(self.ip_file, 'w') as f:
            json.dump(ips, f, indent=4)







root = tk.Tk()
ip = IPApp(root)


root.mainloop()