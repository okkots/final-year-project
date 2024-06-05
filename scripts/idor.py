import mysql.connector
import random
import time
from datetime import datetime
# Database connection details
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Sasori'
MYSQL_DATABASE = 'honeypot'

# Connect to the MySQL database
cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                              host=MYSQL_HOST,
                              database=MYSQL_DATABASE)

# Create a cursor object
cursor = cnx.cursor()

# Prepare the SQL statement to insert the IDOR attack data
add_idorattack = ("INSERT INTO idordata "
                   "(ip_address, destination_port, start_time, end_time, duration, packets_sent, bytes_sent) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s)")

# Function to generate random IP addresses
def generate_ip():
    return f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

# Function to generate random destination port
def generate_destination_port():
    return random.randint(1, 65535)

# Function to generate random start and end times
def generate_start_end_times():
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + random.randint(300, 1800)))
    return start_time, end_time

# Function to calculate duration
def calculate_duration(start_time, end_time):
    start_time_obj = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_time_obj = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    duration = (end_time_obj - start_time_obj).total_seconds()
    return duration

# Generate 20 IDOR attack data entries
for i in range(20):
    ip_address = generate_ip()
    destination_port = generate_destination_port()
    start_time, end_time = generate_start_end_times()
    duration = calculate_duration(start_time, end_time)
    packets_sent = random.randint(1000, 20000)
    bytes_sent = random.randint(100000, 5000000)

    # Insert the IDOR attack data into the idordata table
    cursor.execute(add_idorattack, (ip_address, destination_port, start_time, end_time, duration, packets_sent, bytes_sent))

# Commit the changes
cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()