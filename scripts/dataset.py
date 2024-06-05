import time
import random
import pymysql
from datetime import datetime

# Replace with your own values
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Sasori'
MYSQL_DATABASE = 'honeypot'

NUM_ATTACKERS = 10
ATTACK_DURATION = 600
PACKET_SIZE = 1000
PACKET_INTERVAL = 0.01

# Initialize the variables
packets_sent = 0
bytes_sent = 0

# Connect to the MySQL database
connection = pymysql.connect(host=MYSQL_HOST,
                             user=MYSQL_USER,
                             password=MYSQL_PASSWORD,
                             db=MYSQL_DATABASE)

try:
    # Create a new cursor object
    cursor = connection.cursor()

    # Loop through each attacker
    for i in range(NUM_ATTACKERS):
        # Generate a source IP address for the attacker
        source_ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

        # Simulate the DDoS attack
        start_time = time.time()
        while time.time() - start_time < ATTACK_DURATION:
            # Send a packet
            packets_sent = packets_sent + 1
            bytes_sent = bytes_sent + PACKET_SIZE

            # Insert the attack data into the MySQL database
            query = """
                INSERT INTO ddos_attacks (source_ip, attack_time, attack_type, packets_sent, bytes_sent, duration)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            # Convert the Unix timestamp to a datetime object
            attack_time = datetime.fromtimestamp(int(time.time()))
            data = (source_ip, attack_time, 'DDoS', packets_sent, bytes_sent, ATTACK_DURATION)
            cursor.execute(query, data)

            # Wait for the next packet interval
            time.sleep(PACKET_INTERVAL)

    # Commit the changes
    connection.commit()

finally:
    # Close the database connection
    connection.close()