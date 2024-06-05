import socket
import threading
import time
import logging
import tkinter as tk
from tkinter import messagebox

# Set up logging
logging.basicConfig(filename='honeypot.log', level=logging.INFO)

# Function to handle client connections
def handle_client(client_socket, client_address, connection_attempts, blocked_ips):
    # Get client IP address
    client_ip = client_address[0]
    logging.info(f'Connection from {client_ip}')

    # If the IP address is blocked, close the connection
    if client_ip in blocked_ips:
        client_socket.close()
        return

    # Send response to client
    client_socket.send(b'Welcome to the honeypot!')

    # Close connection
    client_socket.close()

    # Increment the number of connection attempts from this IP address
    if client_ip in connection_attempts:
        connection_attempts[client_ip] += 1
    else:
        connection_attempts[client_ip] = 1

    # If the number of connection attempts exceeds the limit, block the IP address
    if connection_attempts[client_ip] > 5:
        block_ip(client_ip, blocked_ips)

# Function to block IP addresses
def block_ip(ip_address, blocked_ips):
    # Add IP address to blocked list
    blocked_ips.append(ip_address)

    # Log blocked IP address
    logging.info(f'Blocked IP: {ip_address}')

    # Wait for a specified time before unblocking the IP address
    time.sleep(60)

    # Remove IP address from blocked list
    blocked_ips.remove(ip_address)

# Function to run the honeypot loop
def honeypot_loop():
    # Create a socket to listen for incoming connections
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(5)

    # Main event loop for the honeypot system
    while True:
        # Accept incoming connection
        client_socket, client_address = server_socket.accept()

        # Handle the client connection in a separate thread
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address, connection_attempts, blocked_ips))
        client_handler.start()

# Create a list to store blocked IP addresses
blocked_ips = []

# Create a dictionary to store connection attempts
connection_attempts = {}

# Create a UI to display the blocked IP addresses
root = tk.Tk()
root.title('Honeypot System')

# Create a variable to store the current number of blocked IP addresses
num_blocked_ips = tk.IntVar()

# Create a label to display the number of blocked IP addresses
num_blocked_label = tk.Label(root, text='Number of blocked IP addresses:')
num_blocked_label.pack()

# Create a label to display the list of blocked IP addresses
blocked_ips_label = tk.Label(root, text='Blocked IP addresses:')
blocked_ips_label.pack()

# Create a listbox to display the list of blocked IP addresses
blocked_ips_listbox = tk.Listbox(root, width=40, height=10)
blocked_ips_listbox.pack()

# Create a button to unblock a selected IP address
unblock_button = tk.Button(root, text='Unblock', command=lambda: unblock_ip(blocked_ips_listbox.curselection()))
unblock_button.pack()

# Start the honeypot system in a separate thread
honeypot_thread = threading.Thread(target=honeypot_loop, daemon=True)
honeypot_thread.start()

# Function to update the list of blocked IP addresses
def update_blocked_ips():
    # Set the number of blocked IP addresses to the current length of the blocked_ips list
    num_blocked_ips.set(len(blocked_ips))

    # Update the listbox with the current blocked IP addresses
    blocked_ips_listbox.delete(0, tk.END)
    for ip_address in blocked_ips:
        blocked_ips_listbox.insert(tk.END, ip_address)

    # Repeat every second
    root.after(1000, update_blocked_ips)

# Function to unblock a selected IP address
def unblock_ip(selected_ips):
    # Remove the selected IP addresses from the blocked list
    for ip_address in selected_ips:
        if ip_address in blocked_ips:
            blocked_ips.remove(ip_address)

    # Update the list of blocked IP addresses
    update_blocked_ips()

# Start updating the list of blocked IP addresses
root.after(1000, update_blocked_ips)

# Main event loop for the Tkinter GUI
root.mainloop()