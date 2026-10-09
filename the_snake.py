"""Snake game (project 'Bending Python')."""

import sys
from random import randint

import pygame as pg

# Game field and grid sizes:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Start position - center of the screen:
START_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Directions:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Turns dictionary for key handling:
TURNS = {
    pg.K_UP: (UP, DOWN),
    pg.K_DOWN: (DOWN, UP),
    pg.K_LEFT: (LEFT, RIGHT),
    pg.K_RIGHT: (RIGHT, LEFT),
}

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
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Game window caption:
pg.display.set_caption('Snake')

# Time setup:
clock = pg.time.Clock()


class GameObject:
    """Base class for game objects."""

    def __init__(self, position=START_POSITION, body_color=None):
        """Initializes the position and color of a game object."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Draws the object. Overridden in child classes."""
        raise NotImplementedError(
            f'Method draw() is not implemented in {self.__class__.__name__}'
        )

    def draw_cell(self, position):
        """Draws a single cell at the given position."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Apple class that the snake collects."""

    def __init__(
        self,
        occupied_positions,
        position=START_POSITION,
        body_color=APPLE_COLOR,
    ):
        """Creates an apple and assigns it a random position."""
        super().__init__(position=position, body_color=body_color)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """Sets a random position for the apple avoiding occupied cells."""
        while True:
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if new_position not in occupied_positions:
                self.position = new_position
                break

    def draw(self):
        """Draws the apple on the game field."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Snake class controlled by the player."""

    def __init__(self, position=START_POSITION, body_color=SNAKE_COLOR):
        """Creates a snake in its initial state."""
        super().__init__(position=position, body_color=body_color)
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

        # If length didn't increase, remove the tail.
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Draws the snake on the game field."""
        for position in self.positions:
            self.draw_cell(position)

    def get_head_position(self):
        """Returns the position of the snake's head."""
        return self.positions[0]

    def reset(self):
        """Resets the snake to its initial state."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(game_object):
    """Handles key presses for snake control."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key in TURNS:
                new_direction, opposite = TURNS[event.key]
                if game_object.direction != opposite:
                    game_object.next_direction = new_direction


def main():
    """Runs the main game loop."""
    # PyGame initialization:
    pg.init()

    # Create instances of the classes.
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)

        # Clear the screen at the start of each frame.
        screen.fill(BOARD_BACKGROUND_COLOR)

        # Handle key presses.
        handle_keys(snake)

        # Update the direction of movement.
        snake.update_direction()

        # Move the snake.
        snake.move()

        # Check if the snake ate the apple or collided with itself.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            apple.randomize_position(snake.positions)

        # Draw the objects.
        snake.draw()
        apple.draw()

        # Update the screen.
        pg.display.update()


if __name__ == '__main__':
    main()
