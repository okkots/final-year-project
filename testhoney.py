import socket
import datetime
import http.server
import urllib.parse

# Set the IP address and port number for the honeypot
IP_ADDRESS = '0.0.0.0'
PORT_NUMBER = 8080

# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the specified IP address and port number
sock.bind((IP_ADDRESS, PORT_NUMBER))

# Listen for incoming connections
sock.listen(1)

# Log incoming connections to a file
def log_connection(client_address):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp} - Connection from {client_address}\n"
    with open('honeypot.log', 'a') as log_file:
        log_file.write(log_entry)

# Handle incoming connections and log them
class HoneypotHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Log the connection
        log_connection(self.client_address)

        # Get the requested URL
        parsed_url = urllib.parse.urlparse(self.path)

        # Redirect to the UI page
        self.send_response(302)
        self.send_header('Location', 'http://localhost:8080')
        self.end_headers()

# Create an HTTP server object
httpd = http.server.HTTPServer((IP_ADDRESS, PORT_NUMBER), HoneypotHandler)

# Run the server
httpd.serve_forever()