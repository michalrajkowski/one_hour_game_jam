import pyxel
import random


class App:
    def __init__(self):
        pyxel.init(160, 120, title="One hour game jam")
        pyxel.load("assets.pyxres")
        pyxel.mouse(True)

        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)
        


       
App()