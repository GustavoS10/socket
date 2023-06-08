import socket
import os
import time

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = ('localhost', 5000)
client_socket.connect(server_address)

# Se uma operação de socket, 
# exceder o valor de timeout especificado, uma exceção socket.timeout será gerada.
client_socket.settimeout(10)

# Select a local file to send
file_path = input("Enter the path of the file to send: ")

# Send the file name and file size
file_name = os.path.basename(file_path)
print(file_path+"\n")
file_size = os.path.getsize(file_path)
client_socket.sendall(f"{file_name}:{file_size}".encode())

# Send the file
with open(file_path, 'rb') as file:
    bytes_sent = 0
    while bytes_sent < file_size:
        data = file.read(1024)
        client_socket.sendall(data)
        bytes_sent += len(data)
        print("Progress: {:.2f}%".format(bytes_sent / file_size * 100))

def calcular_taxa_transferencia(tamanho_arquivo, tempo_transferencia):
    taxa = tamanho_arquivo / tempo_transferencia
    return taxa

inicio_transferencia = time.time()  # Tempo inicial da transferência
fim_transferencia = time.time()  # Tempo final da transferência
tempo_transferencia = fim_transferencia - inicio_transferencia  # Tempo total de transferência em segundos
taxa_transferencia = calcular_taxa_transferencia(file_size, tempo_transferencia)


print("Timeout ", client_socket.gettimeout())

print("Taxa de transferência:", taxa_transferencia, "bytes por segundo")
print("File sent:", file_name)

# Close the socket
client_socket.close()
