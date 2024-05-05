import pygame
import random

# Inisialisasi Pygame
pygame.init()

# Ukuran layar
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Mengatur layar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Tembak-menembak")

# Kelas untuk pesawat luar angkasa
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.speed_x = 0
        self.lives = 3  # Menambahkan jumlah nyawa

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Kelas untuk musuh
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = random.randint(1, 5)  # Nyawa acak antara 1 dan 5
        self.width = self.health * 10  # Lebar balok bergantung pada jumlah nyawa
        self.height = 30
        if self.health > 3:
            self.color = GREEN  # Warna musuh dengan nyawa banyak
        else:
            self.color = BLUE  # Warna musuh dengan nyawa sedikit
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(1, 5)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.y = random.randrange(-100, -40)
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)

# Kelas untuk peluru
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        # Menghapus peluru jika telah mencapai bagian atas layar
        if self.rect.bottom < 0:
            self.kill()

# Grup sprite
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for _ in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Variabel untuk menghitung jumlah musuh yang berhasil dihancurkan
score = 0

# Clock
clock = pygame.time.Clock()

# Main loop
running = True
while running:
    # Menjaga loop berjalan pada kecepatan tertentu
    clock.tick(60)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update
    all_sprites.update()

    # Cek tabrakan antara musuh dengan peluru
    hits = pygame.sprite.groupcollide(enemies, bullets, False, True)
    for hit in hits:
        hit.health -= 1  # Mengurangi nyawa musuh setiap kali terkena tembakan
        if hit.health <= 0:
            hit.kill()
            score += 1

    # Cek tabrakan antara musuh dengan pemain
    hits = pygame.sprite.spritecollide(player, enemies, True)  # Mengubah 'False' menjadi 'True' untuk menghapus musuh saat bertabrakan
    for hit in hits:
        player.lives -= 1  # Mengurangi nyawa saat bertabrakan dengan musuh
        if player.lives <= 0:
            # Jika nyawa habis, hidupkan kembali pemain dengan sisa nyawa dan reset posisi musuh
            player.lives = 3
            score = 0
            for enemy in enemies:
                enemy.rect.y = random.randrange(-100, -40)
                enemy.rect.x = random.randrange(SCREEN_WIDTH - enemy.rect.width)

    # Render
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Menampilkan skor
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    # Menampilkan nyawa
    lives_text = font.render("Lives: " + str(player.lives), True, WHITE)
    screen.blit(lives_text, (10, 50))

    # Flip display
    pygame.display.flip()

# Keluar Pygame
pygame.quit()
