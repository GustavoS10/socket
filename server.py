import socket
import threading
#import os

def handle_client(client_socket, client_address):
    print("Connection from", client_address)

    # Receive the file name and file size
    file_info = client_socket.recv(1024).decode()
    file_name, file_size = file_info.split(':')
    file_size = int(file_size)

    # Save the file to the server's file system
    with open(file_name, 'wb') as file:
        bytes_received = 0
        while bytes_received < file_size:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data)
            bytes_received += len(data)
            print("Progress: {:.2f}%".format(bytes_received / file_size * 100))

    print("File received and saved:", file_name)
    # Envia uma resposta de confirmação ao cliente
    response = "Arquivo recebido com sucesso!"
    client_socket.send(response.encode())
    client_socket.close()

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('localhost', 5000)
server_socket.bind(server_address)

# Start listening for incoming connections
server_socket.listen(1)

print("Server is listening on", server_address)

while True:
    # Accept a connection from a client
    client_socket, client_address = server_socket.accept()

    # Create a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
