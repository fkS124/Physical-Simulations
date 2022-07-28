from .bubble import Bubble
import math


def resolve_collisions(all_bubbles: list[Bubble], w: int, h: int):

    # prevent the bubbles from going out of screen
    for bubble in all_bubbles:
        _resolve_collision_screen_limits(bubble, w, h)

    # prevent the bubbles from overlapping with each other
    for bubble in all_bubbles:
        for second_bubble in all_bubbles:
            if bubble != second_bubble:
                _resolve_collision_two_bubbles(bubble, second_bubble)


def _resolve_collision_screen_limits(bubble: Bubble, w: int, h: int):
    # get radius and calculate next hypothetical position
    radius = bubble.radius
    new_pos = bubble.pos + bubble.vel

    # get the initial vel to see if it has changed
    initial_vel = bubble.vel.copy()

    # check if the bubble goes out of the screen horizontally and then vertically.
    # if so, calculates the appropriate velocity for a perfect collision

    if new_pos.x + radius > w:
        bubble.vel.x = w - (bubble.pos.x + radius)
    elif new_pos.x - radius < 0:
        bubble.vel.x = bubble.pos.x - radius

    if new_pos.y + radius > h:
        bubble.vel.y = h - (bubble.pos.y + radius)
    elif new_pos.y - radius < 0:
        bubble.vel.y = bubble.pos.y - radius

    # if the bubble hasn't bounced, do nothing
    if bubble.vel == initial_vel:
        bubble.next_vel = bubble.vel

    # otherwise, apply the bouncing effect
    else:
        bubble.next_vel = initial_vel
        if bubble.vel.x != initial_vel.x:
            bubble.next_vel.x = -initial_vel.x
        if bubble.vel.y != initial_vel.y:
            bubble.next_vel.y = -initial_vel.y


def _resolve_collision_two_bubbles(first_bubble: Bubble, second_bubble: Bubble):
    moved_first_bubble = first_bubble.move(first_bubble.vel)
    moved_second_bubble = second_bubble.move(second_bubble.vel)

    if not moved_second_bubble.collide(moved_first_bubble) or (first_bubble.vel + second_bubble.vel).magnitude() == 0:
        return

    b1, b2 = first_bubble, second_bubble
    D = moved_second_bubble.pos.distance_to(moved_first_bubble.pos)
    D_th = b1.radius + b2.radius

    initial_b1_vel = b1.vel.copy()
    initial_b2_vel = b2.vel.copy()

    b1.vel *= D / D_th
    b2.vel *= D / D_th

    mv_pos1, mv_pos2 = b1.pos + b1.vel, b2.pos + b2.vel

    b1.next_vel.xy = (mv_pos1 - mv_pos2).normalize() * initial_b1_vel.length()
    b2.next_vel.xy = (mv_pos2 - mv_pos1).normalize() * initial_b2_vel.length()

    # TODO : add the real physic equations

