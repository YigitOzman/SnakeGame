# This is a simplified remake of a classic snake game from old mobile devices.
# You can use arrow keys or WASD to move the snake.

import pygame
import random
import tkinter as tk
from tkinter import messagebox
from collections import namedtuple

pygame.init() # To initialize all the modules.
font = pygame.font.SysFont('helvetica', 20) # Font and size of the scoreboard in the game screen.


Point = namedtuple("Point", "x, y") # This creates a subclass named Point with x and y that I can use in the code to arrange the coordinates.


squareSize = 10 # This is the pixel amount of the single square of the snake and food.
speed = 10 # Speed of the game

class SnakeGame: # This will be the class for the game.
    
    def __init__(self, width = 640, height = 480):
        self.width = width # Width of the game screen.
        self.height = height # Height of the game screen.
        self.display = pygame.display.set_mode((self.width, self.height)) # This is the game screen.
        pygame.display.set_caption('Snake Game') # This will change the name of the game from pygame window to Snake Game.
        self.clock = pygame.time.Clock() # Speed of the game.
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"]) # The snake will start moving to a random direction at the start.
        self.head = Point(self.width/2, self.height/2) # Start coordinates for the head of the snake.
        self.snake = [self.head] # I wanted my snake to start with only the head and then grow later.
        self.eaten = 0 # Beginning score.
        self.food = None
        self.RandomLocation()


    def play(self):
        global speed # I'll use this to increase the speed of the snake when it eats a food later.
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # When I close the window game will shut down.
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN: # I used four different if conditions for all of the directions that snake can move to prevent the snake turning 180 degrees and eating itself.
                if self.direction == "UP":
                    if event.key ==pygame.K_LEFT or event.key ==ord("a"): # Use a or left arrow key to go left.
                        self.direction = "LEFT"
                    elif event.key ==pygame.K_RIGHT or event.key ==ord("d"): # Use d or down arrow key to go right.
                        self.direction = "RIGHT"
                elif self.direction == "DOWN":
                    if event.key ==pygame.K_LEFT or event.key ==ord("a"): # Use a or left arrow key to go left.
                        self.direction = "LEFT"
                    elif event.key ==pygame.K_RIGHT or event.key ==ord("d"): # Use d or down arrow key to go right.
                        self.direction = "RIGHT"
                elif self.direction == "LEFT":
                    if event.key ==pygame.K_UP or event.key ==ord("w"): # Use w or up arrow key to go up.
                        self.direction = "UP"
                    elif event.key ==pygame.K_DOWN or event.key ==ord("s"): # Use s or down arrow key to go down.
                        self.direction = "DOWN"
                elif self.direction == "RIGHT":
                    if event.key ==pygame.K_UP or event.key ==ord("w"): # Use w or up arrow key to go up.
                        self.direction = "UP"
                    elif event.key ==pygame.K_DOWN or event.key ==ord("s"): # Use s or down arrow key to go down.
                        self.direction = "DOWN"

        self.move(self.direction) # Move the snake.
        self.snake.insert(0, self.head) # This inserts the head into the body.
        
        
        gameOver = False
        if self.dies(): # This checks if the snake dies or not to end the game.
            gameOver = True
            return gameOver, self.eaten

        if self.head == self.food: # If snake eats food.
            self.eaten = self.eaten + 1 # Score + 1.
            speed = speed + 2 # Speed increases when you eat a food.
            self.RandomLocation() # Spawn new food.
        else:
            self.snake.pop() # This removes the last square of the snake when you move so we actually play the snake game instead of drawing something.

            
        self.ui()
        self.clock.tick(speed)
        return gameOver, self.eaten

    def move(self, direction): #  This function will make my snake move in the according direction.
        x = self.head.x
        y = self.head.y
        if direction == "UP":
            y = y - squareSize
        elif direction == "DOWN":
            y = y + squareSize
        elif direction == "LEFT":
            x = x - squareSize
        elif direction == "RIGHT":
            x = x + squareSize
        
        self.head = Point(x,y) # Updates the snake's head coordinates.       

    def ui(self):
        self.display.fill((211, 255, 94)) # Color of the game screen.

        for Point in self.snake: # This draws the snake.
            pygame.draw.rect(self.display, (0,0,0), pygame.Rect(Point.x,Point.y, squareSize, squareSize))

        pygame.draw.rect(self.display, (0,0,0), pygame.Rect(self.food.x, self.food.y, squareSize, squareSize)) # This draws the food.

        pygame.draw.rect(self.display, (0,0,0), pygame.Rect(0, 0, 640, 480),  20) # This adds border lines.

        scoreBoard = font.render(str(self.eaten) , True, (0,0,0)) # This will be the scoreboard.
        self.display.blit(scoreBoard, [610,10]) # Scoreboard location on the screen.
        pygame.display.flip() # This updates the ui when something happens. Without this we could only see a black screen with nothing in it.


    def dies(self):
        if self.head.x > self.width - squareSize - 10 or self.head.x < 10 or self.head.y > self.height - squareSize - 10 or self.head.y < 10: # Checks if snake hits the border lines that I created.
            return True
        if self.head in self.snake[1:]: # Checks if snake eats itself. self.snake[1:] to not include the head.
            return True

        return False


    def RandomLocation(self): # This function will create the food in random location.
        x = random.randint(20,(self.width-(squareSize*2))//squareSize)*squareSize # x coordinate of the food. This way I get a random integer that is between the border lines and then floor divide and multiple it with square size so that I actually get a coordinate that snake can past and eat the food.
        y = random.randint(20,(self.height-(squareSize*2))//squareSize)*squareSize # y coordinate of the food. This way I get a random integer that is between the border lines and then floor divide and multiple it with square size so that I actually get a coordinate that snake can past and eat the food.
        self.food = Point(x, y)
        if self.food in self.snake: # If the food spawns inside the snake this will respawn the food in a different location.
            self.RandomLocation()
    
if __name__ == "__main__": # This will be the main of the code. if __name__ == "__main__" gives the codes below highest priority.
    game = SnakeGame()
    gameOver = False
    # Loop for the game.
    while gameOver == False:
        gameOver,  eaten = game.play()

        if gameOver == True:
            break # break if game over.
    root = tk.Tk()
    root.withdraw() # To remove main tkinter window and only show the game over pop up message.
    
    messagebox.showinfo("Game Over", "You died.\nEaten Food: " + str(eaten) + "\n" + "Thank you for playing!") # This message will pop up when you die.
    
    
    pygame.quit() # This will make the code close pygame.