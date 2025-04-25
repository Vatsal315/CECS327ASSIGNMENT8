import socket


def get_device_data(query):

    if "average moisture" in query:
        return "The average moisture inside the kitchen fridge in the last three hours is 55% RH."
    elif "average water consumption" in query:
        return "The average water consumption per cycle in the smart dishwasher is 4 gallons."
    elif "device consumed more electricity" in query:
        return "The refrigerator 1 consumed more electricity than the other devices."
    return "Invalid query."

def start_server(host, port):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Server started on {host}:{port}", flush=True)

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection established from {client_address}", flush=True)
            
            while True:
                data = client_socket.recv(1024)
                if not data:
                    print(f"No data received. Closing connection with {client_address}", flush=True)
                    break
                message = data.decode()
                print(f"Received from {client_address}: {message}", flush=True)

                # Process the message based on the query
                response = get_device_data(message)
                client_socket.sendall(response.encode())
            
            client_socket.close()
            print(f"Connection closed with {client_address}", flush=True)
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    host = input("Enter IP address to bind server (e.g., '0.0.0.0' for all interfaces): ")
    port = int(input("Enter server Port: "))
    start_server(host, port)

