import customtkinter as ctk
import modules.theme as theme

from socket import socket
from pathlib import Path
from PIL import Image
from math import floor
from base64 import b64encode

from modules.system_helper import get_home_path, path_divider
from modules.ctk_custom_helper import center_gui

class FileSystem(ctk.CTkToplevel):
    def __init__(self, width:int=400, height:int=200, resize:bool=False):
        super().__init__()
        ctk.set_appearance_mode('dark')
        self.list_of_sockets:list[dict[str,any]] = []
        self.current_keycode = None
        self.sql_ip_reference = []
        self.app_width = width
        self.app_height = height
        self.title("Choose a image: ")
        self.resizable(resize, resize)
        self.grab_set()
        center_gui(self, self.app_width, self.app_height)
        self.configure(fg_color=(theme.PRIMARY, theme.GRAY2))

        self.current_var_path = ctk.StringVar()
        self.current_var_path.set(get_home_path())
        CUSTOM_TEXTAREA_COLOR = (theme.WHITE, theme.GRAY2)
        top_frame = ctk.CTkFrame(self, 960, 32)
        self.textarea_path = ctk.CTkTextbox(top_frame,
                                            self.app_width*.82, 
                                            32,
                                            fg_color=CUSTOM_TEXTAREA_COLOR,
                                            border_width=0)
        self._set_disabled_textarea_value(self.textarea_path, 
                                         self.current_var_path.get())
        self.back_button = ctk.CTkButton(top_frame, 
                                         44, 
                                         32, 
                                         text='Back',
                                         command=lambda: self._update_items_from_current_dir(f"{self.current_var_path.get()[0:self.current_var_path.get().rfind(path_divider())]}"))
        top_frame.grid(padx=30, pady=5, ipady=8, sticky='')
        self.textarea_path.place(relx=0.44,rely=0.5,anchor=ctk.CENTER)
        self.back_button.place(relx=0.97,rely=0.5,anchor=ctk.CENTER)
        self.render_path_frame = ctk.CTkScrollableFrame(self, 
                                                        floor(self.app_width*0.9375), 
                                                        floor(self.app_height*.75),
                                                        fg_color=(CUSTOM_TEXTAREA_COLOR[0], theme.GRAY1))
        self.render_path_frame.place(relx=0.5, 
                                     rely=0.55, 
                                     anchor=ctk.CENTER)

        self._render_items_from_current_dir()

    def _set_essentials(self, list_of_sockets:list[dict[str,any]]=[], keycode=None, sql_ip_reference=[]):
        self.list_of_sockets = list_of_sockets
        self.current_keycode = keycode
        self.sql_ip_reference = sql_ip_reference

    def _set_disabled_textarea_value(self, textarea:ctk.CTkTextbox, value:str):
        new_value = f'C:{path_divider()}' if value == 'C:' else value
        textarea.configure(state=ctk.NORMAL)
        textarea.delete('0.0', ctk.END)
        textarea.insert("0.0", new_value)
        textarea.configure(state=ctk.DISABLED)
        self.current_var_path.set(new_value)

    def _update_items_from_current_dir(self, path:str):
        for children in self.render_path_frame.winfo_children():
            try:
                children.destroy()
            except:
                print("Update Error")
        self._set_disabled_textarea_value(self.textarea_path, path)
        self._render_items_from_current_dir()

    def _render_items_from_current_dir(self):
        BASE = 1
        relx = BASE
        rely = BASE*2
        DIVIDER = 7
        p = Path(self.current_var_path.get())
        last_path_divider = self.current_var_path.get().rfind(path_divider())
        self.back_button.configure(state= ctk.DISABLED if last_path_divider <= 2 and last_path_divider+1 == len(self.current_var_path.get()) else ctk.NORMAL )
        for entry in sorted(p.iterdir(), key=lambda cond:not cond.is_dir()):
            file_name = entry.as_posix()[entry.as_posix().rfind('/')+1:len(entry.as_posix())]
            file_command = None 
            dir_command = lambda path=f"{self.current_var_path.get()}{path_divider()}{entry.stem}": self._update_items_from_current_dir(path)
            if not entry.is_dir():
                if (file_name.rfind('.png') or 
                    file_name.rfind('.jpg') or 
                    file_name.rfind('.jpeg') or 
                    file_name.rfind('.gif') or 
                    file_name.rfind('.bmp')) == -1:
                    continue
                else:
                    with open(entry, 'rb') as f:
                        encoded = b64encode(f.read())
                    def base64_message(b:bytes):
                        try:
                            for clients in self.list_of_sockets:
                                client_socket:socket = clients["connection"][0]
                                if self.current_keycode == None:
                                    client_socket.send(b)
                                for address_info in self.sql_ip_reference:
                                    keyCode = address_info[1]
                                    ip_address = client_socket.getpeername()[0]
                                    if keyCode == self.current_keycode and ip_address == address_info[0]:
                                        client_socket.send(b)
                                
                        except ConnectionAbortedError as cae:
                            print(cae)
                        except RuntimeError as re:
                            print(re)
                    file_command = lambda e=encoded: [print(len(e)), base64_message(e), self.destroy()]

            CUSTOM_SIZE = (64,48)
            FOLDER_WIDTH = 120
            FOLDER_HEIGHT = 64
            folder_img_source = Image.open('./src/light_mode/folder.png')
            image_img_source = Image.open('./src/light_mode/image.png')
            folder_img_source.load()
            image_img_source.load()
            folderCTkImage = ctk.CTkImage(light_image=folder_img_source, size=CUSTOM_SIZE)
            imageCTkImage = ctk.CTkImage(light_image=image_img_source, size=CUSTOM_SIZE)
            canvas = ctk.CTkCanvas(self.render_path_frame, width=FOLDER_WIDTH-8, height=FOLDER_HEIGHT, bg=theme.GRAY1, bd=0)
            image_button = ctk.CTkButton(canvas, 
                              text="",
                              width=FOLDER_WIDTH,
                              height=FOLDER_HEIGHT*0.75,
                              fg_color='transparent',
                              hover_color=theme.GRAY1,
                              image=  folderCTkImage if entry.is_dir() else imageCTkImage,
                              command=dir_command if entry.is_dir() else file_command)
            text_button = ctk.CTkButton(canvas, 
                              text=entry.stem if entry.is_dir() else file_name,
                              width=FOLDER_WIDTH,
                              height=FOLDER_HEIGHT*0.25,
                              fg_color='transparent',
                              hover_color=theme.GRAY1,
                              command=dir_command if entry.is_dir() else file_command)
            canvas.create_window(0,0,anchor=ctk.NW,window=image_button)
            canvas.create_window(0,60,anchor=ctk.W,window=text_button)
            image_button.lower()
            canvas.grid(column=relx, row=rely, padx=5, pady= 5)
            if not BASE*DIVIDER == relx:
                relx += BASE
            else:
                relx = BASE
                rely += BASE
