import pygame as pg


class Bubble:

    def __init__(self, pos: pg.Vector2, radius: int, vel: pg.Vector2, color: pg.Color = pg.Color(255, 0, 0), width=0):
        # shape
        self.pos = pos
        self.radius = radius

        # physics
        self.friction = 0.005
        self.vel = vel
        self.next_vel = pg.Vector2(0, 0)
        self.friction_on = True

        # appearance
        self.color = color
        self.width = width

    def collide(self, other: "Bubble"):
        return self.pos.distance_to(other.pos) < self.radius + other.radius

    def update_pos(self):
        # apply vel
        self.pos += self.vel

        # reset vel for next frame
        self.vel = self.next_vel
        # apply friction
        if self.friction_on:
            self.vel *= (1 - self.friction)

    def move(self, vel: pg.Vector2) -> "Bubble":
        return Bubble(self.pos + vel, self.radius, self.vel)

    def draw(self, screen):
        pg.draw.circle(screen, self.color, self.pos, self.radius, width=self.width)
