"""
Moving Ball Game
================
Control a red ball with arrow keys.
The ball moves 20 pixels per key press and cannot leave the screen.

Controls:
  ↑  — Move Up
  ↓  — Move Down
  ←  — Move Left
  →  — Move Right
  Q  — Quit
  R  — Reset to center
"""

import pygame
import sys
from ball import Ball

SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
FPS           = 60

COLOR_BG      = (245, 245, 245)   
COLOR_GRID    = (220, 220, 220)   
COLOR_TEXT    = (60,  60,  80)
COLOR_ACCENT  = (80,  120, 220)


def draw_grid(screen, spacing=40):
    for x in range(0, SCREEN_WIDTH, spacing):
        pygame.draw.line(screen, COLOR_GRID, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, spacing):
        pygame.draw.line(screen, COLOR_GRID, (0, y), (SCREEN_WIDTH, y))


def draw_ui(screen, ball, font_small):
    x, y = ball.get_position()


    pos_text = font_small.render(f"Position: ({x}, {y})", True, COLOR_TEXT)
    screen.blit(pos_text, (10, 10))

    hints = "← ↑ ↓ → Move  |  R Reset  |  Q Quit"
    hint_surf = font_small.render(hints, True, COLOR_ACCENT)
    screen.blit(hint_surf, hint_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 18)))

    r = ball.RADIUS
    step = ball.STEP
    near_edge = (x - r < step or x + r > SCREEN_WIDTH  - step or
                 y - r < step or y + r > SCREEN_HEIGHT - step)
    if near_edge:
        warn = font_small.render("⚠ Near boundary!", True, (200, 100, 0))
        screen.blit(warn, warn.get_rect(topright=(SCREEN_WIDTH - 10, 10)))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Moving Ball Game 🔴")
    clock = pygame.time.Clock()

    font_small = pygame.font.SysFont("Arial", 20)
    font_title = pygame.font.SysFont("Arial", 28, bold=True)

    ball = Ball(SCREEN_WIDTH, SCREEN_HEIGHT)

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_r:
                    ball = Ball(SCREEN_WIDTH, SCREEN_HEIGHT)
                elif event.key == pygame.K_UP:
                    ball.move("up")
                elif event.key == pygame.K_DOWN:
                    ball.move("down")
                elif event.key == pygame.K_LEFT:
                    ball.move("left")
                elif event.key == pygame.K_RIGHT:
                    ball.move("right")

        screen.fill(COLOR_BG)
        draw_grid(screen)

        title_surf = font_title.render("Moving Ball Game", True, COLOR_TEXT)
        screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH // 2, 25)))

        ball.draw(screen)

        draw_ui(screen, ball, font_small)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()