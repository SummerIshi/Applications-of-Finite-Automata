import pygame


class Entity(pygame.Rect):
    def __init__(self, speed, x, y, width, height, color):
        super().__init__(x, y, width, height)  
        self.speed = speed
        self.direction = pygame.Vector2(1, 0)
        self.color = color
        
        self.current_state = 0
        self.move_timer = 0
        self.current_state = 0
        self.background = None
        
    def render(self, screen):
        print("hhh")

        
        
   