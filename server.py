import socket
import threading
import os
import re

BUFFER_SIZE = 100
MAX_CONCURRENT_CONNECTIONS = 5

def is_valid_file_info(file_info):
    pattern = r'^[^:]+:\d+$'
    return bool(re.match(pattern, file_info))

# Crie um objeto de bloqueio para sincronização
lock = threading.Lock()

def handle_client(client_socket, client_address):
    print("Connection from", client_address)

    try:
        # Receba o nome do arquivo e o tamanho do arquivo
        file_info = client_socket.recv(BUFFER_SIZE).decode()

        if not is_valid_file_info(file_info):
            raise ValueError("Invalid file info received")

        file_name, file_size = file_info.split(':')
        file_size = int(file_size)

        # Bloqueie o acesso aos recursos compartilhados
        with lock:
            # Crie o diretório para os arquivos recebidos
            directory = "Recebidos do cliente"
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Crie o diretório para o cliente atual
            client_directory = os.path.join(directory, f"{client_address[0]}_{client_address[1]}")
            if not os.path.exists(client_directory):
                os.makedirs(client_directory)

            # Salve o arquivo no diretório do cliente
            file_path = os.path.join(client_directory, file_name)
            with open(file_path, 'wb') as file:
                bytes_received = 0
                while bytes_received < file_size:
                    data = client_socket.recv(BUFFER_SIZE)
                    if not data:
                        break
                    file.write(data)
                    bytes_received += len(data)
                    print("Progress: {:.2f}%".format(bytes_received / file_size * 100))

        print("File received and saved:", file_path)
        # Envie uma resposta de confirmação para o cliente
        response = "Arquivo recebido com sucesso!"
        client_socket.sendall(response.encode())

    except Exception as e:
        print(f"Error handling client {client_address}: {e}")

    finally:
        client_socket.close()

# Crie um objeto de socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincule o socket a um endereço e porta específicos
server_address = ('localhost', 5001)
server_socket.bind(server_address)

# Inicie a escuta por conexões recebidas
server_socket.listen(MAX_CONCURRENT_CONNECTIONS)

print("Server is listening on", server_address)

while True:
    # Aceite uma conexão de um cliente
    client_socket, client_address = server_socket.accept()

    # Crie uma nova thread para lidar com o cliente
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()

