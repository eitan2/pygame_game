import pygame as pg
from settings import *
import time
from particles import ParticleMaster

vec = pg.math.Vector2

class entity(pg.sprite.Sprite):
	def __init__(self, game, size_x, size_y, color, start_x, start_y, gravity, controlable, acc_, friction_, collide, air_friction):
		pg.sprite.Sprite.__init__(self)

		self.game = game
		self.size_x = size_x
		self.size_y = size_y
		self.color = color
		self.start_x = start_x
		self.start_y = start_y
		self.gravity = gravity
		self.controlable = controlable
		self.acc_ = acc_
		self.friction_ = friction_
		self.collide = collide
		self.air_friction = air_friction

		self.image = pg.Surface((self.size_x, self.size_y))
		self.image.fill(self.color)
		self.rect = self.image.get_rect()
		self.rect.center = (self.start_x, self.start_y)

		self.pos = vec(self.start_x, self.start_y)
		self.vel = vec(0, 0)
		self.acc = vec(0, 0)

	def update(self):
		self.acc = vec(0, self.gravity)

		hits = pg.sprite.spritecollide(self, self.game.platforms, False)
		if hits and self.collide:

			if self.vel.x < 0 and hits[0].rect.right < self.rect.left + 5: # Coll x
				self.vel.x = 0
				self.pos.x += 2
			elif self.vel.x > 0 and hits[0].rect.left > self.rect.right - 5:
				self.vel.x = 0
				self.pos.x -= 2

			elif self.vel.y > 0: # Coll y
				self.pos.y = hits[0].rect.top
				self.vel.y = 0
			elif self.vel.y < 0:
				self.pos.y = hits[0].rect.bottom + self.size_y
				self.vel.y = 0
				self.pos.y += 2

		self.rect.y += 2
		hits = pg.sprite.spritecollide(self, self.game.platforms, False)
		self.rect.y -= 2

		if (not hits) and self.air_friction: # Having less friction in air
			self.acc_ = 0.3
			self.friction_ = -0.05
		else:
			self.acc_ = 0.5
			self.friction_ = -0.12

		if self.controlable:
			# # # Input L/R
			keys = pg.key.get_pressed()
			if keys[pg.K_a]:
				self.acc.x = -self.acc_
			if keys[pg.K_d]:
				self.acc.x = self.acc_

		# # # Movement
		# apply friction
		self.acc.x += self.vel.x * self.friction_
		# equations of motion
		self.vel += self.acc
		self.pos += self.vel + 0.5 * self.acc

		# apply position
		self.rect.midbottom = self.pos

class Player(entity):
	def __init__(self, game):
		super().__init__(game, P_SIZE_X, P_SIZE_Y, RED, WIDTH/2, HEIGHT/2, P_GRAVITY, True, P_ACC, P_FRICTION, False, True)
		self.master = ParticleMaster()

	def update(self):
		super().update()
		
		self.master.update_effects()

	def jump(self):
		self.rect.y += 5
		hits = pg.sprite.spritecollide(self, self.game.platforms, False)
		self.rect.y -= 5
		if hits:
			self.vel.y = P_JUMP
			self.master.add_effect(self.game.screen, (RED, (255, 225, 225)), (0.2, 0.4), False, [*self.rect.center], (5, 10), False, 0.05, False, 1, 0.1, 1)

	def shoot(self, game):
		ms_x, ms_y = pg.mouse.get_pos()
		ms_pos = vec(ms_x, ms_y)
		diff = ms_pos - self.pos

		bvel = diff.normalize() * B_SPEED

		b = Bullet(game, self.rect.centerx, self.rect.centery, bvel)

		self.master.add_effect(game.screen, ((0, 0, 0), (255, 255, 255)), [0.2, 0.4], False, [ms_x, ms_y], (5, 10), True, 0.05, False, 3, 0.1, 1) # Target particles
		self.master.add_effect(game.screen, (YELLOW, WHITE), (0.2, 0.4), False, [self.rect.center[0] + bvel.x * 3, self.rect.center[1] + bvel.y * 3], (5, 10), False, 0, False, 1, 0.1, 1) # Gun particles

		return b

class Enemy(entity):
	def __init__(self, game):
		super().__init__(game, 30, 30, BLUE, 0, 0, P_GRAVITY, False, P_ACC, P_FRICTION, True, True)

class Bullet(entity):
	def __init__(self, game, x, y, vel):
		super().__init__(game, B_SIZE_X, B_SIZE_Y, YELLOWISH, x, y, 0, False, 1, -1, B_COLLIDE, False)
		self.vel = vel
		self.birth = time.time()

	def update(self):
		hits = pg.sprite.spritecollide(self, self.game.platforms, False)
		if hits and B_COLLIDE:
			if self.vel.x < 0 and hits[0].rect.right < self.rect.left + 5: # Coll x
				self.vel.x = 0
				self.pos.x += 2
			elif self.vel.x > 0 and hits[0].rect.left > self.rect.right - 5:
				self.vel.x = 0
				self.pos.x -= 2
			elif self.vel.y > 0: # Coll y
				self.pos.y = hits[0].rect.top
				self.vel.y = 0
			elif self.vel.y < 0:
				self.pos.y = hits[0].rect.bottom + self.size_y
				self.vel.y = 0
				self.pos.y += 2

		self.pos += self.vel

		self.rect.midbottom = self.pos

		if self.rect.right < -WIDTH or self.rect.left > WIDTH * 2 or self.rect.bottom < -HEIGHT or self.rect.top > HEIGHT * 2:
			self.kill()
		if (time.time()) - self.birth >= B_LIFETIME:
			self.kill()

class Platform(pg.sprite.Sprite):
	def __init__(self, x, y, w, h):
		pg.sprite.Sprite.__init__(self)

		self.image = pg.Surface((w, h))
		self.image.fill(GREEN)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y