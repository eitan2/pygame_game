import pygame as pg
import sys, random, time
from settings import *

class Particle:
	def __init__(self, screen, color=[[255, 255, 255], [0, 0, 0]], decrease_by=[0.2, 0.4], follow_mouse=False, pos=[0, 0], radius=[10, 10], rect=False, gravity=0, gray=False, speed=3):
		self.particles = []

		self.screen = screen

		self.color = color
		self.gray = gray

		self.follow_mouse = follow_mouse # position
		self.pos = pos

		self.radius = radius # size
		self.decrease_by = decrease_by

		self.rect = rect # shape

		self.gravity = gravity

		self.speed = speed

	def emit(self):
		if self.particles:
			self.delete_particles()
			for particle in self.particles:
				particle[0][1] += particle[2][0]
				particle[0][0] += particle[2][1]

				particle[2] = [particle[2][0] + self.gravity, particle[2][1]]

				for p in particle[0]: p = int(p)
				particle[1] -= random.uniform(self.decrease_by[0], self.decrease_by[1])

				color = particle[3]

				if self.rect:
					pg.draw.rect(self.screen, color, (*particle[0], particle[1]*2, particle[1]*2))
				else:
					pg.draw.circle(self.screen, color, [int(particle[0][0]), int(particle[0][1])], int(particle[1]))

	def add_particles(self):
		pos_x = self.pos[0]
		pos_y = self.pos[1]
		if self.follow_mouse:
			pos_x = pg.mouse.get_pos()[0]
			pos_y = pg.mouse.get_pos()[1]

		radius = random.uniform(self.radius[0], self.radius[1])

		direction_x = random.uniform(-self.speed, self.speed)
		direction_y = random.uniform(-self.speed, self.speed)

		color = [0, 0, 0]
		if self.gray:
			scale = random.randint(self.color[0][0], self.color[1][0])
			color = [scale, scale, scale]
		else:
			color = [
			random.randint(self.color[0][0], self.color[1][0]),
			random.randint(self.color[0][1], self.color[1][1]),
			random.randint(self.color[0][2], self.color[1][2])
			]

		particle_circle = [[int(pos_x), int(pos_y)],radius,[direction_x,direction_y], color]
		self.particles.append(particle_circle)

	def delete_particles(self):
		particle_copy = [particle for particle in self.particles if particle[1] > 0]
		self.particles = particle_copy

class ParticleMaster():
	def __init__(self):
		self.effects = []

		PARTICLE_EVENT = pg.USEREVENT + 1
		pg.time.set_timer(PARTICLE_EVENT,40)

	def add_effect(self, screen, color=[[255, 255, 255], [0, 0, 0]], decrease_by=[0.2, 0.4], follow_mouse=False, pos=[0, 0], radius=[10, 10], rect=False, gravity=0, gray=False, speed=3, lifetime=10, spawn_speed=4):

		self.effects.append([Particle(screen, color, decrease_by, follow_mouse, pos, radius, rect, gravity, gray, speed), lifetime, time.time(), spawn_speed, spawn_speed])

		#0 = Particle Obj, 1 = maximum lifetime seconds, 2 = birth seconds, 3 = const spawn speed frames, 4 = time since last spawn frames
	def update_effects(self):
		for e in self.effects:
			e[0].emit() # update

			e[4] += 1 # increase frames since last spawn

			if e[4] >= e[3] and not time.time() - e[2] > e[1]: # should spawn a new particle?
				e[0].add_particles()
				e[4] = 0

			if time.time() - e[2] > e[1] + (e[0].radius[1] / e[0].decrease_by[1] / FPS): # should die?
				self.effects.remove(e)

#master = ParticleMaster()
#master.add_effect(((0, 0, 0), (255, 255, 255)), (0.2, 0.5), False, (250, 250), (5, 10), True, 0.2, False, 3, 10, 2)