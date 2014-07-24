from visual import *
from visual.graph import *
import random
import thread
import math

WIDTH = 400
LENGTH = 400
HEIGHT = 50
robot_list = []

color.brown = (0.38,0.26,0.078)
color.orange = (0.85,0.54,0.18)
arenafloor = box(pos=(0,0,0), size=(4,WIDTH,LENGTH), color=color.orange, axis=(0,1,0))
arenawall1 = box(pos=(-WIDTH/2,HEIGHT/2,0), size=(4,HEIGHT,LENGTH), color=color.orange)
arenawall2 = box(pos=(WIDTH/2,HEIGHT/2,0), size=(4,HEIGHT,LENGTH), color=color.orange)
arenawall3 = box(pos=(0,HEIGHT/2,-LENGTH/2), size=(WIDTH,HEIGHT,4), color=color.orange)
arenawall4 = box(pos=(0,HEIGHT/2,LENGTH/2), size=(WIDTH,HEIGHT,4), color=color.orange)

#tower = box(pos=(0,0,-100), size=(5,100,5), color=color.brown, axis=(1,0,0))
#scene.ambient = 0


class Robot(object):
	def __init__(self):
		global robot_list
		self.x = random.randint(-140,140)
		self.y = 7
		self.z = random.randint(-140,140)
		self.heading = (1,0,0)
		self.box = box(pos=(self.x,self.y,self.z), size=(30,10,10), color=color.red, axis=self.heading, material = materials.emissive)
		self.leftlvl = 0
		self.rightlvl = 0
		#self.lamp = local_light(pos=(self.x,self.y,self.z), color=color.red)

	def forwards(self,number_of_repeats):
		for x in xrange(number_of_repeats):
			self.box.pos += self.box.axis/100
			time.sleep(0.01)

	def backwards(self,number_of_repeats):
		for x in xrange(number_of_repeats):
			self.box.pos -= self.box.axis/100
			#self.lamp.pos = self.box.pos
			time.sleep(0.01)

	def anticlockwise(self,number_of_repeats):
		for y in xrange(number_of_repeats):
			self.box.rotate(angle=0.1, axis = (0,1,0), origin = self.box.pos)
			rotate(vector=self.box.axis, angle=0.1, axis=(0,1,0))
			time.sleep(0.1)

	def clockwise(self,number_of_repeats):
		for y in xrange(number_of_repeats):
			self.box.rotate(angle=-0.1, axis = (0,1,0), origin = self.box.pos)
			rotate(vector=self.box.axis, angle=0.1, axis=(0,1,0))
			time.sleep(0.1)	

	def left_sensor(self):
		#find the corners first
		self.middlevector = norm(self.box.axis)
		self.perp = cross(self.middlevector,(0,1,0))
		self.midfront = self.box.pos+15*self.middlevector
		#print midfront
		self.leftcorner = self.midfront-self.perp*5
		for r in robot_list:
			self.distance = mag(-self.leftcorner+r.box.pos)
			if self.distance > 16:
				self.leftlvl +=100/math.pi*self.distance**2




	def right_sensor(self):
		#find the corners first
		self.middlevector = norm(self.box.axis)
		self.perp = cross(self.middlevector,(0,1,0))
		self.midfront = self.box.pos+15*self.middlevector
		#print midfront
		self.rightcorner = self.midfront+self.perp*5
		for r in robot_list:
			self.distance = mag(-self.rightcorner+r.box.pos)
			if self.distance > 16:
				self.rightlvl +=100/math.pi*self.distance**2



	def update(self):
		while True:
			self.leftlvl = 0
			self.rightlvl = 0
			self.left_sensor()
			self.right_sensor()
			if self.leftlvl >=self.rightlvl:
				self.clockwise(10)
			else:
				self.anticlockwise(10)
			self.forwards(30)





robot_list = []
for x in xrange(50):
	robot_list.append(Robot())



for r in robot_list:
	thread.start_new_thread(r.update,())




