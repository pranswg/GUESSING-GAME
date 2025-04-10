import socket

HOST = '127.0.0.1'
PORT = 65432

def player():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        while True:
            data = s.recv(1024).decode()
            if not data:
                break
            print(data, end='')

            if "Correct!" in data or "Access denied" in data:
                break

            msg = input()
            s.sendall(msg.encode())

if __name__ == "__main__":
    player()
