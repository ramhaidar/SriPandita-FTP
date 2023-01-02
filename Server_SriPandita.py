#!/usr/bin/env python
"""Server dari Program FTP SriPandita"""
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
import logging
import os
import socket
import threading

from datetime import datetime
from sys import exit
from time import sleep

try:
    import pyi_splash
except:
    pass
finally:
    pass


def GiveDownloadUploadCount(Connection: socket.socket, Address: tuple, Username: str):
    """Mengirim statistik download dan upload dari user.

    Args:
        Connection (socket.socket): Socket yang akan digunakan Untuk berkomunikasi.
        Address (tuple): Tuple yang berisi alamat dari client dan port yang digunakan.
        Username (str): Username yang akan dikirim statistik download dan uploadnya.
    """
    CheckThis = "Account.bin"
    if not os.path.exists(CheckThis):
        with open(CheckThis, mode="w") as File:
            File.write("[]")

    with open(CheckThis, mode="r") as Read:
        ReadString = str(Read.read())

    ReadString = ast.literal_eval(ReadString)

    User_Stats = []
    for count, value in enumerate(ReadString):
        if Username == value[0]:
            User_Stats.append(ReadString[count][2])
            User_Stats.append(ReadString[count][3])

    HEADER = "SERVER_SENDING_STATS"
    SendThis = str(HEADER + SecretSeparator + str(User_Stats))
    Connection.send(SendThis.encode())

    # * Logger
    now = datetime.now()
    print(
        f"[{now}] [{Address[0]}:{Address[1]}] [Out: {SendThis.split(SecretSeparator)[0]}]"
    )
    logging.info(
        f"[{now}] [{Address[0]}:{Address[1]}] [Out: {SendThis.split(SecretSeparator)[0]}]"
    )


def ReceiveFileFromClient(
    Connection: socket.socket, Address: tuple, FileName: str, Username: str
):
    """Menerima file dari client.

    Args:
        Connection (socket.socket): Socket yang akan digunakan Untuk berkomunikasi.
        Address (tuple): Tuple yang berisi alamat dari client dan port yang digunakan.
        FileName (str): Nama file yang dikirim client.
        Username (str): Username yang mengirim file.
    """
    HEADER = "SERVER_RECEIVE_READY"
    SendThis = str(HEADER + SecretSeparator + str(ServerPort))
    Connection.send(SendThis.encode())

    # * Logger
    now = datetime.now()
    print(
        f"[{now}] [{Address[0]}:{Address[1]}] [Out: {SendThis.split(SecretSeparator)[0]}]"
    )
    logging.info(
        f"[{now}] [{Address[0]}:{Address[1]}] [Out: {SendThis.split(SecretSeparator)[0]}]"
    )

    CheckThis = "Database"
    if not os.path.exists(CheckThis):
        os.mkdir(CheckThis)

    SaveTo = "Database\\" + FileName
    File = open(SaveTo, "wb")
    Line = Connection.recv(BUFFER_SIZE)

    SecretSeparatorByte = bytes(SecretSeparator, "utf-8")
    while Line:
        LineSTR = bytearray(Line).find(SecretSeparatorByte)
        if LineSTR == -1:
            File.write(Line)
            Line = Connection.recv(BUFFER_SIZE)
        else:
            File.write(bytes(bytearray(Line).replace(SecretSeparatorByte, b"")))
            break

    File.close()

    PlusOneUpload(Username)

    HEADER = "SERVER_RECEIVE_SUCCES"
    LastDATA = "File Telah Berhasil di Upload ke Server."
    SendThis = str(HEADER + SecretSeparator + LastDATA)
    Connection.send(SendThis.encode())

    # * Logger
    now = datetime.now()
    print(
        f"[{now}] [{Address[0]}:{Address[1]}] [Out: {SendThis.split(SecretSeparator)[0]}]"
    )
    logging.info(
        f"[{now}] [{Address[0]}:{Address[1]}] [Out: {SendThis.split(SecretSeparator)[0]}]"
    )


def SendFileToClient(
    Connection: socket.socket, Address: tuple, FileName: str, Username: str
):
    """Mengirim file ke client.

    Args:
        Connection (socket.socket): Socket yang akan digunakan Untuk berkomunikasi.
        Address (tuple): Tuple yang berisi alamat dari client dan port yang digunakan.
        FileName (str): Nama file yang diterima client.
        Username (str): Username yang menerima file.
    """
    CheckThis = "Database"
    if not os.path.exists(CheckThis):
        os.mkdir(CheckThis)

    FullPath = "Database\\" + FileName
    File = open(FullPath, "rb")
    Line = File.read(BUFFER_SIZE)

    while Line:
        Connection.send(Line)
        Line = File.read(BUFFER_SIZE)

    DONE = bytes(SecretSeparator, "utf-8")
    Connection.send(DONE)

    File.close()

    PlusOneDownload(Username)

    ReceiveThis = Connection.recv(BUFFER_SIZE).decode()

    # * Logger
    now = datetime.now()
    print(
        f"[{now}] [{Address[0]}:{Address[1]}] [In : {ReceiveThis.split(SecretSeparator)[0]}]"
    )
    logging.info(
        f"[{now}] [{Address[0]}:{Address[1]}] [In : {ReceiveThis.split(SecretSeparator)[0]}]"
    )


def SendFilesListToClient(Connection: socket.socket, Address: tuple):
    """Mengirim list dari file-file yang ada di database ke client.

    Args:
        Connection (socket.socket): Socket yang akan digunakan Untuk berkomunikasi.
        Address (tuple): Tuple yang berisi alamat dari client dan port yang digunakan.
    """
    DatabaseFilesList = []
    DatabaseFolder = "Database\\"
    for Path in os.scandir(DatabaseFolder):
        if Path.is_file():
            DatabaseFilesList.append(Path.name)

    with open("FilesListServer.bin", "w") as File:
        File.write(str(DatabaseFilesList))

    File = open("FilesListServer.bin", "rb")
    Line = File.read(BUFFER_SIZE)

    while Line:
        Connection.send(Line)
        Line = File.read(BUFFER_SIZE)

    DONE = bytes(SecretSeparator, "utf-8")
    Connection.send(DONE)

    ReceiveThis = Connection.recv(BUFFER_SIZE).decode()

    # * Logger
    now = datetime.now()
    print(
        f"[{now}] [{Address[0]}:{Address[1]}] [In : {ReceiveThis.split(SecretSeparator)[0]}]"
    )
    logging.info(
        f"[{now}] [{Address[0]}:{Address[1]}] [In : {ReceiveThis.split(SecretSeparator)[0]}]"
    )

    File.close()

    os.remove("FilesListServer.bin")


def ServerHandleRegister(Connection: socket.socket, Address: tuple, Data: str):
    """Menangani proses registrasi client.

    Args:
        Connection (socket.socket): Socket yang akan digunakan untuk berkomunikasi.
        Address (tuple): Tuple yang berisi alamat dari client dan port yang digunakan.
        Data (str): Data akun baru dan password baru client.
    """
    NewUsername, NewPassword = ast.literal_eval(Data)

    CheckThis = "Account.bin"
    if not os.path.exists(CheckThis):
        with open(CheckThis, "w") as File:
            File.write("[]")

    with open(CheckThis, "r") as File:
        ReadStringTemp = ast.literal_eval(str(File.read()))

    FoundSameUsername = False
    try:
        for i in ReadStringTemp:
            if NewUsername == i[0]:
                FoundSameUsername = True
    finally:
        pass

    ReadString = []
    ReadString.extend(ReadStringTemp)

    if not FoundSameUsername:
        AddThis = [NewUsername, NewPassword, 0, 0]
        ReadString.append(AddThis)
        with open(CheckThis, "w") as File:
            File.write(str(ReadString))

        HEADER = "SERVER_HANDLE_REGISTER_SUCCES"
        LastDATA = "Anda Telah Berhasil Melakukan Registrasi."
        SendThis = str(HEADER + SecretSeparator + LastDATA)
        Connection.send(SendThis.encode())

        # * Logger
        now = datetime.now()
        print(
            f"[{now}] [{Address[0]}:{Address[1]}] [Out: {SendThis.split(SecretSeparator)[0]}]"
        )
        logging.info(
            f"[{now}] [{Address[0]}:{Address[1]}] [Out: {SendThis.split(SecretSeparator)[0]}]"
        )
    else:
        HEADER = "SERVER_HANDLE_REGISTER_FAILED"
        LastDATA = "Username Sudah Terpakai!"
        SendThis = str(HEADER + SecretSeparator + LastDATA)
        Connection.send(SendThis.encode())

        # * Logger
        now = datetime.now()
        print(
            f"[{now}] [{Address[0]}:{Address[1]}] [Out: {SendThis.split(SecretSeparator)[0]}]"
        )
        logging.info(
            f"[{now}] [{Address[0]}:{Address[1]}] [Out: {SendThis.split(SecretSeparator)[0]}]"
        )


def ServerHandleLogin(Connection: socket.socket, Address: tuple, Data: str):
    """Menangani proses login client.

    Args:
        Connection (socket.socket): Socket yang akan digunakan Untuk berkomunikasi.
        Address (tuple): Tuple yang berisi alamat dari client dan port yang digunakan.
        Data (str): Data akun dan password client.
    """
    Username, Password = ast.literal_eval(Data)

    CheckThis = "Account.bin"
    if not os.path.exists(CheckThis):
        with open(CheckThis, "w") as File:
            File.write("[]")

    with open(CheckThis, "r") as File:
        ReadStringTemp = ast.literal_eval(str(File.read()))

    FoundUsername, ThePassword = False, ""
    try:
        for i in ReadStringTemp:
            if Username == i[0]:
                FoundUsername = True
                ThePassword = i[1]
    finally:
        pass

    ReadString = []
    ReadString.extend(ReadStringTemp)
    if FoundUsername and Password == ThePassword:
        HEADER = "SERVER_HANDLE_LOGIN_SUCCES"
        LastDATA = "Anda Telah Berhasil Melakukan Login."
        SendThis = HEADER + SecretSeparator + LastDATA
        Connection.send(SendThis.encode())

        # * Logger
        now = datetime.now()
        print(
            f"[{now}] [{Address[0]}:{Address[1]}] [Out: {SendThis.split(SecretSeparator)[0]}]"
        )
        logging.info(
            f"[{now}] [{Address[0]}:{Address[1]}] [Out: {SendThis.split(SecretSeparator)[0]}]"
        )
    else:
        HEADER = "SERVER_HANDLE_LOGIN_FAILED"
        LastDATA = "Username dan/atau Password Salah!"
        SendThis = str(HEADER + SecretSeparator + LastDATA)
        Connection.send(SendThis.encode())

        # * Logger
        now = datetime.now()
        print(
            f"[{now}] [{Address[0]}:{Address[1]}] [Out: {SendThis.split(SecretSeparator)[0]}]"
        )
        logging.info(
            f"[{now}] [{Address[0]}:{Address[1]}] [Out: {SendThis.split(SecretSeparator)[0]}]"
        )


def PlusOneDownload(Username: str):
    """Menambah counter download untuk username yang bersangkutan.

    Args:
        Username (str): Username yang akan ditambah counter downloadnya.
    """
    CheckThis = "Account.bin"
    if not os.path.exists(CheckThis):
        with open(CheckThis, "w") as File:
            File.write("[]")

    with open(CheckThis, "r") as File:
        ReadString = ast.literal_eval(str(File.read()))

    try:
        for count, value in enumerate(ReadString):
            if Username == value[0]:
                ReadString[count][2] = ReadString[count][2] + 1
    finally:
        pass

    with open(CheckThis, "w") as File:
        File.write(str(ReadString))


def PlusOneUpload(Username: str):
    """Menambah counter upload untuk username yang bersangkutan.

    Args:
        Username (str): Username yang akan ditambah counter uploadnya.
    """
    CheckThis = "Account.bin"
    if not os.path.exists(CheckThis):
        with open(CheckThis, "w") as File:
            File.write("[]")

    with open(CheckThis, "r") as File:
        ReadString = ast.literal_eval(str(File.read()))

    try:
        for count, value in enumerate(ReadString):
            if Username == value[0]:
                ReadString[count][3] = ReadString[count][3] + 1
    finally:
        pass

    with open(CheckThis, "w") as File:
        File.write(str(ReadString))


def FirstTimeClient(Connection: socket.socket, Address: tuple):
    """Mengecek koneksi dengan client untuk pertama kali.

    Args:
        Connection (socket.socket): Socket yang akan digunakan Untuk berkomunikasi.
        Address (tuple): Tuple yang berisi alamat dari client dan port yang digunakan.
    """
    HEADER = "FIRST_TIME_CHECK"
    SendThis = str(HEADER + SecretSeparator + "YNTKTS")
    Connection.send(SendThis.encode())

    # * Logger
    now = datetime.now()
    print(
        f"[{now}] [{Address[0]}:{Address[1]}] [Out: {SendThis.split(SecretSeparator)[0]}]"
    )
    logging.info(
        f"[{now}] [{Address[0]}:{Address[1]}] [Out: {SendThis.split(SecretSeparator)[0]}]"
    )


def HandleClient(Connection: socket.socket, Address: tuple):
    """Menangani setiap request client.

    Args:
        Connection (socket.socket): Socket yang akan digunakan Untuk berkomunikasi.
        Address (tuple): Tuple yang berisi alamat dari client dan port yang digunakan.
    """
    while True:
        ReceiveThis = str(Connection.recv(BUFFER_SIZE).decode())
        if ReceiveThis != "":
            # * Logger
            now = datetime.now()
            print(
                f"[{now}] [{Address[0]}:{Address[1]}] [In : {ReceiveThis.split(SecretSeparator)[0]}]"
            )
            logging.info(
                f"[{now}] [{Address[0]}:{Address[1]}] [In : {ReceiveThis.split(SecretSeparator)[0]}]"
            )

            HEADER, DATA = ReceiveThis.split(SecretSeparator, 1)
            if HEADER == "CLIENT_LOGOUT_EXIT" or HEADER == "CLIENT_EXIT":
                break
            elif HEADER == "CLIENT_REQUEST_REGISTER":
                RegisterThread = threading.Thread(
                    target=ServerHandleRegister,
                    args=(
                        Connection,
                        Address,
                        DATA,
                    ),
                )
                RegisterThread.start()
                RegisterThread.join()
            elif HEADER == "CLIENT_REQUEST_LOGIN":
                LoginThread = threading.Thread(
                    target=ServerHandleLogin,
                    args=(
                        Connection,
                        Address,
                        DATA,
                    ),
                )
                LoginThread.start()
                LoginThread.join()
            elif HEADER == "CLIENT_REQUEST_UPLOAD":
                HEADER, DATA, USERNAME = ReceiveThis.split(SecretSeparator, 2)
                ClientUpload = threading.Thread(
                    target=ReceiveFileFromClient,
                    args=(
                        Connection,
                        Address,
                        DATA,
                        USERNAME,
                    ),
                )
                ClientUpload.start()
                ClientUpload.join()
            elif HEADER == "CLIENT_REQUEST_DOWNLOAD":
                HEADER, DATA, USERNAME = ReceiveThis.split(SecretSeparator, 2)
                ClientDownload = threading.Thread(
                    target=SendFileToClient,
                    args=(
                        Connection,
                        Address,
                        DATA,
                        USERNAME,
                    ),
                )
                ClientDownload.start()
                ClientDownload.join()
            elif HEADER == "CLIENT_REQUEST_FILES_LIST":
                ClientGetFilesList = threading.Thread(
                    target=SendFilesListToClient,
                    args=(
                        Connection,
                        Address,
                    ),
                )
                ClientGetFilesList.start()
                ClientGetFilesList.join()
            elif HEADER == "CLIENT_REQUEST_STATS":
                ClientGetStats = threading.Thread(
                    target=GiveDownloadUploadCount,
                    args=(
                        Connection,
                        Address,
                        DATA,
                    ),
                )
                ClientGetStats.start()
                ClientGetStats.join()
            elif HEADER == "FIRST_TIME":
                FirstTime = threading.Thread(
                    target=FirstTimeClient,
                    args=(
                        Connection,
                        Address,
                    ),
                )
                FirstTime.start()
                FirstTime.join()
        else:
            sleep(1)
    Connection.close()


if __name__ == "__main__":
    """Main program"""
    try:
        sleep(2)
        pyi_splash.close()
    except:
        pass

    logging.basicConfig(
        filename="ServerLog.txt",
        filemode="a",
        format="%(message)s",
        datefmt="%H:%M:%S",
        level=logging.INFO,
    )

    now = datetime.now()
    print(f"[{now}] [0.0.0.0:48632] [Server: Starting...]")
    logging.info(f"[{now}] [0.0.0.0:48632] [Server: Starting...]")

    BUFFER_SIZE = 1024
    SecretSeparator = "!@#$%^&*"

    CheckThis = "Database"
    if not os.path.exists(CheckThis):
        os.mkdir(CheckThis)

    ServerAddress, ServerPort = "0.0.0.0", 48632

    Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Socket.bind((ServerAddress, ServerPort))
    Socket.listen(69)

    sleep(1)

    now = datetime.now()
    print(f"[{now}] [0.0.0.0:48632] [Server: Listening...]")
    logging.info(f"[{now}] [0.0.0.0:48632] [Server: Listening...]")

    while 1:
        Connection, Address = Socket.accept()

        HandleThatClient = threading.Thread(
            target=HandleClient,
            args=(
                Connection,
                Address,
            ),
        ).start()

        Connection, Address = None, None

        sleep(1)

    exit()
