import pyxel
import math
import random

class MovingSprite:
    def __init__(self, x, amplitude, frequency, phase, speed):
        self.x = x
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase
        self.speed = speed

    def update(self, game_speed):
        self.x -= self.speed * game_speed

    def draw(self, center_y):
        y = center_y + self.amplitude * math.sin(self.frequency * self.x + self.phase)
        pyxel.rect(self.x, y, 24, 16, pyxel.frame_count % 16)
        pyxel.blt(self.x, y, 0, 0,0,24,16,8)

class Player:
    def __init__(self, x, y, game):
        self.x = x
        self.y = y
        self.width = 8
        self.height = 8
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.game = game

    def update(self, game_speed):
        self.vx = 0
        if pyxel.btn(pyxel.KEY_A):
            self.vx = -3
        if pyxel.btn(pyxel.KEY_D):
            self.vx = 3
        if pyxel.btn(pyxel.KEY_S):
            if self.vy < 0:
                self.vy = 0
            self.vy += 1.0 * 1.0

        self.vy += 0.2 * game_speed

        print(self.on_ground)
        if self.on_ground and pyxel.btnp(pyxel.KEY_W):
            self.vy = -6
            self.on_ground = False
            self.y += -5

        self.x += self.vx
        self.y += self.vy

        if self.y > pyxel.height:
            self.reset()

    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, 9)

    def reset(self):
        self.x = pyxel.width // 2
        self.y = pyxel.height // 2 - 100
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.game.game_speed = 1.0
        self.game.speed_increment = 0.01

    def check_collision(self, sprite, center_y):
        sprite_y = center_y + sprite.amplitude * math.sin(sprite.frequency * sprite.x + sprite.phase)
        if (self.x + self.width > sprite.x - 4 and
            self.x - self.width < sprite.x + 16 and
            self.y + self.height > sprite_y - 6 and
            self.y + self.height < sprite_y + 6):
            self.y = sprite_y - self.height
            self.vy = 0
            self.on_ground = True
            self.found_this_frame=True
        else:
            self.on_ground = False

class Game:
    def __init__(self):
        self.width = 256
        self.height = 256
        self.center_y = self.height // 2
        self.sprites = []
        self.horizontal_spacing = 100
        self.game_speed = 1.0
        self.speed_increment = 0.01
        self.high_score = 0.0

        self.player = Player(self.width // 2, self.center_y - 20, self)

        self.initialize_sprites()

        pyxel.init(self.width, self.height, title="Carousel")
        pyxel.load("assets.pyxres")
        pyxel.run(self.update, self.draw)

    def initialize_sprites(self):
        num_sprites = self.width // self.horizontal_spacing + 2
        for i in range(num_sprites):
            x_position = self.width + i * self.horizontal_spacing
            new_sprite = MovingSprite(
                x=x_position,
                amplitude=30,
                frequency=0.05,
                phase=0,
                speed=2
            )
            self.sprites.append(new_sprite)

    def update(self):
        self.game_speed += self.speed_increment / 30
        self.speed_increment += 0.01 / 30

        for sprite in self.sprites:
            sprite.update(self.game_speed)

        for sprite in self.sprites:
            if sprite.x < -10:
                sprite.x = max(s.x for s in self.sprites) + self.horizontal_spacing

        self.player.found_this_frame = False
        for sprite in self.sprites:
            if self.player.found_this_frame:
                break
            self.player.check_collision(sprite, self.center_y)

        self.player.update(self.game_speed)

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)
        for sprite in self.sprites:
            sprite.draw(self.center_y)
        self.player.draw()
        self.draw_speed()

    def draw_speed(self):
        if self.high_score < self.game_speed:
            self.high_score = self.game_speed
        speed_text = f"Speed: {self.game_speed:.2f}"
        highschore_text = f"Highschore: {self.high_score:.2f}"
        pyxel.text(5, 5, speed_text, 7)
        pyxel.text(170, 5, highschore_text, 7)

Game()