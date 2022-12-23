#!/usr/bin/env python
"""Client dari Program FTP"""
__author__ = "Haidaruddin Muhammad Ramdhan"
__copyright__ = "© SriPandita 2022"
__credits__ = ["GitHub",
               "VisualStudioCode",
               "https://github.com/justEhmadSaeed/Python-Sockets-File-Transfer",
               "CustomTkinter: https://github.com/TomSchimansky/CustomTkinter",
               "Honest Abe: https://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter",
               "Olikonsti: https://gist.github.com/Olikonsti/879edbf69b801d8519bf25e804cec0aa"]
__license__ = "GNU General Public License v3.0"
__version__ = "0.0.1"
__maintainer__ = ["Muhammad Dimas Rifki Irianto",
                  "Ahmad Fasya Adila",
                  "Haidaruddin Muhammad Ramdhan",
                  "Muhammad Hiksal Daeng Jusuf Bauw"]
__email__ = "haidaruddinmuhammadr@gmail.com"
__status__ = "Production"

import os
import socket
import hashlib
import time
import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinterDnD  # Importing the tkinterDnD module
import customtkinter
from PIL import Image
import ctypes as ct


def SendFilesToServer():
    TCP_IP = '127.0.0.1'
    TCP_PORT = 48632
    BUFFER_SIZE = 1024

    Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Socket.connect((TCP_IP, TCP_PORT))

    file = open('MyFile.bin', 'rb')
    line = file.read(BUFFER_SIZE)

    while line:
        Socket.send(line)
        line = file.read(BUFFER_SIZE)

    file.close()
    print('File has been transferred successfully.')

    Socket.close()


# Fungsi Untuk Registrasi
def ClientRegister(NewUsername, NewPassword, PasswordCheck):
    # Mendefinisikan Variabel Global
    global SecretSeparator, LastDATA

    # Input Username
    # NewUsername = str(input("Masukkan Username: "))
    # Error Jika Username Kosong
    if len(NewUsername) == 0:
        LastDATA = "Username Tidak Boleh Kosong!"
        return  # Exit Function

    # Input Password
    # NewPassword = str(getpass("Masukkan Password Baru: "))
    # Error Jika Panjang Password Kurang dari 8 Karakter
    if len(NewPassword) < 8:
        LastDATA = "Password Harus Memiliki 8 Karakter atau Lebih!"
        return  # Exit Function

    # Input Password Untuk Konfirmasi
    # PasswordCheck = str(getpass("Masukkan Password Lagi: "))
    # Error Jika Kedua Input Password Tidak Sama
    if NewPassword != PasswordCheck:
        LastDATA = "Password tidak cocok!"
        return  # Exit Function

    # Convert Password ke MD5 Hash
    NewPassword = hashlib.md5(NewPassword.encode('utf-8')).hexdigest()

    # Mendifinisikan Koneksi Socket
    TCP_IP = '127.0.0.1'
    TCP_PORT = 48632
    BUFFER_SIZE = 1024
    HEADER = "REGISTER"
    RegistrationData = [NewUsername, NewPassword]
    SendThis = (HEADER + SecretSeparator + str(RegistrationData))

    # Melakukan Koneksi ke Server
    Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Socket.connect((TCP_IP, TCP_PORT))

    # Mengirim TheData Registrasi ke Server
    Socket.send(SendThis.encode())

    # Menerima RESPONSE dari Server
    RESPONSE = Socket.recv(BUFFER_SIZE).decode()
    RESPONSE = str(RESPONSE)
    HEADER, DATA = RESPONSE.split(SecretSeparator, 1)

    # Mengoutputkan Response dari Server
    # print(DATA, sep="")

    # Menutup Koneksi Socket
    Socket.close()

    # Clearing Variables
    try:
        LastDATA = DATA
    finally:
        del NewUsername, NewPassword, PasswordCheck, TCP_IP, TCP_PORT, BUFFER_SIZE, \
            HEADER, RegistrationData, SendThis, Socket, RESPONSE, DATA


# Fungsi Untuk Login
def ClientLogin(Username, Password):
    # Mendefinisikan Variabel Global
    global SecretSeparator, LoginStatus, MyUsername, LastDATA, LoginMenu, RegisterMenu, root

    # Convert Password ke MD5 Hash
    Password = hashlib.md5(Password.encode('utf-8')).hexdigest()

    # Mendifinisikan Koneksi Socket
    TCP_IP = '127.0.0.1'
    TCP_PORT = 48632
    BUFFER_SIZE = 1024
    HEADER = "LOGIN"
    LoginData = [Username, Password]
    SendThis = (HEADER + SecretSeparator + str(LoginData))

    # Melakukan Koneksi ke Server
    Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Socket.connect((TCP_IP, TCP_PORT))

    # Mengirim TheData Registrasi ke Server
    Socket.send(SendThis.encode())

    # Menerima RESPONSE dari Server
    RESPONSE = Socket.recv(BUFFER_SIZE).decode()
    RESPONSE = str(RESPONSE)
    HEADER, DATA = RESPONSE.split(SecretSeparator, 1)

    # Mengubah LoginStatus Sesuai RESPONSE dari Server
    global LoginStatus
    # global Username
    if HEADER == "LOGIN_SUCCES":
        LoginStatus = True
        MyUsername = Username
    if HEADER == "LOGIN_FAILED":
        LoginStatus = False

    # Mengoutputkan Response dari Server
    # print(DATA, sep="")

    # Menutup Koneksi Socket
    Socket.close()

    try:
        LastDATA = DATA
    finally:
        del Username, Password, TCP_IP, TCP_PORT, BUFFER_SIZE, HEADER, \
            LoginData, SendThis, Socket, RESPONSE, DATA


def LoginMenu_GUI():
    # Mendefinisikan Variabel Global
    global MyUsername, LastDATA, LoginMenu, RegisterMenu

    def Login():
        try:
            ClientLogin(
                LoginMenu_UsernameEntry.get(),
                LoginMenu_PasswordEntry.get()
            )
            LoginMenu_Status.configure(
                text=LastDATA,
                font=("Segoe UI", 12),
            )
            if MyUsername != "":
                LoginMenu.destroy()
                root.withdraw()
                SecondMenu_GUI()
        finally:
            pass

    if RegisterMenu:
        RegisterMenu.destroy()
    if LoginMenu:
        LoginMenu.destroy()

    # [Start] Login Menu #
    LoginMenu = customtkinter.CTkToplevel(root)
    LoginMenu.transient(root)
    LoginMenu.iconbitmap("SriPandita-FTP-icon.ico")
    LoginMenu.geometry("400x350")
    LoginMenu.maxsize(400, 350)
    LoginMenu.minsize(400, 350)
    LoginMenu.resizable(False, False)
    LoginMenu.wm_title("")

    LoginMenu_Frame = customtkinter.CTkFrame(master=LoginMenu)
    LoginMenu_Frame.pack(pady=20, padx=60, fill="both", expand=True)

    LoginMenu_Label = customtkinter.CTkLabel(
        master=LoginMenu_Frame, text="Login", font=("Segoe UI", 24))
    LoginMenu_Label.pack(pady=12, padx=10)

    LoginMenu_UsernameEntry = customtkinter.CTkEntry(
        master=LoginMenu_Frame, placeholder_text="Username")
    LoginMenu_UsernameEntry.pack(pady=12, padx=10)

    LoginMenu_PasswordEntry = customtkinter.CTkEntry(
        master=LoginMenu_Frame, placeholder_text="Login", show="*")
    LoginMenu_PasswordEntry.pack(pady=12, padx=10)

    LastDATA = "Silahkan Masukkan Username dan Password."
    LoginMenu_Status = customtkinter.CTkLabel(
        master=LoginMenu_Frame, text=LastDATA, font=("Segoe UI", 12))

    LoginMenu_LoginButton = customtkinter.CTkButton(master=LoginMenu_Frame, text="Login",
                                                    command=Login)
    LoginMenu_LoginButton.pack(pady=12, padx=10)

    LoginMenu_Status.pack(pady=12, padx=10)

    LoginMenu.protocol("WM_DELETE_WINDOW", LoginMenu.destroy)

    CenterMyWindow(LoginMenu)
    LoginMenu.mainloop()
    # [End] Login Menu #


def RegisterMenu_GUI():
    # Mendefinisikan Variabel Global
    global LastDATA, LoginMenu, RegisterMenu

    def RegisterAndUpdate():
        try:
            ClientRegister(
                RegisterMenu_NewUsernameEntry.get(),
                RegisterMenu_NewPasswordEntry.get(),
                RegisterMenu_PasswordCheckEntry,
            )
            RegisterMenu_Status.configure(
                text=LastDATA,
                font=("Segoe UI", 12),
            )
        finally:
            pass

    if LoginMenu:
        LoginMenu.destroy()
    if RegisterMenu:
        RegisterMenu.destroy()

    # [Start] Register Menu #
    RegisterMenu = customtkinter.CTkToplevel(root)
    RegisterMenu.transient(root)
    RegisterMenu.iconbitmap("SriPandita-FTP-icon.ico")
    RegisterMenu.geometry("400x350")
    RegisterMenu.maxsize(400, 350)
    RegisterMenu.minsize(400, 350)
    RegisterMenu.resizable(False, False)
    RegisterMenu.wm_title("")

    RegisterMenu_Frame = customtkinter.CTkFrame(master=RegisterMenu)
    RegisterMenu_Frame.pack(pady=20, padx=60, fill="both", expand=True)

    RegisterMenu_Label = customtkinter.CTkLabel(
        master=RegisterMenu_Frame, text="Register", font=("Segoe UI", 24))
    RegisterMenu_Label.pack(pady=12, padx=10)

    RegisterMenu_NewUsernameEntry = customtkinter.CTkEntry(
        master=RegisterMenu_Frame, placeholder_text="New Username")
    RegisterMenu_NewUsernameEntry.pack(pady=12, padx=10)

    RegisterMenu_NewPasswordEntry = customtkinter.CTkEntry(master=RegisterMenu_Frame, placeholder_text="New Password",
                                                           show="*")
    RegisterMenu_NewPasswordEntry.pack(pady=12, padx=10)

    RegisterMenu_PasswordCheckEntry = customtkinter.CTkEntry(master=RegisterMenu_Frame,
                                                             placeholder_text="New Passoword", show="*")
    RegisterMenu_PasswordCheckEntry.pack(pady=12, padx=10)

    LastDATA = "Silahkan Masukkan Username dan Password."
    RegisterMenu_Status = customtkinter.CTkLabel(
        master=RegisterMenu_Frame, text=LastDATA, font=("Segoe UI", 12))

    RegisterMenu_LoginButton = customtkinter.CTkButton(master=RegisterMenu_Frame, text="Register",
                                                       command=RegisterAndUpdate)
    RegisterMenu_LoginButton.pack(pady=12, padx=10)

    RegisterMenu_Status.pack(pady=12, padx=10)

    RegisterMenu.protocol("WM_DELETE_WINDOW", RegisterMenu.destroy)

    CenterMyWindow(RegisterMenu)
    RegisterMenu.mainloop()
    # [End] Login Menu #


# Fungsi Untuk Mengkombinasi Fungsi
def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)

    return combined_func


def SecondMenu_GUI():
    if LoginStatus:
        # [Start] Main Menu #
        UploadDownload = customtkinter.CTkToplevel(root)
        UploadDownload.iconbitmap("SriPandita-FTP-icon.ico")
        UploadDownload.geometry("400x500")
        UploadDownload.maxsize(400, 500)
        UploadDownload.minsize(400, 500)
        UploadDownload.resizable(False, False)
        UploadDownload.wm_title("Main Menu")

        UploadDownload_Frame = customtkinter.CTkFrame(master=UploadDownload)
        UploadDownload_Frame.pack(pady=20, padx=60, fill="both", expand=True)

        UploadDownload_YNTKTS_Image = customtkinter.CTkImage(light_image=Image.open("SriPandita FTP home.png"),
                                                             dark_image=Image.open(
                                                                 "SriPandita FTP home.png"),
                                                             size=(200, 150))
        UploadDownload_YNTKTS = customtkinter.CTkButton(master=UploadDownload_Frame, image=UploadDownload_YNTKTS_Image,
                                                        text="", border_width=0, corner_radius=0,
                                                        fg_color="transparent",
                                                        state="disabled")
        UploadDownload_YNTKTS.pack(pady=12, padx=10)

        SecondMenuHeader = ("Username: " + MyUsername)
        UploadDownload_Label = customtkinter.CTkLabel(master=UploadDownload_Frame, text=SecondMenuHeader,
                                                      font=("Segoe UI", 18))
        UploadDownload_Label.pack(pady=12, padx=25)

        UploadDownload_UploadFiles = customtkinter.CTkButton(master=UploadDownload_Frame, text="Upload Files",
                                                             command=ShowUploadMenu)
        UploadDownload_UploadFiles.pack(pady=12, padx=10)

        UploadDownload_DownloadFiles = customtkinter.CTkButton(master=UploadDownload_Frame, text="Download Files",
                                                               command=LoginMenu_GUI)
        UploadDownload_DownloadFiles.pack(pady=12, padx=10)

        UploadDownload_SeeFiles = customtkinter.CTkButton(master=UploadDownload_Frame, text="Files List",
                                                          command=LoginMenu_GUI)
        UploadDownload_SeeFiles.pack(pady=12, padx=10)

        UploadDownload_Quit = customtkinter.CTkButton(master=UploadDownload_Frame, text="LogOut and Exit",
                                                      command=FullExitClient)
        UploadDownload_Quit.pack(pady=12, padx=10)

        UploadDownload.protocol("WM_DELETE_WINDOW", FullExitClient)

        CenterMyWindow(UploadDownload)
        UploadDownload.mainloop()

        # [End] Main Menu #


def ShowUploadMenu():
    global UploadMenu

    UploadFolder = ("Upload Here")

    def OpenTheUploadDirectory():
        OpenDirectory(UploadFolder)

    def RefreshLists():
        UploadMenu_ListBox.delete(0, END)
        ListsOnUploadFolder = os.listdir(UploadFolder)
        ListsOnUploadFolder = [f for f in os.listdir(
            UploadFolder) if os.path.isfile(os.path.join(UploadFolder, f))]
        UploadMenu_ListBox.delete(0, END)
        for i in ListsOnUploadFolder:
            UploadMenu_ListBox.insert(END, i)

    def UploadSelected():
        for i in UploadMenu_ListBox.curselection():
            print(UploadMenu_ListBox.get(i))

    if UploadMenu:
        UploadMenu.destroy()

    if not os.path.exists(UploadFolder):
        os.mkdir(UploadFolder)

    UploadMenu = customtkinter.CTkToplevel(UploadDownload)
    UploadMenu.transient(UploadDownload)
    UploadMenu.attributes('-topmost', True)
    UploadMenu.iconbitmap("SriPandita-FTP-icon.ico")
    UploadMenu.geometry("400x430")
    UploadMenu.maxsize(400, 430)
    UploadMenu.minsize(400, 430)
    UploadMenu.resizable(False, False)
    UploadMenu.wm_title("Upload Files")
    UploadMenu.config(bg="#1a1a1a")

    s = ttk.Style()
    s.configure("TFrame", bg="#212121")
    s.configure('Mine.TFrame', background='#212121')

    UploadMenu_Frame = customtkinter.CTkFrame(UploadMenu)
    UploadMenu_Frame.pack(pady=20, padx=60, fill="both", expand=True)

    UploadMenu_SideBySideButton_Frame = customtkinter.CTkFrame(
        UploadMenu_Frame)
    UploadMenu_SideBySideButton_Frame.pack(side=TOP)

    UploadMenu_OpenDirectory = customtkinter.CTkButton(
        master=UploadMenu_Frame, text="Open Directory", command=OpenTheUploadDirectory)
    UploadMenu_OpenDirectory.pack(
        pady=12, padx=10, expand=True, in_=UploadMenu_SideBySideButton_Frame, side=LEFT)

    UploadMenu_Refresh = customtkinter.CTkButton(
        master=UploadMenu_Frame, text="Refresh", command=RefreshLists)
    UploadMenu_Refresh.pack(pady=12, padx=10, expand=True,
                            in_=UploadMenu_SideBySideButton_Frame, side=LEFT)

    UploadMenu_ListBox_Frame = customtkinter.CTkFrame(UploadMenu_Frame)
    UploadMenu_ListBox_Frame.pack(pady=12, padx=10, fill="both", expand=True)

    UploadMenu_ListBox_ScrollBar = customtkinter.CTkScrollbar(
        UploadMenu_ListBox_Frame, width=15)

    UploadMenu_ListBox = tk.Listbox(
        UploadMenu_ListBox_Frame, bg="#212121", fg="white", selectbackground="#1f538d", width=30, height=15, selectmode=SINGLE)
    RefreshLists()
    UploadMenu_ListBox.config(yscrollcommand=UploadMenu_ListBox_ScrollBar.set)
    UploadMenu_ListBox.pack(pady=12, padx=(12, 0), side=LEFT,
                            fill="both", expand=True)

    UploadMenu_ListBox_ScrollBar.configure(command=UploadMenu_ListBox.yview)
    UploadMenu_ListBox_ScrollBar.pack(
        padx=(0, 12), pady=12, side=RIGHT, fill='y')

    UploadMenu_UploadFilesButton_Frame = customtkinter.CTkFrame(
        UploadMenu_Frame)
    UploadMenu_UploadFilesButton_Frame.pack(
        side=BOTTOM, fill='both', expand=True)

    UploadMenu_UploadFiles = customtkinter.CTkButton(
        master=UploadMenu_UploadFilesButton_Frame, text="Upload Now", command=UploadSelected)
    UploadMenu_UploadFiles.pack(
        pady=12, padx=10, fill='both', expand=True)

    UploadMenu.protocol("WM_DELETE_WINDOW", UploadMenu.destroy)

    DarkMyWindowTitleBar(UploadMenu)
    CenterMyWindow(UploadMenu)
    UploadMenu.mainloop()


def OpenDirectory(openThis):
    path = openThis
    path = os.path.realpath(path)
    os.startfile(path)


def FullExitClient():
    try:
        root.destroy()
        LoginMenu.destroy()
        RegisterMenu.destroy()
        UploadDownload.destroy()
    except:
        pass
    finally:
        exit()


def CenterMyWindow(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


def DarkMyWindowTitleBar(window):
    """
    MORE INFO:
    https://docs.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
    """
    window.update()
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 2
    value = ct.c_int(value)
    set_window_attribute(hwnd, rendering_policy,
                         ct.byref(value), ct.sizeof(value))


# Main Program
if __name__ == '__main__':
    # Definisi SecretSeparator
    SecretSeparator = "!@#$%^&*"

    # Definisi LastDATA
    LastDATA = ""

    # Definisi LoginStatus dan Username
    LoginStatus = False
    MyUsername = ''

    # Mengubah Tema Warna CustomTKInter
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    # Membuat Reference LoginMenu dan RegisterMenu
    LoginMenu = None
    RegisterMenu = None
    UploadDownload = None
    UploadMenu = None

    # [Start] Main Menu #
    root = customtkinter.CTk()
    root.iconbitmap("SriPandita-FTP-icon.ico")
    root.geometry("400x350")
    root.maxsize(400, 350)
    root.minsize(400, 350)
    root.resizable(False, False)
    root.wm_title("Yo Ndak Tau Kok Tanya Saya")

    root_Frame = customtkinter.CTkFrame(master=root)
    root_Frame.pack(pady=20, padx=60, fill="both", expand=True)

    # LoginRegister_Label = customtkinter.CTkLabel(master=LoginRegister_Frame, text="SriPandita FTP Client",
    #                                              font=("Segoe UI", 24))
    # LoginRegister_Label.pack(pady=12, padx=25)

    root_Image = customtkinter.CTkImage(light_image=Image.open("SriPandita FTP home.png"),
                                        dark_image=Image.open(
                                            "SriPandita FTP home.png"),
                                        size=(200, 150))
    root_ButtonImage = customtkinter.CTkButton(master=root_Frame, image=root_Image,
                                               text="", border_width=0, corner_radius=0, fg_color="transparent",
                                               state="disabled")
    root_ButtonImage.pack(pady=12, padx=10)

    root_RegisterButton = customtkinter.CTkButton(master=root_Frame, text="Register",
                                                  command=RegisterMenu_GUI)
    root_RegisterButton.pack(pady=12, padx=10)

    root_LoginButton = customtkinter.CTkButton(master=root_Frame, text="Login",
                                               command=LoginMenu_GUI)
    root_LoginButton.pack(pady=12, padx=10)

    root.protocol("WM_DELETE_WINDOW", root.destroy)

    CenterMyWindow(root)
    root.mainloop()

    # [End] Main Menu #
