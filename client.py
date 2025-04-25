import socket

VALID_QUERIES = [
    "What is the average moisture inside my kitchen fridge in the past three hours?",
    "What is the average water consumption per cycle in my smart dishwasher?",
    "Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?"
]

def start_client(server_ip, server_port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        print(f"Connected to server {server_ip}:{server_port}", flush=True)

        while True:
            message = input("Enter message (type 'exit' to quit): ")
            if message.lower() == 'exit':
                break
            
            # Check if the message is valid
            if message not in VALID_QUERIES:
                print(f"Sorry, this query cannot be processed. Please try one of the following:")
                for query in VALID_QUERIES:
                    print(f"- {query}")
                continue

            # Send the valid query to the server
            client_socket.sendall(message.encode())
            response = client_socket.recv(1024).decode()
            print(f"Server Response: {response}", flush=True)
    
        client_socket.close()
    except Exception as e:
        print(f"Client error: {e}")

if __name__ == "__main__":
    server_ip = input("Enter server IP: ")
    server_port = int(input("Enter server Port: "))
    start_client(server_ip, server_port)

