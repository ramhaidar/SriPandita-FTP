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
