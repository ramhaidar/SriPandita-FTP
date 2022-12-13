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

TCP_IP = '127.0.0.1'
TCP_PORT = 48632
BUFFER_SIZE = 1024

UserName = "ContohUserX"
NamaFile = "MyFile.bin"

CheckThis = ("Database\\" + UserName)

if (os.path.exists(CheckThis) == False):
    os.mkdir(CheckThis)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

while 1:
    conn, addr = s.accept()

    SaveTo = ("Database\\" + UserName + "\\" + NamaFile)
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
