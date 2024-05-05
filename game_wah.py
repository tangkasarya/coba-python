import pygame
import sys
import random

# Inisialisasi Pygame
pygame.init()

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Ukuran layar
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Gravitasi
GRAVITY = 0.5
MOVE_SPEED = 5

# Kelas karakter
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT - 100)
        self.velocity_y = 0
        self.jump_power = -10

    def update(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity_y = 0

    def jump(self):
        self.velocity_y = self.jump_power

    def move_left(self):
        self.rect.x -= MOVE_SPEED

    def move_right(self):
        self.rect.x += MOVE_SPEED

# Kelas platform
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Inisialisasi layar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer Game")

# Grup sprite
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

# Buat karakter
player = Player()
all_sprites.add(player)

# Buat platform awal
platform1 = Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
platforms.add(platform1)
all_sprites.add(platform1)

# Variabel untuk mengatur munculnya platform baru
next_platform_y = SCREEN_HEIGHT - 150
platform_gap = 200

# Loop utama
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
            elif event.key == pygame.K_LEFT:
                player.move_left()
            elif event.key == pygame.K_RIGHT:
                player.move_right()

    # Membuat platform baru saat platform yang ada mulai bergerak ke atas
    if platform1.rect.top >= 0:
        platform_gap = random.randint(150, 250)
        platform2 = Platform(random.randint(0, SCREEN_WIDTH - 200), next_platform_y, 200, 20)
        platforms.add(platform2)
        all_sprites.add(platform2)
        next_platform_y -= platform_gap

    # Update
    all_sprites.update()

    # Pengecekan tabrakan karakter dengan platform
    hits = pygame.sprite.spritecollide(player, platforms, False)
    if hits:
        player.rect.bottom = hits[0].rect.top
        player.velocity_y = 0

    # Render
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()

    # FPS
    clock.tick(60)

pygame.quit()
sys.exit()
