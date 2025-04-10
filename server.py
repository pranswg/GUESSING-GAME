import socket
import threading
import random

HOST = '127.0.0.1'
PORT = 65432
PASSWORD = "123"

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.sendall(b"Enter password: ")
    password = conn.recv(1024).decode().strip()

    if password != PASSWORD:
        conn.sendall(b"Access denied.\n")
        conn.close()
        return

    conn.sendall(b"Password accepted. Let's play!\nGuess a number between 1 and 100:\n")
    number_to_guess = random.randint(1, 100)
    guess_count = 0

    while True:
        try:
            data = conn.recv(1024).decode().strip()
            guess = int(data)
            guess_count += 1

            if guess < number_to_guess:
                conn.sendall(b"Higher\n")
            elif guess > number_to_guess:
                conn.sendall(b"Lower\n")
            else:
                if guess_count <= 5:
                    rating = "Excellent"
                elif guess_count <= 20:
                    rating = "Very Good"
                else:
                    rating = "Good/Fair"
                conn.sendall(f"Correct! You guessed it in {guess_count} tries. Rating: {rating}\n".encode())
                break
        except Exception as e:
            conn.sendall(b"Invalid input. Please enter a number.\n")

    conn.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[LISTENING] Server is running on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    start_server()
