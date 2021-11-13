import pygame as pg
from math import pi, ceil
from random import randint
from copy import copy
from itertools import chain
from .physics import DoublePendulum


if not pg.get_init():
    pg.init()


def rand_color():
    r = randint(0, 255)
    g = randint(0, 255-r)
    b = randint(0, 255-r-g)
    return (r, g, b)


def generate_colors(k):
    colors = []

    for r, g, b in zip(
    chain(reversed(range(256)), [0] * 256),
    chain(range(256), reversed(range(256))),
    chain([0] * 256, range(256))):
        colors.append([r, g, b, 255])

    new_list = []
    for color in colors:
        for _ in range(k):
            new_list.append(copy(color))

    return new_list


class App:

    WIDTH, HEIGHT = 1920, 1080
    SCREEN = pg.display.set_mode((WIDTH, HEIGHT), pg.SCALED)
    CLOCK = pg.time.Clock()
    FPS = 30

    def __init__(self, k, m, dm, a1, a2):

        colors = generate_colors(k)
        self.pendulums = [
            DoublePendulum((self.WIDTH//2, self.HEIGHT//2), a1, 250, a2, 250, m+_*dm/(512*k), m+_*dm/(512*k), colors[_]) for _ in range(1, 512*k)
        ]
        print(f"{k*512} double pendulums successfully initialized.")

    def start(self):
        for pendulum in self.pendulums:
            pendulum.start()
        print("Simulation started" if self.pendulums[0].started else "Simulation paused.")

    def run(self):

        while True:

            for event in pg.event.get():

                if event.type == pg.QUIT:
                    pg.quit()
                    raise SystemExit
                if event.type == pg.KEYDOWN:
                    if event.key == 13:
                        self.start()

            self.SCREEN.fill((0, 0, 0))
            for pendulum in self.pendulums:
                pendulum.update(self.SCREEN)

            self.CLOCK.tick(self.FPS)
            pg.display.update()