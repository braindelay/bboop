#!/usr/bin/python3
import random
import pygame

from pygame import sprite
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)


#pygame.sprite.collide_circle
# some constants - these will never change
BOOP_SIZE = 20
SCREEN_WIDTH=400
SCREEN_HEIGHT=700

BALL_COLOURS=[
	(255,0,0),
	(0,255,0),
	(0,0,255),
	(183,53,233),
	(233,163,33),
	(63,123,83),
	(135,0,93)
]
BLACK=(0,0,0)

# the different states the came can be in
state = None
STATE_WAITING=0
STATE_FIRING=1
STATE_FALLING=2
STATE_RESET_BIBBLE=3
STATE_YOU_LOSE=4
STATE_YOU_WIN=5

class Ball(pygame.sprite.Sprite):
	
	def __init__(self, colour):
		#call the parentclass_
		super().__init__()

		self.image=pygame.Surface([BOOP_SIZE, BOOP_SIZE])
		pygame.draw.circle(self.image, colour, [10, 10], 10)
		
		self.colour = colour

		self.rect = self.image.get_rect()

		self.x_speed = 0
		self.y_speed = 0

		self.x=self.rect.x
		self.y=self.rect.y

		self.moving = False
		self.radius = BOOP_SIZE /2


	def place(self, x, y):
		self.rect.x=x
		self.rect.y=y
		self.x= x
		self.y=y

	def fire_bibble(self, x,y):
		base = float(x - self.x)
		height = float(y -self.y)
		diagonal = (base ** 2 + height ** 2) ** 0.5

		ball_speed = 1.0 / diagonal

		self.x_speed = ball_speed * base
		self.y_speed = ball_speed * height

		self.moving= True

		#print ("mouse", x, y, "bibble", self.x, self.y)
		#print ("base", base, "eight", height)
		#print ("xs", self.x_speed,"ys", self.y_speed)

	def touch_same_colour(self, other):
		return self.colour==other.colour and self.touch(other)

	def touch(self, other):
		return sprite.collide_circle(self, other)


	def fall(self):
		global falling_balls
		self.rect.y=self.rect.y+15

		if self.rect.y>=SCREEN_HEIGHT:
			falling_balls.remove(self)
			ball_list.remove(self)
			holding_boops.remove(self)
		
	def slide(self):
		global state

		if not self.moving:
			self.rect.y=self.rect.y+1

			if self.rect.y>=SCREEN_HEIGHT:
				state=STATE_YOU_LOSE

	# move the ball when it's fired
	def move(self):
		# we want to move 10 steps, but if we just move
		# 10 steps the ball will often detect collision
		# half way through another ball
		# So we do it in 10 steps of 1.
		# @Martha: when you're older and learn vectors, there's
		# 			a cleaner way to do this ;)
		for i in range(0,10):
			if state == STATE_FIRING:
				self.inner_move()
	
	# move one step, and check if the ball has hit another ball
	# and then move to the next state
	def inner_move(self):
		global state
		global falling_balls
		global holding_boops
		if self.moving:

			# have i hit other boops
			for other in ball_list:
				if self != other:
					#if self.rect.colliderect(other.rect):
					if sprite.collide_circle(self, other):
						self.moving = False
						hits = HitChecker.check(self,ball_list)

						if len(hits) >2:
							falling_balls = hits
							for h in hits:
								holding_boops.remove(h)

							remaining_boops=[]
							for check in ball_list:
								if check not in hits:
									remaining_boops.append(check)
							
							#print("remaining %s", len(remaining_boops))
							for check in remaining_boops:
								#print('\n-------------------------------------')
								x = HitChecker.touching_holding(check, remaining_boops)
								#print ("xxx:%s", x)
								if not x:
									#print ("adding to falling balls %s %s" %(check.x,check.y))
									falling_balls.add(check)
							
							state = STATE_FALLING
							return

						state = STATE_RESET_BIBBLE
						break


			if self.moving:
				touch_dist=BOOP_SIZE/2

				# do i need to bounce of the sides
				if 	self.x <touch_dist or  self.x>SCREEN_WIDTH-touch_dist:
					self.x_speed=self.x_speed*-1

				# have I gone off the top
				if self.y<0:
					ball_list.remove(self)
					holding_boops.remove(self)
					state = STATE_RESET_BIBBLE

				# move the bibble
				self.x = self.x + self.x_speed
				self.y = self.y + self.y_speed

				self.rect.x=self.x
				self.rect.y=self.y

			#print("where am I?", self.x,self.y, self.x_speed, self.y_speed)


class HitChecker:

	def check(bibble, boops, ignore_colour=False):
		# when we're done, this will bethe set of balls that bibble touches
		# either directly or indirectly
		# bibble will always be in this group
		hits=pygame.sprite.Group()

		# during the loop, this will be reset, so at the start
		# of each loop ONLY the ball we've just added to hits will be here
		new_hits=pygame.sprite.Group()
		new_hits.add(bibble)

		# if this is empty, then we didn't add any new
		# balls to the hits, so we can stop
		while len(new_hits.sprites()) > 0:
			# what do we need to check
			# since there's no need to check things twice, this gets reset to only the
			# new hits list
			hits_to_check = pygame.sprite.Group()
			hits_to_check.add(new_hits)
			new_hits.empty()

			# is there anything new in the all bibbles list?
			for check in hits_to_check:
				# check all the boops
				for other in boops:
					# no need to check it if we already know it's there
					if other not in hits:
						if ignore_colour and other.touch(check) or other.touch_same_colour(check):
							#if there is then add it to the new hits list
							new_hits.add(other)
			hits.add(new_hits)
		return hits

	def touching_holding(check, remaining_boops):
		all_touches= HitChecker.check(check, remaining_boops, ignore_colour=True)
		
		for t in all_touches:
			if t in holding_boops:
				return True
	
	
# this creates a new ball, places it where you want it, and
# adds it to the ball list
def draw_ball(x, y):
	colour=BALL_COLOURS[random.randint(0,len(BALL_COLOURS)-1)]
	ball=Ball(colour)

	ball.place(x,y)
	ball_list.add(ball)

	return ball

# draw a line of boops
def draw_line(x,y,num_balls):
	line=pygame.sprite.Group()

	for i in range(0,num_balls):
		bibble = draw_ball(x+ i*BOOP_SIZE,y)
		line.add(bibble)
	return line

# draw a triangle of boops at the top of the screen
def draw_boops(screen):
	top_x = screen.get_width()/2
	top_y=BOOP_SIZE
	for i in range(0,7):
		num_balls=7-i
		line = draw_line(
			top_x - num_balls * BOOP_SIZE/2,
			top_y + i * (BOOP_SIZE - 3),
			num_balls)   
		if i ==0:
			holding_boops =line
	return holding_boops

def draw_bibble(screen):
	global state
	global bibble
	bottom_x = screen.get_width()/2
	bottom_y = screen.get_height()- BOOP_SIZE
	bibble = draw_ball(bottom_x,bottom_y)
	state=STATE_WAITING





#initialize pygame
pygame.init()
screen=pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
# create a single list for all the boops
# we use this so it's easy to draw them
 # all at once
ball_list=pygame.sprite.Group()

holding_boops=draw_boops(screen)
draw_bibble(screen)

done=False
clock=pygame.time.Clock()
# run until x isclicked

falling_balls=pygame.sprite.Group()

slide_counter=0
slide_step=30
while not done:
	# have I clicked on something
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			done=True
		# if I've clicked, fire bibble
		if state==STATE_WAITING and event.type == pygame.MOUSEBUTTONUP:
			mouse = pygame.mouse.get_pos()
			x=mouse[0]-BOOP_SIZE/2
			y=mouse[1]-BOOP_SIZE/2
			bibble.fire_bibble(x,y)
			state=STATE_FIRING

	# move sprites
	for boop in ball_list:
		boop.move()

	if state==STATE_FALLING:
		for b in falling_balls:
			b.fall()
		if len(falling_balls)==len(ball_list):
			state=STATE_YOU_WIN
		elif len(falling_balls)==0:
			state=STATE_RESET_BIBBLE
	
	slide_counter=slide_counter+1
	if slide_counter%slide_step==0:
		for boop in ball_list:
			if boop != bibble:
				boop.slide()


	if state==STATE_RESET_BIBBLE:
		draw_bibble(screen)

	# clear screen and draw balls
	screen.fill(BLACK)


	# if the game is over, then show the page
	# otherwise wait 1/60th of a second
	# and loop
	if state==STATE_YOU_LOSE:
		textsurface=myfont.render('you lose',False,(255,0,0))
		screen.blit(textsurface,(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
	elif state==STATE_YOU_WIN:
		textsurface=myfont.render('you win',False,(0,255,0))
		screen.blit(textsurface,(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
	else:
		ball_list.draw(screen)
		clock.tick(60)
	
	pygame.display.flip()


pygame.quit()
