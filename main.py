import pyxel
import random

dice_sprites = {
    1: (0,0),
    2: (16,0),
    3: (32,0),
    4: (48,0),
    5: (64,0),
    6: (80,0),
}

SPIN_DICES_BUTTON = (0, 80, 36, 16)
PASS_BUTTON = (0, 100, 36, 16)
DICE_DRAWING_AREA = (60, 100)
DICE_SPACING = (3, 0)


class App:
    def __init__(self):
        pyxel.init(160, 120, title="Gamble Game")
        pyxel.load("assets.pyxres")
        pyxel.mouse(True)
        self.player_dices_amount = 5
        self.player_dices = {}
        self.selected_dices = {}
        for i in range(self.player_dices_amount):
            self.player_dices[i] = random.randint(1,6)
            self.selected_dices[i] = True


        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.dice_selector()
        self.handle_buttons()

    def draw(self):
        pyxel.cls(0)
        self.draw_board()
        self.draw_player_dices()
        self.draw_buttons()


    def draw_player_dices(self):
        # Draw player 5 dices 
        for i in range(self.player_dices_amount):
            dice_result = self.player_dices[i]
            dice_sprite = dice_sprites[dice_result]
            pyxel.blt(DICE_DRAWING_AREA[0] + i*(16 + DICE_SPACING[0]),DICE_DRAWING_AREA[1], 0, dice_sprite[0], dice_sprite[1], 16, 16)
            if (self.selected_dices[i]):
                # Draw selection mark
                pyxel.rectb(DICE_DRAWING_AREA[0] + i*(16 + DICE_SPACING[0]),DICE_DRAWING_AREA[1], 16, 16, 8)

    def dice_selector(self):
        pass

    def draw_buttons(self):
        pyxel.rect(SPIN_DICES_BUTTON[0], SPIN_DICES_BUTTON[1], SPIN_DICES_BUTTON[2], SPIN_DICES_BUTTON[3], 11)
        pyxel.rectb(SPIN_DICES_BUTTON[0], SPIN_DICES_BUTTON[1], SPIN_DICES_BUTTON[2], SPIN_DICES_BUTTON[3], 7)
        pyxel.text(SPIN_DICES_BUTTON[0]+3, SPIN_DICES_BUTTON[1]+3, "Roll\nSelected", 7)

        pyxel.rect(PASS_BUTTON[0], PASS_BUTTON[1], PASS_BUTTON[2], PASS_BUTTON[3], 14)
        pyxel.rectb(PASS_BUTTON[0], PASS_BUTTON[1], PASS_BUTTON[2], PASS_BUTTON[3], 7)
        pyxel.text(PASS_BUTTON[0]+3, PASS_BUTTON[1]+3, "PASS", 7)

    def check_buttton_area(self, button, mouse):
        if (button[0] <= mouse[0] <=button[0]+button[2] and button[1]<= mouse[1] <= button[1]+button[3]):
            return True
        return False

    def handle_buttons(self):
        if not pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            return
        (mouse_x, mouse_y) = (pyxel.mouse_x, pyxel.mouse_y)
        
        for i in range(self.player_dices_amount):
            if self.check_buttton_area((DICE_DRAWING_AREA[0] + i*(16 + DICE_SPACING[0]), DICE_DRAWING_AREA[1], 16, 16), (mouse_x, mouse_y)):
                self.selected_dices[i] = not self.selected_dices[i]


        if self.check_buttton_area(SPIN_DICES_BUTTON, (mouse_x, mouse_y)):
            # Calculate the sum
            current_sum = 0
            for i in range(self.player_dices_amount):
                current_sum += self.player_dices[i]
            # roll dices
            for i in range(self.player_dices_amount):
                if self.selected_dices[i]:
                    self.selected_dices[i] = False
                    self.player_dices[i] = random.randint(1,6)
            # Calculate new sum
            new_sum = 0
            for i in range(self.player_dices_amount):
                new_sum += self.player_dices[i]
            # Check if sum is not smaller
            if new_sum >= current_sum:
                # correct behaviour
                pass

            else:
                # Fail
                pass
            
        if self.check_buttton_area(PASS_BUTTON, (mouse_x, mouse_y)):

    def draw_board(self):
        pyxel.rect(0,0,160,120,3)


        
App()