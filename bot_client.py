import socket

HOST = '127.0.0.1'
PORT = 65432
PASSWORD = "123"

def bot():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        print(s.recv(1024).decode(), end='')  # Password prompt
        s.sendall(PASSWORD.encode())

        print(s.recv(1024).decode(), end='')  # Welcome message

        low, high = 1, 100
        guess_count = 0

        while True:
            guess = (low + high) // 2
            print(f"[Bot Guess #{guess_count + 1}] Trying {guess}")
            s.sendall(str(guess).encode())
            response = s.recv(1024).decode().strip()
            print(f"[Server Response] {response}")

            guess_count += 1

            if "Higher" in response:
                low = guess + 1
            elif "Lower" in response:
                high = guess - 1
            elif "Correct!" in response:
                break

if __name__ == "__main__":
    bot()
