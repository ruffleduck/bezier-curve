import pygame
import copy

pygame.init()

RES = 300

THICKNESS = 4

WHITE = 255, 255, 255
YELLOW = 255, 230, 50
GREEN = 0, 255, 100
RED = 255, 100, 100
BLUE = 0, 100, 255
BLACK = 0, 0, 0

WIDTH = 500
HEIGHT = 500


def step_pos(p1, p2, steps):
    xdiff = p2[0] - p1[0]
    ydiff = p2[1] - p1[1]
    xstep = xdiff / RES
    ystep = ydiff / RES
    x = p1[0] + (steps * xstep)
    y = p1[1] + (steps * ystep)
    return round(x), round(y)


def step_pts(points, steps):
    pts = []
    for i in range(len(points) - 1):
        pts.append(step_pos(points[i], points[i + 1], steps))
    return pts


def create_curve(points):
    curve_points = []
    for steps in range(RES):
        pts = copy.deepcopy(points)
        while len(pts) > 1:
            pts = step_pts(pts, steps)
        curve_points.append(pts[0])
    return curve_points


def render_lines(points, steps):
    if len(points) >= 2:
        pygame.draw.lines(screen, BLACK, False, points, THICKNESS)

    pts = step_pts(points, steps)
    c = 0
    while len(pts) >= 2:
        color = (GREEN, RED, YELLOW)[c % 3]
        pygame.draw.lines(screen, color, False, pts, THICKNESS)
        pts = step_pts(pts, steps)
        c += 1

    if len(pts) >= 1:
        pygame.draw.circle(screen, BLACK, pts[0], THICKNESS)


def render_curve(curve_points):
    pygame.draw.lines(screen, BLUE, False, curve_points, THICKNESS)
    # for pt in curve_points:
    #     pygame.draw.circle(screen, BLUE, pt, THICKNESS)


pygame.display.set_caption('Bezier Curve')
screen = pygame.display.set_mode([WIDTH, HEIGHT])

lines_toggled = False

steps = 0

curve_points = []
points = []

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                lines_toggled = not lines_toggled

            if event.key == pygame.K_r:
                curve_points = []
                points = []
                steps = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            points.append(event.pos)
            curve_points = create_curve(points)

    screen.fill(WHITE)

    if pygame.key.get_pressed()[pygame.K_RIGHT] and lines_toggled:
        steps += 1
        if steps > RES:
            steps = RES

    if pygame.key.get_pressed()[pygame.K_LEFT] and lines_toggled:
        steps -= 1
        if steps < 0:
            steps = 0

    if len(curve_points) > 1:
        render_curve(curve_points)

    if lines_toggled:
        render_lines(points, steps)

    for pt in points:
        pygame.draw.circle(screen, BLACK, pt, THICKNESS)

    pygame.display.update()

pygame.quit()
