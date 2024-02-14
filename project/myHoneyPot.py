import socket
import threading
import time
import logging

# Set up logging
logging.basicConfig(filename='honeypot.log', level=logging.INFO)

# Function to handle client connections
def handle_client(client_socket, client_address):
    # Get client IP address
    client_ip = client_address[0]
    logging.info(f'Connection from {client_ip}')
    
    # Send response to client
    client_socket.send(b'Welcome to the honeypot!')
    
    # Close connection
    client_socket.close()

# Function to block IP addresses
def block_ip(ip_address):
    # Add IP address to blocked list
    blocked_ips.append(ip_address)
    
    # Log blocked IP address
    logging.info(f'Blocked IP: {ip_address}')
    
    # Wait for a specified time before unblocking the IP address
    time.sleep(60)
    
    # Remove IP address from blocked list
    blocked_ips.remove(ip_address)

# Create a list to store blocked IP addresses
blocked_ips = []

# Create a dictionary to store connection attempts
connection_attempts = {}

# Create a socket to listen for incoming connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))
server_socket.listen(5)

# Start the honeypot
while True:
    # Accept incoming connection
    client_socket, client_address = server_socket.accept()
    
    # Check if the IP address is blocked
    if client_address[0] in blocked_ips:
        # Close the connection and ignore the client
        client_socket.close()
    else:
        # Handle the client connection in a separate thread
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()
        
        # Check if the number of connection attempts from this IP address exceeds the limit
        if client_address[0] in connection_attempts:
            connection_attempts[client_address[0]] += 1
            
            # If the limit is exceeded, block the IP address
            if connection_attempts[client_address[0]] > 5:
                block_ip(client_address[0])
        else:
            connection_attempts[client_address[0]] = 1