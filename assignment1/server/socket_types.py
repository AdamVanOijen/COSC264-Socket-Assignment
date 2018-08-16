import socket

class SockWrapper():
    """wrapper for socket object"""
    ENGLISH_TEXT = 1
    MAORI_TEXT = 2
    GERMAN_TEXT = 3
    def __init__(self, socket_number, language):
        self.data = None
        self.req_addr = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('localhost', socket_number))
        self.language = language

    def recieve_data(self):
        self.data, self.req_addr = self.socket.recvfrom(4096)
        return self.data

    def send_data(self, data):
        self.socket.sendto(data, self.req_addr)