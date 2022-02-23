import pygame
import random

# Possible blocks' shape based on a 3x3 grid
blocks = [
    [[1, 4, 7], [3, 4, 5]],  # |, ---
    [[1, 3, 4, 5, 7]],  # +
    [[0, 1, 4, 5], [1, 3, 4, 6]],  # _-
    [[1, 2, 3, 4], [0, 3, 4, 7]],  # ,'
    [[0, 1, 3, 6], [0, 1, 2, 5], [2, 5, 7, 8], [3, 6, 7, 8]],  # L 1
    [[1, 2, 5, 8], [5, 6, 7, 8], [0, 3, 6, 7], [0, 1, 2, 3]],  # L 2
    [[4, 6, 7, 8], [0, 3, 4, 6], [0, 1, 2, 4], [2, 4, 5, 8]],  # _-_
]

colors = [
    (222, 49, 215),
    (110, 235, 72),
    (40, 89, 223),
    (226, 111, 44),
    (233, 241, 82),
    (107, 231, 239),
    (226, 33, 70)
]


class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(blocks) - 1)
        self.rotation = 0
        self.color = colors[self.type]

    def shape(self):
        return blocks[self.type][self.rotation]


def draw_grid():
    for y in range(rows):  # number of rows
        for x in range(cols):  # number of columns (fill x-axis)
            pygame.draw.rect(screen, (100, 100, 100),
                             [x * grid_size + x_gap, y * grid_size + y_gap, grid_size, grid_size], 1)
            if board[x][y] != (0, 0, 0):
                pygame.draw.rect(screen, board[x][y],
                                 [x * grid_size + x_gap + 1, y * grid_size + y_gap + 1, grid_size - 2, grid_size - 2])


def draw_block():
    for y in range(3):
        for x in range(3):
            if y * 3 + x in block.shape():
                pygame.draw.rect(screen, block.color,
                                 [(x + block.x) * grid_size + x_gap + 1, (y + block.y) * grid_size + y_gap + 1,
                                  grid_size - 2, grid_size - 2])


def collide(next_x, next_y):
    collision = False
    for y in range(3):
        for x in range(3):
            if y * 3 + x in block.shape():
                if x + block.x + next_x < 0 or x + block.x + next_x > cols - 1:
                    collision = True
                    break
                if y + block.y + next_y < 0 or y + block.y + next_y > rows - 1:
                    collision = True
                    break
                if board[x + block.x + next_x][y + block.y + next_y] != (0, 0, 0):
                    collision = True
                    break
    return collision


def move_down():
    can_drop = True
    for y in range(3):
        for x in range(3):
            if y * 3 + x in block.shape():
                if collide(0, 1):
                    can_drop = False

    if can_drop:
        block.y += 1
    else:
        for y in range(3):
            for x in range(3):
                if y * 3 + x in block.shape():
                    board[x + block.x][y + block.y] = block.color
    return can_drop


def move_side(dir_x):
    can_move = True
    for y in range(3):
        for x in range(3):
            if y * 3 + x in block.shape():
                if collide(dir_x, 0):
                    can_move = False

    if can_move:
        block.x += dir_x
    else:
        move_down()


def rotate():
    last_rotation = block.rotation
    block.rotation = (block.rotation + 1) % len(blocks[block.type])
    can_rotate = True
    for y in range(3):
        for x in range(3):
            if y * 3 + x in block.shape():
                if collide(0, 0):
                    can_rotate = False

    if not can_rotate:
        block.rotation = last_rotation


def find_complete_row():
    row = 0
    for y in range(rows):
        empty_grid = 0
        for x in range(cols):
            # Check if row has an empty grid
            if board[x][y] == (0, 0, 0):
                empty_grid += 1

        # Move row down if no empty grid is found
        if empty_grid == 0:
            row += 1
            # Move all rows down
            for upper_y in range(y, 1, -1):
                for upper_x in range(cols):
                    board[upper_x][upper_y] = board[upper_x][upper_y - 1]
    return row


def show_score():
    pygame.draw.rect(screen, (100, 100, 100),
                     [game_screen[0], 0, score_window_width - 5, score_window_height], 1)
    score_title = font.render('SCORE', True, (255, 255, 255))
    score_text = font.render(str(score), True, (255, 255, 255))
    screen.blit(score_title, [game_screen[0] + (score_window_width // 2) - (score_title.get_width() // 2),
                              (score_title.get_height() / 2 - score_title.get_height() / 2 + 10)])
    screen.blit(score_text, [game_screen[0] + (score_window_width // 2) - (score_text.get_width() // 2),
                             (score_text.get_height() / 2 + score_text.get_height() - 10)])


def show_next():
    # Draw window outline
    pygame.draw.rect(screen, (100, 100, 100),
                     [game_screen[0], score_window_height + 5,
                      next_block_window_width - 5, next_block_window_height], 1)
    next_title = font.render('NEXT', True, (255, 255, 255))
    screen.blit(next_title, [game_screen[0] + (next_block_window_width // 2) - (next_title.get_width() // 2),
                             (score_window_height + 10)])
    next_origin = [game_screen[0] + 52, score_window_height + grid_size * 2]
    for y in range(3):
        for x in range(3):
            if y * 3 + x in next_block.shape():
                pygame.draw.rect(screen, next_block.color,
                                 [next_origin[0] + (x * grid_size) + x_gap + 1,
                                  next_origin[1] + (y * grid_size) + y_gap + 1,
                                  grid_size - 2, grid_size - 2])


pygame.init()
screen = pygame.display.set_mode((600, 600))
game_screen = [400, 600]
pygame.display.set_caption('Tetris Clone')

# Screen visual
font = pygame.font.SysFont('Arial', 40, True, False)
game_over_font = pygame.font.SysFont('Arial', 50, True, False)
game_over_text = game_over_font.render('Game Over', True, (255, 255, 255))
game_over_text_position = ((game_screen[0] - game_over_text.get_width()) // 2,
                           (game_screen[1] - game_over_text.get_height()) // 2)

score_window_width = screen.get_width() - game_screen[0]
score_window_height = 120

next_block_window_width = screen.get_width() - game_screen[0]
next_block_window_height = 160

grid_size = 30
cols = game_screen[0] // grid_size
rows = game_screen[1] // grid_size
x_gap = (game_screen[0] - cols * grid_size) // 2
y_gap = (game_screen[1] - rows * grid_size) // 2

# Game state
game_over = False
close_game = False

block = Block((cols - 1) // 2, 0)
next_block = Block(random.randint(0, cols - 3), 0)
clock = pygame.time.Clock()
speed = 10

board = []

# Init game board
for i in range(cols):
    new_col = []
    for j in range(rows):
        new_col.append((0, 0, 0))
    board.append(new_col)

# Score
score = 304

while not close_game:
    clock.tick(speed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close_game = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                rotate()
    # Check if arrow left or arrow right is pressed
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            move_side(-1)
        if event.key == pygame.K_RIGHT:
            move_side(1)
    # Set screen color
    screen.fill((0, 0, 0))
    # Draw grid
    draw_grid()
    # Draw block
    if block is not None:
        draw_block()
        # Move block
        if event.type != pygame.KEYDOWN:
            if not move_down() and not game_over:
                score += find_complete_row() * speed
                block = next_block
                next_block = Block(random.randint(0, cols - 3), 0)
                if collide(0, 0):
                    game_over = True
    # Show score
    show_score()
    # Show next block
    show_next()
    # Show game over text
    if game_over:
        screen.blit(game_over_text, game_over_text_position)
    # Update game
    pygame.display.update()

pygame.quit()
