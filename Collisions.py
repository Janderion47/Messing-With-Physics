import math
import sys
import pygame


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

