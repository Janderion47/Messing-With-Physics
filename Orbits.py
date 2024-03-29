# Code based off u/OrionPixels from
# https://github.com/anishsatalkar/python_gravity_simulation_pygame/blob/master/gravity_simulation.py
import math
import random
import sys

import pygame

G = 6.67408e-11 * 100_000_000  # Otherwise the bodies would not move given the small value of gravitational constant
NUM_OF_BODIES = 20
WIDTH = 400
HEIGHT = 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (109, 196, 255)


class Body:
    def __init__(self, pos, a, v, m):
        self.pos = pos  # pos is a list of x and y position of that body in pixels eg : [500,600]
        self.a = a  # a is a list of x and y components of acceleration of that body in pixel units
        self.v = v  # b is a list of x and y components of velocity of that body in pixel units
        self.m = m  # m is the mass of that object


def calculate_forces(pos_a, pos_b, m_a, m_b):

    x_diff = pos_b[0] - pos_a[0]
    y_diff = pos_b[1] - pos_a[1]

    hypotenuse = math.sqrt(((x_diff) ** 2 + (y_diff) ** 2))
    sin = x_diff / hypotenuse
    cos = y_diff / hypotenuse
    f = G * m_a * m_b / hypotenuse ** 2
    fx = f * sin
    fy = f * cos

    return fx, fy


def calculate_collisions(fx_total, fy_total, a_m, b_m, a_pos, b_pos):
    fx_new, fy_new = fx_total, fy_total
    sum_radiuses = (a_m/2)+(b_m/2)

    ax = a_pos[0]
    ay = a_pos[1]
    bx = b_pos[0]
    by = b_pos[1]

    if (ax > bx) and (ax-bx <= sum_radiuses):
        if fx_new == 0:
            fx_new *= 0
        elif fx_new < 0:
            fx_new *= -1
    if (ax < bx) and (bx-ax <= sum_radiuses):
        if fx_new == 0:
            fx_new *= 0
        elif fx_new > 0:
            fx_new *= -1
    if (ay > by) and (ay-by <= sum_radiuses):
        if fy_new == 0:
            fy_new *= 0
        elif fy_new < 0:
            fy_new *= -1
    if (ay < by) and (by-ay <= sum_radiuses):
        if fy_new == 0:
            fy_new *= 0
        elif fy_new > 0:
            fy_new *= -1

    return fx_new, fy_new


bodies = []
for i in range(NUM_OF_BODIES):  # For each item in NUM_OF_BODIES,
    px = random.randint(20, WIDTH - 20)  # (Create variable of the x position)
    py = random.randint(20, HEIGHT - 20)  # (Create variable of the y position)
    m = random.randint(1, 25)  # (Create variable of the mass)
    bodies.append(Body([px, py], [0, 0], [0, 0], m))  # Add a Body with the information of the variables

# Some predefined bodies for the purpose of testing
# bodies.append(Body([500,500],[0,0],[0,0],20))
# bodies.append(Body([510,503],[0,0],[0,0],7))
# bodies.append(Body([400,400],[0,0],[0,0],14))
# bodies.append(Body([10,600],[0,0],[0,0],9))
# bodies.append(Body([250,198],[0,0],[0,0],18))
# bodies.append(Body([340,700],[0,0],[0,0],24))

pygame.init()
pygame.display.set_caption("Orbits")
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)

font = pygame.font.SysFont('Arial', 16)
text = font.render('0', True, BLUE)
textRect = text.get_rect()
while True:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    for body_a in bodies:
        pos_a = body_a.pos
        m_a = body_a.m
        fx_total = 0
        fy_total = 0

        for body_b in bodies:
            if body_b.pos == pos_a:
                continue
            fx, fy = calculate_forces(pos_a, body_b.pos, m_a, body_b.m)
            fx_total += fx
            fy_total += fy

            fx_total, fy_total = calculate_collisions(fx_total, fy_total, body_a.m, body_b.m, body_a.pos, body_b.pos)

        body_a_acceleration = body_a.a

        body_a_acceleration[0] = fx_total / m_a
        body_a_acceleration[1] = fy_total / m_a

        body_a.v[0] = body_a.v[0] + body_a_acceleration[0]
        body_a.v[1] = body_a.v[1] + body_a_acceleration[1]

        pos_a[0] = pos_a[0] + body_a.v[0]
        pos_a[1] = pos_a[1] + body_a.v[1]

        mass_text = 'M={0}'.format(m_a)
        # force_text = 'F=({0},{1})'.format(fx_total.__round__(3), fy_total.__round__(3))
        # velocity_text = 'V=({},{})'.format(body_a.v[0].__round__(3),body_a.v[1].__round__(3))
        # text_str = mass_text + '   ' + force_text + '   ' + velocity_text
        text_str = mass_text

        text = font.render(text_str, True, BLUE)
        textRect.center = (pos_a[0] + m_a + 10, pos_a[1] + m_a + 10)

        screen.blit(text, textRect)

        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(pos_a[0], pos_a[1], m_a, m_a))
    pygame.display.flip()
