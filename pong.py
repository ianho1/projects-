#Ian Ho pong game 
import  SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random
import math

#initialize globals
WIDTH = 600
HEIGHT = 400
ball_pos = [WIDTH / 2, HEIGHT / 2]
BALL_RADIUS = 20
ball_color = ''
background_color = 'white'
colors = ["Red", "Orange", "Yellow", "Green", "Blue", "Purple"]
index = 0
ball_velocity = [1,1]
pointsL = 0
pointsR = 0

#Set Canvas Height
canvas_width = WIDTH
canvas_height = HEIGHT

#Initialize variables: paddle width, paddle center
pad_wth = 10
pad_ht = 80
pad_centL = [pad_wth, canvas_height/2]
pad_centR = [canvas_width-pad_wth,canvas_height/2]
pad_velL = 0
pad_velR= 0 

  
def gutter_reset():
    global ball_pos, ball_velocity, pointsL, pointsR
    #Update the points for both left and right side if it passes the gutter line 
    if ball_pos[0] + BALL_RADIUS > WIDTH-pad_wth:
        pointsL += 1
        print ("The left side has", pointsL, "points.")
    if ball_pos[0] - BALL_RADIUS < pad_wth:
        pointsR += 1
        print ("The right side has", pointsR, "points.")
    reset()
    
def paddle_bounce():
    global ball_pos, ball_velocity
    # checks if any part of the paddle shares the y coordinate of the ball’s center, the ball should “bounce” and be reflected
    if ball_pos[0] + BALL_RADIUS > WIDTH-pad_wth:
        if ball_pos[1] >= pad_centR[1] - 0.5 * pad_ht and ball_pos[1] <= pad_centR[1] + 0.5 * pad_ht:
            ball_velocity[0] = 2* - ball_velocity[0]
        else:
            gutter_reset()
            
    if ball_pos[0] - BALL_RADIUS < pad_wth:
        if ball_pos[1] >= pad_centL[1] - 0.5 * pad_ht and ball_pos[1] <= pad_centL[1] + 0.5 * pad_ht:
            ball_velocity[0] = 2*- ball_velocity[0]
        else:
            gutter_reset()

def bounce_ball():
    global ball_pos, ball_velocity
      #check for bounce off wall 
    if ball_pos[1] + BALL_RADIUS > HEIGHT:
        ball_velocity[1] = - ball_velocity[1]
    if ball_pos[1] - BALL_RADIUS < 0:
        ball_velocity[1] = - ball_velocity[1]
        
def update_pos():
    #update the ball position
    ball_pos [0] += ball_velocity[0]
    ball_pos [1] += ball_velocity[1] 
    
def update_paddle():
    global pad_centL,pad_centR,pad_velL, pad_velR
    
# updating center of the paddle by veolcity number (moves paddle up/down)
    pad_centL[1]+=pad_velL
    pad_centR[1]+=pad_velR
    
def update_color():
    # changes color of the ball at 60fps
    global index, ball_color
    ball_color = colors[index]
    index += 1
    index = index % len(colors)
    
#define reset and start functions    
def reset():
    #puts ball back to center and sets velocity to zero
    global ball_pos, ball_velocity
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_velocity = [0,0]

def start():
    #puts ball back to center
    global ball_pos, ball_velocity
    #this starts the random motion of the ball 
    while ball_velocity [0] == 0 or ball_velocity [1] ==0:
        ball_velocity = [(random.randrange(-6, 6)),(random.randrange(-6, 6))] 
    
#Moves the left paddle up and down when “w” and “s” keys pressed
def keydown(key):
    global pad_velL, pad_velR
    #left paddle    
    if key == simplegui.KEY_MAP['s']:
        pad_velL = 3
    if key == simplegui.KEY_MAP['w']:
        pad_velL=-3
    if key == simplegui.KEY_MAP['up']:
          pad_velR = -3
    if key == simplegui.KEY_MAP['down']:
          pad_velR=3

# Stops moving the left paddle up and down when “w” and “s” keys released
def keyup(key):
    global pad_velL, pad_velR
    
    #left paddle
    if key == simplegui.KEY_MAP['w']:
        pad_velL = 0 
    if key == simplegui.KEY_MAP['s']:
        pad_velL = 0 
    if key == simplegui.KEY_MAP['up']:
          pad_velR = 0 
    if key == simplegui.KEY_MAP['down']:
          pad_velR= 0
    
def draw_handler(canvas):
    global ball_pos, ball_velocity, pad_velL, pad_velR,pointsL,pointsR,WIDTH, HEIGHT, pad_ht,pad_centL,pad_centR
    bounce_ball()
    paddle_bounce()
    update_pos()
    update_color()
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", ball_color)
    canvas.draw_text(str(pointsL), (20, 20), 16, 'Red')
    canvas.draw_text(str(pointsR), (WIDTH-30, 20), 16, 'Green')
    #updates the position of the paddle
    # makes sure both paddles do not pass the top and bottom of the screen  
    if pad_centL[1] - 0.5*pad_ht < 0:
        pad_velL = 1
    elif pad_centL[1] + 0.5*pad_ht > HEIGHT:
        pad_velL = -1
    elif pad_centR[1] - 0.5*pad_ht < 0:
        pad_velR = 1
    elif pad_centR[1] + 0.5*pad_ht > HEIGHT:
        pad_velR = -1

    update_paddle()
        
    #draws left and righ gutter lines
    canvas.draw_line((pad_wth,0), (pad_wth, canvas_height), 2, 'red')
    canvas.draw_line((canvas_width-pad_wth,0), (canvas_width-pad_wth, canvas_height), 2, 'green')

    #draws the left and right paddles 
    canvas.draw_line([pad_centL[0],pad_centL[1]- 40], [pad_centL[0], pad_centL[1]+ 40], pad_wth, 'pink')
    canvas.draw_line([pad_centR[0],pad_centR[1]- 40], [pad_centR[0], pad_centR[1]+ 40], pad_wth, 'blue')

#set frame and handlers
frame = simplegui.create_frame("Ho's Pong Game", WIDTH, HEIGHT)
frame.add_label('Simple information')
frame.set_canvas_background('teal')
frame.add_button('New game', reset)
frame.add_button('Start', start)
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_draw_handler(draw_handler)


#calls draw handler
frame.start()