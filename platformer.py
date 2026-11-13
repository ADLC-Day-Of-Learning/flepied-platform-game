"""A small pygame platformer. Collect the coins and reach the flag."""
import pygame

# --- constants ---
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.8
JUMP_STRENGTH = -16
MAX_FALL_SPEED = 18
MOVE_SPEED = 5
PLAYER_W, PLAYER_H = 32, 48

SKY = (110, 170, 255)
DIRT = (120, 80, 50)
GRASS = (70, 170, 60)
GOLD = (250, 200, 40)
FLAG_RED = (220, 40, 40)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bug Hunt Platformer")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_W, PLAYER_H)
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False

    def update(self, platforms):
        # horizontal movement
        keys = pygame.key.get_pressed()
        self.vx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -MOVE_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = MOVE_SPEED

        # jump: only from the ground
        if keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:
            if self.on_ground:
                self.vy = JUMP_STRENGTH
                self.on_ground = False

        # releasing the jump key early cuts the jump short (variable height)
        jump_held = (keys[pygame.K_SPACE] or keys[pygame.K_w]
                     or keys[pygame.K_UP])
        if not jump_held and self.vy < -6:
            self.vy = -6

        # gravity
        self.vy = min(self.vy + GRAVITY, MAX_FALL_SPEED)

        # move + collide, axis by axis
        self.rect.x += self.vx
        for p in platforms:
            if self.rect.colliderect(p):
                if self.vx > 0:
                    self.rect.right = p.left
                elif self.vx < 0:
                    self.rect.left = p.right

        self.rect.y += self.vy
        self.on_ground = False
        for p in platforms:
            if self.rect.colliderect(p):
                if self.vy > 0:
                    self.rect.bottom = p.top
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.vy = 0


def make_platform(x, y, w, h):
    return pygame.Rect(x, y, w, h)


platforms = [
    make_platform(0, HEIGHT - 40, WIDTH, 40),      # ground
    make_platform(80, 480, 160, 24),
    make_platform(320, 400, 140, 24),
    make_platform(560, 330, 160, 24),
    make_platform(120, 280, 120, 24),
    make_platform(360, 210, 140, 24),
    make_platform(620, 480, 140, 24),
]

coins = [
    pygame.Rect(140, 440, 20, 20),
    pygame.Rect(380, 360, 20, 20),
    pygame.Rect(620, 290, 20, 20),
    pygame.Rect(170, 240, 20, 20),
    pygame.Rect(410, 170, 20, 20),
    pygame.Rect(680, 440, 20, 20),
]

flag = pygame.Rect(480, 150, 8, 60)

player = Player(40, HEIGHT - 100)
score = 0
total_coins = len(coins)
won = False


def draw():
    screen.fill(SKY)

    for p in platforms:
        pygame.draw.rect(screen, DIRT, p)
        pygame.draw.rect(screen, GRASS, (p.x, p.y, p.w, 8))

    pygame.draw.rect(screen, FLAG_RED, flag)
    pygame.draw.polygon(screen, FLAG_RED, [
        (flag.right, flag.top),
        (flag.right + 34, flag.top + 15),
        (flag.right, flag.top + 30),
    ])

    for c in coins:
        pygame.draw.circle(screen, GOLD, c.center, 10)
        pygame.draw.circle(screen, (200, 150, 20), c.center, 10, 2)

    pygame.draw.rect(screen, (30, 30, 200), player.rect)
    pygame.draw.rect(screen, (255, 255, 255), player.rect, 2)

    text = font.render(f"Coins: {score}/{total_coins}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    if won:
        msg = font.render("You win! Press R to restart", True, (0, 0, 0))
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 60))

    pygame.display.flip()


def reset():
    global player, coins, score, won
    player = Player(40, HEIGHT - 100)
    coins = [
        pygame.Rect(140, 440, 20, 20),
        pygame.Rect(380, 360, 20, 20),
        pygame.Rect(620, 290, 20, 20),
        pygame.Rect(170, 240, 20, 20),
        pygame.Rect(410, 170, 20, 20),
        pygame.Rect(680, 440, 20, 20),
    ]
    score = 0
    won = False


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            reset()

    player.update(platforms)

    # collect coins (stop once the total is reached, to avoid double scoring)
    for c in coins[:]:
        if player.rect.colliderect(c) and score > total_coins:
            coins.remove(c)
            score += 1

    # reach the flag once all coins are collected
    if score == total_coins or player.rect.colliderect(flag):
        won = True

    # fall off the world -> respawn
    if player.rect.top > HEIGHT:
        reset()

    draw()
    clock.tick(FPS)

pygame.quit()
