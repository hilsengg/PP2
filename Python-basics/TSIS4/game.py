import pygame
import random

# Basic game settings
WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20
BASE_SPEED = 10

# Color palette definition
C_BG = (30, 30, 30)
C_GRID = (50, 50, 50)
C_FOOD_NORMAL = (200, 0, 0)
C_FOOD_WEIGHTED = (255, 215, 0) # Gold
C_POISON = (139, 0, 0) # Dark Red
C_OBSTACLE = (100, 100, 100) # Gray
C_PW_SPEED = (0, 255, 255) # Cyan
C_PW_SLOW = (0, 0, 255) # Blue
C_PW_SHIELD = (255, 0, 255) # Magenta

def run_game(screen, settings, personal_best):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    # Initialize the snake in the center of the screen with 3 body segments.
    # dx and dy define the movement vector (initially moving right).
    snake = [[WIDTH//2, HEIGHT//2], [WIDTH//2 - BLOCK_SIZE, HEIGHT//2], [WIDTH//2 - 2*BLOCK_SIZE, HEIGHT//2]]
    dx, dy = BLOCK_SIZE, 0
    snake_color = tuple(settings["snake_color"])

    # Game metrics trackers
    score = 0
    level = 1
    food_eaten_this_level = 0
    current_speed = BASE_SPEED

    # Helper function: Generates obstacles dynamically based on the current level.
    # It ensures a safe zone in the center (radius 100) so the snake doesn't spawn inside a wall.
    obstacles = []
    def generate_obstacles():
        obs = []
        if level >= 3:
            num_obs = level * 2
            for _ in range(num_obs):
                while True:
                    ox = random.randrange(0, WIDTH, BLOCK_SIZE)
                    oy = random.randrange(0, HEIGHT, BLOCK_SIZE)
                    # Safe zone check: if coordinates are NOT in the center, add the obstacle
                    if not (WIDTH//2 - 100 <= ox <= WIDTH//2 + 100 and HEIGHT//2 - 100 <= oy <= HEIGHT//2 + 100):
                        obs.append([ox, oy])
                        break
        return obs

    obstacles = generate_obstacles()

    # Helper function: Finds a random coordinate on the grid that is NOT currently 
    # occupied by the snake's body or an obstacle.
    def get_random_pos():
        while True:
            x = random.randrange(0, WIDTH, BLOCK_SIZE)
            y = random.randrange(0, HEIGHT, BLOCK_SIZE)
            if [x, y] not in snake and [x, y] not in obstacles:
                return [x, y]

    # Initial entity spawning
    food = get_random_pos()
    food_type = "normal"
    food_timer = 0
    poison = get_random_pos() if random.random() < 0.3 else None

    # Powerup state management variables
    powerup = None
    powerup_type = None
    powerup_spawn_time = 0
    active_effect = None
    effect_end_time = 0
    shield_active = False

    running = True
    while running:
        current_time = pygame.time.get_ticks()

        # Event handling block: listens for application exit and directional inputs.
        # It prevents reversing direction (e.g., cannot move DOWN if currently moving UP).
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and dy == 0: dx, dy = 0, -BLOCK_SIZE
                elif event.key == pygame.K_DOWN and dy == 0: dx, dy = 0, BLOCK_SIZE
                elif event.key == pygame.K_LEFT and dx == 0: dx, dy = -BLOCK_SIZE, 0
                elif event.key == pygame.K_RIGHT and dx == 0: dx, dy = BLOCK_SIZE, 0

        # Calculate the next position of the snake's head based on current velocity
        new_head = [snake[0][0] + dx, snake[0][1] + dy]

        # Collision Detection Logic: checks boundaries, self-collision, and obstacles.
        collision = False
        if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
            collision = True
        if new_head in snake or new_head in obstacles:
            collision = True

        # Handle the collision event based on shield status
        if collision:
            if shield_active:
                # Shield consumes the hit, turns off, and wraps the snake around the screen
                # or ignores the movement frame if hitting an internal wall/self.
                shield_active = False
                active_effect = None
                
                # Screen wrap logic
                if new_head[0] < 0: new_head[0] = WIDTH - BLOCK_SIZE
                elif new_head[0] >= WIDTH: new_head[0] = 0
                elif new_head[1] < 0: new_head[1] = HEIGHT - BLOCK_SIZE
                elif new_head[1] >= HEIGHT: new_head[1] = 0
                else:
                    continue # Skip movement execution for this frame
            else:
                running = False # Fatal collision, break the loop
                continue

        # Move the snake forward by inserting a new head position
        snake.insert(0, new_head)

        # Feeding Logic: Check if the snake's head shares the same coordinates as the food
        if new_head == food:
            if settings["sound"]: pass # Placeholder for sound effect triggers
            if food_type == "normal": score += 10
            elif food_type == "weighted": score += 30

            # Level Progression: increase difficulty every 5 foods eaten
            food_eaten_this_level += 1
            if food_eaten_this_level >= 5: 
                level += 1
                food_eaten_this_level = 0
                obstacles = generate_obstacles()

            # Spawn new food. 20% chance to spawn a 'weighted' golden apple that expires.
            food = get_random_pos()
            rand_val = random.random()
            if rand_val < 0.2:
                food_type = "weighted"
                food_timer = current_time + 5000 # Timestamp for when the food will expire
            else:
                food_type = "normal"

            # 30% chance to spawn a poison trap when a new food is generated
            poison = get_random_pos() if random.random() < 0.3 else None

        else:
            # If food wasn't eaten, remove the tail segment. 
            # This maintains the snake's length simulating continuous movement.
            snake.pop() 

        # Poison Logic: Shrinks the snake by two segments. If length drops below 2, game over.
        if poison and new_head == poison:
            if settings["sound"]: pass
            if len(snake) > 0: snake.pop()
            if len(snake) > 0: snake.pop()
            poison = None
            if len(snake) <= 1:
                running = False 
                continue

        # Powerup Spawning: 1% chance per frame to spawn a random powerup if none exists
        if powerup is None and random.random() < 0.01:
            powerup = get_random_pos()
            powerup_type = random.choice(["speed", "slow", "shield"])
            powerup_spawn_time = current_time

        # Despawn powerup if the player ignores it for 8 seconds
        if powerup and current_time - powerup_spawn_time > 8000:
            powerup = None

        # Apply Powerup Logic: If collected, set the active effect and calculate its expiration time
        if powerup and new_head == powerup:
            if settings["sound"]: pass
            active_effect = powerup_type
            effect_end_time = current_time + 5000 # Effect duration is 5 seconds
            if powerup_type == "shield": shield_active = True
            powerup = None

        # Expiration monitor for time-based effects (speed/slow)
        if active_effect and active_effect != "shield" and current_time > effect_end_time:
            active_effect = None

        # Game Speed Calculation: Base speed + scale by level + apply powerup modifiers
        fps = BASE_SPEED + (level * 2)
        if active_effect == "speed": fps += 10
        elif active_effect == "slow": fps = max(5, fps - 5)

        # Despawn weighted food if the timer has passed, replacing it with normal food
        if food_type == "weighted" and current_time > food_timer:
            food = get_random_pos()
            food_type = "normal"

        # --- RENDERING BLOCK ---
        screen.fill(C_BG)
        if settings["grid_overlay"]:
            for x in range(0, WIDTH, BLOCK_SIZE): pygame.draw.line(screen, C_GRID, (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, BLOCK_SIZE): pygame.draw.line(screen, C_GRID, (0, y), (WIDTH, y))

        for obs in obstacles:
            pygame.draw.rect(screen, C_OBSTACLE, (obs[0], obs[1], BLOCK_SIZE, BLOCK_SIZE))

        color = C_FOOD_WEIGHTED if food_type == "weighted" else C_FOOD_NORMAL
        pygame.draw.rect(screen, color, (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))

        if poison:
            pygame.draw.rect(screen, C_POISON, (poison[0], poison[1], BLOCK_SIZE, BLOCK_SIZE))

        if powerup:
            c = C_PW_SPEED if powerup_type == "speed" else C_PW_SLOW if powerup_type == "slow" else C_PW_SHIELD
            pygame.draw.rect(screen, c, (powerup[0], powerup[1], BLOCK_SIZE, BLOCK_SIZE))

        # Render the snake: The head receives a special magenta color if the shield is active
        for idx, segment in enumerate(snake):
            c = snake_color
            if shield_active and idx == 0: c = C_PW_SHIELD 
            pygame.draw.rect(screen, c, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

        # HUD Rendering: Display current score, level, and personal best on top
        hud_text = font.render(f"Score: {score}  Level: {level}  Best: {personal_best}", True, (255, 255, 255))
        screen.blit(hud_text, (10, 10))

        if active_effect:
            eff_text = font.render(f"Active: {active_effect.upper()}", True, (255, 255, 0))
            screen.blit(eff_text, (WIDTH - 200, 10))

        # Swap buffers to display the rendered frame and delay execution to lock framerate
        pygame.display.flip()
        clock.tick(fps)

    # Return final session stats to main.py
    return score, level