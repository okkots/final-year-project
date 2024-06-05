import random
import time
from scapy.all import *
import mysql.connector
import argparse
import subprocess

# Parse command-line arguments or configuration parameters
parser = argparse.ArgumentParser(description='Brute force attack script')
parser.add_argument('--target-ip', type=str, default='192.168.1.1',
                    help='The target IP address (default: 192.168.1.1)')
args = parser.parse_args()
target_ip = args.target_ip

# Use a list of plausible source IP addresses
source_ips = [
    "8.8.8.8",
    "8.8.4.4",
    "1.1.1.1",
    "1.0.0.1",
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

# Create a new table to store the brute force attack data
cursor.execute("""
CREATE TABLE IF NOT EXISTS ssh_brute_force (
    id INT AUTO_INCREMENT PRIMARY KEY,
    target_ip VARCHAR(255) NOT NULL,
    source_ip VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Batch the inserts to reduce database load
batch_size = 100
batch = []

target_mac = get_mac_address(target_ip)

while True:
    for _ in range(100):
        # Use a random source IP from the list
        ip = IP(src=random.choice(source_ips), dst=target_ip)
        tcp = TCP(sport=RandShort(),dport=22)

        # Create an Ethernet layer with the correct source MAC address
        ether = Ether(src=target_mac, dst=get_mac_address(target_ip))

        # Append the Ethernet layer to the packet
        packet = ether/ip/tcp

        send(packet, verbose=0)

        # Add the record to the batch
        batch.append((target_ip, random.choice(source_ips), random.choice(["admin", "user", "guest"])))

        # Flush the batch every 100 records
        if len(batch) >= batch_size:
            cursor.executemany("INSERT INTO ssh_brute_force (target_ip, source_ip, username) VALUES (%s, %s, %s)", batch)
            db.commit()
            batch.clear()

        # Add some randomization to the packet rate and the source port
        time.sleep(random.uniform(1, 5))

# Flush any remaining records
if batch:
    cursor.executemany("INSERT INTO ssh_brute_force (target_ip, source_ip, username) VALUES (%s, %s, %s)", batch)
    db.commit()

# Close the database connection
cursor.close()
db.close()