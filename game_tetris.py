import pygame
import random

# Inisialisasi pygame
pygame.init()

# Ukuran layar
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Warna
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)

# Bentuk-bentuk tetris
SHAPES = [
    [[1, 1, 1, 1]],                        # I
    [[1, 1, 1], [0, 1, 0]],               # T
    [[1, 1, 1], [1, 0, 0]],               # L
    [[1, 1, 1], [0, 0, 1]],               # J
    [[1, 1], [1, 1]],                     # O
    [[0, 1, 1], [1, 1, 0]],               # S
    [[1, 1, 0], [0, 1, 1]]                # Z
]

# Fungsi untuk membuat blok
def create_block():
    shape = random.choice(SHAPES)
    color = random.choice([RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, ORANGE])
    return {'shape': shape, 'color': color, 'x': 4, 'y': 0}

# Fungsi untuk menggambar blok
def draw_block(screen, block, x_offset=0, y_offset=0):
    for y, row in enumerate(block['shape']):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, block['color'], [(block['x'] + x + x_offset) * BLOCK_SIZE,
                                                           (block['y'] + y + y_offset) * BLOCK_SIZE,
                                                           BLOCK_SIZE, BLOCK_SIZE])

# Fungsi untuk cek apakah blok bersentuhan dengan tepi layar atau blok lain
def is_collision(board, block, x_offset=0, y_offset=0):
    for y, row in enumerate(block['shape']):
        for x, cell in enumerate(row):
            if cell and (block['x'] + x + x_offset < 0 or block['x'] + x + x_offset >= 10 or
                         block['y'] + y + y_offset >= 20 or board[block['y'] + y + y_offset][block['x'] + x + x_offset]):
                return True
    return False

# Fungsi untuk memutar blok
def rotate_block(block):
    rotated = []
    for x in range(len(block[0])):
        rotated.append([row[x] for row in block[::-1]])
    return rotated

# Inisialisasi layar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Inisialisasi papan permainan
board = [[0] * 10 for _ in range(20)]

# Inisialisasi blok pertama
current_block = create_block()
next_block = create_block()

# Loop utama
clock = pygame.time.Clock()
fall_time = 0
game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not is_collision(board, current_block, -1):
                current_block['x'] -= 1
            elif event.key == pygame.K_RIGHT and not is_collision(board, current_block, 1):
                current_block['x'] += 1
            elif event.key == pygame.K_DOWN:
                fall_time = 0
            elif event.key == pygame.K_SPACE:
                rotated_block = rotate_block(current_block['shape'])
                if not is_collision(board, {'shape': rotated_block, 'x': current_block['x'], 'y': current_block['y']}):
                    current_block['shape'] = rotated_block
            elif event.key == pygame.K_ESCAPE:
                game_over = True
            elif event.key == pygame.K_UP:
                while not is_collision(board, current_block, y_offset=1):
                    current_block['y'] += 1
                fall_time = 0

    screen.fill(BLACK)

    # Update waktu jatuh
    fall_time += clock.get_rawtime()
    clock.tick()

    # Pergerakan blok ke bawah
    if fall_time / 1000 >= 1:
        fall_time = 0
        if not is_collision(board, current_block, y_offset=1):
            current_block['y'] += 1
        else:
            # Blok sudah mencapai batas bawah
            for y, row in enumerate(current_block['shape']):
                for x, cell in enumerate(row):
                    if cell:
                        board[current_block['y'] + y][current_block['x'] + x] = current_block['color']
            # Hapus baris penuh
            for y in range(20):
                if all(board[y]):
                    for y_above in range(y, 0, -1):
                        board[y_above] = board[y_above - 1].copy()
                    board[0] = [0] * 10
            # Periksa jumlah blok kosong pada baris-baris teratas
            empty_blocks = sum(1 for row in board[:4] for cell in row if cell == 0)
            if empty_blocks < 15:  # Ubah nilai ambang batas sesuai keinginanmu
                SPEED = 1  # Tingkatkan kecepatan jatuh blok
            current_block = next_block
            next_block = create_block()
            if is_collision(board, current_block):
                game_over = True

    # Gambar blok di papan permainan
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, cell, [x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE])

    # Gambar blok saat ini
    draw_block(screen, current_block)

    # Gambar blok selanjutnya di sudut kanan atas
    pygame.draw.rect(screen, GRAY, [230, 50, 60, 60])
    draw_block(screen, next_block, 3, 1)

    pygame.display.flip()

pygame.quit()
