#!/usr/bin/env python
'''Client dari Program FTP'''
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
from time import sleep
import hashlib
from getpass import getpass


def SendFilesToServer():
    TCP_IP = '127.0.0.1'
    TCP_PORT = 48632
    BUFFER_SIZE = 1024

    Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Socket.connect((TCP_IP, TCP_PORT))

    file = open('MyFile.bin', 'rb')
    line = file.read(1024)

    while (line):
        Socket.send(line)
        line = file.read(1024)

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
    if (LoginStatus == True):  # Menampilkan Username jika LoginStatus bernilai True
        print("> Username: ", Username, "\n", sep="")
    else:  # Menampilkan Status jika LoginStatus bernilai False
        print("> Status: Belum Login", "\n", sep="")

    for key in menu_options.keys():
        print(key, '--', menu_options[key])


# Fungsi Untuk Registrasi
def ClientRegister():
    # Input Username
    NewUsername = str(input("Masukkan Username: "))
    # Error Jika Username Kosong
    if (len(NewUsername) == 0):
        input("Username Tidak Boleh Kosong!")
        return  # Exit Function

    # Input Password
    NewPassword = str(getpass("Masukkan Password Baru: "))
    # Error Jika Panjang Password Kurang dari 8 Karakter
    if (len(NewPassword) < 8):
        input("Password Harus Memiliki 8 Karakter atau Lebih!")
        return  # Exit Function

    # Input Password Untuk Konfirmasi
    PasswordCheck = str(getpass("Masukkan Password Lagi: "))
    # Error Jika Kedua Input Password Tidak Sama
    if (NewPassword != PasswordCheck):
        input("Password tidak cocok!")
        return  # Exit Function

    # Convert Password ke MD5 Hash
    NewPassword = hashlib.md5(NewPassword.encode('utf-8')).hexdigest()

    # Mendifinisikan Koneksi Socket
    TCP_IP = '127.0.0.1'
    TCP_PORT = 48632
    BUFFER_SIZE = 1024
    HEADER = "REGISTER"
    RegistrationData = [NewUsername, NewPassword]
    SendThis = (HEADER + "!@#$%^&*" + str(RegistrationData))

    # Melakukan Koneksi ke Server
    Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Socket.connect((TCP_IP, TCP_PORT))

    # Mengirim DATA Registrasi ke Server
    Socket.send(SendThis.encode())

    # Menerima RESPONSE dari Server
    RESPONSE = Socket.recv(BUFFER_SIZE).decode()
    RESPONSE = str(RESPONSE)
    HEADER, DATA = RESPONSE.split(SecretSeparator, 1)

    # Mengoutputkan Response dari Server
    print(DATA, sep="", end="")

    # Menutup Koneksi Socket
    Socket.close()
    input()

    # Clearing Variables
    del NewUsername, NewPassword, PasswordCheck, TCP_IP, TCP_PORT, BUFFER_SIZE, HEADER, RegistrationData, SendThis, Socket, RESPONSE, DATA


# Fungsi Untuk Login
def ClientLogin():
    # Input Username
    UsernameInput = str(input("Masukkan Username: "))
    # Input Password
    PasswordInput = str(getpass("Masukkan Password: "))

    # Convert Password ke MD5 Hash
    PasswordInput = hashlib.md5(PasswordInput.encode('utf-8')).hexdigest()

    # Mendifinisikan Koneksi Socket
    TCP_IP = '127.0.0.1'
    TCP_PORT = 48632
    BUFFER_SIZE = 1024
    HEADER = "LOGIN"
    LoginData = [UsernameInput, PasswordInput]
    SendThis = (HEADER + "!@#$%^&*" + str(LoginData))

    # Melakukan Koneksi ke Server
    Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Socket.connect((TCP_IP, TCP_PORT))

    # Mengirim DATA Registrasi ke Server
    Socket.send(SendThis.encode())

    # Menerima RESPONSE dari Server
    RESPONSE = Socket.recv(BUFFER_SIZE).decode()
    RESPONSE = str(RESPONSE)
    HEADER, DATA = RESPONSE.split(SecretSeparator, 1)

    # Mengubah LoginStatus Sesuai RESPONSE dari Server
    global LoginStatus
    global Username
    if (HEADER == "LOGIN_SUCCES"):
        LoginStatus = True
        Username = UsernameInput
    if (HEADER == "LOGIN_FAILED"):
        LoginStatus = False

    # Mengoutputkan Response dari Server
    print(DATA, sep="", end="")

    # Menutup Koneksi Socket
    Socket.close()
    input()

    del UsernameInput, PasswordInput, TCP_IP, TCP_PORT, BUFFER_SIZE, HEADER, LoginData, SendThis, Socket, RESPONSE, DATA


# Main Program
if __name__ == '__main__':

    # Definisi SecretSeparator
    SecretSeparator = "!@#$%^&*"

    # Definisi LoginStatus dan Username
    LoginStatus = False
    Username = ""

    # Loop Untuk Menampilkan Menu
    while True:
        os.system('cls')
        ShowClientMenu()
        option = ''
        try:
            option = int(input('Masukkan pilihan: '))
        except:
            pass
        if option == 1:
            if (LoginStatus == False):
                os.system('cls')
                ClientRegister()
            else:
                input(
                    "Anda sudah melakukan Login.\nKeluar Program Terlebih Dahulu Untuk Melakukan Register.")
        elif option == 2:
            if (LoginStatus == False):
                os.system('cls')
                ClientLogin()
            else:
                input(
                    "Anda sudah melakukan Login.\nKeluar Program Terlebih Dahulu Untuk Melakukan Login Ulang.")
        elif option == 3:
            os.system('cls')
            pass
        elif option == 4:
            os.system('cls')
            pass
        elif option == 5:
            print('Terimakasih', sep="", end="")
            sleep(0.321)
            print('.', sep="", end="")
            sleep(0.321)
            print('.', sep="", end="")
            sleep(0.321)
            print('.', sep="", end="")
            sleep(0.75)
            os.system('cls')
            break
        else:
            print('Pilihan yang Anda masukkan salah', sep="", end="")
            sleep(0.123)
            print('.', sep="", end="")
            sleep(0.123)
            print('.', sep="", end="")
            sleep(0.123)
            print('.', sep="", end="")
            input()
