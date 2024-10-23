from entity import Entity
import pygame
import math
from trash import Trash
from obstacle import Obstacle
from trashbin import Bin

class Robot(Entity):
    
    def __init__(self, speed, x, y, width, height, color):
        super().__init__(speed, x, y, width, height, color)  
        self.collected_trash = 0
        self.move_timer = 0
        self.idle_state_timer = 0
        #kani
        self.background = pygame.image.load("assets/robot.png")
        self.background = pygame.transform.scale(self.background, (60,60))

        self.transition_table = [
            [ 1,  1,  1,  1,  1,  1],
            [ 2,  1, -1, -1, -1, -1],
            [-1, -1,  3,  2, -1,  2],
            [ 4,  3, -1, -1, -1, -1],
            [-1, -1,  5,  1, -1,  4],
            [-1, -1,  5,  1,  6,  5],
            [ 1,  1,  1,  1,  1,  1]
        ]
        
        
    def render(self, screen):
       
        screen.blit(self.background, (self.x, self.y))
    
        font = pygame.font.SysFont('Arial', 12)  
        text_surface = font.render(f'{self.collected_trash}', True, "black") 


        
        text_x = self.x + 6
        text_y = self.y - 15
    
        screen.blit(text_surface, (text_x, text_y))
        
    def update_state(self, trash_list,obstacle_list,trashbin, dt):
        machine_input = None
        
        nearby_trash = self.find_nearest_entity(trash_list)
        nearby_obstacle = self.find_nearest_entity(obstacle_list)
        
        if self.current_state == 0:
            #always go to state 1
            machine_input = 0
        elif self.current_state == 1:
            if nearby_trash:
                machine_input = 0
            else:
                machine_input = 1
        elif self.current_state == 2:
            if nearby_trash and self.detect_collison(nearby_trash):
                machine_input = 2
            elif self.detect_collison(nearby_obstacle):
                machine_input = 3
            else:
                machine_input = 5
        elif self.current_state == 3:
            if nearby_trash:
                machine_input = 0
            else:
                machine_input = 1
        elif self.current_state == 4:
            if nearby_trash and self.detect_collison(nearby_trash):
                machine_input = 2
            elif self.detect_collison(nearby_obstacle):
                machine_input = 3
            else:
                machine_input = 5
        elif self.current_state == 5:
            if nearby_trash and self.detect_collison(nearby_trash):
                machine_input = 2
            elif self.detect_collison(nearby_obstacle):
                machine_input = 3
            elif self.detect_collison(trashbin):
                machine_input = 4
            else:
                machine_input = 5
        elif self.current_state == 6:
            #go back to start
            machine_input = 0
            
            
        self.current_state = self.transition_table[self.current_state][machine_input]
        
        print(f"State: {self.current_state}")
        
        if self.current_state == 0:
            self.spawn_state()
        elif self.current_state == 1:
            self.holding_zero_trash()
        elif self.current_state == 2:
            self.finding_first_trash(nearby_trash, dt)
        elif self.current_state == 3:
            self.holding_one_trash()
        elif self.current_state == 4:
            self.finding_second_trash(nearby_trash, dt)
        elif self.current_state == 5:
            self.holding_two_trash(trashbin, dt)
        else:
            self.all_trashes_thrown_to_bin()
        
    #STATES
    
    #0
    def spawn_state(self):
        print("Robot just spawned")
        
    #1     
    def holding_zero_trash(self):
        print("Robot is holding zero")
            
    #2
    def finding_first_trash(self, trash, dt):
        self.move_towards_entity(trash, dt)
    
    #3
    def holding_one_trash(self):
        print("Picked trash 1")
        
    #4
    def finding_second_trash(self, trash, dt):
        self.move_towards_entity(trash, dt)
    
    #5
    def holding_two_trash(self, trashbin, dt):
        self.move_towards_entity(trashbin, dt)
    
    #6
    def all_trashes_thrown_to_bin(self):
        print("Succesfull throwing")
    
    
    
    #HELPERS
    def move_towards_entity(self, entity, dt):
        self.move_timer += dt
        
        if self.move_timer >= self.speed:
            self.direction = pygame.Vector2(entity.x - self.centerx, entity.y - self.centery)
        
            if self.direction.length() > 0: 
                self.direction.normalize_ip()  
                
            new_position = self.center + (self.direction * self.speed)
            
            if 0 <= new_position.x < 1280 - self.width and 0 <= new_position.y < 720 - self.height:
                self.move_ip(self.direction * 10)  
                self.move_timer = 0
                
    def find_nearest_entity(self, list):
        nearest_entity = None
        nearest_distance = float('inf') 

        for entity in list:

            distance = math.sqrt((self.centerx - entity.x) ** 2 + (self.centery - entity.y) ** 2)

            if distance < nearest_distance:
                nearest_distance = distance
                nearest_entity = entity

        if nearest_entity is not None:
            return nearest_entity 
        else:
            return None
        
        
    def detect_collison(self, entity):
       
        distance = math.sqrt((self.centerx - entity.centerx) ** 2 + (self.centery - entity.centery) ** 2)
            
        if distance <= (entity.width):
            if isinstance(entity, Trash):
                entity.isCollected = True
                self.collected_trash += 1
            elif isinstance(entity, Bin):
                entity.trash_count += self.collected_trash
                self.collected_trash = 0
                self.x += 80
            elif isinstance(entity, Obstacle):
                self.collected_trash = 0
                
            return entity
        
        return None