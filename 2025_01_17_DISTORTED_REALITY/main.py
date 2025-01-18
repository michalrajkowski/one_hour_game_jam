import pyxel
import math
import random

class Game:
    def __init__(self):
        self.width = 256
        self.height = 256
        self.center_y = self.height // 2

        pyxel.init(self.width, self.height, title="Distorted Reality")
        pyxel.load("assets.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)

Game()