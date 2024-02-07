import socket
import threading

class HoneyPotServer:
    def __init__(self, ip_address, port_number):
        self.ip_address = ip_address
        self.port_number = port_number
        self.connections = set()

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.ip_address, self.port_number))
        server_socket.listen(5)
        print(f"Listening on {self.ip_address}:{self.port_number}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")
            connection_handler = ConnectionHandler(client_socket, client_address)
            connection_handler.start()
            self.connections.add(connection_handler)

class ConnectionHandler(threading.Thread):
    def __init__(self, client_socket, client_address):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.client_address = client_address

    def run(self):
        print(f"Handling connection from {self.client_address}")
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                print(f"Received data from {self.client_address}: {data}")
            except Exception as e:
                print(f"Error receiving data from {self.client_address}: {e}")
                break
        self.client_socket.close()
        print(f"Closed connection from {self.client_address}")

if __name__ == "__main__":
    server = HoneyPotServer("0.0.0.0", 8080)
    server.start()