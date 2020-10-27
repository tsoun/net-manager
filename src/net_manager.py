import os
import socket as sc
import tkinter as tk
import tkinter.scrolledtext as scr
import pyperclip
import subprocess
import datetime
from os.path import pardir, abspath, join, dirname
from time import gmtime, strftime
from sys import platform
from tkinter import messagebox
import webbrowser


global hostname, IP_address, VERSION
VERSION = '0.3.1'

current_dir = abspath(join(dirname(__file__), pardir))
image_path = join(current_dir, "img/net.png")

class main_win():
    def __init__(self, master):
        self.master = master
        self.master.option_add("*Font", 'arial 10')
        self.master.title('Net Manager ' + VERSION + ' Alpha')
        self.master.configure(background = 'white')
        self.master.resizable(False, False)
        self.masterback = tk.Frame(height = 500, width = 500)
        self.masterback.pack()
        self.masterback.configure(background = 'white')

        self.Message = tk.Label(self.master, text='Welcome to Net Manager ' + VERSION + ' \nAlpha Build - Exclusive Alpha Access.', font='Helvetica 13 bold', justify='left')
        self.Message.place(relx= 0.415, rely = 0.105, anchor = 'center')
        self.Message.configure(background = 'white')

        self.show_ip = tk.Button(self.master, text = 'Show host IP address', command = self.print_ip)
        self.show_ip.place(relx= 0.62, rely = 0.575, width = 200)
        self.show_ip.configure(background = 'white')

        self.ip_entry = tk.Entry(self.master)
        self.ip_entry.place(relx = 0.1, rely = 0.6)
        self.ip_entry.configure(background = 'white')

        var = tk.StringVar()
        var.set('Current Network: ' + self.find_nw_name())
        self.lbl_lcl_nw = tk.Label(master, textvariable = var, bg = 'white')
        self.lbl_lcl_nw.place(relx = 0.1, rely = 0.3)
        self.lbl_lcl_nw.configure(background = 'white')

        self.lcl_nw = tk.Entry(self.master)
        self.lcl_nw.place(relx = 0.1, rely = 0.4)
        self.lcl_nw.configure(background = 'white')

        self.show_hostname = tk.Button(self.master, text = 'Show hostname', command = self.print_hn)
        self.show_hostname.place(relx= 0.62, rely = 0.475, width = 200)
        self.show_hostname.configure(background = 'white')

        self.show_wifi_password = tk.Button(self.master, text = 'Show WiFi passphrases', command = self.find_wifi_password)
        self.show_wifi_password.place(relx= 0.62, rely = 0.375, width = 200)
        self.show_wifi_password.configure(background = 'white')

        self.show_SPEEDEST = tk.Button(self.master, text = 'Run Speedtest', command = self.print_SPEEDTEST)
        self.show_SPEEDEST.place(relx= 0.62, rely = 0.275, width = 200)
        self.show_SPEEDEST.configure(background = 'white')

        self.hostname_entry = tk.Entry(self.master)
        self.hostname_entry.place(relx = 0.1, rely = 0.5)
        self.hostname_entry.configure(background = 'white')

        img = tk.PhotoImage(file = image_path)
        self.master.label= tk.Label(self.master, image = img)
        self.master.label.image = img
        self.master.label.place(relx = 0.08, rely= 0.07)
        self.master.label.configure(background = 'white')

        self.log_label = tk.Label(self.master, bg = 'white', text = 'Action log:', font='Helvetica 8 italic bold')
        self.log_label.place(rely = 0.7, relx = 0.02)
        self.log_frame = tk.Frame(self.master, bg = 'white')
        self.log_frame.pack(fill = 'both', expand = 'yes')
        self.log = scr.ScrolledText(
            master = self.log_frame,
            wrap = 'word',
            width = 75,
            height = 10,
            background = 'blue',
            font = 'Courier 10',
            fg = 'white'
        )
        self.log.pack(padx = 10, pady = 10, fill = 'both', expand = 'True')
        self.log.insert('insert', 'Your network: ' + self.find_nw_name() + '\n')

    def show_isp(self, isp):
        isp_name = tk.StringVar()
        isp_name.set('ISP : ' + isp)
        self.lbl_lcl_nw = tk.Label(self.master, textvariable = isp_name, bg = 'white')
        self.lbl_lcl_nw.place(relx = 0.1, rely = 0.2)
        self.lbl_lcl_nw.configure(background = 'white')

    def open_browser(self):
        try:
            webbrowser.get(using='microsoft-edge').open('192.168.1.1', 1)
        except:
            webbrowser.open('192.168.1.1', 1)

    def print_hn(self):
        self.hostname_entry.delete(0, 'end')
        self.hostname_entry.insert(0, hostname)

    def show_info(self):
        messagebox.showinfo('Net Manager ' + VERSION + ' Alpha', 'contributors: tsoun and\nvanourogeros.')

    def print_ip(self):
        self.ip_entry.delete(0, 'end')
        self.ip_entry.insert(0, IP_address)

        self.copy_ip()
        self.print_time()
        self.print_to_log('Shown ' + hostname + '\'s IP address and copied it to clipboard.')

    def find_nw_name(self):
        if platform == 'win32':
          self.nw_str = (str(subprocess.check_output('netsh wlan show interfaces')))
        elif platform == 'linux' or platform == 'linux2':
          return (str(subprocess.check_output(('iwgetid', '-r')))[2:-3])
        self.nw_lst = self.nw_str.split()
        idx = self.nw_lst.index('SSID')
        idx += 2
        return self.nw_lst[idx][:-4]

    def copy_ip(self):
        pyperclip.copy(self.ip_entry.get())
        spam = pyperclip.paste()

    def print_to_log(self, msg):
        self.log.insert('insert', msg + '\n\n')
        self.log.see(tk.END)

    def print_time (self):
        self.log.insert('insert', '\n' + str(strftime('%Y.%m.%d, %H:%M:%S', gmtime())) + ' >> ')

    def find_wifi_password(self):
        self.print_time()
        self.print_to_log('Shown network ID\'s and passphrases.')
        data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split('\n')
        profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
        for i in profiles:
            try:
                results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8', errors="backslashreplace").split('\n')
                results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
                try:
                    self.log.insert('insert', str(i) + ' : ' + str(results[0]) + '\n')
                except IndexError:
                    self.log.insert('insert', str(i) + ": OpenNetwork\n")
            except subprocess.CalledProcessError:
                self.log.insert('insert', (i, "ENCODING ERROR"))
                input("")

    def print_SPEEDTEST(self):
        try:
            self.print_time()
            self.print_to_log('Trying to connect.')
            dir = join(current_dir, "src/speed.txt")
            if platform == 'win32':
              subprocess.call(["speedtest-cli",  ">",  join(current_dir, "src/speed.txt")], shell=True)
            elif platform == 'linux' or platform == 'linux2':
              subprocess.call('speedtest-cli > speed.txt', shell=True, cwd = join(current_dir, "src"))
            self.print_time()
            self.print_to_log('Speedtest ready.')
            try:
                with open(join(current_dir, 'src/speed.txt'), 'r') as s:
                    lines = [line.rstrip() for line in s]
                    self.print_time()
                    self.print_to_log(lines[-3].rstrip() + ' // ' + lines[-1].rstrip())
                os.remove(join(current_dir, "src/speed.txt"))
                self.show_isp(lines[1].split(" ")[2])
            except:
                self.print_time()
                self.print_to_log('Error, cannot print the results.')
        except:
            self.print_time()
            self.print_to_log('Error, cannot perform a Speedtest.')

if __name__ == "__main__":
    hostname = sc.gethostname()
    IP_address = sc.gethostbyname(hostname)

    root = tk.Tk()

    window = main_win(root)
    window.lcl_nw.insert('insert', str(window.find_nw_name()))
    root.mainloop()
