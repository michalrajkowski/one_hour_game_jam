import pyxel
import math
import random

player_w = 16
player_h = 16

class Meteorite:
    def __init__(self, start_x=0, start_y=0, start_velocity = (0,0), start_r = 5):
        self.elements = []
        self.rotation = []
        self.x = start_x
        self.y = start_y
        self.r = random.randint(3, 10)
        self.velocity = start_velocity
        self.dead = False

    def update(self):
        self.x += self.velocity[0] * 1/30
        self.y += self.velocity[1] * 1/30

    def draw(self):
        if self.dead:
            pyxel.circ(self.x, self.y, self.r, col=5)
        else:
            pyxel.circ(self.x, self.y, self.r, col=4)

    def is_touching_mouse(self):
        mouse_x, mouse_y = pyxel.mouse_x, pyxel.mouse_y
        mouse_r = 3
        distance = math.sqrt((self.x - mouse_x) ** 2 + (self.y - mouse_y) ** 2)
        return distance <= (self.r + mouse_r)
    
    def is_touching_player(self):
        player_x, player_y = 256//2, 256//2
        mouse_r = 3
        distance = math.sqrt((self.x - player_x) ** 2 + (self.y - player_y) ** 2)
        return distance <= (self.r + mouse_r)

    def __str__(self):
        return f"Meteorite(Position: ({self.x:.2f}, {self.y:.2f}), Velocity: {self.velocity}, Radius: {self.r})"


class Game:
    def game_init(self):
        self.offset = 0
        self.width = 256
        self.height = 256
        self.center_y = self.height // 2
        self.shooting = False
        self.meteorites : list[Meteorite] = []

        self.player_shield = 100.0
        self.shield_change_rate = 0.1

        self.high_score = max(self.high_score, self.current_score)
        self.current_score = 0

        self.meteorite_timer_max = 1.0
        self.meteorite_timer_current = 0.0
    def __init__(self):
        self.high_score = 0
        self.current_score = 0
        self.game_init()
        pyxel.init(self.width, self.height, title="Distorted Reality")
        pyxel.load("assets.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        # Meteorites handler? (spawning etc)
        self.spawn_meteorites()

        # Check if we shoot?
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT) or pyxel.btn(pyxel.MOUSE_BUTTON_MIDDLE):
            self.shooting = True
            self.player_shield -= 1/30 * self.shield_change_rate*100.0
        else:
            self.shooting = False
            self.player_shield += 1/30 * self.shield_change_rate*100.0*2
            if self.player_shield > 100.0:
                self.player_shield = 100.0

        # Simulate meteorites movement?
        for meteorite in self.meteorites:
            # Update meteorite position?
            # Check if should be destroyed?
            meteorite.update()
            if meteorite.is_touching_mouse() and not meteorite.dead:
                # Destroy meteorite!!
                self.current_score +=1
                meteorite.dead = True
            if meteorite.is_touching_player() and not meteorite.dead:
                meteorite.dead = True
                self.player_shield-=0.1*meteorite.r*100

        if self.player_shield <= 0.0:
            # Reset game
            self.game_init()


        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()


    def draw(self):
        pyxel.cls(0)

        # draw laser!
        if self.shooting == True:
            pyxel.line(256//2, 256//2, pyxel.mouse_x, pyxel.mouse_y, col=8)

        # Draw player
        pyxel.rect(256//2 - player_w//2, 256//2 - player_h//2, player_w, player_h, 2)
        pyxel.rect(256//2 - player_w//2, 256//2 - player_h//2 +4, player_w, 3, 3)

        # draw laser coursor under mouse?
        pyxel.circ(pyxel.mouse_x, pyxel.mouse_y, r=3, col=7)

        # Draw meteorites
        for meteorite in self.meteorites:
            # Update meteorite position?
            # Check if should be destroyed?
            meteorite.draw()

        # Draw player hp
        pyxel.rect(3,3+5,256-6,10-1,7)
        pyxel.rect(5,5+5,(256-10)*self.player_shield/100.0,10-5,8)

        # Draw
        pyxel.text(2, 1, "Score:"+str(self.current_score), 7)
        pyxel.text(200, 1, "Highscore:"+str(self.high_score), 7)

    def spawn_meteorites(self):
        # Spawn meteorites every x seconds?
        self.meteorite_timer_current -= 1/30
        if self.meteorite_timer_current <= 0.0:
            self.meteorite_timer_current = self.meteorite_timer_max + random.random() - 0.5
            # SPAWN METEORITE!
            met_points, met_vector = self.random_point_on_circle(256)
            meteorite : Meteorite = Meteorite(met_points[0]+ 256//2, met_points[1] + 256//2, met_vector, 5)
            print(meteorite)
            self.meteorites.append(meteorite)


    def random_point_on_circle(self, radius):
        # Random angle
        theta = random.uniform(0, 2 * math.pi)  
        
        # Point on the circle's edge
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        
        # Generate a random magnitude for the vector
        vector_magnitude = random.uniform(50, 100)  
        
        # Compute the vector pointing to the center with a random magnitude
        vector_x = -x * (vector_magnitude / radius)  # Normalize and scale
        vector_y = -y * (vector_magnitude / radius)
        
        return (x, y), (vector_x, vector_y)

        


Game()