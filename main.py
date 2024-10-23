# Example file showing a circle moving on screen
import pygame
from robot import Robot
from trash import Trash
from trashbin import Bin
from obstacle import Obstacle
import random

class Trash_Generator():
    def __init__(self):
        self.cooldown = 2
        self.cooldown_timer = 0
    
    def generate(self, dt):
        self.cooldown_timer += dt
        
        if self.cooldown_timer >= self.cooldown:
            x = random.randint(100, 1160)
            y = random.randint(100, 620)
            
            new_trash = Trash(x, y, 50,50, "black")
            
            self.cooldown_timer = 0
            
            return new_trash
        else:
            return None

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0


trashbin = Bin(100, 100, 70, 80, "red")
trash_list = []
robot_list = []
obstacle_list = [Obstacle(500, 200, 90, 90, "green") , Obstacle(50, 30, 90, 90, "green"), Obstacle(300, 600, 90, 90, "green"), Obstacle(1100, 400, 90, 90, "green"), Obstacle(100, 350, 90, 90, "green"), Obstacle(700, 440, 90, 90, "green")]


trash_generator = Trash_Generator()

while running:
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_x, mouse_y = pygame.mouse.get_pos()  
                new_robot = Robot(0.1, mouse_x, mouse_y, 60, 60, "blue")
                robot_list.append(new_robot) 

    screen.fill("white")
    
    
    for obstacle in obstacle_list:
        obstacle.render(screen)
        
 
    trashbin.render(screen)
        
  
    new_trash = trash_generator.generate(dt)
    
    if new_trash is not None:
        #only 5 trash max sa map
        if len(trash_list) < 5:
            trash_list.append(new_trash)
            
    for trash in trash_list:
        trash.render(screen)
        trash.update_state(robot_list)
        
    trash_list = [trash for trash in trash_list if trash.isCollected == False]
        
        
    #robot logic
    for robot in robot_list:
        robot.render(screen)
        robot.update_state(trash_list,obstacle_list,trashbin,dt)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
