import pyxel
import random
import math


class App:
    def __init__(self):
        pyxel.init(160, 120, title="One hour game jam: DARKNESS")
        pyxel.load("assets.pyxres")
        pyxel.mouse(True)

        # Create darkness dots
        self.darkness_dots = []
        x_range = (0, 160)
        y_range = (0, 120)

        for _ in range(3000):
            x = random.randint(x_range[0], x_range[1])
            y = random.randint(y_range[0], y_range[1])
            self.darkness_dots.append((x, y))

        self.fuel = []
        for _ in range(3):
            x = random.randint(x_range[0], x_range[1])
            y = random.randint(y_range[0], y_range[1])
            self.fuel.append((x, y))

        self.lost_kids = []
        for _ in range(3):
            x = random.randint(x_range[0], x_range[1])
            y = random.randint(y_range[0], y_range[1])
            self.lost_kids.append((x, y))

        self.max_fuel_counter = 10.0
        self.fuel_counter = 10.0
        self.light_strength = 15.0
        self.max_light_strength = 15.0
        self.kids_found = 0
        pyxel.run(self.update, self.draw)


    def is_in_range(self, x, y):
        if (0 <= x <= 159 and 0 <= y <= 120):
            return True
        return False

    def update(self):
        # Darkness dots chaotic move
        self.update_darkness_dots_pos()
        # repell dots from light?
        self.repell_darkness_dots()
        self.click_on_fuel()

        self.light_strength -= float(1/60)

        self.fuel_counter -= float(1/30)
        if self.fuel_counter <= 0.0:
            self.fuel_counter = self.max_fuel_counter
            self.spawn_fuel()

        self.click_on_kid()

    def draw(self):
        pyxel.cls(0)

        self.draw_game_background()
        self.draw_light_around_mouse()
        self.draw_fuel()
        self.draw_lost_kids()
        self.draw_darkness_dots()
        self.draw_ui_text()
    

    def draw_ui_text(self):
        pyxel.rect(0,0,60, 15, 0)
        pyxel.rectb(0,0,60, 15, 7)
        pyxel.text(2,2,f"Kids found: {self.kids_found}", 7)
        pyxel.text(2, 8, f"Fuel: {round(self.light_strength, 1)}", 7)
    def draw_lost_kids(self):
        for x,y in self.lost_kids:
            pyxel.blt(x, y, 0, 0, 0, 16, 16, 0)
    def spawn_fuel(self):
        x_range = (0, 160)
        y_range = (0, 120)

        for _ in range(1):
            x = random.randint(x_range[0], x_range[1])
            y = random.randint(y_range[0], y_range[1])
            self.fuel.append((x, y))

    def click_on_kid(self):
        if not pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            return
        # check if clicked on fuel
        new_kids = []
        for x,y in self.lost_kids:
            if x <= pyxel.mouse_x <= x + 16 and y <= pyxel.mouse_y <= y+16:
                # Clicked on fuel
                # Add point
                self.kids_found+=1
                # Spawn in new place
                x_range = (0, 160 - 16)
                y_range = (0, 120 - 16)
                x = random.randint(x_range[0], x_range[1])
                y = random.randint(y_range[0], y_range[1])
                self.lost_kids.append((x, y))
                pass
            else:
                new_kids.append((x,y))
        self.lost_kids = new_kids

    def click_on_fuel(self):
        if not pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            return
        # check if clicked on fuel
        new_fuel = []
        for x,y in self.fuel:
            if x <= pyxel.mouse_x <= x + 17 and y <= pyxel.mouse_y <= y+9:
                # Clicked on fuel
                print("clicked!")
                self.light_strength = self.max_light_strength
                pass
            else:
                new_fuel.append((x,y))
        self.fuel = new_fuel

    def draw_fuel(self):
        # Draw fuel rectangle
        # Add fuel text to it:
        for x, y in self.fuel:
            pyxel.rect(x,y,17,7,8)
            pyxel.text(x+1, y+1, "FUEL", 4)

    def update_darkness_dots_pos(self):
        new_dots = []
        for x, y in self.darkness_dots:
            # Randomly choose -1, 0, or 1 to add to x and y
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])

            # Calculate new position
            new_x = x + dx
            new_y = y + dy

            # distance = math.sqrt((new_x - pyxel.mouse_x) ** 2 + (new_y - pyxel.mouse_y) ** 2)

            # Check if new position is within range and add to new_dots if it is
            if self.is_in_range(new_x, new_y):
                new_dots.append((new_x, new_y))
            else:
                # If new position is out of range, keep the old position
                new_dots.append((x, y))

        # Update the darkness_dots with new valid positions
        self.darkness_dots = new_dots

    def repell_darkness_dots(self):
        mouse_x = pyxel.mouse_x
        mouse_y = pyxel.mouse_y
        light_radius = int(self.light_strength)

        new_dots = []

        for x, y in self.darkness_dots:
            # Calculate distance from the mouse position
            distance = math.sqrt((x - mouse_x) ** 2 + (y - mouse_y) ** 2)

            if distance < light_radius:
                # Calculate the direction vector away from the mouse
                direction_x = x - mouse_x
                direction_y = y - mouse_y
                norm = math.sqrt(direction_x ** 2 + direction_y ** 2)

                if norm != 0:
                    # Normalize the direction vector and move dot away
                    direction_x /= norm
                    direction_y /= norm

                    # Move dot one step away from the center
                    move_step = 3
                    new_x = x + direction_x * move_step
                    new_y = y + direction_y * move_step

                    # Ensure the new position is within range
                    if self.is_in_range(new_x, new_y):
                        new_dots.append((int(new_x), int(new_y)))
                    else:
                        new_dots.append((x, y))
                else:
                    new_dots.append((x, y))
            else:
                new_dots.append((x, y))

        self.darkness_dots = new_dots


    def draw_darkness_dots(self):
        for dot in self.darkness_dots:
            pyxel.rect(dot[0], dot[1],4,4, 0)
    
    def draw_game_background(self):
        # Draw background textrure so the game is more interesting?
        pyxel.rect(0,0,160,120,1)

    def draw_light_around_mouse(self):
        
        pyxel.circ(pyxel.mouse_x, pyxel.mouse_y, int(self.light_strength), 10)


App()