import socket

class SockWrapper():
    """wrapper for socket object"""
    def __init__(self):
        self.data = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_addr = None

    def est_server(self, address, port_no):
        """establish the address and port number of the server we are going to
        send packets to"""
        addr_info = socket.getaddrinfo(
            address,
            port_no,
            family=socket.AF_INET,
            type=socket.SOCK_DGRAM
        )
        self.server_addr = addr_info[-1][-1]

    def recieve_data(self):
        """fetch incoming packet from the socket"""
        self.data = self.socket.recvfrom(4096)[0]
        return self.data

    def send_data(self, data):
        """send packet to the established server"""
        self.socket.sendto(data, self.server_addr)