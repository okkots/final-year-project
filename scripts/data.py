import pymysql
import csv
import os
import subprocess

# Set up the MySQL connection
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='Sasori',
    db='honeypot'
)

# Set up the CSV file in the same directory as the script
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(script_dir, "ddos.csv")

try:
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Execute the SQL query and write the results to the CSV file
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM attack_data')
            rows = cursor.fetchall()

            for row in rows:
                writer.writerow(row)

    # Close the MySQL connection
    connection.close()

    # Prompt if the operation is successful
    print("Data exported to {} successfully!".format(csv_file_path))

    # Open the CSV file
    try:
        subprocess.run(r'start "" "{}"'.format(csv_file_path))
    except FileNotFoundError:
        print("Could not find the default program to open the CSV file.")

except pymysql.MySQLError as e:
    print("Error executing SQL query: {}".format(e))

except Exception as e:
    print("Unexpected error: {}".format(e))