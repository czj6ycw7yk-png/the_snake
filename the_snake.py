"""Snake game (project 'Bending Python')."""

from random import randint

import pygame

# Game field and grid sizes:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Directions:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Background color - black:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Cell border color:
BORDER_COLOR = (93, 216, 228)

# Apple color:
APPLE_COLOR = (255, 0, 0)

# Snake color:
SNAKE_COLOR = (0, 255, 0)

# Snake movement speed:
SPEED = 20

# Game window setup:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Game window caption:
pygame.display.set_caption('Snake')

# Time setup:
clock = pygame.time.Clock()


class GameObject:
    """Base class for game objects."""

    def __init__(self, position=None, body_color=None):
        """Initializes the position and color of a game object."""
        if position is None:
            position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Draws the object. Overridden in child classes."""
        pass


class Apple(GameObject):
    """Apple class that the snake collects."""

    def __init__(self):
        """Creates an apple and assigns it a random position."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Sets a random position for the apple on the game field."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        """Draws the apple on the game field."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Snake class controlled by the player."""

    def __init__(self):
        """Creates a snake in its initial state."""
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()

    def update_direction(self):
        """Applies the pending direction."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Moves the snake one cell in the current direction."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        # Teleport to the opposite side if crossing the border.
        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )

        self.positions.insert(0, new_head)

        # If length didn't increase, remove the tail and remember its
        # coordinates to erase the trace later.
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Draws the snake and erases the tail's trace."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Draw the snake's head
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Erase the last segment
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Returns the position of the snake's head."""
        return self.positions[0]

    def reset(self):
        """Resets the snake to its initial state."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Handles key presses for snake control."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            # The snake cannot move in the opposite direction.
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Runs the main game loop."""
    # PyGame initialization:
    pygame.init()

    # Create instances of the classes.
    snake = Snake()
    apple = Apple()

    # Clear the screen at start.
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)

        # Handle key presses.
        handle_keys(snake)

        # Update the direction of movement.
        snake.update_direction()

        # Move the snake.
        snake.move()

        # If the snake ate the apple - increase length and move the apple.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        # Check if the snake collided with itself.
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position()
            screen.fill(BOARD_BACKGROUND_COLOR)
            continue

        # Draw the objects.
        snake.draw()
        apple.draw()

        # Update the screen.
        pygame.display.update()


if __name__ == '__main__':
    main()
