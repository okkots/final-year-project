import random
import time
import mysql.connector

# Database connection details
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Sasori'
MYSQL_DATABASE = 'honeypot'

# Connect to the database
cnx = mysql.connector.connect(
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    host=MYSQL_HOST,
    database=MYSQL_DATABASE
)

# Create a cursor object
cursor = cnx.cursor()

# Define the structure of the ddosAttack table
create_table_query = """
    CREATE TABLE IF NOT EXISTS ddosAttack (
        id INT AUTO_INCREMENT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        src_ip VARCHAR(45),
        dst_ip VARCHAR(45),
        protocol VARCHAR(10),
        packet_size INT,
        packet_count INT,
        PRIMARY KEY (id)
    );
"""
cursor.execute(create_table_query)

# Function to generate random IP addresses
def generate_ip():
    return f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

# Function to generate random protocol (TCP, UDP, ICMP)
def generate_protocol():
    protocols = ["TCP", "UDP", "ICMP"]
    return random.choice(protocols)

# Function to generate random packet size
def generate_packet_size():
    return random.randint(50, 1500)

# Function to generate random packet count
def generate_packet_count():
    return random.randint(1, 100)

# Generate DDOS attack data
for i in range(10000):  # Generate 10,000 attack packets
    src_ip = generate_ip()
    dst_ip = generate_ip()
    protocol = generate_protocol()
    packet_size = generate_packet_size()
    packet_count = generate_packet_count()
    
    insert_query = """
        INSERT INTO ddosAttack (src_ip, dst_ip, protocol, packet_size, packet_count)
        VALUES (%s, %s, %s, %s, %s);
    """
    cursor.execute(insert_query, (src_ip, dst_ip, protocol, packet_size, packet_count))
    
    # Commit every 1000 inserts to avoid memory issues
    if i % 1000 == 0:
        cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()