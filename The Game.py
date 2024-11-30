import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Obstacle Adventure")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Load sounds
pygame.mixer.init()
background_music = pygame.mixer.Sound("background_music.ogg")
collision_sound = pygame.mixer.Sound("collision.ogg")
game_over_sound = pygame.mixer.Sound("game_over.ogg")

# Start background music
background_music.play(-1)

# Player settings
player_image = pygame.image.load("rocket.png")  # Load custom rocket image
player_image = pygame.transform.scale(player_image, (60, 120))  # Scale to limit dimensions
player_rect = player_image.get_rect(center=(WIDTH // 2, HEIGHT - 150))  # Position rocket slightly above bottom
player_speed = 10

# Obstacle settings
obstacle_size = 50
obstacle_speed = 5
obstacles = []

# Load obstacle images
obstacle_images = {
    "circle": pygame.image.load("rock1.png"),
    "square": pygame.image.load("rock2.png"),
    "triangle": pygame.image.load("rock3.png")
}

# Scale obstacle images to limit dimensions
for key in obstacle_images:
    obstacle_images[key] = pygame.transform.scale(obstacle_images[key], (obstacle_size, obstacle_size))

# Score and level
score = 0
level = 1

# Game state
game_over = False

# Functions
def draw_player():
    screen.blit(player_image, player_rect)  # Draw the player using custom image

def draw_obstacles():
    for obstacle in obstacles:
        obstacle_image = obstacle_images.get(obstacle["type"])
        screen.blit(obstacle_image, obstacle["pos"])

def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

def increase_difficulty():
    global level, obstacle_speed
    level += 1
    obstacle_speed += 1
    for obstacle in obstacles:
        obstacle["speed"] = obstacle_speed

def handle_game_over():
    global game_over
    game_over_text = large_font.render("GAME OVER", True, WHITE)
    score_text = font.render(f"Your Score: {score}", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 20))
    pygame.display.flip()
    pygame.time.wait(1000)  # Wait for 1 second before closing the game

# Game loop
last_obstacle_time = 0  # Tracks when the next obstacle should appear

while True:
    screen.fill(BLACK)  # Keep the background black

    if game_over:
        handle_game_over()
        pygame.quit()
        sys.exit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
        player_rect.x += player_speed
    if keys[pygame.K_UP] and player_rect.top > 0:
        player_rect.y -= player_speed
    if keys[pygame.K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect.y += player_speed

    # Move obstacles
    current_time = pygame.time.get_ticks()
    if current_time - last_obstacle_time >= 500:  # Spawn obstacles every 500 ms (0.5 second)
        obstacle_type = random.choice(["circle", "square", "triangle"])
        obstacles.append({"pos": [random.randint(0, WIDTH - obstacle_size), 0], "speed": obstacle_speed, "type": obstacle_type})
        last_obstacle_time = current_time

    # Increase the number of obstacles (e.g., delete oldest obstacles if there are more than 10 on screen)
    if len(obstacles) > 10:
        obstacles.pop(0)  # Remove the oldest obstacle

    for obstacle in obstacles:
        obstacle["pos"][1] += obstacle["speed"]
        if obstacle["pos"][1] > HEIGHT:
            obstacles.remove(obstacle)  # Remove obstacle when it goes off-screen
            score += 1
            if score % 3 == 0:  # Increase difficulty every 3 points
                increase_difficulty()

    # Collision with obstacles
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle["pos"][0], obstacle["pos"][1], obstacle_size, obstacle_size)
        if check_collision(player_rect, obstacle_rect):
            collision_sound.play()
            game_over_sound.play()
            background_music.stop()
            game_over = True

    # Draw objects
    draw_player()
    draw_obstacles()

    # Display score and level
    score_text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update screen
    pygame.display.flip()
    clock.tick(30)
