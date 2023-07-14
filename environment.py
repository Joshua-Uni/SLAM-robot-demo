import pygame
import numpy as np

class Env:
    def __init__(self,map, width, height):
        pygame.init()
        self.image = pygame.image.load(map)
        self.width = width
        self.height = height
        self.map = pygame.display.set_mode((self.width,self.height))
        self.map.blit(self.image, (0,0))



    def draw_points(self, points):
        #Draw points once they've been sensed (not in use currently)

        for point in points:
            red = np.random.randint(100,256)
            green = 255-red
            blue = (green-125) %255
            self.map.set_at((int(point[0]),int(point[1])), (red,green,blue))



    def draw_lines(self, lines):
        #Draw walls once they've been made
        for line in lines:
            pygame.draw.line(self.map,(255,0,0),line[0],line[1],2)
    

    
    def draw_robot(self,move_info:list):
        #Undraw robot (black where it was), then redraw where it is now (coloured at new x,y)
        #We do this since we cannot draw a new black screen each game loop since we are not storing the walls information
        old_x = move_info[0]
        old_y = move_info[1]
        new_x = move_info[2]
        new_y = move_info[3]
        width = move_info[4]
        height = move_info[5]

        #Draw a black box where ROBOT was (since it is not there anymore):
        pygame.draw.rect(self.map, (0,0,0), pygame.Rect(old_x, old_y, width, height))
        
        #Draw ROBOT in new position
        pygame.draw.rect(self.map, (255,0,255), pygame.Rect(new_x, new_y, width, height))


    
        


