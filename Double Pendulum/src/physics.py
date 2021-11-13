import pygame as pg
from copy import copy
from math import (
    cos,
    sin,
    pi,
    sqrt
)


class PhysicalObject:

    def __init__(self, pos, mass):

        self.pos = pos
        self.MASS = mass

    def update(self, screen):

        pg.draw.circle(screen, (255, 0, 0), self.pos, 10)


class Pendulum(PhysicalObject):

    def __init__(self, application_pos, length, starting_angle):
        dx, dy = length * cos(starting_angle), length * sin(starting_angle)
        pos = application_pos + pg.Vector2(dx, dy)
        super().__init__(pos, 1)
        self.starting_angle = starting_angle
        self.application_pos = application_pos
        self.length = length

        self.started = False
        self.pause = False
        self.start_time = 0
        self.dt = 0
        self.pts = []

    def calculate_angle(self):
        return -self.starting_angle*cos(sqrt(9.81/self.length)*self.dt)

    def start(self):
        self.started = True
        self.start_time = pg.time.get_ticks()

    def update(self, screen):

        if self.started and not self.pause:
            self.dt = (pg.time.get_ticks() - self.start_time)/100
            new_angle = self.calculate_angle()+pi/2
            dx, dy = self.length * cos(new_angle), self.length * sin(new_angle)
            # pg.draw.line(screen, (255, 255, 0), self.application_pos, self.application_pos+pg.Vector2(dx, 0))
            # pg.draw.line(screen, (255, 255, 0), self.application_pos, self.application_pos+pg.Vector2(0, dy))
            self.pos = self.application_pos + pg.Vector2(dx, dy)
            self.pts.append(copy(self.pos))

        for pt in self.pts:
            pg.draw.circle(screen, (255, 255, 255), pt, 1)

        pg.draw.circle(screen, (100, 100, 100), self.application_pos, 5)
        pg.draw.line(screen, (100, 100, 100), self.application_pos, self.pos)

        return super().update(screen)


class DoublePendulum:

    def __init__(self, pos1, a1, l1, a2, l2, m1, m2, color):

        self.pos = pos1
        self.started = False
        self.color = color

        self.p1 = self.pos + pg.Vector2(l1*sin(a1),l1*cos(a1))
        self.p2 = self.p1 + pg.Vector2(l2*sin(a2),l2*cos(a2))

        self.a1, self.l1, self.a2, self.l2, self.m1, self.m2 = a1, l1, a2, l2, m1, m2
        self.a1_v = 0
        self.a2_v = 0
        self.a1_a = -0.001
        self.a2_a = 0.01
        self.pts = []
        self.g = 9.81

    def start(self):
        self.started = not self.started

    def update(self, screen):

        if self.started:

            # CALCULATIONS

            self.p1 = self.pos + pg.Vector2(self.l1*sin(self.a1),self.l1*cos(self.a1))
            self.p2 = self.p1 + pg.Vector2(self.l2*sin(self.a2),self.l2*cos(self.a2))

            g = self.g
            num1 = -self.g * (2 * self.m1 + self.m2) * sin(self.a1)
            num2 = -self.m2 * self.g * sin(self.a1-2*self.a2)
            num3 = -2*sin(self.a1-self.a2)*self.m2
            num4 = self.a2_v**2*self.l2+self.a1_v**2*self.l1*cos(self.a1-self.a2)
            den = self.l1 * (2*self.m1*self.m2-self.m2*cos(2*self.a1-2*self.a2))
            self.a1_a = (
                num1 + 
                num2 + 
                num3*num4
            )/den
            
            num1 = 2* sin(self.a1-self.a2)
            num2 = (self.a1_v**2*self.l1*(self.m1+self.m2))
            num3 = g * (self.m1 + self.m2) * cos(self.a1)
            num4 = self.a2_v**2*self.l2*self.m2*cos(self.a1-self.a2)
            den = self.l2 * (2*self.m1*self.m2-self.m2*cos(2*self.a1-2*self.a2))
            self.a2_a = (num1 * (num2 + num3 + num4)) / den

            self.a1_v += self.a1_a
            self.a2_v += self.a2_a
            self.a1 += self.a1_v
            self.a2 += self.a2_v

            #self.pts.append(copy(self.p2))
        
        #pg.draw.circle(screen, (100, 100, 100), self.pos, 5)
        #pg.draw.circle(screen, (100, 100, 100), self.p1, self.m1)
        #pg.draw.circle(screen, (100, 100, 100), self.p2, self.m2)
        pg.draw.lines(screen, self.color, False, (self.pos, self.p1, self.p2), 1)