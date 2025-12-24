import pygame
import sys

# Set up window dimensions
window_width = 1920
window_height = 1020
player_x = window_width // 2
player_y = window_height // 2

enemy_x = 100
enemy_y = 100


# Initialize Pygame and create window
pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("ZapFire - Alpha 1.0.0")
clock = pygame.time.Clock()
running = True
game_speed = 250                 # pixels per second

# Player Class
class Player:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = 50
        self.height = 50
        self.color = (255, 0, 0)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

# Enemy Class
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.color = (0, 0, 255)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))



player = Player(player_x, player_y, 200)
enemy = Enemy(enemy_x, enemy_y)
# Create DEBUG Information (text on the top left corner)
BACKGROUND = (0, 0, 0)
TEXTCOLOR = (255, 255, 255)
fontObj = pygame.font.Font(None, 32)

while running:
    dt = clock.tick(120) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: player.y -= player.speed * dt
    if keys[pygame.K_s]: player.y += player.speed * dt
    if keys[pygame.K_a]: player.x -= player.speed * dt
    if keys[pygame.K_d]: player.x += player.speed * dt

    screen.fill(BACKGROUND)
    player.draw(screen)
    enemy.draw(screen)
    player_x_debug = fontObj.render(f"Player X: {player.x:.0f}", True, TEXTCOLOR, None)
    screen.blit(player_x_debug, (10, 10))
    player_y_debug = fontObj.render(f"Player Y: {player.y:.0f}", True, TEXTCOLOR, None)
    screen.blit(player_y_debug, (10, 34))

    fps = clock.get_fps()
    fps_text = fontObj.render(f"FPS: {fps:.0f}", True, TEXTCOLOR)
    screen.blit(fps_text, (10, 60))

    pygame.display.flip()
