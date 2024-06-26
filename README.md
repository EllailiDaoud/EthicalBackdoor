# Ethical Backdoor

This project demonstrates a basic client-server architecture for an ethical backdoor implemented in Python. The backdoor allows for remote command execution, file download, and screen capture on the client machine. It is intended for educational purposes only to understand how backdoors work and to improve network security.

## Prerequisites

- Python 3.x
- `Pillow` library for screen capture

## Files

1. **Backdoor_client.py**: The client-side script that connects to the server and executes commands received from it.
2. **capture_ecran.py**: A standalone script to capture the screen and save it as an image.
3. **Backdoor_serveur.py**: The server-side script that listens for incoming connections from the client and sends commands to it.

## Setup

1. **Install the required libraries:**

    ```bash
    pip install pillow
    ```

2. **Configure the IP addresses and ports:**

    - In `Backdoor_client.py`, set the `HOST_IP` to the server's IP address.
    - In `Backdoor_serveur.py`, set the `HOST_IP` to the server's IP address.

## Usage

1. **Run the server:**

    ```bash
    python Backdoor_serveur.py
    ```

    The server will start listening for incoming connections.

2. **Run the client:**

    ```bash
    python Backdoor_client.py
    ```

    The client will attempt to connect to the server. Once connected, it will wait for commands from the server.

3. **Commands:**

    - `infos`: Get system information and current working directory from the client.
    - `cd <directory>`: Change the directory on the client machine.
    - `dl <file>`: Download a file from the client machine to the server.
    - `capture <filename>`: Capture the screen of the client machine and save it as a PNG file.
    - Any other command will be executed on the client machine's shell.

## Example

1. Start the server and client as described above.
2. On the server, you can now enter commands to control the client. For example:

    ```bash
    192.168.101.109:32000 > infos
    ```

    This will return the client's system information and current working directory.

    ```bash
    192.168.101.109:32000 > cd C:\Users
    ```

    This will change the client's directory to `C:\Users`.

    ```bash
    192.168.101.109:32000 > dl example.txt
    ```

    This will download the file `example.txt` from the client to the server.

    ```bash
    192.168.101.109:32000 > capture screenshot
    ```

    This will capture the client's screen and save it as `screenshot.png`.

## Disclaimer

This project is for educational purposes only. The use of this code in real-world scenarios without explicit permission is illegal and unethical. The author is not responsible for any misuse of this code.
