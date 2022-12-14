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


def SendFilesToServer():
    TCP_IP = '127.0.0.1'
    TCP_PORT = 48632
    BUFFER_SIZE = 1024

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))

    file = open('MyFile.bin', 'rb')
    line = file.read(1024)

    while (line):
        s.send(line)
        line = file.read(1024)

    file.close()
    print('File has been transferred successfully.')

    s.close()


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
    if (LoginStatus == False):
        print("> Status: ", LoginStatus, "\n", sep="")
    else:
        print("> Username: ", Username, "\n", sep="")

    for key in menu_options.keys():
        print(key, '--', menu_options[key])


# Melakukan Registrasi
def ClientRegister():
    # Input Username
    NewUsername = str(input("Masukkan Username: "))
    # Error Jika Username Kosong
    if (len(NewUsername) == 0):
        input("Username Tidak Boleh Kosong!")
        return  # Exit Function

    # Input Password
    NewPassword = str(input("Masukkan Password Baru: "))
    # Error Jika Panjang Password Kurang dari 8 Karakter
    if (len(NewPassword) < 8):
        input("Password Harus Memiliki 8 Karakter atau Lebih!")
        return  # Exit Function

    # Input Password Untuk Konfirmasi
    PasswordCheck = str(input("Masukkan Password Lagi: "))
    # Error Jika Kedua Input Password Tidak Sama
    if (NewPassword != PasswordCheck):
        input("Password tidak cocok!")
        return  # Exit Function

    # Convert Password to MD5 Hash
    NewPassword = hashlib.md5(NewPassword.encode('utf-8')).hexdigest()

    # Mendifinisikan Koneksi Socket
    TCP_IP = '127.0.0.1'
    TCP_PORT = 48632
    BUFFER_SIZE = 1024
    HEADER = "REGISTER"
    RegistrationData = [NewUsername, NewPassword]
    SendThis = (HEADER + "!@#$%^&*" + str(RegistrationData))

    # Melakukan Koneksi ke Server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))

    # Mengirim DATA Registrasi ke Server
    s.send(SendThis.encode())
    RESPONSE = s.recv(BUFFER_SIZE).decode()

    # Menerima RESPONSE dari Server
    RESPONSE = str(RESPONSE)
    HEADER, DATA = RESPONSE.split(SecretSeparator, 1)

    # Mengoutputkan Response dari Server
    print(DATA, sep="", end="")

    # Menutup Koneksi Socket
    s.close()
    input()


def ClientLogin():
    print('Handle option \'Option 2\'')


if __name__ == '__main__':
    SecretSeparator = "!@#$%^&*"

    LoginStatus = False
    Username = ""

    while (True):
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
                input("Anda sudah melakukan Registrasi.")
        elif option == 2:
            if (LoginStatus == False):
                os.system('cls')
                ClientLogin()
            else:
                input("Anda sudah melakukan Login.")
        elif option == 3:
            os.system('cls')
            print()
        elif option == 4:
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
