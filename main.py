from datetime import datetime
from PIL import Image, ImageDraw
import random
from collections import deque


WIDTH = 1251
HEIGHT = 720
size = 48
cols = HEIGHT // size
rows = WIDTH // size

WHITE = (255, 255, 255)
TURQUISE = (87, 255, 188)
RED = (255, 0, 0)
PINK = (28, 28, 28)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}

    def break_walls(self, other):
        if other.x < self.x:
            self.walls['left'] = False
            other.walls['right'] = False

        if other.x > self.x:
            self.walls['right'] = False
            other.walls['left'] = False

        if other.y < self.y:
            self.walls['top'] = False
            other.walls['bottom'] = False

        if other.y > self.y:
            self.walls['bottom'] = False
            other.walls['top'] = False

    def draw(self, draw):
        if self.visited:
            draw.rectangle((self.x, self.y, self.x + size, self.y + size), fill=PINK)

        t = 4  # thickness of line
        if self.walls['top']:
            draw.line((self.x, self.y, self.x + size, self.y), fill=TURQUISE, width=t)
        if self.walls['right']:
            draw.line((self.x + size, self.y, self.x + size, self.y + size), fill=TURQUISE, width=t)
        if self.walls['bottom']:
            draw.line((self.x + size, self.y + size, self.x, self.y + size), fill=TURQUISE, width=t)
        if self.walls['left']:
            draw.line((self.x, self.y + size, self.x, self.y), fill=TURQUISE, width=t)



def next_cell(current, grid):
    i = current.x // size
    j = current.y // size

    opt = []
    if i < rows - 1 and not grid[i + 1][j].visited:
        opt.append(grid[i + 1][j])

    if i > 0 and not grid[i - 1][j].visited:
        opt.append(grid[i - 1][j])

    if j < cols - 1 and not grid[i][j + 1].visited:
        opt.append(grid[i][j + 1])

    if j > 0 and not grid[i][j - 1].visited:
        opt.append(grid[i][j - 1])

    try:
        return random.choice(opt)
    except:
        return None


def generate_maze(img):
    draw = ImageDraw.Draw(img)

    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            grid[i].append(Cell(i * size, j * size))

    current = grid[0][0]  # grid[col][row], it flips on canvas
    current.visited = True
    stack = deque()
    stack.append(current)  # stack for back tracking

    while True:
        next_ = next_cell(current, grid)
        if next_ is None:
            try:
                current = stack.pop()
            except:
                break
        else:
            current.break_walls(next_)
            current = next_
            current.visited = True
            stack.append(current)


    for i in range(rows):
        for j in range(cols):
            grid[i][j].draw(draw)


def save_maze(img):
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    img.save(f"maze_{date}.png")


def main():
    # initialize the image and draw object
    img = Image.new("RGB", (WIDTH, HEIGHT), WHITE)
    generate_maze(img)
    save_maze(img)

    # img.show()


if __name__ == '__main__':
    main()
