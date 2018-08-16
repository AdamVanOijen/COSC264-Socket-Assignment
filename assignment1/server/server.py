from socket_types import SockWrapper
from packets import DtRequestIncoming, DtResponseOutgoing
from text_time import TextTime
from datetime import datetime
import sys, socket, select

def main():
    params = sys.argv[1:]
    if len(params) is not 3:
        print("must specify 3 distinct ports")
        return None

    EnglishSocket = SockWrapper(int(params[0]), SockWrapper.ENGLISH_TEXT)
    MaoriSocket = SockWrapper(int(params[1]), SockWrapper.MAORI_TEXT)
    GermanSocket = SockWrapper(int(params[2]), SockWrapper.GERMAN_TEXT)

    sockets = {
        EnglishSocket.socket.fileno(): EnglishSocket,
        MaoriSocket.socket.fileno():   MaoriSocket,
        GermanSocket.socket.fileno():  GermanSocket
    }
    Time = TextTime()
    while True:
        requests = select.select([fileno for fileno, s in sockets.items()],[],[])

        for fileno, sock in sockets.items():
            if fileno in requests[0]:
                data = DtRequestIncoming(sock.recieve_data())
                if data.is_valid:
                    if data.get_value('RequestType') == 1:
                        text = Time.text_date(sock.language)
                    else:
                        text = Time.text_time(sock.language)

                    now = datetime.now()
                    response = DtResponseOutgoing(
                        sock.language,
                        now.year,
                        now.month,
                        now.day,
                        now.hour,
                        now.minute,
                        len(text),
                        text
                    )
                    sock.send_data(response.data)

    EnglishSocket.socket.close()
    MaoriSocket.socket.close()
    GermanSocket.socket.close()

main()

#nc -u localhost 2000 ctrl+d