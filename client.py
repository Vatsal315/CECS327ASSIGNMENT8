import socket
import sys


MENU = [
    "What is the average moisture inside my kitchen fridge in the past three hours?",
    "What is the average water consumption per cycle in my smart dishwasher?",
    "Which device consumed more electricity among my three IoT devices?",
]


def main(ip: str, port: int) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((ip, port))
        except OSError as err:
            sys.exit(f"Could not connect to {ip}:{port} ⇒ {err}")

        while True:
            print("\nAvailable Queries:")
            for idx, q in enumerate(MENU, 1):
                print(f"{idx}. {q}")
            print("0. Exit")

            choice = input("Select 0-3 ➜ ").strip()
            if choice == "0":
                break
            if choice not in {"1", "2", "3"}:
                print("Sorry, this query cannot be processed. Please try one of the following:")
                print("What is the average moisture inside my kitchen fridge in the past three hours?")
                print("What is the average water consumption per cycle in my smart dishwasher?")
                print("Which device consumed more electricity among my three IoT devices?")
                continue

            question = MENU[int(choice) - 1]
            sock.sendall(question.encode())
            reply = sock.recv(4096).decode()
            print("\nServer says →", reply)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: python client.py <SERVER_IP> <PORT>")
    main(sys.argv[1], int(sys.argv[2]))
