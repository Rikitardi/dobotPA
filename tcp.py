import socket
import threading

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(1)
        while True:
            conn, address = self.sock.accept()
            conn.settimeout(60)
            threading.Thread(target = self.listenToClient,args = (conn,address)).start()

    def listenToClient(self, conn, address, size):
        while True:
            try:
                data = conn.recv(size)
                if data:
                    response = data
                    conn.send(response)
                else:
                    raise error('Client disconnected')
            except:
                conn.close()
                return False

if __name__ == "__main__":
    while True:
        port_num = input("Port? ")
        try:
            port_num = int(port_num)
            break
        except ValueError:
            pass

    ThreadedServer('',port_num).listen()

