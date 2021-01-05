import pygame as pg
import random
from settings import *
from sprites import *

class Game(object):
	def __init__(self): # Initialize
		pg.init()
		pg.mixer.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		pg.display.set_caption(TITLE)
		self.clock = pg.time.Clock()

		self.running = True

		self.font_name = pg.font.match_font(FONT_NAME)

	def new(self): # Start a new game
		self.all_sprites = pg.sprite.Group()
		self.platforms = pg.sprite.Group()
		self.entitys = pg.sprite.Group()
		self.bullets = pg.sprite.Group()

		self.player = Player(self)
		self.all_sprites.add(self.player)
		self.entitys.add(self.player)
		
		self.enemy = Enemy(self)
		self.all_sprites.add(self.enemy)
		self.entitys.add(self.enemy)

		for plat in PLATFORM_LIST:
			p = Platform(*plat)
			self.all_sprites.add(p)
			self.platforms.add(p)

		self.run()

	def run(self): # Game loop
		self.playing = True

		while self.playing:
			self.cls()

			self.clock.tick(FPS) # FPS

			self.events() # Input

			self.update() # Update - Proccesing

			self.draw() # Rendering

	def events(self): # Game Loop - Input
		for event in pg.event.get():
			if event.type == pg.QUIT:
				if self.playing:
					self.playing = False
				self.running = False
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_SPACE:
					self.player.jump()
			if event.type == pg.MOUSEBUTTONDOWN:
				b = self.player.shoot(self)
				self.all_sprites.add(b)
				self.entitys.add(b)
				self.bullets.add(b)

		#self.ms_x, self.ms_y = pg.mouse.get_pos()

	def update(self): # Game Loop - Update
		self.all_sprites.update()

		# Player collision
		hits = pg.sprite.spritecollide(self.player, self.platforms, False)
		if hits:

			if self.player.vel.x < 0 and hits[0].rect.right < self.player.rect.left + 5: # Coll x
				self.player.vel.x = 0
				self.player.pos.x += 2
			elif self.player.vel.x > 0 and hits[0].rect.left > self.player.rect.right - 5:
				self.player.vel.x = 0
				self.player.pos.x -= 2

			elif self.player.vel.y > 0: # Coll y
				self.player.pos.y = hits[0].rect.top
				self.player.vel.y = 0
			elif self.player.vel.y < 0:
				self.player.pos.y = hits[0].rect.bottom + P_SIZE_Y
				self.player.vel.y = 0
				self.player.pos.y += 2

		# Camera movement
		if self.player.rect.top <= HEIGHT / 4: # y
			for s in self.all_sprites:
				s.rect.y += abs(self.player.vel.y)
			for e in self.entitys:
				e.pos.y += abs(self.player.vel.y)
			for ef in self.player.master.effects:
				for p in ef[0].particles:
					p[0][1] += abs(self.player.vel.y)
		elif self.player.rect.bottom >= HEIGHT - HEIGHT / 4:
			for s in self.all_sprites:
				s.rect.y -= abs(self.player.vel.y)
			for e in self.entitys:
				e.pos.y -= abs(self.player.vel.y)
			for ef in self.player.master.effects:
				for p in ef[0].particles:
					p[0][1] -= abs(self.player.vel.y)
		if self.player.rect.left <= WIDTH / 4: # x
			for s in self.all_sprites:
				s.rect.x += abs(self.player.vel.x)
			for e in self.entitys:
				e.pos.x += abs(self.player.vel.x)
			for ef in self.player.master.effects:
				for p in ef[0].particles:
					p[0][0] += abs(self.player.vel.x)
		elif self.player.rect.right >= WIDTH - WIDTH / 4:
			for s in self.all_sprites:
				s.rect.x -= abs(self.player.vel.x)
			for e in self.entitys:
				e.pos.x -= abs(self.player.vel.x)
			for ef in self.player.master.effects:
				for p in ef[0].particles:
					p[0][0] -= abs(self.player.vel.x)
	
	def cls(self):
		self.screen.fill(LIGHTBLUE)

	def draw(self): # Game Loop - Draw
		self.all_sprites.draw(self.screen)
		# after drawing everything flip the display
		pg.display.flip()

	def show_start_screen(self): # Start screen
		self.screen.fill(LIGHTBLUE)
		self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/4)
		self.draw_text("Press a key to play", 22, WHITE, WIDTH/2, HEIGHT / 2)
		pg.display.flip()

		self.wait_for_key()

	def show_go_screen(self): # End screen
		self.screen.fill(LIGHTBLUE)
		self.draw_text("BYE", 48, WHITE, WIDTH/2, HEIGHT/4)
		self.draw_text("Press a key to quit", 22, WHITE, WIDTH/2, HEIGHT / 2)
		pg.display.flip()

		self.wait_for_key()

	def wait_for_key(self):
		waiting = True
		while waiting:
			self.clock.tick(FPS)
			for event in pg.event.get():
				if event.type == pg.QUIT:
					waiting = False
					self.running = False
				if event.type == pg.KEYUP:
					waiting = False

	def draw_text(self, text, textsize, color, x, y):
		font = pg.font.Font(self.font_name, textsize)
		text_surface = font.render(text, True, color)
		text_rect = text_surface.get_rect()
		text_rect.midtop = (x, y)
		self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
	g.new()
	if g.running:
		g.show_go_screen()

pg.quit()