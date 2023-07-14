class Robot:
    def __init__(self,x,y,width,height,max_vel,speed,map_,m_width,m_height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.x_vel = 0
        self.y_vel = 0
        self.max_vel = max_vel
        self.speed = speed
        self.map = map_
        self.map_width = m_width
        self.map_height = m_height
        self.detection_buffer = 2
    


    def move(self, vertical, horizontal):
        #Function does two things:
        #1. Update x,y position of ROBOT
        #2. Return a list of variables needed for ENVIRONMENT.draw_robot() (NEED WHERE ROBOT WAS + WHERE IT IS NOW)

        vertical *= self.speed
        horizontal *= self.speed

        #Get old position
        old_x = self.x
        old_y = self.y

        #Update velocity
        self.x_vel+=horizontal
        self.y_vel+=vertical

        #degrade velocity (move toward 0) and cap max velocity
        #X
        if self.x_vel > 0:
            self.x_vel -= 1
            self.x_vel = min(self.x_vel, self.max_vel)
        elif self.x_vel < 0:
            self.x_vel += 1
            self.x_vel = max(self.x_vel,-self.max_vel)
        #Y
        if self.y_vel > 0:
            self.y_vel -= 1
            self.y_vel = min(self.y_vel,self.max_vel)
        elif self.y_vel < 0:
            self.y_vel += 1
            self.y_vel = max(self.y_vel,-self.max_vel)

        #update new position
        new_x = self.x + self.x_vel
        new_y = self.y + self.y_vel

        buffer = self.detection_buffer #how far away from a barrier do we want to be before we stop

        #Stay within screen:
        x_screen_boundary = new_x - buffer > 0 and new_x+self.width + buffer < self.map_width
        y_screen_boundary = new_y - buffer > 0 and new_y+self.height + buffer < self.map_height
        in_boundary = x_screen_boundary and y_screen_boundary

        #Dont go thru walls:
        #For each direction you are moving check all pixels to see if theres a wall on that side
        x_clear = True
        y_clear = True

        #RIGHT:
        if self.x_vel > 0 and in_boundary:
            for i in range(self.height):
                if self.map.get_at((new_x+self.width+buffer,new_y+i)) == (0,0,0,255):
                    x_clear = False
        #LEFT:
        elif self.x_vel < 0 and in_boundary:
             for i in range(self.height):
                if self.map.get_at((new_x-buffer,new_y+i)) == (0,0,0,255):
                    x_clear = False
        #BOTTOM:
        if self.y_vel > 0 and in_boundary:
            for i in range(self.width):
                if self.map.get_at((new_x+i,new_y+self.height+buffer)) == (0,0,0,255):
                    y_clear = False
        #TOP
        if self.y_vel < 0 and in_boundary:
            for i in range(self.width):
                if self.map.get_at((new_x+i,new_y-buffer)) == (0,0,0,255):
                    y_clear = False

        #Check boundaries violated and update position
        if x_screen_boundary and x_clear:
            self.x = new_x
        if y_screen_boundary and y_clear:
            self.y = new_y

        #return old and new position
        return [old_x,old_y,self.x,self.y,self.width,self.height]

