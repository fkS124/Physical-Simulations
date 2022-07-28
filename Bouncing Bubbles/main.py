import pygame as pg

from random import randint, gauss
from src import Bubble, resolve_collisions

vec = pg.math.Vector2


def _initialize(width: int, height: int) -> pg.Surface:
    pg.init()
    return pg.display.set_mode((width, height), pg.SCALED)


def _quit():
    pg.quit()
    raise SystemExit


def _initialize_bubbles(n: int, w: int, h: int) -> list[Bubble]:
    bubbles = []
    for _ in range(n):
        valid = False
        it = 0
        while not valid:
            it += 1

            # generate random position, radius and velocity
            radius = int(gauss(20, 5))
            pos = vec(randint(0, w), randint(0, h))
            vel = pg.Vector2(gauss(0, 5), gauss(0, 5))

            # generate the actual bubble
            new_bubble = Bubble(pos, radius, vel)

            # check if it fits in the screen
            if pos.x - radius < 0 or pos.x + radius > w or pos.y + radius > h or pos.y - radius < 0:
                continue

            # check if it doesn't collide with any other bubble
            for bubble in bubbles:
                if bubble.collide(new_bubble):
                    break
            else:
                valid = True
                bubbles.append(new_bubble)

            # if the screen full, the algorithm will iterate over a thousand times without finding a correct location
            # then break the loop and stop the generation
            if it > 1000:
                return bubbles
    return bubbles


def _main_loop(screen: pg.Surface):
    # app constants
    running = True
    w, h = screen.get_size()
    clock = pg.time.Clock()
    fps = 60

    # bubbles
    n_bubbles = 100
    bubbles = _initialize_bubbles(n=n_bubbles, w=w, h=h)

    while running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_f:
                    for bubble in bubbles:
                        bubble.friction_on = not bubble.friction_on

        screen.fill((0, 0, 0))

        resolve_collisions(all_bubbles=bubbles, w=w, h=h)

        for bubble in bubbles:
            bubble.draw(screen)
            bubble.update_pos()

        pg.display.update()
        pg.display.set_caption(f"Elastic Collision Simulation. [entity_count={n_bubbles}, "
                               f"fps={round(clock.get_fps(), 2)}, friction={bubbles[0].friction_on}]")
        clock.tick(fps)


def main():
    screen = _initialize(1000, 1000)
    pg.display.set_caption("Elastic Collision Simulation.")
    _main_loop(screen=screen)
    _quit()


if __name__ == "__main__":
    main()
