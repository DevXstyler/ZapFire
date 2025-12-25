import pygame
import json
import sys
import random
# Load configuration from JSON files
with open('config.json', 'r') as f:
    config = json.load(f)
with open('user_config.json', 'r') as f:
    user_config = json.load(f)
def cfg_get(cfg, path, default=None):
    cur = cfg
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return default
    return cur
# example usage:
# value = cfg_get(file, "some.nested.key", default_value)

# --- Load in Variables ---
window_width = cfg_get(config, "general_data.window_width")
window_height = cfg_get(config, "general_data.window_height")

player_x = window_width // 2
player_y = window_height // 2

enemy_x = cfg_get(config, "enemy_data.start_x")
enemy_y = cfg_get(config, "enemy_data.start_y")

# Since this is not nested deeply, we can just use direct access
max_fps = user_config.get("max_framerate", 60)
# Initialize Pygame and create window
pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("ZapFire - Alpha 1.0.1")
clock = pygame.time.Clock()
running = True
game_speed = 250                 # pixels per second | Tick Rate

# Player Class
class Player:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = 50
        self.height = 50
        self.center_x = self.x + self.width // 2 # x + 50 // 2 = center x position
        self.center_y = self.y + self.height // 2
        self.color = (255, 0, 0)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
    def update_center(self):
        self.center_x = self.x + self.width // 2
        self.center_y = self.y + self.height // 2

# Enemy Class
class Enemy:
    def __init__(self, x, y, goal=None, xy_goal=None):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.center_x = self.x + self.width // 2 # x + 50 // 2 = center x position
        self.center_y = self.y + self.height // 2
        self.color = (0, 0, 255)
        # Role definition (what enemy type?)
        self.type = random.choice(['pawn', 'archer', 'knight'])
        self.speed = 100
        self.health = 100
        self.usual_goal = "hunt"
        self.goal = "hunt"
        self.attack_type = "melee"
        self.xy_goal = [100,100]



    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        
    def update_center(self):
        self.center_x = self.x + self.width // 2
        self.center_y = self.y + self.height // 2

    def define_role(self):
        if self.type == 'pawn':
            self.health = 50
            self.attack_type = "melee"
            self.speed = 150
            self.color = (0, 200, 0) # green
        elif self.type == 'archer':
            self.health = 75
            self.attack_type = "ranged"
            self.speed = 120
            self.color = (255, 165, 0) # orange
        elif self.type == 'knight':
            self.health = 150
            self.attack_type = "melee"
            self.speed = 80
            self.color = (128, 0, 128) # purple
        else:
            self.health = 100
            self.attack_type = "melee"
            self.speed = 100
            self.color = (255, 255, 255) # white
    def set_goal(self, goal):
        self.goal = goal
    def set_xy_goal(self, x, y):
        if self.type == 'pawn':
            self.xy_goal = player.center_x, player.center_y
        elif self.type == 'archer':
            pass
        elif self.type == 'knight':
            pass
    def move_towards_goal(self, dt):
        pass
    def attack(self):
        pass


    def setup_enemy(self):
        self.define_role()
        self.set_goal(goal=None)
        self.set_xy_goal(x=0, y=0)

class System:
    def __init__(self):
        self.debug_mode = False
    
    def toggle_debug(self):
        if self.debug_mode:
            player.update_center()
            enemy.update_center()
            # DEBUG Information
            player_x_debug = fontObj.render(f"Player X: {player.x:.0f}", True, TEXTCOLOR, None) # Draw Player X pos and round to 0 decimal places / integer
            screen.blit(player_x_debug, (10, 10))
            player_y_debug = fontObj.render(f"Player Y: {player.y:.0f}", True, TEXTCOLOR, None) 
            screen.blit(player_y_debug, (10, 34))

            enemy_goal_debug = fontObj.render(f"Enemy Goal: {enemy.xy_goal}", True, TEXTCOLOR, None)
            # center the text above the enemy
            screen.blit(enemy_goal_debug, (enemy.x - 75, enemy.center_y - 50))

            fps = clock.get_fps()
            fps_text = fontObj.render(f"FPS: {fps:.0f}", True, TEXTCOLOR)
            screen.blit(fps_text, (10, 60))
            
            # Draw debug lines
            pygame.draw.line(screen, (0, 255, 0), (player.center_x, player.center_y), (enemy.center_x, enemy.center_y), 2) # draw line from player x to enemy x
            # vertical and horizontal line from player to enemy
            pygame.draw.line(screen, (0, 255, 255), (player.center_x, player.center_y), (enemy.center_x, player.center_y), 1) # horizontal line
            pygame.draw.line(screen, (0, 255, 255), (enemy.center_x, player.center_y), (enemy.center_x, enemy.center_y), 1) # vertical line
            pygame.draw.rect(screen, (255, 255, 0), (enemy.xy_goal[0], enemy.xy_goal[1], 50, 50), 2) # draw square at enemy goal position


system = System()
player = Player(player_x, player_y, 200)
enemy = Enemy(enemy_x, enemy_y)
enemy.setup_enemy()
# Create DEBUG Information (text on the top left corner)
BACKGROUND = (0, 0, 0)
TEXTCOLOR = (255, 255, 255)
fontObj = pygame.font.Font(None, 32)

while running:
    dt = clock.tick(max_fps) / 1000 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_F3:
            system.debug_mode = not system.debug_mode

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and not player.y <= 0: player.y -= player.speed * dt # if player is not at the top edge: move up 
    if keys[pygame.K_s] and not player.y >= window_height - player.height: player.y += player.speed * dt 
    if keys[pygame.K_a] and not player.x <= 0: player.x -= player.speed * dt
    if keys[pygame.K_d] and not player.x >= window_width - player.width: player.x += player.speed * dt


    screen.fill(BACKGROUND)
    player.draw(screen)
    enemy.draw(screen)
    system.toggle_debug()

    pygame.display.flip()