import math
import pygame
import numpy as np

class Sensor:
    def __init__(self,range,beams, map):
        self.x = 0
        self.y = 0
        self.range = range
        self.beams = beams #no. beams
        self.map=map
        self.width,self.height= pygame.display.get_surface().get_size() #window dimensions
        self.points = [] #x,y of points detected, resets upon each iteration



    def detect(self):
        #Mimic a LIDAR sensor, in 360 degrees send out beams till you find a point where a wall is.
        #Record the x,y coordinates of the point
        #Return x,y coordinates of all points found

        self.points = []

        #Each beam has an angle. Along this angle we will check every 1% increment from 0 to range. If it's black, we hit a wall
        for angle in np.linspace(0,2*math.pi,self.beams,False):
            #Find end of beam
            tip_x = math.cos(angle)*self.range + self.x
            tip_y = -math.sin(angle)*self.range + self.y #-sin since y is inverted (0 at top, increasing as we go down)

            #Move incrementally from self to end of beam
            for increment in np.linspace(0,1,50):
                point_x = tip_x*increment + self.x*(1-increment)
                point_y = tip_y*increment + self.y*(1-increment)
                point_x, point_y = int(point_x), int(point_y)

                #HIT WAll?:
                if 0<point_x<self.width and 0<point_y<self.height: #if in the screen
                    color = self.map.get_at((point_x,point_y))
                    if (color[0],color[1],color[2]) == (0,0,0):
                        self.points.append([point_x,point_y])
                        break
        
        return self.points
    


    def add_error(self, variance):
        #add variance to points to simulate error / uncertainty

        for point in self.points:
            point[0] = np.random.normal(point[0], np.sqrt(variance))
            point[1] = np.random.normal(point[1], np.sqrt(variance))
        return self.points








    
    