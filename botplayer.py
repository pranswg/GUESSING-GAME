import socket

HOST = '127.0.0.1'
PORT = 65432
PASSWORD = "francis123"

def bot():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        print(s.recv(1024).decode(), end='')  
        s.sendall(PASSWORD.encode())

        print(s.recv(1024).decode(), end='')  

        low, high = 1, 100
        guess_count = 0

        while True:
            guess = (low + high) // 2
            print(f"[Bot Guess #{guess_count + 1}] Trying {guess}")
            s.sendall(str(guess).encode())
            response = s.recv(1024).decode().strip()
            print(f"[Server Response] {response}")

            guess_count += 1

            if "higher" in response.lower():
                low = guess + 1
            elif "lower" in response.lower():
                high = guess - 1
            elif "correct" in response.lower():
                print(f"Bot guessed the number in {guess_count} attempts!")
                break

if __name__ == "__main__":
    bot()
