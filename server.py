import socket
import threading
import random

HOST = '127.0.0.1'
PORT = 65432
PASSWORD = "francis123"

def clientcontrol(conn, addr):
    print(f"[Connection Found] {addr} connected.")
    conn.sendall(b"Enter password: ")
    password = conn.recv(1024).decode().strip()

    if password != PASSWORD:
        conn.sendall(b"Wrong password! Access denied.\n")
        conn.close()
        return

    conn.sendall(b"Login successful. Let's play.\nGuess a number between 1 and 100:\n")
    number_to_guess = random.randint(1, 100)
    guess_count = 0

    while True:
        try:
            data = conn.recv(1024).decode().strip()
            guess = int(data)
            guess_count += 1

            if guess < number_to_guess:
                conn.sendall(b"Higher!\n")
            elif guess > number_to_guess:
                conn.sendall(b"Lower!\n")
            else:
                if guess_count <= 5:
                    rating = "Excellent"
                elif guess_count <= 20:
                    rating = "Very Good"
                else:
                    rating = "Good/Fair"
                conn.sendall(f"Correct! You got {guess_count} tries. Your performance rating is: {rating}\n".encode())
                break
        except Exception as e:
            conn.sendall(b"Enter numbers ONLY.\n")

    conn.close()

def startserver():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server is running on {HOST}:{PORT}. Press Ctrl+C to stop the server.")
        
        s.settimeout(1)

        while True:
            try:
                conn, addr = s.accept()
                thread = threading.Thread(target=clientcontrol, args=(conn, addr))
                thread.start()
            except socket.timeout:
                pass
            except KeyboardInterrupt:
                print("\nServer is now shutting down.")
                break

if __name__ == "__main__":
    startserver()
