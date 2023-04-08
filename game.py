"""
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

if __name__ == "__main__":
    Snake()

