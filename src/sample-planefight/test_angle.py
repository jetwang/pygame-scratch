import math
import sys

import pygame

DIMENSIONS = (600, 600)
window = pygame.display.set_mode(DIMENSIONS, pygame.RESIZABLE)
window.fill((20, 20, 20))
pygame.font.init()

pygame.display.set_caption("Pygame template")
clock = pygame.time.Clock()

player_pos = pygame.Vector2(275, 275)
player = pygame.Rect(player_pos.xy, (50, 50))
player_center = pygame.Vector2(player.center)

looking_vector = pygame.Vector2(1, 1)
text_font = pygame.font.Font(None, 20)

while True:

    window.fill((20, 20, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    player = pygame.Rect(player_pos.xy, (50, 50))

    # Relative position of mouse
    mouse_pos = pygame.mouse.get_pos()
    delta = mouse_pos - player_center

    # Calculate the angle
    angle_to_mouse = math.atan2(delta.y, delta.x)
    looking_vector.xy = (100 * math.cos(angle_to_mouse), 100 * math.sin(angle_to_mouse))

    text_image = text_font.render(str(angle_to_mouse), True, (255, 255, 255))
    window.blit(text_image, (10, 10))

    direction = (angle_to_mouse * 180) / math.pi
    text_image = text_font.render("角度："+str(direction), True, (255, 255, 255))
    window.blit(text_image, (10, 30))

    # Player rect
    pygame.draw.rect(window, (50, 50, 255), player)
    # Line to mouse
    pygame.draw.line(window, (255, 50, 50), player_center, pygame.mouse.get_pos())
    # Line in direction to looking_vector
    pygame.draw.line(window, (50, 255, 50), player_center, player_center + looking_vector)

    pygame.display.update()
    clock.tick(60)
