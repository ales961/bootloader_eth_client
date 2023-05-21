import socket

HOST = '169.254.8.45'  # IP address of STM32F4
PORT = 80  # Port number on which lwIP TCP server is running


def tcpConnect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.setblocking(True)
    return s
