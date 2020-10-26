import socket as sc
import tkinter as tk
import tkinter.scrolledtext as scr
import pyperclip
import subprocess
import datetime
from os.path import pardir, abspath, join, dirname
from time import gmtime, strftime

""" v0.2.1 """

global hostname, IP_address

current_dir = abspath(join(dirname(__file__), pardir))
image_path = join(current_dir, "img/net.png")

class main_win():
    def __init__(self, master):
        self.master = master
        self.master.option_add("*Font", 'arial 10')
        self.master.title('Net Manager 0.2 Alpha')
        self.master = master
        self.master.configure(background = 'white')
        self.master.resizable(False, False)
        self.masterback = tk.Frame(height = 300, width = 500)
        self.masterback.pack()
        self.masterback.configure(background = 'white')
         
        self.Message = tk.Label(master, text='Welcome to Net Manager 0.2 Alpha Build - Exclusive Alpha Access.')
        self.Message.place(relx= 0.5, rely = 0.105, anchor = 'center')
        self.Message.configure(background = 'white')
 
        self.show_ip = tk.Button(master, text = 'Show host IP address', command = self.print_ip)
        self.show_ip.place(relx= 0.62, rely = 0.575)
        self.show_ip.configure(background = 'white')
                        
        self.ip_entry = tk.Entry(master)
        self.ip_entry.place(relx = 0.1, rely = 0.6)
        self.ip_entry.configure(background = 'white')
        
        var = tk.StringVar()
        var.set('Crnt NW Name: ' + self.find_nw_name())
        self.lbl_lcl_nw = tk.Label(master, textvariable = var, bg = 'white')
        self.lbl_lcl_nw.place(relx = 0.1, rely = 0.3)
        self.lbl_lcl_nw.configure(background = 'white')

        self.lcl_nw = tk.Entry(master)
        self.lcl_nw.place(relx = 0.1, rely = 0.4)
        self.lcl_nw.configure(background = 'white')

        self.show_hostname = tk.Button(master, text = 'Show hostname', command = self.print_hn)
        self.show_hostname.place(relx= 0.62, rely = 0.475)
        self.show_hostname.configure(background = 'white')
        
        self.show_wifi_password = tk.Button(master, text = 'Show Wifi password', command = self.find_wifi_password)
        self.show_wifi_password.place(relx= 0.62, rely = 0.375)
        self.show_wifi_password.configure(background = 'white')
                        
        self.hostname_entry = tk.Entry(master)
        self.hostname_entry.place(relx = 0.1, rely = 0.5)
        self.hostname_entry.configure(background = 'white')
        
        img = tk.PhotoImage(file = image_path)
        self.master.label= tk.Label(self.master, image = img)
        self.master.label.image = img
        self.master.label.place(relx = 0.08, rely= 0.175, anchor="s")
        self.master.label.configure(background = 'white')

        self.log_label = tk.Label(self.master, bg = 'white', text = 'Action log:')
        self.log_label.place(rely = 0.69, relx = 0.02)
        self.log_frame = tk.Frame(master, bg = 'white')
        self.log_frame.pack(fill = 'both', expand = 'yes')
        self.log = scr.ScrolledText(
            master = self.log_frame,
            wrap = 'word',
            width = 75,
            height = 5
        )
        self.log.pack(padx = 10, pady = 10, fill = 'both', expand = 'True')
        self.log.insert('insert', 'Your network: ' + self.find_nw_name() + '\n')

    def print_hn(self):
        self.hostname_entry.delete(0, 'end')
        self.hostname_entry.insert(0, hostname)
        
    def print_ip(self):
        self.ip_entry.delete(0, 'end')
        self.ip_entry.insert(0, IP_address)
        
        self.copy_ip()
        self.print_time()
        self.print_to_log()

    def find_nw_name(self):
        self.nw_str = (str(subprocess.check_output('netsh wlan show interfaces')))
        self.nw_lst = self.nw_str.split()
        idx = self.nw_lst.index('SSID')
        idx += 2
        return self.nw_lst[idx][:-4]
    
    def copy_ip(self):
        pyperclip.copy(self.ip_entry.get())
        spam = pyperclip.paste()

    def print_to_log(self):
        self.log.insert('insert', 'Shown ' + hostname +'\'s IP address and copied it to clipboard.' + '\n')

    def print_time (self):
        self.log.insert('insert', str(strftime('%Y.%m.%d, %H:%M:%S', gmtime())) + ' // ')

    def find_wifi_password(self):
        self.print_time()
        self.log.insert('insert', ' Shown network ID\'s and passphrases.\ns')
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

if __name__ == "__main__":
    hostname = sc.gethostname()
    IP_address = sc.gethostbyname(hostname)

    root = tk.Tk()

    window = main_win(root)
    window.lcl_nw.insert('insert', str(window.find_nw_name()))
    root.mainloop()