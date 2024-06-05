import socket
import threading

# Honeypot host and port
honeypot_host = '127.0.0.1'
honeypot_port = 12345

# Number of attacker threads to simulate
num_attackers = 100

# Function to simulate a DDOS attack
def attack():
    # Create a socket to connect to the honeypot
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((honeypot_host, honeypot_port))

    # Send a message to the honeypot
    client_socket.send(b'Attack!')

    # Close the socket
    client_socket.close()

# Start the DDOS attack
for i in range(num_attackers):
    attacker = threading.Thread(target=attack)
    attacker.start()