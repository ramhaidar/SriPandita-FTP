#!/usr/bin/env python
"""Client dari Program FTP"""
__author__ = "Haidaruddin Muhammad Ramdhan"
__copyright__ = "© SriPandita 2022"
__credits__ = ["GitHub",
               "VisualStudioCode",
               "https://github.com/justEhmadSaeed/Python-Sockets-File-Transfer"]
__license__ = "GNU General Public License v3.0"
__version__ = "0.0.1"
__maintainer__ = ["Muhammad Dimas Rifki Irianto",
                  "Ahmad Fasya Adila",
                  "Haidaruddin Muhammad Ramdhan",
                  "Muhammad Hiksal Daeng Jusuf Bauw"]
__email__ = "haidaruddinmuhammadr@gmail.com"
__status__ = "Production"

import socket
import hashlib
import time
import tkinter as tk
from tkinter import ttk
import tkinterDnD  # Importing the tkinterDnD module
import customtkinter
from PIL import Image


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


# Menampilkan Menu
def ShowClientMenu():
    # Opsi Menu
    menu_options = {
        1: 'Register',
        2: 'Login',
        3: 'Send File(s) to Server',
        4: 'Receive File from Server',
        5: 'Exit',
    }

    print("[-- FTP Client Menu --]")
    if LoginStatus:  # Menampilkan Username jika LoginStatus bernilai True
        print("> Username: ", MyUsername, "\n", sep="")
    else:  # Menampilkan Status jika LoginStatus bernilai False
        print("> Status: Belum Login", "\n", sep="")

    for key in menu_options.keys():
        print(key, '--', menu_options[key])


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
                # LoginRegister.destroy()
                root.withdraw()
                SecondMenu()
        finally:
            pass

    if RegisterMenu:
        RegisterMenu.destroy()

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

    LoginMenu_Label = customtkinter.CTkLabel(master=LoginMenu_Frame, text="Login", font=("Segoe UI", 24))
    LoginMenu_Label.pack(pady=12, padx=10)

    MyUsername = customtkinter.StringVar()
    LoginMenu_UsernameEntry = customtkinter.CTkEntry(master=LoginMenu_Frame, placeholder_text="Username")
    LoginMenu_UsernameEntry.pack(pady=12, padx=10)

    LoginMenu_PasswordEntry = customtkinter.CTkEntry(master=LoginMenu_Frame, placeholder_text="Login", show="*")
    LoginMenu_PasswordEntry.pack(pady=12, padx=10)

    LastDATA = "Silahkan Masukkan Username dan Password."
    LoginMenu_Status = customtkinter.CTkLabel(master=LoginMenu_Frame, text=LastDATA, font=("Segoe UI", 12))

    LoginMenu_LoginButton = customtkinter.CTkButton(master=LoginMenu_Frame, text="Login",
                                                    command=Login)
    LoginMenu_LoginButton.pack(pady=12, padx=10)

    LoginMenu_Status.pack(pady=12, padx=10)

    LoginMenu.protocol("WM_DELETE_WINDOW", LoginMenu.destroy)
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

    # [Start] Login Menu #
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

    RegisterMenu_Label = customtkinter.CTkLabel(master=RegisterMenu_Frame, text="Registrasi", font=("Segoe UI", 24))
    RegisterMenu_Label.pack(pady=12, padx=10)

    RegisterMenu_NewUsernameEntry = customtkinter.CTkEntry(master=RegisterMenu_Frame, placeholder_text="New Username")
    RegisterMenu_NewUsernameEntry.pack(pady=12, padx=10)

    RegisterMenu_NewPasswordEntry = customtkinter.CTkEntry(master=RegisterMenu_Frame, placeholder_text="New Password",
                                                           show="*")
    RegisterMenu_NewPasswordEntry.pack(pady=12, padx=10)

    RegisterMenu_PasswordCheckEntry = customtkinter.CTkEntry(master=RegisterMenu_Frame,
                                                             placeholder_text="New Passoword", show="*")
    RegisterMenu_PasswordCheckEntry.pack(pady=12, padx=10)

    LastDATA = "Silahkan Masukkan Username dan Password."
    RegisterMenu_Status = customtkinter.CTkLabel(master=RegisterMenu_Frame, text=LastDATA, font=("Segoe UI", 12))

    RegisterMenu_LoginButton = customtkinter.CTkButton(master=RegisterMenu_Frame, text="Register",
                                                       command=RegisterAndUpdate)
    RegisterMenu_LoginButton.pack(pady=12, padx=10)

    RegisterMenu_Status.pack(pady=12, padx=10)

    RegisterMenu.protocol("WM_DELETE_WINDOW", RegisterMenu.destroy)
    RegisterMenu.mainloop()
    # [End] Login Menu #


# Fungsi Untuk Mengkombinasi Fungsi
def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)

    return combined_func


def SecondMenu():
    if LoginStatus:
        # [Start] Main Menu #
        UploadDownload = customtkinter.CTkToplevel(root)
        UploadDownload.iconbitmap("SriPandita-FTP-icon.ico")
        UploadDownload.geometry("400x500")
        UploadDownload.maxsize(400, 500)
        UploadDownload.minsize(400, 500)
        UploadDownload.resizable(False, False)
        UploadDownload.wm_title("Yo Ndak Tau Kok Tanya Saya")

        UploadDownload_Frame = customtkinter.CTkFrame(master=UploadDownload)
        UploadDownload_Frame.pack(pady=20, padx=60, fill="both", expand=True)

        UploadDownload_YNTKTS_Image = customtkinter.CTkImage(light_image=Image.open("SriPandita FTP home.png"),
                                                             dark_image=Image.open("SriPandita FTP home.png"),
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
                                                             command=RegisterMenu_GUI)
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

        UploadDownload.mainloop()

        # [End] Main Menu #


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


# Main Program
if __name__ == '__main__':
    # Definisi SecretSeparator
    SecretSeparator = "!@#$%^&*"

    # Definisi LastDATA
    LastDATA = ""

    # Definisi LoginStatus dan Username
    LoginStatus = False
    MyUsername = ""

    # Mengubah Tema Warna CustomTKInter
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    # Membuat Reference LoginMenu dan RegisterMenu
    LoginMenu = None
    RegisterMenu = None

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
                                        dark_image=Image.open("SriPandita FTP home.png"),
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

    root.mainloop()

    # [End] Main Menu #
