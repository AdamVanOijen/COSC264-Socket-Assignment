from socket_types import SockWrapper
from packets import DtRequest, DtResponseIncoming
import sys, socket, select

def main():
    params = sys.argv[1:]

    if len(params) != 3:
        print("must specify date/time, address, port number respectively")
        return None

    if (params[0] != 'date') and (params[0] != 'time'):
        print("first parameter must be \"date\" or \"time\"")

    ClientSocket = SockWrapper()
    ClientSocket.est_server(params[1], params[2])
    sock_file_num = ClientSocket.socket.fileno()

    data = DtRequest(params[0])
    ClientSocket.send_data(data.data)
    response = select.select([sock_file_num],[],[], 1.0)

    if sock_file_num not in response[0]:
        print("no response from server")
        return None

    response_packet = DtResponseIncoming(ClientSocket.recieve_data())
    if response_packet.is_valid:
        print("whole packet byte array: ", response_packet.data)
        print("magicNo = ", hex(response_packet.get_value('magicNo')))
        print("packetType = ", response_packet.get_value('packetType'))
        print("LanguageCode = ", response_packet.get_value('LanguageCode'))
        print("year = ", response_packet.get_value('year'))
        print("month = ", response_packet.get_value('month'))
        print("day = ", response_packet.get_value('day'))
        print("hour = ", response_packet.get_value('hour'))
        print("minute = ", response_packet.get_value('minute'))
        print("length = ", response_packet.get_value('length'))
        print("text = ", response_packet.get_value('text'))

    ClientSocket.socket.close()
main()

