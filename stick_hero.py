#importations:
import pygame as pg
from colors import *
import random
import sys
import time

#initializations
pg.mixer.pre_init(frequency=44100,size=16,channels=1,buffer=512)
pg.init()

#screen dimensions 
screen_w=540
screen_h=868
screen=pg.display.set_mode((screen_w,screen_h))
pg.display.set_caption('Stick Hero')
clock=pg.time.Clock()

#importing the background and the first hero image
background=pg.image.load('images/background.png').convert()
hero=pg.image.load('images/idle/1.png').convert_alpha()
hero=pg.transform.scale(hero,(100,100))

#Playing starting sound
pg.mixer.music.load('Sounds/Bells2.mp3')
pg.mixer.music.play()



#Importing the frames as lists to animate the hero 
walkRight = [pg.image.load('images/walking/1.png').convert_alpha(), pg.image.load('images/walking/2.png').convert_alpha(), pg.image.load('images/walking/3.png').convert_alpha(), pg.image.load('images/walking/4.png').convert_alpha(), pg.image.load('images/walking/5.png').convert_alpha(), pg.image.load('images/walking/6.png').convert_alpha(), pg.image.load('images/walking/7.png').convert_alpha(), pg.image.load('images/walking/8.png').convert_alpha(), pg.image.load('images/walking/9.png').convert_alpha(), pg.image.load('images/walking/10.png').convert_alpha(), pg.image.load('images/walking/11.png').convert_alpha(), pg.image.load('images/walking/12.png').convert_alpha()]
idle = [pg.image.load('images/idle/1.png').convert_alpha(), pg.image.load('images/idle/2.png').convert_alpha(), pg.image.load('images/idle/3.png').convert_alpha(), pg.image.load('images/idle/4.png').convert_alpha(), pg.image.load('images/idle/5.png').convert_alpha(), pg.image.load('images/idle/6.png').convert_alpha(), pg.image.load('images/idle/7.png').convert_alpha(), pg.image.load('images/idle/8.png').convert_alpha(), pg.image.load('images/idle/9.png').convert_alpha(), pg.image.load('images/idle/10.png').convert_alpha(), pg.image.load('images/idle/11.png').convert_alpha(), pg.image.load('images/idle/12.png').convert_alpha()]
dying = [pg.image.load('images/die/1.png').convert_alpha(), pg.image.load('images/die/2.png').convert_alpha(), pg.image.load('images/die/3.png').convert_alpha(), pg.image.load('images/die/4.png').convert_alpha(), pg.image.load('images/die/5.png').convert_alpha(), pg.image.load('images/die/6.png').convert_alpha(), pg.image.load('images/die/7.png').convert_alpha(), pg.image.load('images/die/8.png').convert_alpha(), pg.image.load('images/die/9.png').convert_alpha(), pg.image.load('images/die/10.png').convert_alpha(), pg.image.load('images/die/11.png').convert_alpha(), pg.image.load('images/die/12.png').convert_alpha()]





#The obstacle class
class Obstacle ():
	def __init__(self, pos, width, height):
		self.color=black
		self.x,self.y=pos
		self.width=width
		self.height=height

	def draw(self,screen):
		pg.draw.rect(screen,self.color,(self.x,self.y,self.width,self.height))
		
	def move(self,dist):
		self.x-=dist
		
	def get_tr_pos(self):
		return self.x+self.width,self.y

	def get_width(self):
		return self.width
	
	def get_tl_pos(self):
		return self.x,self.y


# Misc. functions:        
g_font1=pg.font.Font('04B_19.TTF',50)
g_font2=pg.font.Font('04B_19.TTF',35)

def move_hero(hero,dist):#To move the hero
	hero_rect=hero.get_rect()
	hero_rect.centerx-=dist

def score_dis_on(s):#To show current score
    score_s=g_font1.render(str(s), True,(255,255,255))
    score_rect=score_s.get_rect(center=(270,100))
    screen.blit(score_s,score_rect)
        
def high_score_dis(hs):#To show high score
    high_score_s=g_font1.render(f'High score : {str(hs)}', True,(255,255,255))
    high_score_rect=high_score_s.get_rect(center=(270,768))
    screen.blit(high_score_s,high_score_rect)
        
def game_over_screen(new_hs):#To show the game over screen with : current score, high score and info to start again and if it is a new high score, show "high score !" in turquoise        
	game_over_screen1=g_font1.render(f'GAME OVER', True,(255,255,255))
	game_over_screen2=g_font2.render(f'Right click to restart', True,(255,255,255))
	game_over_screen3=g_font2.render(f'or press \'Esc\' to quit', True,(255,255,255))
	game_over_rect1=game_over_screen1.get_rect(center=(270,384))
	game_over_rect2=game_over_screen2.get_rect(center=(270,484))
	game_over_rect3=game_over_screen3.get_rect(center=(270,534))
	screen.blit(game_over_screen1,game_over_rect1)
	screen.blit(game_over_screen2,game_over_rect2)
	screen.blit(game_over_screen3,game_over_rect3)
	if new_hs:
		game_over_screen4=g_font2.render(f'High score !', True,turquoise)
		game_over_rect4=game_over_screen4.get_rect(center=(270,150))
		screen.blit(game_over_screen4,game_over_rect4)


#creating 3 obstacles, 2 with random width
first_obstacle=Obstacle((0,screen_h-350),100,500)
second_obstacle=Obstacle((screen_w/2,screen_h-350),random.randint(50, 200),500)
third_obstacle=Obstacle((screen_w,screen_h-350),random.randint(50, 200),500)

#Global variables:
stick_height=10
stick_drawn=False
rotate=True
angle=0
i=0
herox=0
heroy=440
stick_all_set=False
stick_horizantal=False
game_lost=False
game_won=False
stick_180=False
game_over=False
exceed_right=False
exceed_left=False
score=0
high_score=0
adapt_hero=True
game_ended=False
image_ind=0
stab=0
is_idle=True
is_dying=False
is_moving=False
dead=False
desactivate_click=False

#the main game loop
while True:
	
    #Animating the hero : every picture stays on for 13 frames (on 160 FPS)
	stab+=1
	if stab%13==0:
		screen.blit(background,(0,0))
		image_ind+=1
		if image_ind>=12:
			image_ind=0
		
		if is_idle:	
			hero=idle[image_ind]
			hero=pg.transform.scale(hero,(100,100))
		elif is_moving:
			hero=walkRight[image_ind]
			hero=pg.transform.scale(hero,(100,100))
		elif  is_dying:
			hero=dying[image_ind]
			hero=pg.transform.scale(hero,(100,100))
			if image_ind==11:
				dead=True
		stab=0
	if dead:
		hero=dying[11]
		hero=pg.transform.scale(hero,(100,100))


	#event loop	
	for event in pg.event.get():
		#Exit strategy
		if event.type==pg.QUIT  :
			pg.quit()
			sys.exit()
		if event.type==pg.KEYDOWN:	
			if event.key==pg.K_ESCAPE:
				pg.quit()
				sys.exit()

		
	if stick_horizantal:
		screen.blit(background,(0,0))
	#draw a growing stick while mouse left is clicked	
	if pg.mouse.get_pressed()[0] and not desactivate_click:
		pg.mixer.music.load('Sounds/sus.wav')
		pg.mixer.music.play()
		x,y=first_obstacle.get_tr_pos()
		stick=pg.Rect(x-10,y+10,10,stick_height)	
		pg.draw.rect(screen,black,stick)
		stick_height-=2
		stick_drawn=True
		
	#animate the stick rotation and finding if the game is lost or won
	if stick_drawn and not pg.mouse.get_pressed()[0]:
		desactivate_click=True
		x,y=first_obstacle.get_tr_pos()	
		stick_surface= pg.Surface((10,-stick_height+10),pg.SRCALPHA)
		stick_surface.fill(black)
		angle+=1
		stick_surface=pg.transform.rotozoom(stick_surface,180-angle,1)
		rect=stick_surface.get_rect()
		xx,yy=rect.bottomleft
		comp=-stick_height-yy
		screen.blit(stick_surface,(x-10,y+stick_height+comp))		
		time.sleep(.01)
		stick_horizantal=True
						
		if angle==90:
			
			screen.blit(background,(0,0))
			screen.blit(stick_surface,(x-10,y+stick_height+comp+10))
			stick_drawn=False
			stick_all_set=True
			stick_horizantal=False
			angle=0
			if -stick_height<abs(second_obstacle.get_tl_pos()[0]-first_obstacle.get_tr_pos()[0]) or -stick_height>abs(second_obstacle.get_tr_pos()[0]-first_obstacle.get_tr_pos()[0]):
				game_lost=True
				adapt_hero=False

			else:
				adapt_hero=True
				game_won=True
				desactivate_click=False
				score+=1
				pg.mixer.music.load('Sounds/Bells6.mp3')
				pg.mixer.music.play()
				
				if high_score<score:
					high_score=score
					

	#moving everything to left 			
	if stick_all_set and game_lost==False :

		if second_obstacle.get_tr_pos()[0] >second_obstacle.get_width(): 
			screen.blit(background,(0,0))	
			first_obstacle.move(2)
			second_obstacle.move(2)
			third_obstacle.move(2)
			i-=2
			screen.blit(stick_surface,(x-10+i,y+stick_height+comp+10))
			is_moving=True
			is_idle=False
		else:
			stick_all_set=False		
			first_obstacle=second_obstacle
			second_obstacle=third_obstacle
			third_obstacle=Obstacle((screen_w,screen_h-350),random.randint(50, 200),500)
			stick_height=10
			angle=0
			i=0
			is_moving=False
			is_idle=True
			
	#adapting the hero position to the new obstacle
	if adapt_hero:			
		if first_obstacle.get_tr_pos()[0]-80>herox  :
			herox+=2
			screen.blit(background,(0,0))
			screen.blit(hero,(herox,heroy))
				
		elif abs(herox-second_obstacle.get_tr_pos()[0]) < 80:
			herox-=2
			screen.blit(hero,(herox,heroy))
			screen.blit(background,(0,0))

	

	# If the stick is short, rotating it to 180°
	if game_lost and stick_180==False and exceed_left :
		screen.blit(background,(0,0))
		x,y=first_obstacle.get_tr_pos()	
		stick_surface= pg.Surface((-stick_height,10),pg.SRCALPHA)
		stick_surface.fill(black)
		angle+=1
		stick_surface=pg.transform.rotozoom(stick_surface,-angle,1)
		screen.blit(stick_surface,(x-10,y))		
		time.sleep(.01)
		desactivate_click=True
		if angle==80:
			stick_180=True	


	#Simulating the fall of the hero if game lost
	if game_lost :
		desactivate_click=True
		if -stick_height<abs(second_obstacle.get_tl_pos()[0]-first_obstacle.get_tr_pos()[0]):
			exceed_left=True
		if -stick_height>abs(second_obstacle.get_tr_pos()[0]-first_obstacle.get_tr_pos()[0]):
			exceed_right=True

		if exceed_left and stick_180:
			herox+=1
			is_moving=True
			is_idle=False
			if herox>first_obstacle.get_tr_pos()[0] :				
				heroy+=2
				herox-=0.7
				is_dying=True
				is_moving=False
				is_idle=False
			screen.blit(background,(0,0))
			screen.blit(stick_surface,(x-10,y))

		elif exceed_right:
			herox+=2
			is_moving=True
			is_idle=False
			if herox>first_obstacle.get_tr_pos()[0]-stick_height-10:				
				heroy+=2
				herox-=0.7
				is_dying=True
				is_moving=False
				is_idle=False				
			screen.blit(background,(0,0))
			screen.blit(stick_surface,(x-10,y+stick_height+comp+10))

		#ending the game if hero touch screen borders
		if heroy+80>=screen_h or herox-80>=screen_w:
			pg.mixer.music.load('Sounds/sfx_hit.wav')
			pg.mixer.music.play()
			game_over=True
			stick_180=False
			game_lost=False
			stick_surface=pg.Surface((0,0))
			game_ended=True			

	
	#restarting the game 
	if pg.mouse.get_pressed()[2] and game_over:
		stick_height=10
		stick_drawn=False
		rotate=True
		angle=0
		i=0
		herox=0
		heroy=440
		stick_all_set=False
		stick_horizantal=False
		game_lost=False
		game_won=False
		stick_180=False
		game_over=False
		exceed_right=False
		exceed_left=False
		score=0
		adapt_hero=True
		game_ended=False
		image_ind=0		
		stab=0
		is_idle=True
		is_dying=False
		is_moving=False
		dead=False
		new_hs=False
		desactivate_click=False
		pg.mixer.music.load('Sounds/Bells2.mp3')
		pg.mixer.music.play()
	
	#Displaying the current score all the time
	score_dis_on(score)	
	#setting what to show depending on the outcome of the game
	if game_ended:
		if not pg.mouse.get_pressed()[2]:
			high_score_dis(high_score)
			if high_score==score:
				new_hs=True

			game_over_screen(new_hs)
			score_dis_on(score)	
		if pg.mouse.get_pressed()[2]:
			game_ended=False
	else:
		first_obstacle.draw(screen)	
		second_obstacle.draw(screen)
		third_obstacle.draw(screen)		
		screen.blit(hero,(herox,heroy))
		score_dis_on(score)	
    
    #updating the display
	pg.display.update()
    
    #setting the FPS (framerate)
	clock.tick(160)
