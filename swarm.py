from visual import *
from visual.graph import *
import random
import thread
import math


robot_list = []
WIDTH = 1000
LENGTH = 1000
HEIGHT = 50

color.brown = (0.38,0.26,0.078)
color.orange = (0.85,0.54,0.18)
arenafloor = box(pos=(0,0,0), size=(4,WIDTH,LENGTH), color=color.orange, axis=(0,1,0))
arenawall1 = box(pos=(-WIDTH/2,HEIGHT/2,0), size=(4,HEIGHT,LENGTH), color=color.orange)
arenawall2 = box(pos=(WIDTH/2,HEIGHT/2,0), size=(4,HEIGHT,LENGTH), color=color.orange)
arenawall3 = box(pos=(0,HEIGHT/2,-LENGTH/2), size=(WIDTH,HEIGHT,4), color=color.orange)
arenawall4 = box(pos=(0,HEIGHT/2,LENGTH/2), size=(WIDTH,HEIGHT,4), color=color.orange)

#tower = box(pos=(0,0,-100), size=(5,100,5), color=color.brown, axis=(1,0,0))
scene.ambient = 0

class Food(object):
	def __init__(self):
		self.x = random.randint(-WIDTH/2+30,WIDTH/2-30)
		self.y = 17
		self.z = random.randint(-LENGTH/2+30,LENGTH/2-30)
		self.box = box(pos=(self.x,self.y,self.z), size=(30,30,30), color=color.green, axis=(1,0,0), material = materials.emissive)
		self.intensity = 1.00
		self.time_off = random.randint(1,9)
		self.time_on = random.randint(1,9)
		self.state = True


	def update(self):
		while True:
			self.state = True
			self.intensity = 1.00
			self.box = box(pos=(self.x,self.y,self.z), size=(30,30,30), color=color.green, axis=(1,0,0), material = materials.emissive)
			time.sleep(self.time_on)
			self.state = False
			self.intensity = 0
			self.box = box(pos=(self.x,self.y,self.z), size=(30,30,30), color=color.orange, axis=(1,0,0), material = materials.emissive)
			time.sleep(self.time_off)
			rate(100)










class Robot(object):
	def __init__(self):
		global food_list
		self.x = random.randint(-WIDTH/2+30,WIDTH/2-3)
		self.y = 7
		self.z  = random.randint(-LENGTH/2+30,LENGTH/2-30)
		self.box = box(pos=(self.x,self.y,self.z), size=(30,10,10), color=color.blue, axis=(1,0,0), material = materials.emissive)
		self.state = "alive"
		self.intensity =1 #random.randint(80,120)
		#self.box = box(pos=(self.x,self.y,self.z), size=(30,10,10), color=color.red, axis=self.heading, material = materials.emissive)
		self.leftlvl = 0
		self.rightlvl = 0
		self.turning_speed = random.randint(0,15)
		self.forwards_speed = random.randint(0,40)
		self.energy = 100000
		self.range = 800#random.randint(50,800)

	def forwards(self,number_of_repeats):
		for x in xrange(number_of_repeats):
			self.box.pos += self.box.axis/100
			#time.sleep(0.01)

	def backwards(self,number_of_repeats):
		for x in xrange(number_of_repeats):
			self.box.pos -= self.box.axis/100
			#self.lamp.pos = self.box.pos
			#time.sleep(0.01)

	def anticlockwise(self,number_of_repeats):
		for y in xrange(number_of_repeats):
			self.box.rotate(angle=0.05, axis = (0,1,0), origin = self.box.pos)
			rotate(vector=self.box.axis, angle=0.1, axis=(0,1,0))
			#time.sleep(0.1)

	def clockwise(self,number_of_repeats):
		for y in xrange(number_of_repeats):
			self.box.rotate(angle=-0.05, axis = (0,1,0), origin = self.box.pos)
			rotate(vector=self.box.axis, angle=0.1, axis=(0,1,0))
			#time.sleep(0.1)	

	def left_sensor(self):
		#find the corners first
		self.middlevector = norm(self.box.axis)
		self.perp = cross(self.middlevector,(0,1,0))
		self.midfront = self.box.pos+15*self.middlevector
		#print midfront
		self.leftcorner = self.midfront+self.perp*5
		for r in food_list:
			self.distance = mag(-self.leftcorner+r.box.pos)
			if self.distance < self.range:
				self.leftlvl +=r.intensity/1.33*math.pi*self.distance**3
			else:
				self.rightlvl +=0




	def right_sensor(self):
		#find the corners first
		self.middlevector = norm(self.box.axis)
		self.perp = cross(self.middlevector,(0,1,0))
		self.midfront = self.box.pos+15*self.middlevector
		#print midfront
		self.rightcorner = self.midfront-self.perp*5
		for r in food_list:
			self.distance = mag(-self.rightcorner+r.box.pos)
			if self.distance < 600:
				self.rightlvl +=r.intensity/1.33*math.pi*self.distance**3
			else:
				self.rightlvl += 0



	def update(self):
		while True:
			self.leftlvl = 0
			self.rightlvl = 0
			self.left_sensor()
			self.right_sensor()
			if self.state == "alive":
				if self.energy > 0:
					if self.leftlvl >=self.rightlvl-200:
						self.anticlockwise(self.turning_speed)
						self.energy -= self.turning_speed**2
					elif self.leftlvl <=self.rightlvl+200:
						self.clockwise(self.turning_speed)
						self.energy -= self.turning_speed**2
					else: 
						self.forwards(self.forwards_speed)
						self.energy -= self.forwards_speed**2
					self.forwards(self.turning_speed)
					self.energy -= self.turning_speed**2
				else:
					self.box.color = color.red
					self.state = "dead"
					
				if (self.leftlvl +self.rightlvl)*0.5 > 1600000:
					self.energy += (self.turning_speed**2)
			else:
				pass


			rate(24)



food_list = []

for x in xrange(6):
	food_list.append(Food())


for x in xrange(45):
	robot_list.append(Robot())


for f in food_list:
	thread.start_new_thread(f.update,())

total = 0
for r in robot_list:
	thread.start_new_thread(r.update,())
	total += r.range




