import math
import numpy as np
from scipy.odr import *



class wall_generator:
    def __init__(self,x,y, epsilon, delta, seed_amount, pd_max, l_min, p_min):
        self.x = x
        self.y = y
        self.epsilon = epsilon
        self.delta = delta
        self.seed_amount = seed_amount
        self.pd_max = pd_max
        self.l_min = l_min
        self.p_min = p_min

    

    def find_seed_region(self, points, start):
        #Find first (only 1) seed region starting at start variable until end of points

        #If start is ahead of points return None
        if start >= len(points)-self.seed_amount:
            return None

        for i in range(start, len(points)-self.seed_amount):
            flag = True
            j = i + self.seed_amount #note that j is the NON-INCLUSIVE end
            m,b = self.make_odr(points[i:j])

            for k in range(i,j):
                point = points[k] #potential seed

                #DELTA ERROR
                pred_point = self.get_predicted_point( (self.x,self.y), point, (m,b)) #Predicted point
                current_delta = self.dist_2points(point,pred_point)

                if current_delta > self.delta:
                    flag=False
                    break
                    
                #EPSILON ERROR
                current_epsilon = self.dist_pointLine(point, (m,b))
                if current_epsilon > self.epsilon:
                    flag=False
                    break

                #PD_MAX
                #i.e. if any point is too far away from the previous one there might be a door there so disregard seed/
                if (k!=i) and self.dist_2points(points[k], points[k-1]) > self.pd_max: #not for first point tho
                    flag=False
                    break

            if flag==True:
                return (i,j) #j is new startpoint
        
        #if none found
        return None



    def grow_seed_region(self, points, seed_index):
        #Given one seed region keep adding points until you add a point which has an epsilon error too large

        num_points = len(points)
        i,j = seed_index[0], seed_index[1] #First and last point in seed (j is actually non inclusive)

        #Make ODR Line
        m,b = self.make_odr(points[i:j]) #note j is not inlcuded in these points

        #Define points to potenitally add
        #Start with one DEFINITELY in the m,b equation i.e. the first and last points (inclusive)
        p_behind = i
        p_infront = j-1 #-1 since j is NON-inclusive so far

        #Add to the right
        while self.dist_pointLine(points[p_infront], (m,b)) <= self.epsilon: #Check if point fits into current ODR Line

            #Refit line (integrate p_infront)
            m,b = self.make_odr(points[p_behind:p_infront+1]) #+1 since we WANT to include p_infront in our m,b since it passed our epsilon test
            
            #MOVE ONTO NEXT POINT
            p_infront+=1
            #If no more points:
            if p_infront >= num_points:
                break

            #Check if next point is too far off (checking for potential doors which epsilon cant)
            if self.dist_2points(points[p_infront],points[p_infront-1]) >= self.pd_max:
                break

        #If loop broken it mean that most recent p_infront should not be added: hence go back 1
        p_infront-=1


        #Add to the left
        while self.dist_pointLine(points[p_behind], (m,b)) <= self.epsilon:
            #Refit line
            m,b = self.make_odr(points[p_behind:p_infront+1])

            #Next point
            p_behind-=1
            if p_behind < 0:
                break

            #Check if next point is too far away
            if self.dist_2points(points[p_behind],points[p_behind+1]) >= self.pd_max:
                break

        #loop broken means last one was unacceptable
        p_behind +=1 #this is the last integrated point


        #IS WALL APPROPRIATE:
        #Length of line
        if self.dist_2points(points[p_behind], points[p_infront]) < self.l_min:
            #NOTE: technically this is not the distance of the line but the distance between the last and first point that training the m,b of the line.
            #Still a good proxy
            return None
        
        #Number of points in line
        if (p_infront-p_behind+1) < self.p_min:
            return None
        
        
        #Return pb,pf and m,b
        return (p_behind, p_infront), (m,b)
    


    def cut_line(self, line_equation, end_point):
        #Given a line and a point, make an othognal line to original line that goes through said point. Then find intersection of original and othogonal line.
        #Used to find the end points of a line equation of a wall: where othogonal line (that goes through first/last point used in training orignal line) intersects with orignal line

        m,b = line_equation
        x,y = end_point[0], end_point[1]

        #Find othogonal line
        o_m = -1/m #othogonal m
        o_b = y - o_m*x #y = mx+b --> b = y - mx

        #Find intersection of lines
        intersection_x = (o_b - b) / (m - o_m)
        intersection_y = m*intersection_x + b

        return(intersection_x, intersection_y)



    def linear_func(self,p,x):
        #Used in make_odr() function
        m,b = p
        return m*x+b 
    
    

    def make_odr(self, points):
        #Given points makes an ODR line and returns m,b
        
        x = np.array([i[0] for i in points])
        y= np.array([i[1] for i in points])

        #create model
        linear_model = Model(self.linear_func)

        #create data object
        data = RealData(x,y)

        #setup
        odr_model = ODR(data,linear_model, beta0=[0.,0.])

        #run
        out = odr_model.run()
        m,b = out.beta #get parameters
        return m,b
    


    def get_predicted_point(self, sensor_position, point, odr_line):
        #Used in delta error. Every point in a seed segment has a 'predicted point' counterpart.
        #The predicted point is found in the intersection of two lines.
        #First being the Othogonal Least squares lines of the seed segment points.
        #The second is where the line between the sensor and the predicted point
         
        #Generate line from two points (second 'line' in description)
        m = (sensor_position[1]-point[1]) / (sensor_position[0]-point[0])
        b = point[1] - m*point[0] #y = mx + b --> y -mx = b

        #find intersection of lines
        x = (b-odr_line[1]) / (odr_line[0] - m)
        y = m*x + b
        return (x,y)
    


    def dist_2points(self, point1, point2):
        #Returns distance between two points

        x = (point1[0]-point2[0])**2
        y = (point1[1]-point2[1])**2
        distance = math.sqrt(x+y)
        return distance



    def dist_pointLine(self, point, line_coord):
        #Returns othogonal distance between a point and a line

        #Convert to standard form
        A,B,C = line_coord[0], -1, line_coord[1]

        distance = abs(A*point[0]+B*point[1]+C) / math.sqrt(A**2 + B**2)
        return distance