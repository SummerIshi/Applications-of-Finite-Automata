import pygame
import math
from entity import Entity

class Bin(Entity):
    
    def __init__(self, x, y, width, height, color):
        super().__init__(0, x, y, width, height, color)  
        self.trash_count = 0
        self.background = pygame.image.load("assets/trashcan.png")
        self.background = pygame.transform.scale(self.background, (70,80))
        
    def render(self, screen):
        #super().render(screen)
    
        screen.blit(self.background, (self.x, self.y))

        font = pygame.font.SysFont('Arial', 24)  
        text_surface = font.render(f'{self.trash_count}', True, "black") 
        
        text_x = self.x + 12
        text_y = self.y - 30 
    
        screen.blit(text_surface, (text_x, text_y))
    