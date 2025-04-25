import socket

def start_client(server_ip, server_port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        print(f"Connected to server {server_ip}:{server_port}", flush=True)

        while True:
            message = input("Enter message (type 'exit' to quit): ")
            if message.lower() == 'exit':
                break
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
