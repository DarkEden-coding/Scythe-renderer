import pygame
from draw import draw_object
import Color
from settings import width, height
from assets.tank import Tank
from camera import Camera
import sys
import time

pygame.display.init()
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.font.init()
pygame.display.set_caption("3D Renderer")
# add background of grey color
screen.fill(Color.grey)

camera_velocity = 2
camera = Camera()
fps = 60

objects = []

tank_1 = Tank()
tank_1.move(0, 400, -100)
tank_1.rotate(-90, 0, 0)

objects.append(tank_1)


def draw_objects():
    screen.fill(Color.grey)

    for obj in objects:
        draw_object(obj.verticies, obj.lines, screen, camera)
    # Update the screen
    pygame.display.flip()


def keyboard_input():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        camera.move(0, camera_velocity, 0)
    if keys[pygame.K_s]:
        camera.move(0, -camera_velocity, 0)
    if keys[pygame.K_a]:
        camera.move(-camera_velocity, 0, 0)
    if keys[pygame.K_d]:
        camera.move(camera_velocity, 0, 0)
    if keys[pygame.K_q]:
        camera.move(0, 0, camera_velocity)
    if keys[pygame.K_e]:
        camera.move(0, 0, -camera_velocity)
    if keys[pygame.K_LEFT]:
        camera.rotate(0, 0, -camera_velocity)
    if keys[pygame.K_RIGHT]:
        camera.rotate(0, 0, camera_velocity)
    if keys[pygame.K_UP]:
        camera.rotate(camera_velocity, 0, 0)
    if keys[pygame.K_DOWN]:
        camera.rotate(-camera_velocity, 0, 0)


def main():
    while True:
        clock = pygame.time.Clock()
        # Limit to 60 frames per second
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        start_time = time.time()

        keyboard_input()
        draw_objects()

        frame_time = time.time() - start_time
        #  print(f"Frame time: {frame_time:.6f}")


if __name__ == "__main__":
    main()
