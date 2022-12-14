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
        Connection, Address = s.accept()

        SaveTo = ("Database\\" + Username + "\\" + NamaFile)
        print(SaveTo)
        file = open(SaveTo, 'wb')
        line = Connection.recv(BUFFER_SIZE)

        while (line):
            file.write(line)
            line = Connection.recv(BUFFER_SIZE)

        file.close()
        Connection.close()
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

        HEADER = "REGISTER_SUCCES"
        DATA = "Anda Telah Berhasil Melakukan Registrasi."
        SendThis = (HEADER + SecretSeparator + DATA)
        Connection.send(SendThis.encode())
    else:  # Percabangan Jika Username Sudah Terpakai
        Write.write(str(ReadString))
        Write.close()

        HEADER = "REGISTER_FAILED"
        DATA = "Username Sudah Terpakai!"
        SendThis = (HEADER + SecretSeparator + DATA)
        Connection.send(SendThis.encode())


# Fungsi Login User
def ServerLogin(DATA):
    # Mendefinisikan NewUsername dan NewPassword dari DATA yang telah diterima
    Username = ast.literal_eval(DATA)[0]
    Password = ast.literal_eval(DATA)[1]

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

    # Mengecek Apakah Username Ada Pada Account.bin atau Tidak
    FoundUsername = False
    try:
        for i in ReadString:
            if (Username == i[0]):
                FoundUsername = True
                ThePassword = i[1]
    except:
        pass

    # Mengecek Apakah Password Login Benar atau Salah
    if (FoundUsername == True and Password == ThePassword):
        HEADER = "LOGIN_SUCCES"
        DATA = "Anda Telah Berhasil Melakukan Login."
        SendThis = (HEADER + SecretSeparator + DATA)
        Connection.send(SendThis.encode())
    else:
        HEADER = "LOGIN_FAILED"
        DATA = "Username dan/atau Password Salah!"
        SendThis = (HEADER + SecretSeparator + DATA)
        Connection.send(SendThis.encode())


# Main Program
if __name__ == '__main__':

    # Definisi SecretSeparator
    SecretSeparator = "!@#$%^&*"

    # Membuat Folder Database jika Tidak Ditemukan
    CheckThis = ("Database")
    if (os.path.exists(CheckThis) == False):
        os.mkdir(CheckThis)

    # Definisi Koneksi Socket
    TCP_IP = '127.0.0.1'
    TCP_PORT = 48632
    BUFFER_SIZE = 1024

    # Menjalankan Koneksi Socket Sebagai Server dan Melakukan Listen Koneksi
    Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Socket.bind((TCP_IP, TCP_PORT))
    Socket.listen(1)

    # Melakukan Perulangan Untuk Menerima Request dari Client Sampai Diberhentikan
    while 1:
        # Mendefinisikan Koneksi dan Alamat
        Connection, Address = Socket.accept()

        # Menerima HEADER dan DATA dari Client
        ReceiveThis = Connection.recv(BUFFER_SIZE).decode()
        ReceiveThis = str(ReceiveThis)
        HEADER, DATA = ReceiveThis.split(SecretSeparator, 1)

        # Menjalankan Tugas Sesuai Request Client
        if (HEADER == "REGISTER"):  # Register Akun
            RegisterThread = threading.Thread(
                target=ServerRegister,
                args=(DATA,)
            )
            RegisterThread.start()
        elif (HEADER == "LOGIN"):  # Login Akun
            LoginThread = threading.Thread(
                target=ServerLogin,
                args=(DATA,)
            )
            LoginThread.start()

    # Menutup Koneksi dan Socket
    Connection.close()
    Socket.close()
