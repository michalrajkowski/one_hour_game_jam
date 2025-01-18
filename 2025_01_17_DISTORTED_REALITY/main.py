import pyxel
import math
import random

player_w = 16
player_h = 16

class Particle:
    def __init__(self, x, y, vx, vy, life_time, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life_time = life_time
        self.color = color

    def update(self):
        self.x += self.vx * (1 / 30) * 15
        self.y += self.vy * (1 / 30) * 15
        self.life_time -= 1 / 30

    def draw(self):
        if self.life_time > 0:
            pyxel.circ(self.x, self.y, 2, self.color)

    def is_dead(self):
        return self.life_time <= 0


class Meteorite:
    def __init__(self, start_x=0, start_y=0, start_velocity=(0, 0), start_r = 1):
        self.x = start_x
        self.y = start_y
        self.r = random.randint(3, 10)
        self.velocity = start_velocity
        self.dead = False
        self.particles = []

    def update(self):
        if not self.dead:
            self.x += self.velocity[0] * (1 / 30)
            self.y += self.velocity[1] * (1 / 30)
        else:
            self.particles = [p for p in self.particles if not p.is_dead()]
            for particle in self.particles:
                particle.update()

    def draw(self):
        if self.dead:
            for particle in self.particles:
                particle.draw()
        else:
            pyxel.circ(self.x, self.y, self.r, col=4)

    def die(self):
        self.dead = True
        self.spawn_particles()

    def spawn_particles(self):
        num_particles = random.randint(5*self.r, 10*self.r)
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.5, 2)
            vx = speed * math.cos(angle)
            vy = speed * math.sin(angle)
            life_time = random.uniform(0.5, 1.5)
            color = random.choice([7, 10, 8, 9])
            self.particles.append(Particle(self.x, self.y, vx, vy, life_time, color))

    def is_touching_mouse(self):
        mouse_x, mouse_y = pyxel.mouse_x, pyxel.mouse_y
        mouse_r = 3
        distance = math.sqrt((self.x - mouse_x) ** 2 + (self.y - mouse_y) ** 2)
        return distance <= (self.r + mouse_r)

    def is_touching_player(self):
        player_x, player_y = 256 // 2, 256 // 2
        player_r = 3
        distance = math.sqrt((self.x - player_x) ** 2 + (self.y - player_y) ** 2)
        return distance <= (self.r + player_r)

    def __str__(self):
        return f"Meteorite(Position: ({self.x:.2f}, {self.y:.2f}), Radius: {self.r}, Dead: {self.dead})"


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
                meteorite.die()
            if meteorite.is_touching_player() and not meteorite.dead:
                meteorite.die()
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
            pyxel.line(256//2, 256//2, pyxel.mouse_x + random.randrange(-3, 3), pyxel.mouse_y + random.randrange(-3, 3), col=11)
            pyxel.line(256//2, 256//2, pyxel.mouse_x + random.randrange(-3, 3), pyxel.mouse_y + random.randrange(-3, 3), col=14)
            pyxel.line(256//2, 256//2, pyxel.mouse_x + random.randrange(-3, 3), pyxel.mouse_y + random.randrange(-3, 3), col=6)

        # Draw player
        pyxel.rect(256//2 - player_w//2, 256//2 - player_h//2, player_w, player_h, 2)
        pyxel.rect(256//2 - player_w//2, 256//2 - player_h//2 +4, player_w, 3, 3)
        pyxel.rect(256//2 - player_w//2 + 3, 256//2 - player_h//2 +4, 4, 2, 7)
        pyxel.rect(256//2 - player_w//2 + 5, 256//2 - player_h//2 +4, 2, 2, 0)

        pyxel.rect(256//2 - player_w//2 + 10, 256//2 - player_h//2 +4, 4, 2, 7)
        pyxel.rect(256//2 - player_w//2 + 12, 256//2 - player_h//2 +4, 2, 2, 0)


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