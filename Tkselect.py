from socket import *
from tkinter import *
from select import *
import time

root = Tk()
bin_color = 'red'
bin_text = 'ON'

LED_label = Label(text="LED")
switch_label = Label(text="SWITCH")
switch_state_label = Label(text="Switch is off ",fg='blue')
LED_button = Button(text=bin_text,fg='yellow', bg=bin_color, command=button_command)

LED_label.grid(row=0, column = 0)
LED_button.grid(row=0, column= 1)
switch_label.grid(row=1, column=0 )
switch_state_label.grid(row=1, column=1, sticky=E)

sock =socket()
sock.connect_(('localhost', 2500))
mainloop()

def button_command(bin_text=None):
    global sock, btn_text , btn_color
    if bin_text == 'ON':
        bin_text ="OFF"
        bin_color = 'blue'
    else:
        btn_text = "ON"
        btn_color = 'red'
    LED_button.configure(text=btn_text, bg=bin_color)
    sock.send(btn_text.encode())

def handle():
    global root, sock, switch_state_label, sock_list
    #root.mainloop()
    r_sock, w_sock, e_sock = select([sock],[],[],0)
    if r_sock:
        msg = sock.recv(1024).decode()
        print(msg)
        if msg.upper() == 'OFF':
            switch_state_label.configure(text="switch is off")
        else:
            switch_state_label.configure(text="switch is on")
        root.after(200, handle)