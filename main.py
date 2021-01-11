import pygame
import sys  # used to exit the program immediately
from math import sqrt  # used for square root
from random import randint  # used to generate random integers


#  given a vector with x and y, this will normalize the vector and return the results as a tuple
def normalize(vx, vy):
    mag = abs((vx * vx) + (vy * vy))  # find the magnitude using pythagorean theorem
    mag = sqrt(mag)

    if mag == 0: return vx, vy  # to prevent division by zero

    return (vx / mag), (vy / mag)  # divide vector by magnitude to create a unit vector


#  given a magnitude and a vector with x and y, this will normalize and scale the given vector and return a tuple (vx, vy)
def setMag(vx, vy, mag):
    vx, vy = normalize(vx, vy)  # normalize
    vx *= mag  # scale the vector
    vy *= mag

    return vx, vy


#  similar to setMag but this function will only scale the vector if the magnitude is greater than the limit magnitude
def limitMag(vx, vy, limit):
    mag = abs((vx * vx) + (vy * vy))  # find the magnitude using pythagorean theorem
    mag = sqrt(mag)

    if mag >= limit:
        vx, vy = setMag(vx, vy, limit)  # if the limit is reached then keep the magnitude set at the limit

    return vx, vy


def draw():
    pygame.draw.circle(screen, (255, 255, 255), pygame.mouse.get_pos(), 5)  # white circle with radius of 5
    pygame.draw.circle(screen, (0, 255, 255), [circlex, circley], 20)

    # the vectors are drawn as lines from the circle and scaled to make them easier to see
    if vec_show:
        pygame.draw.line(screen, (255, 0, 0), (circlex, circley), (circlex + accx * 10, circley + accy * 10), 2)
        pygame.draw.line(screen, (0, 255, 0), (circlex, circley), (circlex + pullx * 60, circley + pully * 60), 2)


#  screen width and height parameters
WIDTH = 1280
HEIGHT = 900

pygame.init()  # initialize pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # display surface
clock = pygame.time.Clock()  # game clock
pygame.mouse.set_visible(False)  # mouse is not visible
pygame.display.set_caption("Pygame- Simple orbit using basic vector math")

#  some lovely global variables :)

#  define circle position vector with random values
circlex = randint(0, WIDTH)
circley = randint(0, HEIGHT)

#  define acceleration vector with 0
accx = 0
accy = 0

#  define pull vector with 0
pullx = 0
pully = 0

vec_show = False

# main loop
while True:
    for event in pygame.event.get():  # check events and quit if the program is closed
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:  # press the the SPACE BAR to reveal the vectors
            if event.key == pygame.K_SPACE: vec_show = True  # enable vector lines
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE: vec_show = False  # disable vector lines

    screen.fill((0, 0, 0))  # black screen

    mx, my = pygame.mouse.get_pos()  # get mouse position as 'mx' and 'my'

    pullx = mx - circlex  # subtract mouse position vector with circle position vector
    pully = my - circley

    pullx, pully = limitMag(pullx, pully, 1.1)  # limit the pull vector

    accx, accy = setMag(accx, accy, 12)  # normalize and scale the acceleration vector

    accx += pullx  # add the pull vector to the acceleration vector
    accy += pully

    accx, accy = limitMag(accx, accy, 10)  # limit the acceleration vector

    circlex = circlex + accx  # add the acceleration vector to the circle position vector
    circley = circley + accy

    draw()  # draw everything to the screen

    pygame.display.update()
    clock.tick(60)
