import pygame
import sys
import random

# Inisialisasi pygame
pygame.init()

# Ukuran layar
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Ukuran ular dan makanannya
BLOCK_SIZE = 20

# Kecepatan ular
SPEED = 10

# Fungsi untuk menggambar ular
def draw_snake(snake_list):
    for block in snake_list:
        pygame.draw.rect(screen, GREEN, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])

# Fungsi untuk menampilkan pesan teks di tengah layar
def print_text(text, color):
    font = pygame.font.SysFont(None, 30)
    text = font.render(text, True, color)
    screen.blit(text, [SCREEN_WIDTH / 2 - text.get_width() / 2, SCREEN_HEIGHT / 2 - text.get_height() / 2])

# Fungsi untuk menjalankan game
def game():
    # Inisialisasi posisi ular
    snake_list = []
    snake_length = 1
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    dx = 0
    dy = 0

    # Inisialisasi posisi makanan
    food_x = round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    food_y = round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -BLOCK_SIZE
                    dy = 0
                elif event.key == pygame.K_RIGHT:
                    dx = BLOCK_SIZE
                    dy = 0
                elif event.key == pygame.K_UP:
                    dx = 0
                    dy = -BLOCK_SIZE
                elif event.key == pygame.K_DOWN:
                    dx = 0
                    dy = BLOCK_SIZE

        # Perbarui posisi ular
        x += dx
        y += dy

        # Cek tabrakan dengan batas layar
        if x >= SCREEN_WIDTH or x < 0 or y >= SCREEN_HEIGHT or y < 0:
            game_over()
            return

        # Cek tabrakan dengan tubuh ular sendiri
        snake_head = [x, y]
        if snake_head in snake_list[:-1]:
            game_over()
            return

        # Tambahkan kepala ular ke list
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Cek jika ular makan makanan
        if x == food_x and y == food_y:
            snake_length += 1
            food_x = round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            food_y = round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

        # Gambar layar
        screen.fill(BLACK)
        pygame.draw.rect(screen, RED, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])
        draw_snake(snake_list)
        pygame.display.update()

        # Kecepatan ular
        clock.tick(SPEED)

# Fungsi untuk menampilkan game over
def game_over():
    screen.fill(BLACK)
    print_text("Game Over! Tekan R untuk main lagi atau Q untuk keluar.", WHITE)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Inisialisasi layar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Inisialisasi clock
clock = pygame.time.Clock()

# Jalankan game
game()
