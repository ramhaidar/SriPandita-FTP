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
import os
import random
import socket
import threading


def GiveDownloadUploadCount(USERNAME, Connection):
    """Mengirim Statistik Download dan Upload dari User

    Args:
        USERNAME (str): Username yang Akan Dikirim Statistik Download dan Uploadnya
        Connection (socket): Socket yang Akan digunakan Untuk Berkomunikasi
    """
    CheckThis = "Account.bin"
    if not os.path.exists(CheckThis):
        File = open(CheckThis, "w")
        File.write("[]")
        File.close()

    Read = open(CheckThis, "r")
    ReadString = str(Read.read())
    Read.close()
    ReadString = ast.literal_eval(ReadString)

    User_Stats = []
    try:
        for count, value in enumerate(ReadString):
            if USERNAME == value[0]:
                User_Stats.append(ReadString[count][2])
                User_Stats.append(ReadString[count][3])
    finally:
        pass

    HEADER = "GIVE_STATS"
    SendThis = HEADER + SecretSeparator + str(User_Stats)
    Connection.send(SendThis.encode())


def ReceiveFileFromClient(FileName, Username, Connection):
    """Menerima File dari Client

    Args:
        FileName (str): Nama File yang Akan Diterima
        Connection (socket): Socket yang Akan digunakan Untuk Berkomunikasi
    """
    global BUFFER_SIZE, LastDATA, SecretSeparator

    PORT_RANDOM_TRANSFER = random.randint(49152, 65535)
    while not CheckPortAvailability(PORT_RANDOM_TRANSFER):
        PORT_RANDOM_TRANSFER = random.randint(49152, 65535)

    HEADER = "GIVE_PORT"
    SendThis = HEADER + SecretSeparator + str(PORT_RANDOM_TRANSFER)
    Connection.send(SendThis.encode())

    TCP_IP_TRANSFER = "127.0.0.1"
    TCP_PORT_TRANSFER = PORT_RANDOM_TRANSFER

    CheckThis = "Database"
    if not os.path.exists(CheckThis):
        os.mkdir(CheckThis)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP_TRANSFER, TCP_PORT_TRANSFER))
    s.listen(1)

    while True:
        Connection_Transfer, Address_Transfer = s.accept()

        SaveTo = "Database\\" + FileName
        File = open(SaveTo, "wb")
        Line = Connection_Transfer.recv(BUFFER_SIZE)

        while Line:
            File.write(Line)
            Line = Connection_Transfer.recv(BUFFER_SIZE)

        File.close()
        Connection_Transfer.close()
        s.close()
        break

    PlusOneUpload(Username)

    try:
        HEADER = "UPLOAD_SUCCES"
        LastDATA = "File Telah Berhasil di Upload ke Server."
        SendThis = HEADER + SecretSeparator + LastDATA
        Connection.send(SendThis.encode())
    except:
        pass
    finally:
        del (
            Address_Transfer,
            Connection_Transfer,
            File,
            HEADER,
            Line,
            PORT_RANDOM_TRANSFER,
            SaveTo,
            SendThis,
            TCP_IP_TRANSFER,
            TCP_PORT_TRANSFER,
        )


def SendFileToClient(FileName, Username, Connection):
    """Mengirim File ke Client

    Args:
        FileName (str): Nama File yang Akan Dikirim
        Connection (socket): Socket yang Akan digunakan Untuk Berkomunikasi
    """
    global BUFFER_SIZE, LastDATA, SecretSeparator

    PORT_RANDOM_TRANSFER = random.randint(49152, 65535)
    while not CheckPortAvailability(PORT_RANDOM_TRANSFER):
        PORT_RANDOM_TRANSFER = random.randint(49152, 65535)

    HEADER = "GIVE_PORT"
    SendThis = HEADER + SecretSeparator + str(PORT_RANDOM_TRANSFER)
    Connection.send(SendThis.encode())

    TCP_IP_TRANSFER = "127.0.0.1"
    TCP_PORT_TRANSFER = PORT_RANDOM_TRANSFER

    CheckThis = "Database"
    if not os.path.exists(CheckThis):
        os.mkdir(CheckThis)

    Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Socket.bind((TCP_IP_TRANSFER, TCP_PORT_TRANSFER))
    Socket.listen(1)

    Connection_Transfer, Address_Transfer = Socket.accept()

    FullPath = "Database\\" + FileName
    File = open(FullPath, "rb")
    Line = File.read(BUFFER_SIZE)

    while Line:
        Connection_Transfer.send(Line)
        Line = File.read(BUFFER_SIZE)

    File.close()
    Socket.close()

    PlusOneDownload(Username)

    try:
        HEADER = "DOWNLOAD_SUCCES"
        LastDATA = "File Telah Berhasil di Download dari Server."
        SendThis = HEADER + SecretSeparator + LastDATA
        Connection.send(SendThis.encode())
    except:
        pass
    finally:
        del (
            Address_Transfer,
            CheckThis,
            Connection_Transfer,
            File,
            FullPath,
            HEADER,
            Line,
            PORT_RANDOM_TRANSFER,
            SendThis,
            Socket,
            TCP_IP_TRANSFER,
            TCP_PORT_TRANSFER,
        )


def SendFilesListToClient(Port_Number):
    """Mengirim List dari File yang Ada di Database ke Client

    Args:
        Port_Number (str): Port yang akan Digunakan pada Socket
    """
    global BUFFER_SIZE, SecretSeparator

    TCP_IP_TRANSFER = "127.0.0.1"
    TCP_PORT_TRANSFER = int(Port_Number)

    TransferSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TransferSocket.connect((TCP_IP_TRANSFER, TCP_PORT_TRANSFER))

    ListsOnUploadFolder = []
    DatabaseFolder = r"Database\\"
    for Path in os.scandir(DatabaseFolder):
        if Path.is_file():
            ListsOnUploadFolder.append(Path.name)

    with open("FilesListServer.bin", "w") as F:
        F.write(str(ListsOnUploadFolder))
        F.close()

    File = open("FilesListServer.bin", "rb")
    Line = File.read(BUFFER_SIZE)

    while Line:
        TransferSocket.send(Line)
        Line = File.read(BUFFER_SIZE)

    try:
        File.close()
        TransferSocket.close()
    except:
        pass
    finally:
        del (
            DatabaseFolder,
            F,
            File,
            Line,
            ListsOnUploadFolder,
            Path,
            TCP_IP_TRANSFER,
            TCP_PORT_TRANSFER,
            TransferSocket,
        )


def ServerRegister(DATA, Connection):
    """Menangani Proses Registrasi Client

    Args:
        DATA (str): Data Akun Baru dan Password Baru Client
        Connection (socket): Socket yang Akan digunakan Untuk Berkomunikasi
    """
    global LastDATA

    NewUsername = ast.literal_eval(DATA)[0]
    NewPassword = ast.literal_eval(DATA)[1]

    CheckThis = "Account.bin"
    if not os.path.exists(CheckThis):
        File = open(CheckThis, "w")
        File.write("[]")
        File.close()

    Read = open(CheckThis, "r")
    ReadString = str(Read.read())
    Read.close()
    ReadString = ast.literal_eval(ReadString)
    Write = open(CheckThis, "w")

    FoundSameUsername = False
    try:
        for i in ReadString:
            if NewUsername == i[0]:
                FoundSameUsername = True
    finally:
        pass

    if not FoundSameUsername:
        AddThis = [NewUsername, NewPassword, 0, 0]
        ReadString.append(AddThis)
        Write.write(str(ReadString))
        Write.close()

        HEADER = "REGISTER_SUCCES"
        LastDATA = "Anda Telah Berhasil Melakukan Registrasi."
        SendThis = HEADER + SecretSeparator + LastDATA
        Connection.send(SendThis.encode())
    else:
        Write.write(str(ReadString))
        Write.close()

        HEADER = "REGISTER_FAILED"
        LastDATA = "Username Sudah Terpakai!"
        SendThis = HEADER + SecretSeparator + LastDATA
        Connection.send(SendThis.encode())

    try:
        pass
    except:
        pass
    finally:
        del (
            AddThis,
            CheckThis,
            FoundSameUsername,
            HEADER,
            NewPassword,
            NewUsername,
            Read,
            ReadString,
            SendThis,
            Write,
            i,
        )


def ServerLogin(DATA, Connection):
    """Menangani Proses Login Client

    Args:
        DATA (str): Data Akun dan Password Client
        Connection (socket): Socket yang Akan digunakan Untuk Berkomunikasi
    """
    Username = ast.literal_eval(DATA)[0]
    Password = ast.literal_eval(DATA)[1]

    CheckThis = "Account.bin"
    if not os.path.exists(CheckThis):
        File = open(CheckThis, "w")
        File.write("[]")
        File.close()

    Read = open(CheckThis, "r")
    ReadString = str(Read.read())
    Read.close()
    ReadString = ast.literal_eval(ReadString)

    FoundUsername = False
    ThePassword = ""
    try:
        for i in ReadString:
            if Username == i[0]:
                FoundUsername = True
                ThePassword = i[1]
    finally:
        pass

    if FoundUsername and Password == ThePassword:
        HEADER = "LOGIN_SUCCES"
        LastDATA = "Anda Telah Berhasil Melakukan Login."
        SendThis = HEADER + SecretSeparator + LastDATA
        Connection.send(SendThis.encode())
    else:
        HEADER = "LOGIN_FAILED"
        LastDATA = "Username dan/atau Password Salah!"
        SendThis = HEADER + SecretSeparator + LastDATA
        Connection.send(SendThis.encode())

    try:
        pass
    except:
        pass
    finally:
        del (
            CheckThis,
            FoundUsername,
            HEADER,
            Password,
            Read,
            ReadString,
            SendThis,
            ThePassword,
            Username,
            i,
        )


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


def PlusOneDownload(USERNAME):
    """Menambah Counter Download Untuk Username yang Bersangkutan

    Args:
        USERNAME (str): Username yang Akan Ditambah Counter Downloadnya
    """
    CheckThis = "Account.bin"
    if not os.path.exists(CheckThis):
        File = open(CheckThis, "w")
        File.write("[]")
        File.close()

    Read = open(CheckThis, "r")
    ReadString = str(Read.read())
    Read.close()
    ReadString = ast.literal_eval(ReadString)

    try:
        for count, value in enumerate(ReadString):
            if USERNAME == value[0]:
                ReadString[count][2] = ReadString[count][2] + 1
    finally:
        pass

    Write = open(CheckThis, "w")
    Write.write(str(ReadString))
    Write.close()


def PlusOneUpload(USERNAME):
    """Menambah Counter Upload Untuk Username yang Bersangkutan

    Args:
        USERNAME (str): Username yang Akan Ditambah Counter Uploadnya
    """
    CheckThis = "Account.bin"
    if not os.path.exists(CheckThis):
        File = open(CheckThis, "w")
        File.write("[]")
        File.close()

    Read = open(CheckThis, "r")
    ReadString = str(Read.read())
    Read.close()
    ReadString = ast.literal_eval(ReadString)

    try:
        for count, value in enumerate(ReadString):
            if USERNAME == value[0]:
                ReadString[count][3] = ReadString[count][3] + 1
    finally:
        pass

    Write = open(CheckThis, "w")
    Write.write(str(ReadString))
    Write.close()


def HandleClient(Port_Number):
    """Menangani Setiap Request Client

    Args:
        Port_Number (int): Nomor Port yang Akan digunakan oleh Socket
    """
    global SecretSeparator, BUFFER_SIZE, ServerRegister, ServerLogin
    global ReceiveFileFromClient, GiveDownloadUploadCount

    TCP_IP = "127.0.0.1"
    TCP_PORT = Port_Number

    Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Socket.bind((TCP_IP, TCP_PORT))
    Socket.listen(1)

    while 1:
        ConnectionX, AddressX = Socket.accept()

        ReceiveThis = ConnectionX.recv(BUFFER_SIZE).decode()
        ReceiveThis = str(ReceiveThis)
        HEADER, DATA = ReceiveThis.split(SecretSeparator, 1)

        if HEADER == "LOGOUT_EXIT":
            break
        elif HEADER == "REGISTER":
            RegisterThread = threading.Thread(
                target=ServerRegister,
                args=(
                    DATA,
                    ConnectionX,
                ),
            )
            RegisterThread.start()
        elif HEADER == "LOGIN":
            LoginThread = threading.Thread(
                target=ServerLogin,
                args=(
                    DATA,
                    ConnectionX,
                ),
            )
            LoginThread.start()
        elif HEADER == "GET_PORT_FOR_UPLOAD":
            HEADER, DATA, USERNAME = ReceiveThis.split(SecretSeparator, 2)
            ClientUpload = threading.Thread(
                target=ReceiveFileFromClient,
                args=(
                    DATA,
                    USERNAME,
                    ConnectionX,
                ),
            )
            ClientUpload.start()
        elif HEADER == "GET_PORT_FOR_DOWNLOAD":
            HEADER, DATA, USERNAME = ReceiveThis.split(SecretSeparator, 2)
            ClientDownload = threading.Thread(
                target=SendFileToClient,
                args=(
                    DATA,
                    USERNAME,
                    ConnectionX,
                ),
            )
            ClientDownload.start()
        elif HEADER == "GET_FILES_LIST":
            ClientGetFilesList = threading.Thread(
                target=SendFilesListToClient, args=(DATA,)
            )
            ClientGetFilesList.start()
        elif HEADER == "GET_USER_STATS":
            ClientGetStats = threading.Thread(
                target=GiveDownloadUploadCount, args=(DATA, ConnectionX)
            )
            ClientGetStats.start()

    try:
        Connection.close()
        Socket.close()
    except:
        pass
    finally:
        del (
            AddressX,
            ConnectionX,
            DATA,
            HEADER,
            ReceiveThis,
            Socket,
            TCP_IP,
            TCP_PORT,
        )


if __name__ == "__main__":
    BUFFER_SIZE = 1024
    SecretSeparator = "!@#$%^&*"

    CheckThis = "Database"
    if not os.path.exists(CheckThis):
        os.mkdir(CheckThis)

    TCP_IP = "127.0.0.1"
    TCP_PORT = 48632

    Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Socket.bind((TCP_IP, TCP_PORT))
    Socket.listen(1)

    while 1:
        Connection, Address = Socket.accept()

        PORT_RANDOM = random.randint(49152, 65535)
        while not CheckPortAvailability(PORT_RANDOM):
            PORT_RANDOM = random.randint(49152, 65535)

        Connection.send(str(PORT_RANDOM).encode())

        HandleThatClient = threading.Thread(target=HandleClient, args=(PORT_RANDOM,))
        HandleThatClient.start()

    try:
        pass
    except:
        pass
    finally:
        del (
            Address,
            BUFFER_SIZE,
            CheckThis,
            Connection,
            HandleThatClient,
            PORT_RANDOM,
            SecretSeparator,
            SecretSeparator,
            Socket,
            TCP_IP,
            TCP_PORT,
        )

    exit()
