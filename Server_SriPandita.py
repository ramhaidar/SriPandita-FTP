#!/usr/bin/env python
'''Server dari Program FTP'''
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
import os
import ast
import threading


def ReceiveFilesFromClient():
    TCP_IP = '127.0.0.1'
    TCP_PORT = 48632
    BUFFER_SIZE = 1024

    Username = "ContohUserX"
    NamaFile = "MyFile.bin"

    CheckThis = ("Database\\" + Username)

    if (os.path.exists(CheckThis) == False):
        os.mkdir(CheckThis)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    while 1:
        conn, addr = s.accept()

        SaveTo = ("Database\\" + Username + "\\" + NamaFile)
        print(SaveTo)
        file = open(SaveTo, 'wb')
        line = conn.recv(BUFFER_SIZE)

        while (line):
            file.write(line)
            line = conn.recv(BUFFER_SIZE)

        file.close()
        conn.close()
        s.listen(0)
        s.close()
        break


# Fungsi Registrasi User Baru
def ServerRegister(DATA):
    # Mendefinisikan NewUsername dan NewPassword dari DATA yang telah diterima
    NewUsername = ast.literal_eval(DATA)[0]
    NewPassword = ast.literal_eval(DATA)[1]

    # Membuat File Account.bin Jika File Tersebut Tidak Ditemukan
    CheckThis = ("Database\Account.bin")
    if (os.path.exists(CheckThis) == False):
        file = open(CheckThis, 'w')
        file.write("[]")
        file.close()

    # Membaca Isi dari Account.bin
    Read = open(CheckThis, 'r')
    ReadString = str(Read.read())
    Read.close()
    ReadString = ast.literal_eval(ReadString)
    Write = open(CheckThis, 'w')

    # Mengecek Apakah Username Sudah Terpakai Atau Belum
    FoundSameUsername = False
    try:
        for i in ReadString:
            if (NewUsername == i[0]):
                FoundSameUsername = True
    except:
        pass

    if (FoundSameUsername == False):  # Percabangan Jika Username Belum Terpakai
        AddThis = [NewUsername, NewPassword]
        ReadString.append(AddThis)
        Write.write(str(ReadString))
        Write.close()

        HEADER = "REPLY"
        DATA = "Anda Telah Berhasil Melakukan Registrasi."
        SendThis = (HEADER + SecretSeparator + DATA)
        conn.send(SendThis.encode())
    else:  # Percabangan Jika Username Sudah Terpakai
        Write.write(str(ReadString))
        Write.close()

        HEADER = "REPLY"
        DATA = "Username Sudah Terpakai!"
        SendThis = (HEADER + SecretSeparator + DATA)
        conn.send(SendThis.encode())


# Fungsi Login User
def ServerLogin(DATA):
    pass


if __name__ == '__main__':

    SecretSeparator = "!@#$%^&*"

    CheckThis = ("Database")
    if (os.path.exists(CheckThis) == False):
        os.mkdir(CheckThis)
    TCP_IP = '127.0.0.1'
    TCP_PORT = 48632
    BUFFER_SIZE = 1024

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    while 1:
        conn, addr = s.accept()

        ReceiveThis = conn.recv(BUFFER_SIZE).decode()
        ReceiveThis = str(ReceiveThis)
        HEADER, DATA = ReceiveThis.split(SecretSeparator, 1)

        if (HEADER == "REGISTER"):
            RegisterThread = threading.Thread(
                target=ServerRegister,
                args=(DATA,)
            )
            RegisterThread.start()
        elif (HEADER == "LOGIN"):
            LoginThread = threading.Thread(
                target=ServerLogin,
                args=(DATA,)
            )
            LoginThread.start()

    conn.close()
