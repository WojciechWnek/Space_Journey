def the_game():
	""" Whole code closed in a function to make it possible for calling it from other app. """

	import random, pygame, os
	from superwires import games, color

	#Initializes screen
	games.init(screen_width = 600, screen_height = 700, fps = 100)
	pygame.display.set_caption("SPACE JOURNEY")

	class Collider(games.Sprite):
		
		def update(self):
			""" 
			Checks for collisions.
			overlapping_sprites is a games. Spirit method that detects if on sprite is on top of another.
			This method works fine but it returns True even when sprites backgrounds overlap.
			To overcome this problem and detect accurate collisions, I'm checking for those sprites if offset value is True.
			If result is True, one life is taken away.
			"""
			if self.overlapping_sprites:
				for sprite in self.overlapping_sprites:
					offset_x = sprite.get_x() -  self.get_x()
					offset_y = sprite.get_y() - self.get_y()
					offset = (int(offset_x), int(offset_y))
					result = self.mask.overlap(sprite.mask, offset)
					if result:
						sprite.die()
						new_bang = Bang(x = sprite.x, y = sprite.y)
						games.screen.add(new_bang)
						self.lives -= 1
						if self.lives <= 0:
							self.die()
					
		def die(self):
			""" Delete sprite from screen """
			self.destroy()


	class Background(games.Sprite):
		"""
		There is an games. Screen attribute, but it can only be set in place, so I've used non collidable sprite as background.
		It is made of two identical images that are displayed on top of each other and are continuously scrolling down.
		"""
		background_image = games.load_image(os.path.join('images', 'background_image.png'), transparent = False)
		background_velocity = 2

		def __init__(self, x, y):
			super(Background, self).__init__(image = Background.background_image, is_collideable = False)
			# x and y coordinates
			self.x = x
			self.y = y
		
		def update(self):
			""" Checks if one of images is over bottom edge of the screen then places it over top edge of the screen. """

			# value specifying how fast should it scroll down
			self.y += Background.background_velocity

			if self.y == games.screen.height/2 + games.screen.height:
				self.y = games.screen.height/2 - games.screen.height

		
	class Ship(Collider):
		"""
		Inherits form Collider class.
		"""
		ship_image = games.load_image(os.path.join('images', 'ship_image.png'))
		ship_velocity = 3

		def __init__(self, game, x, y):
			super(Ship, self).__init__(image = Ship.ship_image)
			self.game = game

			# x and y coordinates
			self.x = x
			self.y = y

			# mask for accurate collision detection
			self.mask = pygame.mask.from_surface(self.image)

			# value specifying times ship can collide
			self.lives = 5

		def update(self):
			"""
			In order not to overwrite Collider method, super is used.
			Ship sprite that can be moved around the screen with W, S, A, D keys.
			"""
			super(Ship, self).update()
			if games.keyboard.is_pressed(games.K_a) and self.get_left()  > 0:
				self.x -= Ship.ship_velocity
			if games.keyboard.is_pressed(games.K_d) and self.get_right() < games.screen.width:
				self.x += Ship.ship_velocity
			if games.keyboard.is_pressed(games.K_w) and self.get_top() > 0:
				self.y -= Ship.ship_velocity
			if games.keyboard.is_pressed(games.K_s) and self.get_bottom() < games.screen.height:
				self.y += Ship.ship_velocity

			# update lives label
			self.game.lives_label.set_value("Lives: " + str(self.lives))

		def die(self):
			""" Destroy the ship and finish the game. """
			global final_score
			final_score = self.game.score
			self.game.end()
			super(Ship, self).die()




	class Asteroid(games.Sprite):
		"""
		Asteroid sprite that is created before entering screen with random x and y coordinates.
		"""
		asteroid_image = games.load_image(os.path.join('images', 'asteroid_image.png'))
		asteroid_velocity = 2
		#constant holding amount of asteroids in one level
		span = 0

		def __init__(self, game):
			super(Asteroid, self).__init__(image = Asteroid.asteroid_image)
			self.game = game

			# x and y coordinates
			self.x = random.randint(0, games.screen.width)
			if self.game.level <= 10:
				self.y = random.randint(-games.screen.height * self.game.level, -100)
			else:
				self.y = random.randint(-games.screen.height *10, -100)

			# mask for accurate collision detection
			self.mask = pygame.mask.from_surface(self.image)

		def update(self):
			"""	After leaving screen it is destroyed."""
			self.y += Asteroid.asteroid_velocity
			if self.get_top() > games.screen.height:
				Asteroid.span -= 1
				self.destroy()
				# add points but only if player has lives and update score label
				if self.game.the_ship.lives:
					self.game.score += 5 * self.game.level
					self.game.score_label.set_value("Score: " + str(self.game.score))
					self.game.score_label.right = games.screen.width - 10

			# when there is no asteroids at the level generate new wave 
			if Asteroid.span == 0:
				self.game.wave()

		def die(self):
			""" Delete sprite from screen. """
			Asteroid.span -= 1
			self.destroy()


	class Bang(games.Sprite):
		""" Is used for displaying bang_image after collision. """
		bang_image = games.load_image(os.path.join('images', 'bang.png'))

		def __init__(self, x, y):
			super(Bang, self).__init__(image = Bang.bang_image, x = x, y = y,  is_collideable = False)

			# value specifying lifespan of this sprite 
			self.counter = 3

		def tick(self):
			"""
			Similar to update method but it is called every interval frames.
			Counts down before destroying sprite.
			"""
			self.counter-=1
			if not self.counter:
				self.destroy()

	class Game():
		""" Game itself with its methods. """
		def __init__(self):
			# create level variable
			self.level = 1
			# create score variable
			self.score = 0

			# create visible score label in upper right corner
			self.score_label = games.Text(value = "Score: 0",
									size = 40,
									color = color.white,
									top = 5,
									right = games.screen.width - 10,
									is_collideable = False)
			games.screen.add(self.score_label)

			# create visible level label in upper middle section
			self.level_label = games.Text(value = "Level 1",
										size = 40,
										color = color.white,
										x = games.screen.width/2,
										y = 20,
										is_collideable = False)
			games.screen.add(self.level_label)

			# add ship to the screen and place it in the middle
			self.the_ship = Ship(game = self, x = games.screen.width/2, y = games.screen.height - 200)
			games.screen.add(self.the_ship)

			# create visible lives label in upper left corner
			self.lives_label = games.Text(value = self.the_ship.lives,
										size = 40,
										color = color.white,
										x = 55,
										y = 20,
										is_collideable = False)
			games.screen.add(self.lives_label)

		def play(self):
			""" Starts the game. """
			self.wave()
			games.screen.mainloop()

		def wave(self):
			""" Creates amount of asteroids appropriate for each level. """
			if self.level <= 10:
				for i in range(self.level * 5):
					Asteroid.span += 1
			else:
				Asteroid.span = 60

			for i in range(Asteroid.span): #
				
				the_asteroid = Asteroid(game = self)
				games.screen.add(the_asteroid)

			# update level label
			self.level_label.set_value("Level " + str(self.level))

			self.level += 1

			# increase velocity of ship and asteroids
			Ship.ship_velocity += 0.2
			Asteroid.asteroid_velocity += 0.4

		def end(self):
			""" Ending message printed when out of lives. """
			end_message = games.Message(value = "Game Over",
										size = 90,
										color = color.red,
										x = games.screen.width/2,
										y = games.screen.height/2,
										lifetime = 3 * games.screen.fps,
										after_death = games.screen.quit,
										is_collideable = False)

			# add another message, because it is impossible to use \n messages
			score_message = games.Message(value="Your score: " + str(final_score),
										size=90,
										color=color.red,
										x=games.screen.width / 2,
										y=games.screen.height / 1.7,
										lifetime=3 * games.screen.fps,
										after_death=games.screen.quit,
										is_collideable=False)
			games.screen.add(end_message)
			games.screen.add(score_message)


	def add_background():
		""" It concretizes and displays two same background images to the screen. """
		the_background = Background(x = games.screen.width/2, y = games.screen.height/2)
		the_background2 = Background(x = games.screen.width/2 , y = games.screen.height/2 - games.screen.height)
		games.screen.add(the_background)
		games.screen.add(the_background2)

	def main():

		add_background()

		space_journey = Game()

		space_journey.play()

	main()

def pass_score():
	try:
		return final_score
	except:
		return 0

if __name__ == "__main__":
	the_game()

