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
__version__ = "0.0.7"
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
__status__ = "Production"

import ast
import ctypes as ct
import hashlib
import os
import random
import socket
import tkinter as tk
from tkinter import *
from tkinter import ttk

import customtkinter
import PIL.Image


def GetDownloadUploadCount(Username):
    """Meminta Statistik Upload dan Download Milik User dari Server

    Args:
        Username (str): Username yang Akan diminta Statistik Download dan Uploadnya
    """
    global DownloadCount, UploadCount

    TCP_IP = "127.0.0.1"
    TCP_PORT = CLIENT_PORT

    Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Socket.connect((TCP_IP, TCP_PORT))

    HEADER = "GET_USER_STATS"
    SendThis = HEADER + SecretSeparator + Username
    Socket.send(SendThis.encode())

    RESPONSE = Socket.recv(BUFFER_SIZE).decode()
    RESPONSE = str(RESPONSE)
    HEADER, DATA = RESPONSE.split(SecretSeparator, 1)

    if HEADER == "GIVE_STATS":
        DATA = ast.literal_eval(DATA)

    DownloadCount = DATA[0]
    UploadCount = DATA[1]

    Socket.close()


def SendFileToServer(TheFile):
    """Mengirim File ke Server

    Args:
        TheFile (str): Nama File yang Akan Dikirim
    """
    global BUFFER_SIZE, SecretSeparator, LastDATA, CLIENT_PORT, MyUsername

    TCP_IP = "127.0.0.1"
    TCP_PORT = CLIENT_PORT
    HEADER = "GET_PORT_FOR_UPLOAD"

    Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Socket.connect((TCP_IP, TCP_PORT))

    FileName = TheFile
    SendThis = HEADER + SecretSeparator + FileName + SecretSeparator + MyUsername
    Socket.send(SendThis.encode())

    RESPONSE = Socket.recv(BUFFER_SIZE).decode()
    RESPONSE = str(RESPONSE)
    HEADER, PORT = RESPONSE.split(SecretSeparator, 1)
    if HEADER != "GIVE_PORT":
        return

    TCP_IP_TRANSFER = "127.0.0.1"
    TCP_PORT_TRANSFER = int(PORT)

    TransferSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TransferSocket.connect((TCP_IP_TRANSFER, TCP_PORT_TRANSFER))

    FullPath = "Upload Here\\" + TheFile
    File = open(FullPath, "rb")
    Line = File.read(BUFFER_SIZE)

    while Line:
        TransferSocket.send(Line)
        Line = File.read(BUFFER_SIZE)

    File.close()
    TransferSocket.close()

    RESPONSE = Socket.recv(BUFFER_SIZE).decode()
    RESPONSE = str(RESPONSE)
    HEADER, DATA = RESPONSE.split(SecretSeparator, 1)

    Socket.close()

    try:
        LastDATA = DATA
    finally:
        del (
            DATA,
            File,
            FileName,
            FullPath,
            HEADER,
            Line,
            PORT,
            RESPONSE,
            SendThis,
            Socket,
            TCP_IP,
            TCP_IP_TRANSFER,
            TCP_PORT,
            TCP_PORT_TRANSFER,
            TransferSocket,
        )


def GetFileFromServer(TheFile):
    """Mengunduh File dari Server

    Args:
        TheFile (str): Nama File yang Ingin di Download
    """
    global BUFFER_SIZE, SecretSeparator, LastDATA, CLIENT_PORT, MyUsername

    TCP_IP = "127.0.0.1"
    TCP_PORT = CLIENT_PORT
    HEADER = "GET_PORT_FOR_DOWNLOAD"

    Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Socket.connect((TCP_IP, TCP_PORT))

    FileName = TheFile
    SendThis = HEADER + SecretSeparator + FileName + SecretSeparator + MyUsername
    Socket.send(SendThis.encode())

    RESPONSE = Socket.recv(BUFFER_SIZE).decode()
    RESPONSE = str(RESPONSE)
    HEADER, PORT = RESPONSE.split(SecretSeparator, 1)
    if HEADER != "GIVE_PORT":
        return

    TCP_IP_TRANSFER = "127.0.0.1"
    TCP_PORT_TRANSFER = int(PORT)

    TransferSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TransferSocket.connect((TCP_IP_TRANSFER, TCP_PORT_TRANSFER))

    while True:
        SaveTo = "Download Here\\" + FileName
        File = open(SaveTo, "wb")
        Line = TransferSocket.recv(BUFFER_SIZE)

        while Line:
            File.write(Line)
            Line = TransferSocket.recv(BUFFER_SIZE)

        File.close()
        TransferSocket.close()
        TransferSocket.close()
        break

    RESPONSE = Socket.recv(BUFFER_SIZE).decode()
    RESPONSE = str(RESPONSE)
    HEADER, DATA = RESPONSE.split(SecretSeparator, 1)

    Socket.close()

    try:
        LastDATA = DATA
    finally:
        del (
            DATA,
            File,
            FileName,
            HEADER,
            Line,
            PORT,
            RESPONSE,
            SaveTo,
            SendThis,
            Socket,
            TCP_IP,
            TCP_IP_TRANSFER,
            TCP_PORT,
            TCP_PORT_TRANSFER,
            TransferSocket,
        )


def ClientRegister(NewUsername, NewPassword, PasswordCheck):
    """Melakukan Registrasi Client ke Server

    Args:
        NewUsername (str): Username Baru yang Akan di Daftarkan
        NewPassword (str): Password Baru yang Akan di Daftarkan
        PasswordCheck (str): Password Baru yang Akan di Daftarkan
    """
    global BUFFER_SIZE, SecretSeparator, LastDATA, CLIENT_PORT

    if len(NewUsername) == 0:
        LastDATA = "Username Tidak Boleh Kosong!"
        return

    if len(NewPassword) < 8:
        LastDATA = "Password Harus Memiliki 8 Karakter atau Lebih!"
        return

    if NewPassword != PasswordCheck:
        LastDATA = "Password tidak cocok!"
        return

    NewPassword = hashlib.md5(NewPassword.encode("utf-8")).hexdigest()

    TCP_IP = "127.0.0.1"
    TCP_PORT = CLIENT_PORT
    HEADER = "REGISTER"
    RegistrationData = [NewUsername, NewPassword]
    SendThis = HEADER + SecretSeparator + str(RegistrationData)

    Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Socket.connect((TCP_IP, TCP_PORT))

    Socket.send(SendThis.encode())

    RESPONSE = Socket.recv(BUFFER_SIZE).decode()
    RESPONSE = str(RESPONSE)
    HEADER, DATA = RESPONSE.split(SecretSeparator, 1)

    Socket.close()

    try:
        LastDATA = DATA
    finally:
        del (
            DATA,
            HEADER,
            NewPassword,
            NewUsername,
            PasswordCheck,
            RESPONSE,
            RegistrationData,
            SendThis,
            Socket,
            TCP_IP,
            TCP_PORT,
        )


def ClientLogin(Username, Password):
    """Melakukan Login ke Server

    Args:
        Username (str): Username dari Client
        Password (str): Password dari Client
    """
    global CLIENT_PORT, BUFFER_SIZE, SecretSeparator, LoginStatus
    global MyUsername, LastDATA, LoginMenu, RegisterMenu

    Password = hashlib.md5(Password.encode("utf-8")).hexdigest()

    TCP_IP = "127.0.0.1"
    TCP_PORT = CLIENT_PORT
    HEADER = "LOGIN"
    LoginData = [Username, Password]
    SendThis = HEADER + SecretSeparator + str(LoginData)

    Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Socket.connect((TCP_IP, TCP_PORT))

    Socket.send(SendThis.encode())

    RESPONSE = Socket.recv(BUFFER_SIZE).decode()
    RESPONSE = str(RESPONSE)
    HEADER, DATA = RESPONSE.split(SecretSeparator, 1)

    global LoginStatus
    if HEADER == "LOGIN_SUCCES":
        LoginStatus = True
        MyUsername = Username
    if HEADER == "LOGIN_FAILED":
        LoginStatus = False

    Socket.close()

    try:
        LastDATA = DATA
    finally:
        del (
            DATA,
            HEADER,
            LoginData,
            Password,
            RESPONSE,
            SendThis,
            Socket,
            TCP_IP,
            TCP_PORT,
            Username,
        )


def LoginMenu_GUI():
    """Menampilkan GUI dari Menu Login"""
    global MyUsername, LastDATA, LoginMenu, RegisterMenu

    def Login():
        """Perintah yang Dijalankan Ketika Login Button di Tekan"""
        try:
            ClientLogin(LoginMenu_UsernameEntry.get(), LoginMenu_PasswordEntry.get())
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

    LoginMenu = customtkinter.CTkToplevel(root)
    LoginMenu.transient(root)
    LoginMenu.iconbitmap(".icon/SriPandita-FTP.ico")
    LoginMenu.geometry("400x350")
    LoginMenu.maxsize(400, 350)
    LoginMenu.minsize(400, 350)
    LoginMenu.resizable(False, False)
    LoginMenu.wm_title("")

    LoginMenu_Frame = customtkinter.CTkFrame(master=LoginMenu)
    LoginMenu_Frame.pack(pady=20, padx=60, fill="both", expand=True)

    LoginMenu_Label = customtkinter.CTkLabel(
        master=LoginMenu_Frame, text="Login", font=("Segoe UI", 24)
    )
    LoginMenu_Label.pack(pady=12, padx=10)

    LoginMenu_UsernameEntry = customtkinter.CTkEntry(
        master=LoginMenu_Frame, placeholder_text="Username"
    )
    LoginMenu_UsernameEntry.pack(pady=12, padx=10)

    LoginMenu_PasswordEntry = customtkinter.CTkEntry(
        master=LoginMenu_Frame, placeholder_text="Login", show="*"
    )
    LoginMenu_PasswordEntry.pack(pady=12, padx=10)

    LastDATA = "Silahkan Masukkan Username dan Password."
    LoginMenu_Status = customtkinter.CTkLabel(
        master=LoginMenu_Frame, text=LastDATA, font=("Segoe UI", 12)
    )

    LoginMenu_LoginButton = customtkinter.CTkButton(
        master=LoginMenu_Frame, text="Login", command=Login
    )
    LoginMenu_LoginButton.pack(pady=12, padx=10)

    LoginMenu_Status.pack(pady=12, padx=10)

    LoginMenu.protocol("WM_DELETE_WINDOW", LoginMenu.destroy)

    CenterMyWindow(LoginMenu)
    LoginMenu.mainloop()

    try:
        pass
    except:
        pass
    finally:
        del (
            Login,
            LoginMenu_Frame,
            LoginMenu_Label,
            LoginMenu_UsernameEntry,
            LoginMenu_PasswordEntry,
            LoginMenu_Status,
            LoginMenu_LoginButton,
            LoginMenu_Status,
        )


def RegisterMenu_GUI():
    """Menampilkan GUI dari Menu Registrasi"""
    global LastDATA, LoginMenu, RegisterMenu, ClientRegister

    def RegisterAndUpdate():
        """Perintah yang Dijalankan Ketika Tombol Register Ditekan"""
        try:
            ClientRegister(
                RegisterMenu_NewUsernameEntry.get(),
                RegisterMenu_NewPasswordEntry.get(),
                RegisterMenu_PasswordCheckEntry.get(),
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

    RegisterMenu = customtkinter.CTkToplevel(root)
    RegisterMenu.transient(root)
    RegisterMenu.iconbitmap(".icon/SriPandita-FTP.ico")
    RegisterMenu.geometry("400x350")
    RegisterMenu.maxsize(400, 350)
    RegisterMenu.minsize(400, 350)
    RegisterMenu.resizable(False, False)
    RegisterMenu.wm_title("")

    RegisterMenu_Frame = customtkinter.CTkFrame(master=RegisterMenu)
    RegisterMenu_Frame.pack(pady=20, padx=60, fill="both", expand=True)

    RegisterMenu_Label = customtkinter.CTkLabel(
        master=RegisterMenu_Frame, text="Register", font=("Segoe UI", 24)
    )
    RegisterMenu_Label.pack(pady=12, padx=10)

    RegisterMenu_NewUsernameEntry = customtkinter.CTkEntry(
        master=RegisterMenu_Frame, placeholder_text="New Username"
    )
    RegisterMenu_NewUsernameEntry.pack(pady=12, padx=10)

    RegisterMenu_NewPasswordEntry = customtkinter.CTkEntry(
        master=RegisterMenu_Frame, placeholder_text="New Password", show="*"
    )
    RegisterMenu_NewPasswordEntry.pack(pady=12, padx=10)

    RegisterMenu_PasswordCheckEntry = customtkinter.CTkEntry(
        master=RegisterMenu_Frame, placeholder_text="New Passoword", show="*"
    )
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

    try:
        pass
    except:
        pass
    finally:
        del (
            RegisterAndUpdate,
            RegisterMenu_Frame,
            RegisterMenu_Label,
            RegisterMenu_LoginButton,
            RegisterMenu_NewPasswordEntry,
            RegisterMenu_NewUsernameEntry,
            RegisterMenu_PasswordCheckEntry,
            RegisterMenu_Status,
            RegisterMenu_Status,
        )


def SecondMenu_GUI():
    """Menampilan GUI Dashboard Setelah Client Berhasil Login"""
    global LoginStatus, GetDownloadUploadCount, MyUsername
    global DownloadCount, UploadCount, UploadDownload_Label

    GetDownloadUploadCount(MyUsername)

    if LoginStatus:
        UploadDownload = customtkinter.CTkToplevel(root)
        UploadDownload.iconbitmap(".icon/SriPandita-FTP.ico")
        UploadDownload.geometry("400x550")
        UploadDownload.maxsize(400, 550)
        UploadDownload.minsize(400, 550)
        UploadDownload.resizable(False, False)
        UploadDownload.wm_title("Main Menu")

        UploadDownload_Frame = customtkinter.CTkFrame(master=UploadDownload)
        UploadDownload_Frame.pack(pady=20, padx=60, fill="both", expand=True)

        UploadDownload_YNTKTS_Image = customtkinter.CTkImage(
            light_image=PIL.Image.open(".icon/SriPandita-FTP-Home.png"),
            dark_image=PIL.Image.open(".icon/SriPandita-FTP-Home.png"),
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
            master=UploadDownload_Frame, text=SecondMenuHeader, font=("Segoe UI", 18)
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
        UploadDownload.mainloop()

        try:
            pass
        except:
            pass
        finally:
            del (
                SecondMenuHeader,
                UploadDownload,
                UploadDownload_DownloadFiles,
                UploadDownload_Frame,
                UploadDownload_Label,
                UploadDownload_Quit,
                UploadDownload_SeeFiles,
                UploadDownload_UploadFiles,
                UploadDownload_YNTKTS,
                UploadDownload_YNTKTS_Image,
            )


def ShowDownloadMenu_GUI():
    """Menampilkan GUI Menu Download File"""
    global DownloadMenu, LastDATA, CheckPortAvailability

    DownloadFolder = "Download Here"

    def OpenTheUploadDirectory():
        """Membuka Folder Download"""
        OpenDirectory(DownloadFolder)

    def RefreshLists():
        """Mengupdate Tampilan ListBox dari Window"""
        TCP_IP = "127.0.0.1"
        TCP_PORT = CLIENT_PORT

        Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Socket.connect((TCP_IP, TCP_PORT))

        PORT_RANDOM_TRANSFER = random.randint(49152, 65535)
        while not CheckPortAvailability(PORT_RANDOM_TRANSFER):
            PORT_RANDOM_TRANSFER = random.randint(49152, 65535)

        HEADER = "GET_FILES_LIST"
        SendThis = HEADER + SecretSeparator + str(PORT_RANDOM_TRANSFER)
        Socket.send(SendThis.encode())

        TCP_IP_TRANSFER = "127.0.0.1"
        TCP_PORT_TRANSFER = PORT_RANDOM_TRANSFER

        Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Socket.bind((TCP_IP_TRANSFER, TCP_PORT_TRANSFER))
        Socket.listen(1)

        while True:
            Connection_Transfer, Address_Transfer = Socket.accept()

            SaveTo = "FilesListClient.bin"
            file = open(SaveTo, "wb")
            line = Connection_Transfer.recv(BUFFER_SIZE)

            while line:
                file.write(line)
                line = Connection_Transfer.recv(BUFFER_SIZE)

            file.close()
            Connection_Transfer.close()
            Socket.close()
            break

        with open("FilesListClient.bin", "r") as f:
            DATA = f.read()
            f.close()

        DATA = ast.literal_eval(DATA)

        try:
            DownloadMenu_ListBox.delete(0, END)
            for i in DATA:
                DownloadMenu_ListBox.insert(END, i)
            DownloadMenu_UploadFiles_Label.configure(
                text=LastDATA,
                font=("Segoe UI", 12),
            )
        except:
            pass
        finally:
            os.remove("FilesListClient.bin")

    def DownloadSelected():
        """Melakukan Download Untuk File yang di Pilih pada ListBox"""
        for i in DownloadMenu_ListBox.curselection():
            GetFileFromServer(DownloadMenu_ListBox.get(i))
        DownloadMenu_UploadFiles_Label.configure(
            text=LastDATA,
            font=("Segoe UI", 12),
        )

    if DownloadMenu:
        DownloadMenu.destroy()

    if not os.path.exists(DownloadFolder):
        os.mkdir(DownloadFolder)

    DownloadMenu = customtkinter.CTkToplevel(UploadDownload)
    DownloadMenu.transient(UploadDownload)
    DownloadMenu.attributes("-topmost", True)
    DownloadMenu.iconbitmap(".icon/SriPandita-FTP.ico")
    DownloadMenu.geometry("400x450")
    DownloadMenu.maxsize(400, 450)
    DownloadMenu.minsize(400, 450)
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

    DownloadMenu_UploadFilesButton_Frame = customtkinter.CTkFrame(DownloadMenu_Frame)
    DownloadMenu_UploadFilesButton_Frame.pack(side=BOTTOM, fill="x", expand=True)

    LastDATA = "Pilih File Untuk di Download dari Server"
    DownloadMenu_UploadFiles_Label = customtkinter.CTkLabel(
        DownloadMenu_UploadFilesButton_Frame, text=LastDATA, font=("Segoe UI", 12)
    )
    DownloadMenu_UploadFiles_Label.pack(
        pady=(5, 0), padx=10, fill="x", expand=True, side=TOP
    )

    DownloadMenu_UploadFiles_Button = customtkinter.CTkButton(
        master=DownloadMenu_UploadFilesButton_Frame,
        text="Download.",
        command=DownloadSelected,
    )
    DownloadMenu_UploadFiles_Button.pack(
        pady=(0, 10), padx=10, fill="x", expand=True, side=BOTTOM
    )

    DownloadMenu.protocol(
        "WM_DELETE_WINDOW", KombinasiFungsi(UpdateTheCount, DownloadMenu.destroy)
    )

    DarkMyWindowTitleBar(DownloadMenu)
    CenterMyWindow(DownloadMenu)
    DownloadMenu.mainloop()

    try:
        pass
    except:
        pass
    finally:
        del (
            DownloadFolder,
            DownloadMenu,
            DownloadMenu_Frame,
            DownloadMenu_ListBox,
            DownloadMenu_ListBox_Frame,
            DownloadMenu_ListBox_ScrollBar,
            DownloadMenu_OpenDirectory,
            DownloadMenu_Refresh,
            DownloadMenu_SideBySideButton_Frame,
            DownloadMenu_UploadFiles_Button,
            DownloadMenu_UploadFiles_Label,
            DownloadSelected,
            OpenTheUploadDirectory,
            RefreshLists,
        )


def ShowUploadMenu_GUI():
    """Menampilkan GUI Menu Upload File"""
    global UploadMenu, LastDATA

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
    UploadMenu.iconbitmap(".icon/SriPandita-FTP.ico")
    UploadMenu.geometry("400x450")
    UploadMenu.maxsize(400, 450)
    UploadMenu.minsize(400, 450)
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

    LastDATA = "Pilih File Untuk di Upload Ke Server"
    UploadMenu_UploadFiles_Label = customtkinter.CTkLabel(
        UploadMenu_UploadFilesButton_Frame, text=LastDATA, font=("Segoe UI", 12)
    )
    UploadMenu_UploadFiles_Label.pack(
        pady=(5, 0), padx=10, fill="x", expand=True, side=TOP
    )

    UploadMenu_UploadFiles_Button = customtkinter.CTkButton(
        master=UploadMenu_UploadFilesButton_Frame,
        text="Upload.",
        command=UploadSelected,
    )
    UploadMenu_UploadFiles_Button.pack(
        pady=(0, 10), padx=10, fill="x", expand=True, side=BOTTOM
    )

    UploadMenu.protocol(
        "WM_DELETE_WINDOW", KombinasiFungsi(UpdateTheCount, UploadMenu.destroy)
    )

    DarkMyWindowTitleBar(UploadMenu)
    CenterMyWindow(UploadMenu)
    UploadMenu.mainloop()

    try:
        pass
    except:
        pass
    finally:
        del (
            OpenTheUploadDirectory,
            RefreshLists,
            UploadFolder,
            UploadMenu,
            UploadMenu_Frame,
            UploadMenu_ListBox,
            UploadMenu_ListBox_Frame,
            UploadMenu_ListBox_ScrollBar,
            UploadMenu_OpenDirectory,
            UploadMenu_Refresh,
            UploadMenu_SideBySideButton_Frame,
            UploadMenu_UploadFilesButton_Frame,
            UploadMenu_UploadFiles_Button,
            UploadMenu_UploadFiles_Label,
            UploadSelected,
        )


def ShowFilesListMenu_GUI():
    """Menampilkan GUI Menu List Files Pada Server"""
    global FilesListMenu, CLIENT_PORT, SecretSeparator, BUFFER_SIZE

    def RefreshLists():
        """Mengupdate Tampilan ListBox dari Window"""
        TCP_IP = "127.0.0.1"
        TCP_PORT = CLIENT_PORT

        Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Socket.connect((TCP_IP, TCP_PORT))

        PORT_RANDOM_TRANSFER = random.randint(49152, 65535)
        while not CheckPortAvailability(PORT_RANDOM_TRANSFER):
            PORT_RANDOM_TRANSFER = random.randint(49152, 65535)

        HEADER = "GET_FILES_LIST"
        SendThis = HEADER + SecretSeparator + str(PORT_RANDOM_TRANSFER)
        Socket.send(SendThis.encode())

        TCP_IP_TRANSFER = "127.0.0.1"
        TCP_PORT_TRANSFER = PORT_RANDOM_TRANSFER

        Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Socket.bind((TCP_IP_TRANSFER, TCP_PORT_TRANSFER))
        Socket.listen(1)

        while True:
            Connection_Transfer, Address_Transfer = Socket.accept()

            SaveTo = "FilesListClient.bin"
            file = open(SaveTo, "wb")
            line = Connection_Transfer.recv(BUFFER_SIZE)

            while line:
                file.write(line)
                line = Connection_Transfer.recv(BUFFER_SIZE)

            file.close()
            Connection_Transfer.close()
            Socket.close()
            break

        with open("FilesListClient.bin", "r") as f:
            DATA = f.read()
            f.close()

        DATA = ast.literal_eval(DATA)

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
    FilesListMenu.iconbitmap(".icon/SriPandita-FTP.ico")
    FilesListMenu.geometry("400x450")
    FilesListMenu.maxsize(400, 450)
    FilesListMenu.minsize(400, 450)
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
    FilesListMenu.mainloop()

    try:
        pass
    except:
        pass
    finally:
        del (
            FilesListMenu,
            FilesListMenu_Frame,
            FilesListMenu_ListBox,
            FilesListMenu_ListBox_Frame,
            FilesListMenu_ListBox_ScrollBar,
            FilesListMenu_Refresh,
            FilesListMenu_SideBySideButton_Frame,
            RefreshLists,
        )


def KombinasiFungsi(*funcs):
    """Mengkombinasi Beberapa Fungsi"""

    def FungsiTerkombinasi(*args, **kwargs):
        """Mengkombinasi Beberapa Fungsi"""
        for f in funcs:
            f(*args, **kwargs)

    return FungsiTerkombinasi


def UpdateTheCount():
    """Mengupdate Jumlah Statistik Download dan Upload Milik User pada Dashboard"""
    global UploadDownload_Label, MyUsername, UploadCount, DownloadCount

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
    """Fungsi Untuk Melakukan Exit Program Secara Menyeluruh"""
    try:
        root.destroy()
        LoginMenu.destroy()
        RegisterMenu.destroy()
        UploadDownload.destroy()
        UploadMenu.destroy()
    except:
        pass
    finally:
        HEADER = "LOGOUT_EXIT"
        DATA = ""
        SendThis = HEADER + SecretSeparator + str(DATA)

        TCP_IP = "127.0.0.1"
        TCP_PORT = CLIENT_PORT

        Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Socket.connect((TCP_IP, TCP_PORT))
        Socket.send(SendThis.encode())

        Socket.close()

        try:
            pass
        except:
            pass
        finally:
            del (
                DATA,
                HEADER,
                SendThis,
                Socket,
                TCP_IP,
                TCP_PORT,
            )

        exit()


def CenterMyWindow(win):
    """Memindahkan Window TKinter ke Tengah Layar"""
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry("{}x{}+{}+{}".format(width, height, x, y))
    win.deiconify()

    try:
        pass
    except:
        pass
    finally:
        del (
            frm_width,
            height,
            titlebar_height,
            width,
            win_height,
            win_width,
            x,
            y,
        )


def DarkMyWindowTitleBar(window):
    """Mengubah Background dari Title Bar TKinter Menjadi Gelap"""
    window.update()
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 2
    value = ct.c_int(value)
    set_window_attribute(hwnd, rendering_policy, ct.byref(value), ct.sizeof(value))

    try:
        pass
    except:
        pass
    finally:
        del (DWMWA_USE_IMMERSIVE_DARK_MODE, get_parent, hwnd, rendering_policy, value)


def CheckPortAvailability(Port_Number):
    """Mengecek Apakah Port Tersedia atau Tidak

    Args:
        Port_Number (int): Nomor Port yang Akan Dicek

    Returns:
        Boolean: True jika Port Tersedia / False jika Port Sudah Dipakai
    """
    Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        Socket.bind(("127.0.0.1", Port_Number))
    except:
        del Socket
        return False
    else:
        Socket.close()
        del Socket
        return True


def OpenDirectory(OpenThis):
    """Membuka Folder

    Args:
        OpenThis (str): Alamat dari Folder yang Akan Dibuka
    """
    Path = OpenThis
    Path = os.path.realpath(Path)
    os.startfile(Path)

    try:
        pass
    except:
        pass
    finally:
        del (Path,)


def FirstTimeConnectServer():
    """Perintah yang Dijalankan Pada Client Saat Pertama Kali Tersambung ke Server"""
    global CLIENT_PORT, BUFFER_SIZE

    TCP_IP = "127.0.0.1"
    TCP_PORT = 48632

    try:
        Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Socket.connect((TCP_IP, TCP_PORT))
    except ConnectionRefusedError:
        print("Server Tidak Sedang Berjalan...")
        exit()
    else:
        CLIENT_PORT = int(Socket.recv(BUFFER_SIZE).decode())

    try:
        pass
    except:
        pass
    finally:
        del (
            TCP_IP,
            TCP_PORT,
            Socket,
        )


if __name__ == "__main__":
    CLIENT_PORT = 0
    BUFFER_SIZE = 1024
    SecretSeparator = "!@#$%^&*"
    LastDATA = ""
    MyUsername = ""
    LoginStatus = False

    DownloadCount = 0
    UploadCount = 0

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    LoginMenu = None
    RegisterMenu = None
    UploadDownload = None
    UploadMenu = None
    FilesListMenu = None
    DownloadMenu = None
    UploadDownload_Label = None

    FirstTimeConnectServer()

    root = customtkinter.CTk()
    root.iconbitmap(".icon/SriPandita-FTP.ico")
    root.geometry("400x350")
    root.maxsize(400, 350)
    root.minsize(400, 350)
    root.resizable(False, False)
    root.wm_title("Yo Ndak Tau Kok Tanya Saya")

    root_Frame = customtkinter.CTkFrame(master=root)
    root_Frame.pack(pady=20, padx=60, fill="both", expand=True)

    root_Image = customtkinter.CTkImage(
        light_image=PIL.Image.open(".icon/SriPandita-FTP-Home.png"),
        dark_image=PIL.Image.open(".icon/SriPandita-FTP-Home.png"),
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

    CenterMyWindow(root)
    root.mainloop()

    try:
        pass
    except:
        pass
    finally:
        del (
            BUFFER_SIZE,
            CLIENT_PORT,
            DownloadMenu,
            FilesListMenu,
            LastDATA,
            LoginMenu,
            LoginStatus,
            MyUsername,
            RegisterMenu,
            SecretSeparator,
            UploadDownload,
            UploadMenu,
            root,
            root_ButtonImage,
            root_Frame,
            root_Image,
            root_LoginButton,
            root_RegisterButton,
        )

    exit()
