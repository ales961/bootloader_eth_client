import connection
from PyQt6.QtWidgets import QApplication, QFileDialog
import time

ACK = '0x79'
NACK = '0xF1'
EOT = '0xF5'
JUMP = '0x21'
UPDATE = '0x63'
VER = '0x02'
HELP = '0x10'
CLR = '0x43'
BOOT = '0xFF'

commands = {'jump': JUMP, 'version': VER, 'help': HELP, 'clear': CLR, 'boot': BOOT}

CODE = 0
DATA = 1

if __name__ == '__main__':
    while True:
        try:
            input('Press ENTER to connect...')
            recv_status = CODE
            s = connection.tcpConnect()
            print("Connected")
            while True:
                if recv_status == CODE:
                    found = 0
                    user_input = input()
                    for command in commands:
                        if command == user_input:
                            bytes_data = bytes.fromhex(commands[command].replace('0x', ''))
                            s.sendall(bytes_data)
                            recv_data = s.recv(256)
                            print(recv_data.decode('utf-8'))
                            found = 1
                            break
                    if found == 1:
                        found = 0
                        continue
                    if user_input.startswith('update'):
                        splitted_input = user_input.split(" ")
                        header = int(UPDATE, 16)
                        try:
                            version = int(splitted_input[1])
                        except:
                            print("Incorrect command usage")
                            continue
                        data = bytes([header, version])
                        s.sendall(data)
                        recv_data = s.recv(256)
                        # print(recv_data.decode('utf-8'))
                        recv_status = DATA
                    else:
                        print("Command not found, print help")
                else:
                    app = QApplication([])
                    file_path = QFileDialog.getOpenFileName(None, "Select file", "", "Hex files (*.hex)")
                    with open(file_path[0], "rb") as f:
                        app = None
                        file_path = None
                        start = time.time()
                        while True:
                            data = f.read(512)
                            if not data:
                                s.sendall(bytes.fromhex(EOT.replace('0x', '')))
                                s.close()
                                print("Jumped to application, connection closed")
                                recv_status = CODE
                                end = time.time() - start
                                print(end)
                                break
                            # Send the chunk over the socket
                            header = bytes([0])
                            s.sendall(header + data)
                            raw_answer = s.recv(256)
                            hex_answer = int.from_bytes(raw_answer, byteorder='big')
                            while hex_answer == int(NACK, 16):
                                s.sendall(header + data)
                                hex_answer = s.recv(256)
                            if hex_answer != int(ACK, 16):
                                print(raw_answer.decode('utf-8'))
                                recv_status = CODE
                                break
        except:
            print("Unable to connect")








# while True:
#     if recv_status == CODE:
#         found = 0
#         user_input = input()
#         for command in commands:
#             if command == user_input:
#                 bytes_data = bytes.fromhex(commands[command].replace('0x', ''))
#                 s.sendall(bytes_data)
#                 recv_data = s.recv(256)
#                 print(recv_data.decode('utf-8'))
#                 found = 1
#                 break
#         if found == 1:
#             found = 0
#             continue
#         if user_input.startswith('update'):
#             splitted_input = user_input.split(" ")
#             header = int(UPDATE, 16)
#             try:
#                 version = int(splitted_input[1])
#             except:
#                 print("Incorrect command usage")
#                 continue
#             data = bytes([header, version])
#             s.sendall(data)
#             recv_data = s.recv(256)
#             # print(recv_data.decode('utf-8'))
#             recv_status = DATA
#         else:
#             print("Command not found, print help")
#     else:
#         app = QApplication([])
#         file_path = QFileDialog.getOpenFileName(None, "Select file", "", "Hex files (*.hex)")
#         with open(file_path[0], "rb") as f:
#             app = None
#             file_path = None
#             while True:
#                 data = f.read(512)
#                 if not data:
#                     s.sendall(bytes.fromhex(EOT.replace('0x', '')))
#                     s.close()
#                     print("Jumped to application, connection closed")
#                     recv_status = CODE
#                     exit(0)
#                     break
#                 # Send the chunk over the socket
#                 header = bytes([0])
#                 s.sendall(header + data)
#                 raw_answer = s.recv(256)
#                 hex_answer = int.from_bytes(raw_answer, byteorder='big')
#                 while hex_answer == int(NACK, 16):
#                     s.sendall(header + data)
#                     hex_answer = s.recv(256)
#                 if hex_answer != int(ACK, 16):
#                     print(raw_answer.decode('utf-8'))
#                     recv_status = CODE
#                     break

