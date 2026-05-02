import pygame
import sys
import os
import db
import config
import game

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Snake - JSON Storage")
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 36)

def draw_button(text, rect, color, hover_color, mouse_pos):
    """
    Helper function to render interactive UI buttons.
    Checks if the current mouse_pos intersects with the button's Rect.
    Returns True if the mouse is hovering over it, enabling click detection logic.
    """
    is_hover = rect.collidepoint(mouse_pos)
    pygame.draw.rect(screen, hover_color if is_hover else color, rect)
    text_surf = font.render(text, True, (255, 255, 255))
    screen.blit(text_surf, (rect.x + (rect.width - text_surf.get_width())//2, rect.y + 10))
    return is_hover

def main():
    # Application startup routine: ensure storage files exist and settings are loaded
    db.setup_database()
    settings = config.load_settings()

    # The application uses a finite state machine pattern. 
    # 'state' determines which screen is currently being rendered and evaluated.
    state = "MENU"
    username = ""
    player_id = None
    last_score, last_level = 0, 0
    personal_best = 0

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        click = False

        # Global event loop for handling OS-level events like closing the window or keystrokes
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

            # Text Input Handling: Allows the user to type their username in the MENU state.
            # Handles backspace for corrections and limits the length to 15 characters.
            if state == "MENU" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.key != pygame.K_RETURN and len(username) < 15:
                    username += event.unicode

        screen.fill((20, 20, 20))

        # STATE: Main Menu screen logic
        if state == "MENU":
            title = font.render("SNAKE GAME", True, (0, 255, 0))
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))

            # Blinking cursor effect: Toggles an underscore on/off every 500 milliseconds using mod math
            prompt = small_font.render("Type Username: " + username + ("_" if pygame.time.get_ticks() % 1000 < 500 else ""), True, (200, 200, 200))
            screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, 150))

            btn_play = pygame.Rect(WIDTH//2 - 100, 250, 200, 50)
            btn_lead = pygame.Rect(WIDTH//2 - 125, 320, 250, 50)
            btn_sett = pygame.Rect(WIDTH//2 - 100, 390, 200, 50)
            btn_quit = pygame.Rect(WIDTH//2 - 100, 460, 200, 50)

            # Button Actions: If draw_button returns True (hovering) AND click is True, execute the action
            if draw_button("Play", btn_play, (50, 150, 50), (80, 200, 80), mouse_pos) and click and username != "":
                # Authenticate player and transition to the PLAYING state
                player_id = db.get_or_create_player(username)
                personal_best = db.get_personal_best(player_id)
                state = "PLAYING"
            if draw_button("Leaderboard", btn_lead, (50, 50, 150), (80, 80, 200), mouse_pos) and click:
                state = "LEADERBOARD"
            if draw_button("Settings", btn_sett, (150, 150, 50), (200, 200, 80), mouse_pos) and click:
                state = "SETTINGS"
            if draw_button("Quit", btn_quit, (150, 50, 50), (200, 80, 80), mouse_pos) and click:
                running = False

        # STATE: Core Gameplay Loop execution
        elif state == "PLAYING":
            # Handoff control to the game.py module. It blocks here until the game finishes.
            last_score, last_level = game.run_game(screen, settings, personal_best)
            if last_score is None: 
                # If run_game returns None, it means the user forcibly closed the window while playing
                running = False
            else:
                # Normal game over condition: record metrics to the JSON storage and switch state
                db.save_score(player_id, last_score, last_level)
                state = "GAME_OVER"

        # STATE: Results Screen
        elif state == "GAME_OVER":
            go_text = font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(go_text, (WIDTH//2 - go_text.get_width()//2, 100))

            s_text = small_font.render(f"Score: {last_score} | Level: {last_level}", True, (255, 255, 255))
            screen.blit(s_text, (WIDTH//2 - s_text.get_width()//2, 200))

            btn_retry = pygame.Rect(WIDTH//2 - 100, 300, 200, 50)
            btn_menu = pygame.Rect(WIDTH//2 - 100, 370, 200, 50)

            if draw_button("Retry", btn_retry, (50, 150, 50), (80, 200, 80), mouse_pos) and click:
                # Re-fetch personal best in case they just beat it, then start game again
                personal_best = db.get_personal_best(player_id)
                state = "PLAYING"
            if draw_button("Menu", btn_menu, (100, 100, 100), (150, 150, 150), mouse_pos) and click:
                state = "MENU"

        # STATE: High Scores display
        elif state == "LEADERBOARD":
            title = font.render("TOP 10 SCORES", True, (255, 215, 0))
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))

            # Dynamically generate text surfaces for the top 10 database rows
            y_offset = 100
            for rank, row in enumerate(db.get_top_10(), 1):
                txt = small_font.render(f"{rank}. {row[0]} - Score: {row[1]} - Lvl: {row[2]}", True, (200, 200, 200))
                screen.blit(txt, (WIDTH//2 - txt.get_width()//2, y_offset))
                y_offset += 35

            btn_back = pygame.Rect(WIDTH//2 - 100, 500, 200, 50)
            if draw_button("Back", btn_back, (100, 100, 100), (150, 150, 150), mouse_pos) and click:
                state = "MENU"

        # STATE: Configuration options
        elif state == "SETTINGS":
            title = font.render("SETTINGS", True, (255, 255, 255))
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))

            grid_lbl = "Grid: ON" if settings["grid_overlay"] else "Grid: OFF"
            sound_lbl = "Sound: ON" if settings["sound"] else "Sound: OFF"

            btn_grid = pygame.Rect(WIDTH//2 - 150, 150, 300, 50)
            btn_sound = pygame.Rect(WIDTH//2 - 150, 220, 300, 50)
            btn_color = pygame.Rect(WIDTH//2 - 150, 290, 300, 50)
            btn_back = pygame.Rect(WIDTH//2 - 100, 450, 200, 50)

            # Toggle booleans directly in the dictionary and flush changes to disk immediately
            if draw_button(grid_lbl, btn_grid, (70, 70, 70), (100, 100, 100), mouse_pos) and click:
                settings["grid_overlay"] = not settings["grid_overlay"]
                config.save_settings(settings)

            if draw_button(sound_lbl, btn_sound, (70, 70, 70), (100, 100, 100), mouse_pos) and click:
                settings["sound"] = not settings["sound"]
                config.save_settings(settings)

            # Iterative state modification: Cycles through predefined RGB lists for the snake body
            if draw_button("Cycle Snake Color", btn_color, tuple(settings["snake_color"]), (150, 150, 150), mouse_pos) and click:
                c = settings["snake_color"]
                if c == [0, 255, 0]: settings["snake_color"] = [0, 100, 255]   # Green -> Blue
                elif c == [0, 100, 255]: settings["snake_color"] = [255, 255, 0] # Blue -> Yellow
                else: settings["snake_color"] = [0, 255, 0]                     # Yellow -> Green
                config.save_settings(settings)

            if draw_button("Back", btn_back, (100, 100, 100), (150, 150, 150), mouse_pos) and click:
                state = "MENU"

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()