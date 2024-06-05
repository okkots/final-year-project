import pymysql
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from signup import signup_page
from login import authenticate

import threading
import socket
import ipaddress

# Set page config only once
st.set_page_config(page_title='Chungu', page_icon=':computer:', layout='wide', initial_sidebar_state='expanded', menu_items=None)

# Define the function to monitor traffic
def monitor_traffic(port_number, ip_address):
    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the specified IP address and port number
    sock.bind((ip_address, port_number))

    # Listen for incoming connections
    sock.listen(1)

    # Monitor traffic
    while True:
        conn, addr = sock.accept()
        data = conn.recv(1024)
        print(f"Received data from {addr}: {data.decode()}")

# Define a thread to run the monitoring function in the background
def run_monitoring_function(port_number, ip_address):
    threading.Thread(target=monitor_traffic, args=(port_number, ip_address)).start()

# Function to check if a port is open
def is_port_open(ip_address, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        sock.connect((ip_address, port))
        sock.close()
        return True
    except socket.error:
        return False

# Add a monitor traffic button on the top right of the page
monitor_button = st.button("Monitor Traffic", key="monitor_button")

# Initialize a variable to track the status of the monitoring function
monitoring = False

# Add an event handler for the monitor button
if monitor_button:
    if not monitoring:
        # Prompt the user to input an IP address
        ip_address = st.text_input("Enter IP address:")

        # Check if the IP address is valid
        try:
            ipaddress.ip_address(ip_address)
        except ValueError:
            st.error("Invalid IP address")
            ip_address = None

        if ip_address:
            # Get a list of available ports on the IP address
            ports = [port for port in range(1,65535) if is_port_open(ip_address, port)]

            # Display the available ports to the user
            if ports:
                selected_ports = st.multiselect("Select ports to monitor:", ports)
            else:
                st.error("No available ports found")
                selected_ports = None

            if selected_ports:
                # Start monitoring traffic on the selected ports
                for port in selected_ports:
                    st.button(f"Running on {ip_address}:{port}", key=f"monitor_button_{ip_address}_{port}", disabled=True)
                    run_monitoring_function(port, ip_address)

                monitoring = True
            else:
                st.error("No ports selected")
    else:
        st.button("Monitor Traffic", key="monitor_button", disabled=False)
        monitoring = False
    
# Sample data for traps
sample_traps = pd.DataFrame({
    'ID': [1, 2, 3, 4, 5],
    'Name': ['Trap 1', 'Trap 2', 'Trap 3', 'Trap 4', 'Trap 5'],
    'Status': ['Active', 'Inactive', 'Active', 'Inactive', 'Active'],
    'Last Triggered': ['2023-01-01', '', '2023-02-01', '', '2023-03-01']
})

sample_logs = pd.DataFrame({
    'Date': pd.date_range(start='2024-04-01', periods=10, freq='D')+ pd.to_timedelta(np.random.randint(0, 86400, 10), unit='s'),
    'IP': np.random.choice(['192.168.1.1', '10.0.0.1', '172.16.0.1'], size=10),
    'Event': np.random.choice(['Connection Attempt', 'Login Failure', 'File Access'], size=10),
    'Status': np.random.choice(['Success', 'Failure'], size=10)
})

sample_analytics = pd.DataFrame({
    'Event': ['Connection Attempt', 'Login Failure', 'File Access'],
    'Count': [50, 30, 20]
})

THEME_MAP = {
    'light': 'light',
    'dark': 'dark',
    'cerulean': 'cerulean',
    'corporate': 'corporate',
    'darkgrid': 'darkgrid',
    'highcontrast': 'highcontrast',
    'retro': 'retro',
    'slate': 'slate'
}

MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Sasori'
MYSQL_DATABASE = 'honeypot'


def format_time_for_chart(date):
    return date.strftime('%H:%M') if date.hour < 20 else date.strftime('%H:00')
def fetch_blocked_ips():
    connection = pymysql.connect(host=MYSQL_HOST,
                                 user=MYSQL_USER,
                                 password=MYSQL_PASSWORD,
                                 db=MYSQL_DATABASE)

    try:
        query = "SELECT ip FROM blocked_ips;"
        df = pd.read_sql(query, connection)
    finally:
        connection.close()

    return df['ip'].tolist()

def add_blocked_ip(ip):
    connection = pymysql.connect(host=MYSQL_HOST,
                                 user=MYSQL_USER,
                                 password=MYSQL_PASSWORD,
                                 db=MYSQL_DATABASE)

    try:
        query = f"INSERT INTO blocked_ips (ip) VALUES ('{ip}');"
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
    finally:
        connection.close()

def fetch_ssh_brute_force_logs():
    connection = pymysql.connect(host=MYSQL_HOST,
                                 user=MYSQL_USER,
                                 password=MYSQL_PASSWORD,
                                 db=MYSQL_DATABASE)

    try:
        query = "SELECT * FROM ssh_brute_force;"
        df = pd.read_sql(query, connection)
    finally:
        connection.close()

    return df

def fetch_idor_attacks():
    connection = pymysql.connect(host=MYSQL_HOST,
                                 user=MYSQL_USER,
                                 password=MYSQL_PASSWORD,
                                 db=MYSQL_DATABASE)

    try:
        query = "SELECT id, ip_address, destination_port, start_time, end_time, duration, packets_sent, bytes_sent FROM idordata;"
        df = pd.read_sql(query, connection)
    finally:
        connection.close()

    return df

def fetch_dos_attacks():
    connection = pymysql.connect(host=MYSQL_HOST,
                                 user=MYSQL_USER,
                                 password=MYSQL_PASSWORD,
                                 db=MYSQL_DATABASE)

    try:
        query = "SELECT id, timestamp, src_ip, dst_ip, protocol, packet_size, packet_count FROM ddosattack;"
        df = pd.read_sql(query, connection)
    finally:
        connection.close()

    return df
#def check_and_block_ip(logs):
 #   blocked_ips = fetch_blocked_ips()

  #  failed_logins = logs[logs['Event'] == 'Login Failure']
  #  failed_logins['Date'] = pd.to_datetime(failed_logins['Date'])
    #failed_logins['Time'] = pd.to_timedelta(failed_logins['Time'], unit='ns')
   # failed_logins['Timestamp'] = failed_logins['Date'] + failed_logins['Time']

  #  login_attempts = failed_logins.groupby('IP').filter(lambda x: len(x) > 5)

 #   for index, row in login_attempts.iterrows():
  #      if row['IP'] not in blocked_ips:
   #         add_blocked_ip(row['IP'])

def display_blocked_ips(blocked_ips):
    st.write('## Blocked IPs')
    st.dataframe(blocked_ips)

def change_theme(theme):
    st.write('Changing theme to {}...'.format(theme))
    st.markdown('''<style>
    body {{
        /* background-color: {}; */
        color: #{{settings.text_color}};
    }}
    </style>''', unsafe_allow_html=True)
    st.query_params['theme'] = THEME_MAP[theme]
# Function to log out the user
def logout():
    st.write('Logging out...')
    st.experimental_set_query_params(logout=True)

# Main app layout for Settings page
def settings_page():
    st.title('Chungu - Settings')
    
    # Sub-sections for Settings page
    st.write('### Change Theme')
    theme = st.selectbox('Select a theme:', ['light', 'dark', 'cerulean', 'corporate', 'darkgrid', 'highcontrast', 'retro', 'slate'])
    if st.button('Apply'):
        change_theme(theme)

    st.write('### Logout')
    if st.button('Logout'):
        logout()

    st.write('### More Settings')
    # Add other settings options here
    st.write('Other settings options will be displayed here.')
# Function to display logs
def display_logs(logs):
    st.write('## Attack Logs')

    # Display brute force attacks
    st.write('### Brute Force Attacks')
    brute_force_logs = fetch_ssh_brute_force_logs()
    st.dataframe(brute_force_logs.style.set_table_styles([{'selector': 'th', 'props': [('max-width', '100px')]}]), height=300)

    # Display IDOR attacks
    st.write('### IDOR Attacks')
    idor_logs = fetch_idor_attacks()
    st.dataframe(idor_logs.style.set_table_styles([{'selector': 'th', 'props': [('max-width', '100px')]}]), height=300)

    # Display DoS attacks
    st.write('### DoS Attacks')
    dos_logs = fetch_dos_attacks()
    st.dataframe(dos_logs.style.set_table_styles([{'selector': 'th', 'props': [('max-width', '100px')]}]), height=300)

    # Display a subset of the logs (up to 50 rows)
    st.write('### Sample Logs')
    num_rows = min(50, len(logs))
    st.dataframe(logs.sample(num_rows, random_state=42).style.set_table_styles([{'selector': 'th', 'props': [('max-width', '100px')]}]), height=300)

    # ... other Streamlit commands ...
# Function to display analytics
def display_attack_analytics(logs):
    st.write('## Attack Analytics')

    # Count the number of occurrences of each attack type
    attack_counts = logs['Event'].value_counts()

    # Create a stacked dataframe of the attack counts
    stacked_df = attack_counts.reset_index().set_index('Event').stack().reset_index()
    stacked_df.columns = ['Event', 'Attack Type', 'Count']

    # Create a stacked bar chart of the attack counts
    fig, ax = plt.subplots()
    ax.pie(stacked_df['Count'], labels=stacked_df['Event'], autopct='%1.1f%%')
    ax.axis('equal')
    ax.set_title('Attack Frequency by Attack Type')
    st.pyplot(fig)

    # Count the number of occurrences of each attack type for brute force, DDoS, and idor attacks
    attack_type_counts = logs.groupby('Event').size().reset_index(name='Count')

    # Create a stacked dataframe of the attack counts
    stacked_df = attack_type_counts.set_index('Event').stack().reset_index()
    stacked_df.columns = ['Event', 'Attack Type', 'Count']

    # Create a stacked bar chart of the attack counts
    fig, ax = plt.subplots()
    ax.pie(stacked_df['Count'], labels=stacked_df['Event'], autopct='%1.1f%%')
    ax.axis('equal')
    ax.set_title('Attack Frequency by Attack Type')
    st.pyplot(fig)

    # Brute force attacks
    brute_force_logs = fetch_ssh_brute_force_logs()

    # Count the number of occurrences of each IP address
    ip_counts = brute_force_logs['source_ip'].value_counts()

    # Create a pie chart of the IP addresses
    fig, ax = plt.subplots()
    ax.pie(ip_counts, labels=ip_counts.index, autopct='%1.1f%%')
    ax.axis('equal')
    ax.set_title('Brute Force Attacks by IP Address')
    st.pyplot(fig)

    # idor attacks
    idor_logs = fetch_idor_attacks()

    # Count the number of occurrences of each URL
    port_counts = idor_logs['destination_port'].value_counts()

    # Create a pie chart of the URLs
    fig, ax = plt.subplots()
    ax.pie(port_counts, labels=port_counts.index, autopct='%1.1f%%')
    ax.axis('equal')
    ax.set_title('Idor Attacks by ports')
    st.pyplot(fig)

    # DDoS attacks
    dos_logs = fetch_dos_attacks()

    # Count the number of occurrences of each IP address
    ip_counts = dos_logs['src_ip'].value_counts()

    # Create a pie chart of the IP addresses
    fig, ax = plt.subplots()
    ax.pie(ip_counts, labels=ip_counts.index, autopct='%1.1f%%')
    ax.axis('equal')
    ax.set_title('DDoS Attacks by IP Address')
    st.pyplot(fig)
    
    
def display_time_based_analytics(logs):
    st.write('## Time-based Analytics')

    # Filter logs to only include Login Failure events
    login_failures = logs[logs['Event'] == 'Login Failure']

    # Group login failures by four-hour blocks
    time_grouped_failures = login_failures.groupby(pd.Grouper(key='Date', freq='4H')).size().reset_index(name='Count')

    # Format the time column for the chart
    time_grouped_failures['Time'] = time_grouped_failures['Date'].apply(format_time_for_chart)

    # Create a bar chart
    st.bar_chart(time_grouped_failures.set_index('Time')['Count'])

# Function to display active traps
def display_active_traps(traps):
    st.write('## Active Traps')
    active_traps = traps[traps['Status'] == 'Active']
    st.dataframe(active_traps)

# Function to display triggered traps
def display_triggered_traps(traps):
    st.write('## Triggered Traps')
    triggered_traps = traps[traps['Last Triggered'] != '']
    st.dataframe(triggered_traps)

# Function to remove a trap
def remove_trap(traps, trap_id):
    traps = traps[traps['ID'] != trap_id]
    return traps

# Function to add a trap
def add_trap(traps, trap_name):
    new_trap = pd.DataFrame({
        'ID': [len(traps) + 1],
        'Name': [trap_name],
        'Status': ['Inactive'],
        'Last Triggered': ['']
    })
    traps = pd.concat([traps, new_trap], ignore_index=True)
    
    return traps

# Main app layout for Traps page
def traps_page():
    global sample_traps
    st.title('Chungu - Traps')

    connection = pymysql.connect(host=MYSQL_HOST,
                                 user=MYSQL_USER,
                                 password=MYSQL_PASSWORD,
                                 db=MYSQL_DATABASE)

    try:
        query = "SELECT ID, Name, Status, Last_Triggered FROM trapslist;"
        df = pd.read_sql(query, connection)
        sample_traps = df
        m_value = len(sample_traps)
        st.write('### Active Traps')
        display_active_traps(sample_traps)

        st.write('### Remove Trap')
        if m_value > 0:
            selected_trap_id = st.number_input('Enter the ID of the trap to remove:', min_value=1, max_value=m_value) # type: ignore
            if st.button('Remove Trap'):
                if 1 <= selected_trap_id <= len(sample_traps):
                    sample_traps = remove_trap(sample_traps, selected_trap_id)
                    st.write('Trap with ID {} has been removed.'.format(selected_trap_id))
                else:
                    st.write('Invalid trap ID. Please enter a value between 1 and {}.'.format(len(sample_traps)))
        else:
            st.write('No traps available to remove.')
        st.write('### Add Trap')
        new_trap_name = st.text_input('Enter the name of the new trap:')
        if st.button('Add Trap'):
            sample_traps = add_trap(sample_traps, new_trap_name)
            st.write('Trap with name "{}" has been added.'.format(new_trap_name))

     #   display_triggered_traps(sample_traps)

    finally:
        connection.close()

# Main app layout
def main():
    
    st.title('Chungu')
    
    #print( sample_traps.columns)
    
    # Dropdown menu
    menu = ['Home', 'Traps', 'Stats', 'Settings', 'Logs','Blocked IPs']
    choice = st.sidebar.selectbox('Menu', menu)
    
    if choice == 'Home':
        st.write('Welcome to the Chungu')
        display_logs(sample_logs)
        display_attack_analytics(sample_analytics)
        
    elif choice == 'Traps':
        traps_page()
        
    elif choice == 'Stats':
        st.write('## Statistics')
        # Add statistical analysis of the honeypot data here
        display_attack_analytics(sample_analytics)
        
    elif choice == 'Settings':
        settings_page()
        
    elif choice == 'Logs':
        st.write('## Logs')
        # Display the full log data
        display_logs(sample_logs)
                # Add block IP mechanism
        #check_and_block_ip(sample_logs)

        st.write('## Blocked IPs')
        blocked_ips = fetch_blocked_ips()
        st.write(blocked_ips)
    
    elif choice == 'Blocked IPs':
        blocked_ips = fetch_blocked_ips()
        display_blocked_ips(blocked_ips)

if __name__ == '__main__':
    main()