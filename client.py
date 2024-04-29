import tkinter as tk
import customtkinter as ctk
import socket
import ast
import logging
import traceback
import time
import playsound
import threading

from tkinter import ttk
from os import path
from multiprocessing import Process
from getIp import getIPv4Addr

HOST = '10.0.103.13'
PORT = 65432
RECONNECTION_DELAY = 5

is_terminated = False
localIp = getIPv4Addr()
dirPath = path.dirname(path.realpath(__file__))
ctk.set_default_color_theme("./src/ace.json")

class Client(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.width = 280
        self.height = 500
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 3

        self.geometry(f"{self.width}x{self.height}+{x}+{y}")
        # self.iconbitmap("./src/ace-logo.ico")

        self.option_variable = ctk.StringVar()
        self.option_label = ctk.CTkLabel(self, text="Choose your department:", font=ctk.CTkFont(size=16, weight="bold"))
        self.option_label.place(relx=0.5, rely=0.35, anchor=ctk.CENTER)
        self.option_menu = ctk.CTkOptionMenu(
            self,
            command=self.get_option_menu_value,
            variable=self.option_variable,
            state=ctk.DISABLED
        )
        self.option_menu.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self.confirm_btn = ctk.CTkButton(self, 
            text="confirm", 
            command=self.confirm_pressed, 
            border_width=1,
            state=ctk.DISABLED
        )
        self.confirm_btn.place(relx=0.5, rely=0.65, anchor=ctk.CENTER)
    
    def connect_to_server(self):
        global is_terminated
        while not is_terminated:
            try:
                self.client_socket.connect((HOST, PORT))
                self.connected = True
                print("Connected to server")
                self.receive_messages()
            except Exception as e:
                msg = f"Connection to server failed: {e}"
                self.exception_message(msg)

    def exception_message(self, message:str):
        print(message)
        self.connected = False
        self.reconnect()

    def reconnect(self):
        print("Attempting to reconnect...")

        self.option_variable.set("Reconnecting...")
        while not self.connected:
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((HOST, PORT))
                self.connected = True
                print("Reconnected to server")
                self.receive_messages()
            except Exception as e:
                print(f"Reconnection failed: {e}")
                time.sleep(RECONNECTION_DELAY)

    def alert(self):
        sound_thread = Process(target=playsound.playsound, args=('./src/carmen-bizet.mp3',), daemon=True)
        return sound_thread

    def popup_message(self, msg:str):
        self.popup = ctk.CTkToplevel(self)
        self.popup.wm_title(self.title_value)
        sound_alert = self.alert()
        sound_alert.start()

        self.style = ttk.Style()
        self.style.configure("Popup.TLabel", font=("Arial", 12), foreground="black", background="lightgrey", padding=10)

        self.text = tk.Text(self.popup, wrap="word", font=("Arial", 12))
        self.text.insert(tk.END, msg)
        
        # # Check for special formatting requests from the server
        if 'bold' in msg:
            self.text.tag_configure("bold", font=("Arial", 12, "bold"))
            self.text.tag_add("bold", "1.0", "end")
        if 'italic' in msg:
            self.text.tag_configure("italic", font=("Arial", 12, "italic"))
            self.text.tag_add("italic", "1.0", "end")
        if 'underline' in msg:
            self.text.tag_configure("underline", underline=True)
            self.text.tag_add("underline", "1.0", "end")
        if 'color' in msg:
            self.text.tag_configure("color", foreground="red")
            self.text.tag_add("color", "1.0", "end")
        
        self.text.configure(state="disabled")
        self.text.pack(padx=10, pady=5, expand=True, fill="both")
        
        self.button = ctk.CTkButton(self.popup, text="OK", command=lambda: [self.popup.destroy(), self.destroy_sound_alert(sound_alert)])
        self.button.pack(pady=10)

        # Center the popup window
        self.popup.update_idletasks()
        width = self.popup.winfo_width()
        height = self.popup.winfo_height()
        x = (self.popup.winfo_screenwidth() // 2) - (width // 2)
        y = (self.popup.winfo_screenheight() // 3) - (height // 3)
        self.popup.geometry(f"{width}x{height}+{x}+{y}")
        # self.popup.iconbitmap("./src/ace-logo.ico")
        self.popup.grab_set()
        self.popup.focus_set()
        
        self.popup.mainloop()

    def destroy_sound_alert(self, sound_thread:Process):
        sound_thread.terminate()

    def get_option_menu_value(self, department):
        print(department)
        
    def receive_messages(self):
        index = 0
        while True:
            try:
                debug = self.client_socket.recv(2048)
                msg = debug.decode("utf-8")

                print(debug)

                if not msg:
                    return None
                if index == 0: # Departments sent from the Server
                    init_value = ast.literal_eval(msg)
                    departments:list = init_value[0]
                    button_state:str = init_value[1]
                    self.initialize_dropdown(departments)
                    self.disable_inputs(button_state)
                    
                if msg and index > 0:
                    self.popup_message(msg)
                else:
                    print('No message received:', index)
            except Exception as e:
                msg = f"Error receiving data: {e}"
                self.exception_message(msg)
            index += 1

    def send_messages(self, msg:str):
        try:
            self.client_socket.sendall(msg.encode())
        except Exception as e:
                logging.error(traceback.format_exc())
                print(f'Error in Send Message: {e}')

    def confirm_pressed(self):
        self.confirmation_window()

    def confirmed_button_pressed(self):
        self.disable_inputs(self.option_variable.get())
        self.send_messages(self.option_variable.get())

    def confirmation_window(self):
        popup = ctk.CTkToplevel(self)
        confirm_button = ctk.CTkButton(popup, text="Confirm", command=lambda:[self.confirmed_button_pressed(), popup.destroy()])
        decline_button = ctk.CTkButton(popup, text="Decline", command=lambda:popup.destroy())
        confirm_button.pack()
        decline_button.pack()
        popup.mainloop()

    def disable_inputs(self, button_state:str):
        print(button_state)
        boolean = button_state.lower() != "false"
        state = ctk.DISABLED if boolean else ctk.ACTIVE
        self.confirm_btn.configure(state=state)
        self.option_menu.configure(state=state)
        if boolean:
            self.option_variable.set(value=button_state)
            self.title(button_state.upper())
            self.title_value=button_state.upper()

    def initialize_dropdown(self, departments):
        self.option_menu._dropdown_menu.delete(0, 'end')
        self.option_variable.set(departments[0][1])
        for choice in departments:
            self.option_menu._dropdown_menu.add_command(
                label=choice[1],
                command=tk._setit(self.option_variable, choice[1], self.get_option_menu_value)
            )

def on_frame_destroy(event):
    print(f"destroyed {event}")

def main():
    global is_terminated
    client = Client()
    client_thread = threading.Thread(target=client.connect_to_server)
    client_thread.start()
    client.deiconify()
    # client.bind("<Destroy>", on_frame_destroy)
    client.mainloop()
    is_terminated = True


if __name__ == "__main__":
    main()  