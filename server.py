import socket

def start_server(host, port):
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the specified address and port
    server_socket.bind((host, port))

    # Enable the server to accept connections (maximum number of queued connections is set to 5)
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        # Accept a connection from a client
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")

        # Receive data from the client
        data = client_socket.recv(1024).decode('utf-8')

        if data:
            print(f"Received from client: {data}")

            # Send the data back to the client
            client_socket.sendall(data.encode('utf-8'))
        else:
            print("Client disconnected")

        # Close the connection with the client
        client_socket.close()

if __name__ == "__main__":
    # Replace 'your_public_ip' with your server's public IP address
    HOST = '131.252.223.181'
    PORT = 8090       # Choose any available port number
    start_server(HOST, PORT)
