import subprocess

def get_ip_and_mac_addresses():
    ip_address=None
    output = subprocess.check_output("ipconfig /all")
    interfaces = []
    for line in output.decode().split("\n"):
        if "IPv4 Address" in line:
            ip_address = line.split(":")[1].strip()
        if "Physical Address" in line:
            mac_address = line.split(":")[1].strip()
        if ip_address and mac_address:
            interfaces.append((ip_address, mac_address))
            ip_address = None
            mac_address = None
    return interfaces

interfaces = get_ip_and_mac_addresses()
for interface in interfaces:
    print(f"IP Address: {interface[0]}, MAC Address: {interface[1]}")