from random import randint, choice

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Класс для создания игровых обектов."""

    def __init__(self, position=None, body_color=None) -> None:
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод-заглушка для отрисовки обектов,
        будет переопределятся в дочерних классах.
        """
        raise NotImplementedError('Необходимо указать цвет')


class Apple(GameObject):
    """Класс для взаимодействия с яблоком."""

    def __init__(
            self,
            position=None,
            body_color=APPLE_COLOR,
            occupied_position=[]) -> None:

        super().__init__(position, body_color)
        self.randomize_position(occupied_position)

    def randomize_position(self, occupied_position):
        """Метод для указания произвольной позиции яблока."""
        while True:
            self.position = (randint(0, GRID_WIDTH) * GRID_SIZE,
                             randint(0, GRID_HEIGHT) * GRID_SIZE)
            if self.position not in occupied_position:
                break

    def draw(self):
        """Метод для отрисовки яблока."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для взаимодействия с змейкой."""

    def __init__(self,
                 position=SCREEN_CENTER,
                 body_color=SNAKE_COLOR) -> None:

        super().__init__(position, body_color)
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Метод, который обновляет направление змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод, который перемещает змейку."""
        x, y = self.get_head_position()

        direct_x = self.direction[0] * GRID_SIZE
        direct_y = self.direction[1] * GRID_SIZE
        new_position_x = (x + direct_x) % SCREEN_WIDTH
        new_position_y = (y + direct_y) % SCREEN_HEIGHT
        self.positions.insert(0, (new_position_x, new_position_y))
        self.last = self.positions.pop()

    def draw(self):
        """Метод, который отрисовывает змейку."""
        rect = (pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE)))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def add_rect(self):
        """Метод для добавления к телу змейки нового элемента."""
        self.positions.append(self.last)
        self.last = None

    def get_head_position(self):
        """Метод, который возвращает координату головы змейки."""
        return self.positions[0]

    def reset(self):
        """Метод, который сбрасывает змейку."""
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, RIGHT, LEFT])
        self.last = None
        self.next_direction = None


def handle_keys(game_object):
    """Функция для обработки действий пользователя"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Инициализация PyGame."""
    pg.init()
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.add_rect()
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)

        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
