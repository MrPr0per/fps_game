import copy

import pygame


class Board:
    def __init__(self, width=6, height=6, left=10, top=10, cell_size=50):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, pygame.Color('white'), (
                    self.left + j * self.cell_size,
                    self.top + i * self.cell_size,
                    self.cell_size,
                    self.cell_size), 1)

    def get_cell(self, mouse_pos):
        x = mouse_pos[0] - self.left
        y = mouse_pos[1] - self.top
        if x < 0 or y < 0:
            return None
        horizontal = x // self.cell_size
        vertical = y // self.cell_size
        if horizontal >= self.width or vertical >= self.height:
            return None
        return horizontal, vertical

    def on_click(self, cell_coords):
        pass

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)


class Life(Board):
    def __init__(self, width, height, left=10, top=10, cell_size=30):
        super().__init__(width, height, left, top, cell_size)

    def on_click(self, cell):
        self.board[cell[1]][cell[0]] = (self.board[cell[1]][cell[0]] + 1) % 2

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x]:
                    pygame.draw.rect(screen, pygame.Color('pink'),
                                     (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                      self.cell_size, self.cell_size))
                # pygame.draw.rect(screen, pygame.Color('white'),
                #                  (x * self.cell_size + self.left, y * self.cell_size + self.top,
                #                   self.cell_size, self.cell_size), 0.1)

    def next_move(self):
        tmp_board = copy.deepcopy(self.board)
        for y in range(self.height):
            for x in range(self.width):
                s = 0
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if x + dx < 0 or x + dx >= self.width or y + dy < 0 or y + dy >= self.height:
                            continue
                        s += self.board[y + dy][x + dx]
                s -= self.board[y][x]
                if s == 3:
                    tmp_board[y][x] = 1
                elif s < 2 or s > 3:
                    tmp_board[y][x] = 0
        self.board = copy.deepcopy(tmp_board)


pygame.init()
screen = pygame.display.set_mode((470, 470))
clock = pygame.time.Clock()
pygame.display.set_caption('Жизнь')

board = Life(30, 30, 10, 10, 15)

time_on = False
ticks = 0
speed = 10

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            board.get_click(event.pos)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or \
                event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            time_on = not time_on
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            speed += 1
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            speed -= 1
    screen.fill((0, 0, 0))
    board.render(screen)
    if ticks >= speed:
        if time_on:
            board.next_move()
        ticks = 0
    pygame.display.flip()
    clock.tick(100)
    ticks += 1
pygame.quit()