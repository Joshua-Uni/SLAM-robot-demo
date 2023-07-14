import environment, sensor, walls, robot
import pygame
import numpy as np

###ESTABLISH ENVIRONMENT
MAP = "map.png"
WIDTH = 1200
HEIGHT = 600
ENVIRONMENT = environment.Env(MAP,WIDTH,HEIGHT)

ORIGINAL_MAP = ENVIRONMENT.map.copy() #white background w black walls (for sensor)
ENVIRONMENT.map.fill((0,0,0)) #fill w/ black

###ESTABLISH SENSOR
RANGE= 125 
BEAMS = 120
VARIANCE = 0.5
SENSOR = sensor.Sensor(RANGE,BEAMS,ORIGINAL_MAP)

###ESTABLISH WALL GENERATOR
#Higher errors mean more seeds
EPSILON = 3 #Distance from point to Fitted line
DELTA = 1 #Makes the things straight
SEED_AMOUNT = 4
PD_MAX = 5 #Point distance max i.e. if the next point in a wall is over this, dont continue the wall (to account for door and windows)
L_MIN = 12 #minimum length a line must be to be valid
P_MIN = 2 #minimum amount of points a wall must have to be valid
WALLS = walls.wall_generator(0,0, EPSILON,DELTA,SEED_AMOUNT, PD_MAX, L_MIN, P_MIN)

###ESTABLISH ROBOT
R_X = WIDTH//2
R_Y = HEIGHT//2
R_WIDTH = 18
R_HEIGHT = 18
MAX_VEL = 2
R_SPEED = 2
ROBOT = robot.Robot(R_X,R_Y,R_WIDTH,R_HEIGHT,MAX_VEL,R_SPEED,ORIGINAL_MAP,WIDTH,HEIGHT)
ENVIRONMENT.draw_robot([ROBOT.x,ROBOT.y,ROBOT.x,ROBOT.y,ROBOT.width,ROBOT.height])
pygame.display.update()

###MOVEMENT VARS
up = False
down = False
left = False
right = False

###SENSOR TRIGGER
#run sensor + wall building at every spillover+1 game loop
counter = 0
spillover = 3

#MAIN LOOP
clock = pygame.time.Clock()
running = True
while running:

    #EVENTS:
    clock.tick(60)
    for event in pygame.event.get():
        #QUIT
        if event.type == pygame.QUIT:
            running=False
        #MOVEMENT KEYS: KEYDOWN only triggers once so need keyup too
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                up = True
            if event.key == pygame.K_DOWN:
                down = True
            if event.key == pygame.K_LEFT:
                left = True
            if event.key == pygame.K_RIGHT:
                right = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                up = False
            if event.key == pygame.K_DOWN:
                down = False
            if event.key == pygame.K_LEFT:
                left = False
            if event.key == pygame.K_RIGHT:
                right = False

    #UPDATE ROBOT POSITION:
    #Store old ROBOT x,y
    old_RX = ROBOT.x
    old_RY = ROBOT.y
    #Add movement
    vertical = int(down) - int(up)
    horizontal = int(right) - int(left)
    move_info = ROBOT.move(vertical,horizontal)
    #If robot hasn't moved, no need to continue
    if old_RX == ROBOT.x and old_RY == ROBOT.y:
        continue
    #Draw robot
    ENVIRONMENT.draw_robot(move_info)

    #UPDATE POINT SENSOR + WALL GENERATOR:
    SENSOR.x, SENSOR.y = ROBOT.x+(ROBOT.width//2), ROBOT.y+(ROBOT.height//2) #get MIDDLE of square
    WALLS.x, WALLS.y = ROBOT.x+(ROBOT.width//2), ROBOT.y+(ROBOT.height//2)

    #SENSOR + WALLBUILDING SPILLOVER:
    if counter < spillover:
        counter +=1
        pygame.display.update()
        continue
    counter = 0

    #SENSE SURROUNGS AND RETURN X,Y points
    points = SENSOR.detect()

    #ADD ERROR
    points = SENSOR.add_error(VARIANCE)

    #FIND WALLS + GROW WALLS:
    last_point = 0 #index of last point we had as a seeded region / wall region
    lines = []

    while True:
        #loop continues till we cannot find any more seeds from points gathered

        #Find a seeded region
        seed = WALLS.find_seed_region(points, last_point)
        if not seed:
            break

        #Grow seeded region into walls
        wall = WALLS.grow_seed_region(points,seed)
        if wall:
            last_point = wall[0][1] #p_infront
            #find wall endpoints
            m,b = wall[1][0], wall[1][1]
            start = WALLS.cut_line((m,b), (points[wall[0][0]]))
            end = WALLS.cut_line((m,b), (points[wall[0][1]]))
            lines.append((start,end))
        else:
            last_point = seed[0]+1 #start again from i

    #DRAW LINES:
    ENVIRONMENT.draw_lines(lines)

    #DRAW POINTS:
    #ENVIRONMENT.draw_points(points)

    pygame.display.update()

    
