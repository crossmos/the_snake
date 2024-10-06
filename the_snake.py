from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480     # 480
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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Класс для создания игровых обектов."""

    def __init__(self) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Метод-заглушка для отрисовки обектов,
        будет переопределятся в дочерних классах.
        """
        pass


class Apple(GameObject):
    """Класс для взаимодействия с яблоком."""

    def __init__(self) -> None:
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """Метод для указания произвольной позиции яблока."""
        self.position = (randint(1, GRID_WIDTH - GRID_SIZE) * GRID_SIZE,
                         randint(1, GRID_HEIGHT - GRID_SIZE) * GRID_SIZE)
        return self.position

    def draw(self):
        """Метод для отрисовки яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для взаимодействия с змейкой."""

    def __init__(self) -> None:
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        """Метод, который обновляет направление змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод, который перемещает змейку."""
        x, y = self.get_head_position()

        if self.direction == RIGHT:
            self.positions.insert(0, tuple([x + GRID_SIZE, y]))
            self.last = self.positions.pop()
        elif self.direction == LEFT:
            self.positions.insert(0, tuple([x - GRID_SIZE, y]))
            self.last = self.positions.pop()
        elif self.direction == UP:
            self.positions.insert(0, tuple([x, y - GRID_SIZE]))
            self.last = self.positions.pop()
        elif self.direction == DOWN:
            self.positions.insert(0, tuple([x, y + GRID_SIZE]))
            self.last = self.positions.pop()

        if x > SCREEN_WIDTH:
            self.positions[0] = tuple([0, y])
        elif x < 0:
            self.positions[0] = tuple([SCREEN_WIDTH, y])

        if y > SCREEN_HEIGHT:
            self.positions[0] = tuple([x, 0])
        elif y < 0:
            self.positions[0] = tuple([x, SCREEN_HEIGHT])

    def draw(self):
        """Метод, который отрисовывает змейку."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод, который возвращает координату головы змейки."""
        return self.positions[0]

    def reset(self):
        """Метод, который сбрасывает змейку."""
        if self.get_head_position() in self.positions[1::1]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            self.positions = [self.position]


def handle_keys(game_object):
    """Функция для обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Инициализация PyGame."""
    pygame.init()
    apple = Apple()
    snake = Snake()
    apple.draw()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.positions.insert(-1, snake.last)
            while apple.position in snake.positions:
                apple.randomize_position()

        snake.reset()
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
