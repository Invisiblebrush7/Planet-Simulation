# Cool video I followed:
# https://www.youtube.com/watch?v=WTLPmUHTPqo

import pygame
import math

pygame.init()


HEIGHT = 800
WIDTH = 800

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Cool Planet Simulation')

FONT = pygame.font.SysFont("helvetica", 16)

# Colors
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (255, 0, 0)
DARK_GREY = (80, 78, 81)
WHITE = (255, 255, 255)


class Planet:
    AU = 149.6e6 * 1000     # Astronomical Units-> Distance from earth to the sun  (in meters)
    G = 6.67428E-11         # Gravitational Constant -> is an empirical physical constant involved in the calculation of gravitational effects
    SCALE = 150 / AU        # 1 AU = 100px
    TIMESTEP = 3600 * 24    # We use this so that we can see days instead of seconds in the simulation

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.isSun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0
    
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y

        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        if(other.isSun):
            self.distance_to_sun = distance
        
        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)

        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))




    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        updated_points = []

        if(len(self.orbit) > 2):
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)
        
        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if not self.isSun:
            distance_text = FONT.render(f"{round(self.distance_to_sun / 1000, 1)} km", 1, WHITE)
            win.blit(distance_text, ((x - distance_text.get_width() / 2) + 50, (y - distance_text.get_height() / 2) - 30))

def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.99892 * 10**30)
    sun.isSun = True

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.3 * 10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    planets = [sun, mercury, venus, earth, mars]

    while run:
        clock.tick(60) # It allows the "game" to run at max 60fps
        WIN.fill((0, 0, 0))
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                run = False
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)
        pygame.display.update()

    pygame.quit()

main()