#!/usr/bin/env python
"""Client dari Program FTP SriPandita"""
__author__ = "Haidaruddin Muhammad Ramdhan"
__copyright__ = "© SriPandita 2022"
__credits__ = [
    "GitHub",
    "VisualStudioCode",
    "Ehmad Saeed: https://github.com/justEhmadSaeed/Python-Sockets-File-Transfer",
    "Tom Schimansky: https://github.com/TomSchimansky/CustomTkinter",
    "Honest Abe: https://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter",
    "Olikonsti: https://gist.github.com/Olikonsti/879edbf69b801d8519bf25e804cec0aa",
]
__license__ = "GNU General Public License v3.0"
__version__ = "0.1.2"
__maintainer__ = [
    {"Muhammad Dimas Rifki Irianto": "1301204112"},
    {"Ahmad Fasya Adila": "1301204231"},
    {"Haidaruddin Muhammad Ramdhan": "1301204459"},
    {"Muhammad Hiksal Daeng Jusuf Bauw": "1301204416"},
]
__email__ = [
    "dimasrfq@student.telkomuniversity.ac.id",
    "ahmadfasya@student.telkomuniversity.ac.id",
    "haidarx@student.telkomuniversity.ac.id",
    "hiksal@student.telkomuniversity.ac.id",
]
__status__ = "Release"


import ast
import ctypes
import hashlib
import logging
import os
import socket
import tempfile
import threading
import tkinter as tk
from datetime import datetime
from sys import exit
from time import sleep
from tkinter import *
from typing import Union

import customtkinter
import PIL.Image
import requests

MessageBoxW = ctypes.windll.user32.MessageBoxW

try:
    import pyi_splash
except:
    pass
finally:
    pass


def GetDownloadUploadCount(Username: str):
    """Meminta statistik upload dan download milik user dari server.

    Args:
        Username (str): Username yang akan diminta statistik download dan uploadnya.
    """
    global DownloadCount, UploadCount

    TCP_IP, TCP_PORT = ServerAddress, ServerPort

    HEADER = "CLIENT_REQUEST_STATS"
    Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Socket.connect((TCP_IP, TCP_PORT))
    SendThis = str(HEADER + SecretSeparator + Username)
    Socket.send(SendThis.encode())

    # * Logger
    now = datetime.now()
    print(f"[{now}] [Out: {SendThis.split(SecretSeparator)[0]}]")
    logging.info(f"[{now}] [Out: {SendThis.split(SecretSeparator)[0]}]")

    RESPONSE = str(Socket.recv(BUFFER_SIZE).decode())

    # * Logger
    now = datetime.now()
    print(f"[{now}] [In : {RESPONSE.split(SecretSeparator)[0]}]")
    logging.info(f"[{now}] [In : {RESPONSE.split(SecretSeparator)[0]}]")

    HEADER, DATA = RESPONSE.split(SecretSeparator, 1)

    if HEADER == "SERVER_SENDING_STATS":
        DATA = ast.literal_eval(DATA)

    DownloadCount = DATA[0]
    UploadCount = DATA[1]

    Socket.close()


def SendFileToServer(FileName: str):
    """Mengirim file ke server.

    Args:
        FileName (str): Nama file yang dikirim.
    """
    global LastDATA

    TCP_IP, TCP_PORT = ServerAddress, ServerPort

    Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Socket.connect((TCP_IP, TCP_PORT))

    HEADER = "CLIENT_REQUEST_UPLOAD"
    SendThis = str(HEADER + SecretSeparator + FileName + SecretSeparator + MyUsername)
    Socket.send(str(SendThis).encode())

    # * Logger
    now = datetime.now()
    print(f"[{now}] [Out: {SendThis.split(SecretSeparator)[0]}]")
    logging.info(f"[{now}] [Out: {SendThis.split(SecretSeparator)[0]}]")

    RESPONSE = Socket.recv(BUFFER_SIZE).decode()

    # * Logger
    now = datetime.now()
    print(f"[{now}] [In : {RESPONSE.split(SecretSeparator)[0]}]")
    logging.info(f"[{now}] [In : {RESPONSE.split(SecretSeparator)[0]}]")

    HEADER = str(RESPONSE).split(SecretSeparator, 1)[0]
    if HEADER != "SERVER_RECEIVE_READY":
        return

    FullPath = "Upload Here\\" + FileName
    File = open(FullPath, "rb")
    Line = File.read(BUFFER_SIZE)

    while Line:
        Socket.send(Line)
        Line = File.read(BUFFER_SIZE)

    DONE = bytes(SecretSeparator, "utf-8")
    Socket.send(DONE)

    File.close()

    RESPONSE = str(Socket.recv(BUFFER_SIZE).decode())

    # * Logger
    now = datetime.now()
    print(f"[{now}] [In : {RESPONSE.split(SecretSeparator)[0]}]")
    logging.info(f"[{now}] [In : {RESPONSE.split(SecretSeparator)[0]}]")

    HEADER, DATA = RESPONSE.split(SecretSeparator, 1)

    threading.Thread(
        target=ResetMessage, args=("Pilih File Untuk di Upload Ke Server.",)
    ).start()
    LastDATA = DATA


def ResetMessage(OldLastDATA: str):
    """Mereset pesan error menjadi pesan sebelumnya.

    Args:
        OldLastDATA (str): Pesan lama yang akan dikembalikan.
    """
    global LastDATA, DownloadMenu_DownloadFiles_Label, UploadMenu_UploadFiles_Label
    global LoginMenu_Status, RegisterMenu_Status

    sleep(3)
    LastDATA = OldLastDATA
    try:
        DownloadMenu_DownloadFiles_Label.configure(
            text=LastDATA,
            font=("Segoe UI", 12),
        )
    except:
        pass

    try:
        UploadMenu_UploadFiles_Label.configure(
            text=LastDATA,
            font=("Segoe UI", 12),
        )
    except:
        pass

    try:
        LoginMenu_Status.configure(
            text=LastDATA,
            font=("Segoe UI", 12),
        )
    except:
        pass

    try:
        RegisterMenu_Status.configure(
            text=LastDATA,
            font=("Segoe UI", 12),
        )
    except:
        pass


def GetFileFromServer(FileName: str):
    """Mengunduh file dari server.

    Args:
        FileName (str): Nama file yang di download.
    """
    global LastDATA

    TCP_IP, TCP_PORT = ServerAddress, ServerPort

    Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Socket.connect((TCP_IP, TCP_PORT))

    HEADER = "CLIENT_REQUEST_DOWNLOAD"
    SendThis = str(HEADER + SecretSeparator + FileName + SecretSeparator + MyUsername)
    Socket.send(SendThis.encode())

    # * Logger
    now = datetime.now()
    print(f"[{now}] [Out: {SendThis.split(SecretSeparator)[0]}]")
    logging.info(f"[{now}] [Out: {SendThis.split(SecretSeparator)[0]}]")

    SecretSeparatorByte = bytes(SecretSeparator, "utf-8")

    SaveTo = "Download Here\\" + FileName
    File = open(SaveTo, "wb")
    Line = Socket.recv(BUFFER_SIZE)

    while Line:
        if bytearray(Line).find(SecretSeparatorByte) == -1:
            File.write(Line)
            Line = Socket.recv(BUFFER_SIZE)
        else:
            File.write(bytes(bytearray(Line).replace(SecretSeparatorByte, b"")))
            break

    File.close()

    if os.path.exists(SaveTo):
        threading.Thread(
            target=ResetMessage, args=("Pilih File Untuk di Download dari Server.",)
        ).start()
        LastDATA = "File Telah Berhasil di Download dari Server."

        HEADER = "CLIENT_DOWNLOAD_SUCCES"
        SendThis = str(HEADER + SecretSeparator + LastDATA)
        Socket.send(SendThis.encode())

    # * Logger
    now = datetime.now()
    print(f"[{now}] [Out: {SendThis.split(SecretSeparator)[0]}]")
    logging.info(f"[{now}] [Out: {SendThis.split(SecretSeparator)[0]}]")

    Socket.close()


def ClientRegister(NewUsername: str, NewPassword: str, PasswordCheck: str):
    """Melakukan registrasi client ke server.

    Args:
        NewUsername (str): Username baru yang akan di daftarkan.
        NewPassword (str): Password baru yang akan di daftarkan.
        PasswordCheck (str): Password baru yang sama dengan NewPassword.
    """
    global LastDATA

    TCP_IP, TCP_PORT = ServerAddress, ServerPort

    if len(NewUsername) == 0:
        threading.Thread(
            target=ResetMessage, args=("Silahkan Masukkan Username dan Password.",)
        ).start()
        LastDATA = "Username Tidak Boleh Kosong!"
        return

    if len(NewPassword) < 8:
        threading.Thread(
            target=ResetMessage, args=("Silahkan Masukkan Username dan Password.",)
        ).start()
        LastDATA = "Password Harus Memiliki 8 Karakter atau Lebih!"
        return

    if NewPassword != PasswordCheck:
        threading.Thread(
            target=ResetMessage, args=("Silahkan Masukkan Username dan Password.",)
        ).start()
        LastDATA = "Password tidak cocok!"
        return

    Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Socket.connect((TCP_IP, TCP_PORT))

    NewPassword = str(hashlib.md5(NewPassword.encode("utf-8")).hexdigest())

    HEADER = "CLIENT_REQUEST_REGISTER"
    RegistrationData = [NewUsername, NewPassword]
    SendThis = str(HEADER + SecretSeparator + str(RegistrationData))
    Socket.send(SendThis.encode())

    # * Logger
    now = datetime.now()
    print(f"[{now}] [Out: {SendThis.split(SecretSeparator)[0]}]")
    logging.info(f"[{now}] [Out: {SendThis.split(SecretSeparator)[0]}]")

    RESPONSE = Socket.recv(BUFFER_SIZE).decode()
    HEADER, DATA = RESPONSE.split(SecretSeparator, 1)

    # * Logger
    now = datetime.now()
    print(f"[{now}] [In : {RESPONSE.split(SecretSeparator)[0]}]")
    logging.info(f"[{now}] [In : {RESPONSE.split(SecretSeparator)[0]}]")

    Socket.close()

    LastDATA = DATA


def ClientLogin(Username: str, Password: str):
    """Melakukan Login ke Server

    Args:
        Username (str): Username dari Client
        Password (str): Password dari Client
    """
    global LoginStatus, MyUsername, LastDATA

    TCP_IP, TCP_PORT = ServerAddress, ServerPort

    if len(Username) == 0:
        threading.Thread(
            target=ResetMessage, args=("Silahkan Masukkan Username dan Password.",)
        ).start()
        LastDATA = "Username Tidak Boleh Kosong!"
        return

    if len(Password) == 0:
        threading.Thread(
            target=ResetMessage, args=("Silahkan Masukkan Username dan Password.",)
        ).start()
        LastDATA = "Password Tidak Boleh Kosong!"
        return

    Password = hashlib.md5(Password.encode("utf-8")).hexdigest()

    Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Socket.connect((TCP_IP, TCP_PORT))

    HEADER = "CLIENT_REQUEST_LOGIN"
    LoginData = [Username, Password]
    SendThis = str(HEADER + SecretSeparator + str(LoginData))
    Socket.send(SendThis.encode())

    # * Logger
    now = datetime.now()
    print(f"[{now}] [Out: {SendThis.split(SecretSeparator)[0]}]")
    logging.info(f"[{now}] [Out: {SendThis.split(SecretSeparator)[0]}]")

    RESPONSE = Socket.recv(BUFFER_SIZE).decode()

    # * Logger
    now = datetime.now()
    print(f"[{now}] [In : {RESPONSE.split(SecretSeparator)[0]}]")
    logging.info(f"[{now}] [In : {RESPONSE.split(SecretSeparator)[0]}]")

    HEADER, DATA = RESPONSE.split(SecretSeparator, 1)

    global LoginStatus
    if HEADER == "SERVER_HANDLE_LOGIN_SUCCES":
        LoginStatus = True
        MyUsername = Username
    if HEADER == "SERVER_HANDLE_LOGIN_FAILED":
        LoginStatus = False

    threading.Thread(
        target=ResetMessage, args=("Silahkan Masukkan Username dan Password.",)
    ).start()
    LastDATA = DATA

    Socket.close()


def LoginMenu_GUI():
    """Menampilkan gui dari menu login."""
    global LoginMenu, RegisterMenu, LastDATA, LoginMenu_Status

    def LoginAndUpdate():
        """Perintah yang dijalankan ketika login button di tekan."""
        ClientLogin(LoginMenu_UsernameEntry.get(), LoginMenu_PasswordEntry.get())
        LoginMenu_Status.configure(
            text=LastDATA,
            font=("Segoe UI", 12),
        )
        if MyUsername != "":
            LoginMenu.destroy()
            root.withdraw()
            SecondMenu_GUI()

    LoginMenu = customtkinter.CTkToplevel(root)
    LoginMenu.transient(root)
    LoginMenu.iconbitmap(TemporaryDirectory.name + "/SriPandita-FTP.ico")
    LoginMenu.geometry("400x300")
    LoginMenu.resizable(False, False)
    LoginMenu.wm_title("")

    if RegisterMenu:
        RegisterMenu.destroy()

    LoginMenu_Frame = customtkinter.CTkFrame(master=LoginMenu)
    LoginMenu_Frame.pack(pady=20, padx=60, fill="both", expand=True)

    LoginMenu_Label = customtkinter.CTkLabel(
        master=LoginMenu_Frame, text="Login", font=("Segoe UI", 24)
    )
    LoginMenu_Label.pack(pady=12, padx=10)

    LoginMenu_UsernameEntry = customtkinter.CTkEntry(
        master=LoginMenu_Frame, placeholder_text="Username"
    )
    LoginMenu_UsernameEntry.configure(justify="center")
    LoginMenu_UsernameEntry.pack(pady=12, padx=10)

    LoginMenu_PasswordEntry = customtkinter.CTkEntry(
        master=LoginMenu_Frame, placeholder_text="Password", show="*"
    )
    LoginMenu_PasswordEntry.configure(justify="center")
    LoginMenu_PasswordEntry.pack(pady=12, padx=10)

    LastDATA = "Silahkan Masukkan Username dan Password."
    LoginMenu_Status = customtkinter.CTkLabel(
        master=LoginMenu_Frame, text=LastDATA, font=("Segoe UI", 12)
    )

    LoginMenu_LoginButton = customtkinter.CTkButton(
        master=LoginMenu_Frame, text="Login", command=LoginAndUpdate
    )
    LoginMenu_LoginButton.pack(pady=12, padx=10)

    LoginMenu_Status.pack(pady=12, padx=10)

    LoginMenu.protocol("WM_DELETE_WINDOW", LoginMenu.destroy)

    CenterMyWindow(LoginMenu)

    LoginMenu.mainloop()


def RegisterMenu_GUI():
    """Menampilkan gui dari menu registrasi."""
    global LoginMenu, RegisterMenu, LastDATA, RegisterMenu_Status

    def RegisterAndUpdate():
        """Perintah yang dijalankan ketika tombol register ditekan."""
        ClientRegister(
            RegisterMenu_NewUsernameEntry.get(),
            RegisterMenu_NewPasswordEntry.get(),
            RegisterMenu_PasswordCheckEntry.get(),
        )
        RegisterMenu_Status.configure(
            text=LastDATA,
            font=("Segoe UI", 12),
        )

    RegisterMenu = customtkinter.CTkToplevel(root)
    RegisterMenu.transient(root)
    RegisterMenu.iconbitmap(TemporaryDirectory.name + "/SriPandita-FTP.ico")
    RegisterMenu.geometry("400x350")
    RegisterMenu.resizable(False, False)
    RegisterMenu.wm_title("")

    if LoginMenu:
        LoginMenu.destroy()

    RegisterMenu_Frame = customtkinter.CTkFrame(master=RegisterMenu)
    RegisterMenu_Frame.pack(pady=20, padx=60, fill="both", expand=True)

    RegisterMenu_Label = customtkinter.CTkLabel(
        master=RegisterMenu_Frame, text="Register", font=("Segoe UI", 24)
    )
    RegisterMenu_Label.pack(pady=12, padx=10)

    RegisterMenu_NewUsernameEntry = customtkinter.CTkEntry(
        master=RegisterMenu_Frame, placeholder_text="New Username"
    )
    RegisterMenu_NewUsernameEntry.configure(justify="center")
    RegisterMenu_NewUsernameEntry.pack(pady=12, padx=10)

    RegisterMenu_NewPasswordEntry = customtkinter.CTkEntry(
        master=RegisterMenu_Frame, placeholder_text="New Password", show="*"
    )
    RegisterMenu_NewPasswordEntry.configure(justify="center")
    RegisterMenu_NewPasswordEntry.pack(pady=12, padx=10)

    RegisterMenu_PasswordCheckEntry = customtkinter.CTkEntry(
        master=RegisterMenu_Frame, placeholder_text="New Passoword", show="*"
    )
    RegisterMenu_PasswordCheckEntry.configure(justify="center")
    RegisterMenu_PasswordCheckEntry.pack(pady=12, padx=10)

    LastDATA = "Silahkan Masukkan Username dan Password."
    RegisterMenu_Status = customtkinter.CTkLabel(
        master=RegisterMenu_Frame, text=LastDATA, font=("Segoe UI", 12)
    )

    RegisterMenu_LoginButton = customtkinter.CTkButton(
        master=RegisterMenu_Frame, text="Register", command=RegisterAndUpdate
    )
    RegisterMenu_LoginButton.pack(pady=12, padx=10)

    RegisterMenu_Status.pack(pady=12, padx=10)

    RegisterMenu.protocol("WM_DELETE_WINDOW", RegisterMenu.destroy)

    CenterMyWindow(RegisterMenu)

    RegisterMenu.mainloop()


def SecondMenu_GUI():
    """Menampilan GUI Dashboard setelah client berhasil login."""
    global UploadDownload, UploadDownload_Label, LastDATA

    if LoginStatus:
        GetDownloadUploadCount(MyUsername)

        UploadDownload = customtkinter.CTkToplevel(root)
        UploadDownload.iconbitmap(TemporaryDirectory.name + "/SriPandita-FTP.ico")
        UploadDownload.geometry("400x550")
        UploadDownload.resizable(False, False)
        UploadDownload.wm_title("Main Menu")

        UploadDownload_Frame = customtkinter.CTkFrame(master=UploadDownload)
        UploadDownload_Frame.pack(pady=20, padx=60, fill="both", expand=True)

        UploadDownload_YNTKTS_Image = customtkinter.CTkImage(
            LightImage,
            DarkImage,
            size=(200, 150),
        )
        UploadDownload_YNTKTS = customtkinter.CTkButton(
            master=UploadDownload_Frame,
            image=UploadDownload_YNTKTS_Image,
            text="",
            border_width=0,
            corner_radius=0,
            fg_color="transparent",
            state="disabled",
        )
        UploadDownload_YNTKTS.pack(pady=12, padx=10)

        SecondMenuHeader = (
            "Username: "
            + MyUsername
            + "\nUpload Count: "
            + str(UploadCount)
            + "\nDownload Count: "
            + str(DownloadCount)
        )
        UploadDownload_Label = customtkinter.CTkLabel(
            master=UploadDownload_Frame,
            text=SecondMenuHeader,
            font=("Segoe UI", 18),
        )
        UploadDownload_Label.pack(pady=12, padx=25)

        UploadDownload_UploadFiles = customtkinter.CTkButton(
            master=UploadDownload_Frame,
            text="Upload Files",
            command=KombinasiFungsi(UpdateTheCount, ShowUploadMenu_GUI),
        )
        UploadDownload_UploadFiles.pack(pady=12, padx=10)

        UploadDownload_DownloadFiles = customtkinter.CTkButton(
            master=UploadDownload_Frame,
            text="Download Files",
            command=KombinasiFungsi(UpdateTheCount, ShowDownloadMenu_GUI),
        )
        UploadDownload_DownloadFiles.pack(pady=12, padx=10)

        UploadDownload_SeeFiles = customtkinter.CTkButton(
            master=UploadDownload_Frame,
            text="Server Files List",
            command=KombinasiFungsi(UpdateTheCount, ShowFilesListMenu_GUI),
        )
        UploadDownload_SeeFiles.pack(pady=12, padx=10)

        UploadDownload_Quit = customtkinter.CTkButton(
            master=UploadDownload_Frame,
            text="LogOut and Exit",
            command=KombinasiFungsi(UpdateTheCount, FullExitClient),
        )
        UploadDownload_Quit.pack(pady=12, padx=10)

        UploadDownload.protocol("WM_DELETE_WINDOW", FullExitClient)

        CenterMyWindow(UploadDownload)

        UploadDownload.deiconify()
        UploadDownload.mainloop()


def ShowDownloadMenu_GUI():
    """Menampilkan GUO Menu download file."""
    global DownloadMenu, LastDATA, DownloadMenu_DownloadFiles_Label

    DownloadFolder = "Download Here"

    def OpenTheUploadDirectory():
        """Membuka folder download."""
        OpenDirectory(DownloadFolder)

    def RefreshLists():
        """Mengupdate tampilan ListBox dari Window."""
        TCP_IP, TCP_PORT = ServerAddress, ServerPort

        Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Socket.connect((TCP_IP, TCP_PORT))

        HEADER = "CLIENT_REQUEST_FILES_LIST"
        SendThis = str(HEADER + SecretSeparator + str(ServerPort))
        Socket.send(SendThis.encode())

        # * Logger
        now = datetime.now()
        print(f"[{now}] [Out: {SendThis.split(SecretSeparator)[0]}]")
        logging.info(f"[{now}] [Out: {SendThis.split(SecretSeparator)[0]}]")

        SecretSeparatorByte = bytes(SecretSeparator, "utf-8")

        SaveTo = "FilesListClient.bin"
        with open(SaveTo, mode="wb") as File:
            Line = Socket.recv(BUFFER_SIZE)
            while Line:
                if bytearray(Line).find(SecretSeparatorByte) == -1:
                    File.write(Line)
                    Line = Socket.recv(BUFFER_SIZE)
                else:
                    File.write(bytes(bytearray(Line).replace(SecretSeparatorByte, b"")))
                    break

        with open("FilesListClient.bin", "r") as File:
            DATA = ast.literal_eval(File.read())

        if os.path.exists("FilesListClient.bin"):
            HEADER = "FILES_LIST_RECEIVED"
            SendThis = str(HEADER + SecretSeparator + "YNTKTS")
            Socket.send(SendThis.encode())

        # * Logger
        now = datetime.now()
        print(f"[{now}] [Out: {SendThis.split(SecretSeparator)[0]}]")
        logging.info(f"[{now}] [Out: {SendThis.split(SecretSeparator)[0]}]")

        try:
            DownloadMenu_ListBox.delete(0, END)
            for i in DATA:
                DownloadMenu_ListBox.insert(END, i)
            DownloadMenu_DownloadFiles_Label.configure(
                text=LastDATA,
                font=("Segoe UI", 12),
            )
        except:
            pass
        finally:
            os.remove("FilesListClient.bin")

    def DownloadSelected():
        """Melakukan download untuk file yang di pilih pada ListBox."""
        for i in DownloadMenu_ListBox.curselection():
            GetFileFromServer(DownloadMenu_ListBox.get(i))
        DownloadMenu_DownloadFiles_Label.configure(
            text=LastDATA,
            font=("Segoe UI", 12),
        )

    if not os.path.exists(DownloadFolder):
        os.mkdir(DownloadFolder)

    DownloadMenu = customtkinter.CTkToplevel(UploadDownload)
    DownloadMenu.transient(UploadDownload)
    DownloadMenu.attributes("-topmost", True)
    DownloadMenu.iconbitmap(TemporaryDirectory.name + "/SriPandita-FTP.ico")
    DownloadMenu.geometry("400x450")
    DownloadMenu.resizable(False, False)
    DownloadMenu.wm_title("Download Files")
    DownloadMenu.config(bg="#1a1a1a")

    DownloadMenu_Frame = customtkinter.CTkFrame(DownloadMenu)
    DownloadMenu_Frame.pack(pady=20, padx=60, fill="both", expand=True)

    DownloadMenu_SideBySideButton_Frame = customtkinter.CTkFrame(DownloadMenu_Frame)
    DownloadMenu_SideBySideButton_Frame.pack(side=TOP)

    DownloadMenu_OpenDirectory = customtkinter.CTkButton(
        master=DownloadMenu_Frame,
        text="Buka Folder Download",
        command=OpenTheUploadDirectory,
    )
    DownloadMenu_OpenDirectory.pack(
        pady=12,
        padx=10,
        expand=True,
        in_=DownloadMenu_SideBySideButton_Frame,
        side=LEFT,
    )

    DownloadMenu_Refresh = customtkinter.CTkButton(
        master=DownloadMenu_Frame, text="Refresh", command=RefreshLists
    )
    DownloadMenu_Refresh.pack(
        pady=12,
        padx=10,
        expand=True,
        in_=DownloadMenu_SideBySideButton_Frame,
        side=LEFT,
    )

    DownloadMenu_ListBox_Frame = customtkinter.CTkFrame(DownloadMenu_Frame)
    DownloadMenu_ListBox_Frame.pack(pady=12, padx=10, fill="both", expand=True)

    DownloadMenu_ListBox_ScrollBar = customtkinter.CTkScrollbar(
        DownloadMenu_ListBox_Frame, width=15
    )

    DownloadMenu_ListBox = tk.Listbox(
        DownloadMenu_ListBox_Frame,
        bg="#212121",
        fg="white",
        selectbackground="#1f538d",
        width=30,
        height=15,
        selectmode=SINGLE,
    )
    RefreshLists()
    DownloadMenu_ListBox.config(yscrollcommand=DownloadMenu_ListBox_ScrollBar.set)
    DownloadMenu_ListBox.pack(
        pady=12, padx=(12, 0), side=LEFT, fill="both", expand=True
    )

    DownloadMenu_ListBox_ScrollBar.configure(command=DownloadMenu_ListBox.yview)
    DownloadMenu_ListBox_ScrollBar.pack(padx=(0, 12), pady=12, side=RIGHT, fill="y")

    DownloadMenu_DownloadFilesButton_Frame = customtkinter.CTkFrame(DownloadMenu_Frame)
    DownloadMenu_DownloadFilesButton_Frame.pack(side=BOTTOM, fill="x", expand=True)

    LastDATA = "Pilih File Untuk di Download dari Server."
    DownloadMenu_DownloadFiles_Label = customtkinter.CTkLabel(
        DownloadMenu_DownloadFilesButton_Frame, text=LastDATA, font=("Segoe UI", 12)
    )
    DownloadMenu_DownloadFiles_Label.pack(
        pady=(5, 0), padx=10, fill="x", expand=True, side=TOP
    )

    DownloadMenu_DownloadFiles_Button = customtkinter.CTkButton(
        master=DownloadMenu_DownloadFilesButton_Frame,
        text="Download.",
        command=KombinasiFungsi(DownloadSelected, UpdateTheCount),
    )
    DownloadMenu_DownloadFiles_Button.pack(
        pady=(0, 10), padx=10, fill="x", expand=True, side=BOTTOM
    )

    DownloadMenu.protocol(
        "WM_DELETE_WINDOW", KombinasiFungsi(UpdateTheCount, DownloadMenu.destroy)
    )

    DarkMyWindowTitleBar(DownloadMenu)
    CenterMyWindow(DownloadMenu)

    DownloadMenu.deiconify()
    DownloadMenu.mainloop()


def ShowUploadMenu_GUI():
    """Menampilkan GUI Menu Upload File"""
    global UploadMenu, LastDATA, UploadMenu_UploadFiles_Label

    UploadFolder = "Upload Here"

    def OpenTheUploadDirectory():
        """Membuka Folder Upload"""
        OpenDirectory(UploadFolder)

    def RefreshLists():
        """Mengupdate Tampilan ListBox dari Window"""
        try:
            UploadMenu_ListBox.delete(0, END)
            ListsOnUploadFolder = [
                f
                for f in os.listdir(UploadFolder)
                if os.path.isfile(os.path.join(UploadFolder, f))
            ]
            for i in ListsOnUploadFolder:
                UploadMenu_ListBox.insert(END, i)
            UploadMenu_UploadFiles_Label.configure(
                text=LastDATA,
                font=("Segoe UI", 12),
            )
        except:
            pass
        finally:
            pass

    def UploadSelected():
        """Melakukan Upload Untuk File yang di Pilih pada ListBox"""
        for i in UploadMenu_ListBox.curselection():
            SendFileToServer(UploadMenu_ListBox.get(i))
        UploadMenu_UploadFiles_Label.configure(
            text=LastDATA,
            font=("Segoe UI", 12),
        )

    if UploadMenu:
        UploadMenu.destroy()

    if not os.path.exists(UploadFolder):
        os.mkdir(UploadFolder)

    UploadMenu = customtkinter.CTkToplevel(UploadDownload)
    UploadMenu.transient(UploadDownload)
    UploadMenu.attributes("-topmost", True)
    UploadMenu.iconbitmap(TemporaryDirectory.name + "/SriPandita-FTP.ico")
    UploadMenu.geometry("400x450")
    UploadMenu.resizable(False, False)
    UploadMenu.wm_title("Upload Files")
    UploadMenu.config(bg="#1a1a1a")

    UploadMenu_Frame = customtkinter.CTkFrame(UploadMenu)
    UploadMenu_Frame.pack(pady=20, padx=60, fill="both", expand=True)

    UploadMenu_SideBySideButton_Frame = customtkinter.CTkFrame(UploadMenu_Frame)
    UploadMenu_SideBySideButton_Frame.pack(side=TOP)

    UploadMenu_OpenDirectory = customtkinter.CTkButton(
        master=UploadMenu_Frame,
        text="Buka Folder Upload",
        command=OpenTheUploadDirectory,
    )
    UploadMenu_OpenDirectory.pack(
        pady=12, padx=10, expand=True, in_=UploadMenu_SideBySideButton_Frame, side=LEFT
    )

    UploadMenu_Refresh = customtkinter.CTkButton(
        master=UploadMenu_Frame, text="Refresh", command=RefreshLists
    )
    UploadMenu_Refresh.pack(
        pady=12, padx=10, expand=True, in_=UploadMenu_SideBySideButton_Frame, side=LEFT
    )

    UploadMenu_ListBox_Frame = customtkinter.CTkFrame(UploadMenu_Frame)
    UploadMenu_ListBox_Frame.pack(pady=12, padx=10, fill="both", expand=True)

    UploadMenu_ListBox_ScrollBar = customtkinter.CTkScrollbar(
        UploadMenu_ListBox_Frame, width=15
    )

    UploadMenu_ListBox = tk.Listbox(
        UploadMenu_ListBox_Frame,
        bg="#212121",
        fg="white",
        selectbackground="#1f538d",
        width=30,
        height=15,
        selectmode=SINGLE,
    )
    RefreshLists()
    UploadMenu_ListBox.config(yscrollcommand=UploadMenu_ListBox_ScrollBar.set)
    UploadMenu_ListBox.pack(pady=12, padx=(12, 0), side=LEFT, fill="both", expand=True)

    UploadMenu_ListBox_ScrollBar.configure(command=UploadMenu_ListBox.yview)
    UploadMenu_ListBox_ScrollBar.pack(padx=(0, 12), pady=12, side=RIGHT, fill="y")

    UploadMenu_UploadFilesButton_Frame = customtkinter.CTkFrame(UploadMenu_Frame)
    UploadMenu_UploadFilesButton_Frame.pack(side=BOTTOM, fill="x", expand=True)

    LastDATA = "Pilih File Untuk di Upload Ke Server."
    UploadMenu_UploadFiles_Label = customtkinter.CTkLabel(
        UploadMenu_UploadFilesButton_Frame, text=LastDATA, font=("Segoe UI", 12)
    )
    UploadMenu_UploadFiles_Label.pack(
        pady=(5, 0), padx=10, fill="x", expand=True, side=TOP
    )

    UploadMenu_UploadFiles_Button = customtkinter.CTkButton(
        master=UploadMenu_UploadFilesButton_Frame,
        text="Upload.",
        command=KombinasiFungsi(UploadSelected, UpdateTheCount),
    )
    UploadMenu_UploadFiles_Button.pack(
        pady=(0, 10), padx=10, fill="x", expand=True, side=BOTTOM
    )

    UploadMenu.protocol(
        "WM_DELETE_WINDOW", KombinasiFungsi(UpdateTheCount, UploadMenu.destroy)
    )

    DarkMyWindowTitleBar(UploadMenu)
    CenterMyWindow(UploadMenu)

    UploadMenu.deiconify()
    UploadMenu.mainloop()


def ShowFilesListMenu_GUI():
    """Menampilkan Menu list file-file yand ada di server."""
    global FilesListMenu

    def RefreshLists():
        """Mengupdate tampilan ListBox dari Window."""
        TCP_IP, TCP_PORT = ServerAddress, ServerPort

        Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Socket.connect((TCP_IP, TCP_PORT))

        HEADER = "CLIENT_REQUEST_FILES_LIST"
        SendThis = str(HEADER + SecretSeparator + str(ServerPort))
        Socket.send(SendThis.encode())

        # * Logger
        now = datetime.now()
        print(f"[{now}] [Out: {SendThis.split(SecretSeparator)[0]}]")
        logging.info(f"[{now}] [Out: {SendThis.split(SecretSeparator)[0]}]")

        SecretSeparatorByte = bytes(SecretSeparator, "utf-8")

        SaveTo = "FilesListClient.bin"
        with open(SaveTo, mode="wb") as File:
            Line = Socket.recv(BUFFER_SIZE)
            while Line:
                if bytearray(Line).find(SecretSeparatorByte) == -1:
                    File.write(Line)
                    Line = Socket.recv(BUFFER_SIZE)
                else:
                    File.write(bytes(bytearray(Line).replace(SecretSeparatorByte, b"")))
                    break

        with open("FilesListClient.bin", "r") as File:
            DATA = ast.literal_eval(File.read())

        if os.path.exists("FilesListClient.bin"):
            HEADER = "FILES_LIST_RECEIVED"
            SendThis = str(HEADER + SecretSeparator + "YNTKTS")
            Socket.send(SendThis.encode())

        # * Logger
        now = datetime.now()
        print(f"[{now}] [Out: {SendThis.split(SecretSeparator)[0]}]")
        logging.info(f"[{now}] [Out: {SendThis.split(SecretSeparator)[0]}]")

        try:
            FilesListMenu_ListBox.delete(0, END)
            for i in DATA:
                FilesListMenu_ListBox.insert(END, i)
        except:
            pass
        finally:
            os.remove("FilesListClient.bin")

    if FilesListMenu:
        FilesListMenu.destroy()

    FilesListMenu = customtkinter.CTkToplevel(UploadDownload)
    FilesListMenu.transient(UploadDownload)
    FilesListMenu.attributes("-topmost", True)
    FilesListMenu.iconbitmap(TemporaryDirectory.name + "/SriPandita-FTP.ico")
    FilesListMenu.geometry("400x450")
    FilesListMenu.resizable(False, False)
    FilesListMenu.wm_title("Server Files Lists")
    FilesListMenu.config(bg="#1a1a1a")

    FilesListMenu_Frame = customtkinter.CTkFrame(FilesListMenu)
    FilesListMenu_Frame.pack(pady=20, padx=60, fill="both", expand=True)

    FilesListMenu_SideBySideButton_Frame = customtkinter.CTkFrame(FilesListMenu_Frame)
    FilesListMenu_SideBySideButton_Frame.pack(side=TOP, fill="x", expand=True)

    FilesListMenu_Refresh = customtkinter.CTkButton(
        master=FilesListMenu_Frame, text="Refresh", command=RefreshLists
    )
    FilesListMenu_Refresh.pack(
        pady=3,
        padx=10,
        expand=True,
        in_=FilesListMenu_SideBySideButton_Frame,
        side=LEFT,
        fill="x",
    )

    FilesListMenu_ListBox_Frame = customtkinter.CTkFrame(FilesListMenu_Frame)
    FilesListMenu_ListBox_Frame.pack(pady=3, padx=10, fill="both", expand=True)

    FilesListMenu_ListBox_ScrollBar = customtkinter.CTkScrollbar(
        FilesListMenu_ListBox_Frame, width=15
    )

    FilesListMenu_ListBox = tk.Listbox(
        FilesListMenu_ListBox_Frame,
        bg="#212121",
        fg="white",
        selectbackground="#1f538d",
        width=30,
        height=15,
        selectmode=SINGLE,
    )
    RefreshLists()
    FilesListMenu_ListBox.config(yscrollcommand=FilesListMenu_ListBox_ScrollBar.set)
    FilesListMenu_ListBox.pack(
        pady=12, padx=(12, 0), side=LEFT, fill="both", expand=True
    )

    FilesListMenu_ListBox_ScrollBar.configure(command=FilesListMenu_ListBox.yview)
    FilesListMenu_ListBox_ScrollBar.pack(padx=(0, 12), pady=12, side=RIGHT, fill="y")

    FilesListMenu.protocol(
        "WM_DELETE_WINDOW", KombinasiFungsi(UpdateTheCount, FilesListMenu.destroy)
    )

    DarkMyWindowTitleBar(FilesListMenu)
    CenterMyWindow(FilesListMenu)

    FilesListMenu.deiconify()
    FilesListMenu.mainloop()


def KombinasiFungsi(*funcs):
    """Mengkombinasi beberapa fungsi."""

    def FungsiTerkombinasi(*args, **kwargs):
        """Mengkombinasi beberapa fungsi."""
        for TheFunction in funcs:
            TheFunction(*args, **kwargs)

    return FungsiTerkombinasi


def UpdateTheCount():
    """Mengupdate Jumlah Statistik Download dan Upload Milik User pada Dashboard"""
    global UploadDownload_Label

    GetDownloadUploadCount(MyUsername)
    SecondMenuHeader = (
        "Username: "
        + MyUsername
        + "\nUpload Count: "
        + str(UploadCount)
        + "\nDownload Count: "
        + str(DownloadCount)
    )
    UploadDownload_Label.configure(text=SecondMenuHeader, font=("Segoe UI", 18))


def FullExitClient():
    """Fungsi untuk melakukan exit program secara menyeluruh."""
    TCP_IP, TCP_PORT = ServerAddress, ServerPort

    try:
        root.destroy()

        LoginMenu.destroy()
        RegisterMenu.destroy()
        UploadDownload.destroy()
        UploadMenu.destroy()
        FilesListMenu.destroy()
        DownloadMenu.destroy()
        UploadDownload_Label.destroy()
        CustomHost.destroy()
    except Exception as e:
        pass
    finally:
        if MyUsername != "":
            HEADER = "CLIENT_LOGOUT_EXIT"
        else:
            HEADER = "CLIENT_EXIT"
        DATA = ""
        SendThis = str(HEADER + SecretSeparator + str(DATA))

        Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Socket.connect((TCP_IP, TCP_PORT))
        Socket.send(SendThis.encode())

        # * Logger
        now = datetime.now()
        print(f"[{now}] [Out: {SendThis.split(SecretSeparator)[0]}]")
        logging.info(f"[{now}] [Out: {SendThis.split(SecretSeparator)[0]}]")

        Socket.close()

        try:
            TemporaryDirectory.cleanup()
        except:
            pass
        finally:
            exit()


def CenterMyWindow(Window: Union[customtkinter.CTkToplevel, customtkinter.CTk]):
    """Memindahkan window tkinter ke tengah layar.

    Args:
        Window (Union[customtkinter.CTkToplevel, customtkinter.CTk]): Window yang akan diposisikan ke tengah layar.
    """
    Window.update_idletasks()
    width = Window.winfo_width()
    frm_width = Window.winfo_rootx() - Window.winfo_x()
    win_width = width + 2 * frm_width
    height = Window.winfo_height()
    titlebar_height = Window.winfo_rooty() - Window.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = Window.winfo_screenwidth() // 2 - win_width // 2
    y = Window.winfo_screenheight() // 2 - win_height // 2
    Window.geometry("{}x{}+{}+{}".format(width, height, x, y))


def DarkMyWindowTitleBar(window: Union[customtkinter.CTkToplevel, customtkinter.CTk]):
    """Mengubah background dari title bar tkinter menjadi gelap.

    Args:
        win (Union[customtkinter.CTkToplevel, customtkinter.CTk]): Window yang akan diubah menjadi mode gelap.
    """
    window.update()
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ctypes.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 2
    value = ctypes.c_int(value)
    set_window_attribute(
        hwnd, rendering_policy, ctypes.byref(value), ctypes.sizeof(value)
    )


def OpenDirectory(OpenThis: str):
    """Membuka folder.

    Args:
        OpenThis (str): Alamat dari folder yang akan dibuka.
    """
    os.startfile(os.path.realpath(OpenThis))


def FirstTimeConnectServer():
    """Perintah yang dijalankan pada client saat pertama kali tersambung ke server."""
    TCP_IP, TCP_PORT = ServerAddress, ServerPort
    try:
        Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Socket.connect((TCP_IP, TCP_PORT))

        HEADER = "FIRST_TIME"
        SendThis = str(HEADER + SecretSeparator + "YNTKTS")
        Socket.send(SendThis.encode())

        # * Logger
        now = datetime.now()
        print(f"[{now}] [Out: {SendThis.split(SecretSeparator)[0]}]")
        logging.info(f"[{now}] [Out: {SendThis.split(SecretSeparator)[0]}]")

        ReceiveThis = str(Socket.recv(BUFFER_SIZE).decode())

        # * Logger
        now = datetime.now()
        print(f"[{now}] [In : {ReceiveThis.split(SecretSeparator)[0]}]")
        logging.info(f"[{now}] [In : {ReceiveThis.split(SecretSeparator)[0]}]")

        Socket.close()
    except:
        MessageBoxW(0, "Tidak Dapat Terhubung Ke Server...", "Error", 0)
        try:
            TemporaryDirectory.cleanup()
        except:
            pass
        finally:
            exit()


def CustomServer():
    """Mengubah alamat server dan port server host yang akan dituju."""
    global CustomHost, root

    def ChangeHostIP():
        """Perintah yang dijalankan ketika tombol continue ditekan."""
        global ServerAddress, ServerPort
        try:
            if CustomHost_CustomHostEntry.get() != "":
                ServerAddress, ServerPort = str(CustomHost_CustomHostEntry.get()).split(
                    ":"
                )
                ServerPort = int(ServerPort)
        except:
            CustomHost.destroy()
            CustomHost.update()
            MessageBoxW(0, "Server Tidak Valid...", "Error", 0)
            exit()
        finally:
            if ServerPort < 0 or ServerPort > 65535:
                CustomHost.destroy()
                CustomHost.update()
                MessageBoxW(0, "Server Port Tidak Valid...", "Error", 0)
                exit()
        CustomHost.destroy()
        CustomHost.update()

        FirstTimeConnectServer()
        CenterMyWindow(root)

        root.deiconify()
        root.mainloop()

    CustomHost = customtkinter.CTkToplevel()
    CustomHost.transient()
    CustomHost.iconbitmap(TemporaryDirectory.name + "/SriPandita-FTP.ico")
    CustomHost.geometry("420x200")
    CustomHost.resizable(False, False)
    CustomHost.wm_title("Custom Host Server and Port")

    CustomHost_Frame = customtkinter.CTkFrame(master=CustomHost)
    CustomHost_Frame.pack(pady=20, padx=20, fill="both", expand=True)

    CustomHost_Label = customtkinter.CTkLabel(
        master=CustomHost_Frame,
        text="Custom Server Host and Port",
        font=("Segoe UI", 24),
    )
    CustomHost_Label.pack(pady=12, padx=10, fill="x", expand=True)

    CustomHost_CustomHostEntry = customtkinter.CTkEntry(
        master=CustomHost_Frame,
        placeholder_text="Kosongkan Untuk Menggunakan Default (127.0.0.1:48632)",
    )
    CustomHost_CustomHostEntry.configure(justify="center")
    CustomHost_CustomHostEntry.pack(pady=12, padx=10, fill="x", expand=True)

    CustomHost_ContinueButton = customtkinter.CTkButton(
        master=CustomHost_Frame, text="Continue", command=ChangeHostIP
    )
    CustomHost_ContinueButton.pack(pady=12, padx=10, fill="x", expand=True)

    CustomHost.protocol("WM_DELETE_WINDOW", ChangeHostIP)

    CenterMyWindow(CustomHost)

    CustomHost.deiconify()
    CustomHost.mainloop()


if __name__ == "__main__":
    try:
        sleep(1)
        pyi_splash.close()
    except:
        pass
    finally:
        pass

    logging.basicConfig(
        filename="ClientLog.txt",
        filemode="a",
        format="%(message)s",
        datefmt="%H:%M:%S",
        level=logging.INFO,
    )

    TemporaryDirectory = tempfile.TemporaryDirectory()

    URL = "https://cdn.discordapp.com/attachments/703242278189269004/1056533501010247751/wHeA8Gp.ico"
    response = requests.get(URL)
    TempICOFile = TemporaryDirectory.name + "/SriPandita-FTP.ico"
    open(TempICOFile, "wb").write(response.content)

    URL = "https://cdn.discordapp.com/attachments/703242278189269004/1056533523999248434/qVUFcFM.png"
    response = requests.get(URL)
    TempPNGFile = TemporaryDirectory.name + "/SriPandita-FTP-Home.png"
    open(TempPNGFile, "wb").write(response.content)

    ServerPort = 0
    BUFFER_SIZE = 1024
    SecretSeparator = "!@#$%^&*"
    LastDATA = ""
    MyUsername = ""
    LoginStatus = False

    DownloadCount = 0
    UploadCount = 0

    LoginMenu = None
    RegisterMenu = None
    UploadDownload = None
    UploadMenu = None
    FilesListMenu = None
    DownloadMenu = None
    CustomHost = None

    UploadDownload_YNTKTS_Image = None
    root_Image = None

    UploadDownload_Label = None
    DownloadMenu_DownloadFiles_Label = None
    UploadMenu_UploadFiles_Label = None
    LoginMenu_Status = None
    RegisterMenu_Status = None

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    LightImage = PIL.Image.open(TempPNGFile)
    DarkImage = PIL.Image.open(TempPNGFile)

    root = customtkinter.CTk()
    root.iconbitmap(TemporaryDirectory.name + "/SriPandita-FTP.ico")
    root.geometry("400x350")
    root.resizable(False, False)
    root.wm_title("Yo Ndak Tau Kok Tanya Saya")

    root_Frame = customtkinter.CTkFrame(master=root)
    root_Frame.pack(pady=20, padx=60, fill="both", expand=True)

    root_Image = customtkinter.CTkImage(
        LightImage,
        DarkImage,
        size=(200, 150),
    )
    root_ButtonImage = customtkinter.CTkButton(
        master=root_Frame,
        image=root_Image,
        text="",
        border_width=0,
        corner_radius=0,
        fg_color="transparent",
        state="disabled",
    )
    root_ButtonImage.pack(pady=12, padx=10)

    root_RegisterButton = customtkinter.CTkButton(
        master=root_Frame, text="Register", command=RegisterMenu_GUI
    )
    root_RegisterButton.pack(pady=12, padx=10)

    root_LoginButton = customtkinter.CTkButton(
        master=root_Frame, text="Login", command=LoginMenu_GUI
    )
    root_LoginButton.pack(pady=12, padx=10)

    root.protocol("WM_DELETE_WINDOW", FullExitClient)

    ServerAddress = "127.0.0.1"
    ServerPort = 48632

    CustomServer()

    exit()
