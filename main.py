import pygame
import time
from random import randrange

# TODO:
# BUG - Able to go left when direction is right by pressing up/down key fast before pressing right
# Fix text related variables shadowing

# Global variables
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GREEN = (11, 144, 28)
BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
RED = (221, 47, 8)
GREY = (35, 35, 35)
LIGHT_GREY = (110, 110, 110)
FPS = 30
TILE_SIZE = 10
MOVEMENT_DELAY = 0.16

# Initializing Pygame, game window and the clock
pygame.init()
pygame.display.set_caption("Snake-3000")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Global font variables
EXTRA_LARGE_TEXT = pygame.font.SysFont("Rockwell", 100)
LARGE_TEXT = pygame.font.SysFont("Rockwell", 50)
SMALL_TEXT = pygame.font.SysFont("Rockwell", int(TILE_SIZE * 1.5))


def text_objects(text, font, color):
    """Helper function for displaying text on the screen"""
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def get_random_x_position():
    """This function returns a pseudo-random x position within the allowed range"""
    return randrange(TILE_SIZE, SCREEN_WIDTH - TILE_SIZE*2, TILE_SIZE)


def get_random_y_position():
    """This function returns a pseudo-random y position within the allowed range"""
    return randrange(TILE_SIZE*2, SCREEN_HEIGHT - TILE_SIZE*2, TILE_SIZE)


def start_sequence(number):
    """Helper function for displaying the countdown sequence at the start of the game"""
    text_surf, text_rect = text_objects(number, LARGE_TEXT, RED)
    text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    screen.blit(text_surf, text_rect)
    pygame.draw.rect(text_surf, WHITE, text_rect)
    pygame.display.flip()
    pygame.mixer.Sound.play(arcade_beep)
    pygame.mixer.music.stop()
    time.sleep(1)


def game_over_sequence():
    """Helper function for displaying the game over banner on the screen as well as playing the failure.wav sound"""
    pygame.draw.rect(screen, BLACK, pygame.Rect(SCREEN_WIDTH * 0.2, SCREEN_HEIGHT * 0.2, SCREEN_WIDTH * 0.75,
                                                SCREEN_HEIGHT * 0.75))
    text_surf, text_rect = text_objects("GAME OVER", LARGE_TEXT, RED)
    text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    screen.blit(text_surf, text_rect)
    text_surf, text_rect = text_objects("Your Final Score: " + str(score), SMALL_TEXT, GREEN)
    text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 5 * TILE_SIZE)
    screen.blit(text_surf, text_rect)
    pygame.draw.rect(text_surf, WHITE, text_rect)
    text_surf, text_rect = text_objects("Press any key to exit...", SMALL_TEXT, LIGHT_GREY)
    text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.85)
    screen.blit(text_surf, text_rect)
    pygame.draw.rect(text_surf, WHITE, text_rect)
    pygame.mixer.Sound.play(failure_sound)
    pygame.mixer.music.stop()
    game_over_screen = True
    pygame.display.flip()
    time.sleep(2)

    while game_over_screen:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over_screen = False
            if event.type == pygame.KEYDOWN:
                game_over_screen = False


def draw_border():
    """Helper function for drawing the border of the game board"""
    for x1 in range(0, SCREEN_WIDTH, TILE_SIZE):
        pygame.draw.rect(screen, LIGHT_GREY, (x1, 0, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(screen, BLACK, (x1 + 4, 4, TILE_SIZE - 6, TILE_SIZE - 6))
    for y1 in range(0 + TILE_SIZE, SCREEN_HEIGHT - TILE_SIZE, TILE_SIZE):
        pygame.draw.rect(screen, LIGHT_GREY, (0, y1, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(screen, BLACK, (4, y1 + 4, TILE_SIZE - 6, TILE_SIZE - 6))
    for x2 in range(0, SCREEN_WIDTH, TILE_SIZE):
        pygame.draw.rect(screen, LIGHT_GREY, (x2, SCREEN_HEIGHT - TILE_SIZE, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(screen, BLACK, (x2 + 4, SCREEN_HEIGHT - TILE_SIZE + 4, TILE_SIZE - 6, TILE_SIZE - 6))
    for y2 in range(0 + TILE_SIZE, SCREEN_HEIGHT - TILE_SIZE, TILE_SIZE):
        pygame.draw.rect(screen, LIGHT_GREY, (SCREEN_WIDTH - TILE_SIZE, y2, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - TILE_SIZE + 4, y2 + 4, TILE_SIZE - 6, TILE_SIZE - 6))


class Snake:
    """Class for the player - the main sprite"""
    def __init__(self, length, direction, head_position):
        self.length = length
        self.direction = direction  # 0-left 1-up 2-right 3-down
        self.head = [head_position[0], head_position[1]]
        self.body_parts = []

    def draw(self):
        """This method draws the snake on the screen with its updated size, direction and location on the game board"""
        pygame.draw.rect(screen, GREEN, pygame.Rect(self.head[0], self.head[1], TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(screen, BLACK, pygame.Rect(self.head[0] + 2, self.head[1] + 2, TILE_SIZE - 4, TILE_SIZE - 4))
        pygame.draw.rect(screen, RED, pygame.Rect(self.head[0] + 4, self.head[1] + 4, TILE_SIZE - 8, TILE_SIZE - 8))
        for i in self.body_parts:
            pygame.draw.rect(screen, RED, pygame.Rect(i[0], i[1], TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, GREEN, pygame.Rect(i[0] + 1, i[1] + 1, TILE_SIZE - 2, TILE_SIZE - 2))

    def move(self):
        """This method advances the location of the snake's head and its body parts according to the direction
        by one TILE_SIZE"""
        current_head_position = [self.head[0], self.head[1]]
        if self.direction == 0:
            self.head[0] -= TILE_SIZE
        elif self.direction == 1:
            self.head[1] -= TILE_SIZE
        elif self.direction == 2:
            self.head[0] += TILE_SIZE
        elif self.direction == 3:
            self.head[1] += TILE_SIZE
        new_position = current_head_position
        for i, e in enumerate(reversed(self.body_parts)):
            current_position = e
            self.body_parts[len(self.body_parts) - 1 - i] = new_position
            new_position = current_position

    def detect_collision(self):
        """This method checks whether the snake's head after movement has collided with either the border of the
        screen or with one of its body parts"""
        if (((self.head[0] <= TILE_SIZE) and self.direction == 0) or ((self.head[0] >= (SCREEN_WIDTH - 2 * TILE_SIZE))
            and self.direction == 2) or ((self.head[1] <= TILE_SIZE) and self.direction == 1) or
                ((self.head[1] >= (SCREEN_HEIGHT - 2 * TILE_SIZE)) and self.direction == 3)):
            return True
        for j in self.body_parts:
            if self.head == j:
                return True


# Loading game assets
title_icon = pygame.image.load("assets/Title_Logo.png").convert()
failure_sound = pygame.mixer.Sound("assets/failure.wav")
arcade_beep = pygame.mixer.Sound("assets/arcade-beep.wav")

# Declaring helper variables
running = True
score = 0
food_eaten = False
window_was_closed = False
start_menu = True

# Creating the player instance at a pseudo-random location
player = Snake(1, randrange(0, 3, 1), (get_random_x_position(), get_random_y_position()))

# Creating the food rectangle object in a pseudo-random location
food = pygame.Rect(get_random_x_position(), get_random_y_position(), TILE_SIZE, TILE_SIZE)

# Displaying the start screen (menu) of the game
while start_menu:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            start_menu = False
            window_was_closed = True
        if event.type == pygame.KEYDOWN:
            start_menu = False
    screen.fill(BLACK)

    title_icon_rec = title_icon.get_rect()
    title_icon_rec.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
    screen.blit(title_icon, title_icon_rec)

    text_surf, text_rect = text_objects("Press any key to start!", LARGE_TEXT, WHITE)
    text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    screen.blit(text_surf, text_rect)
    pygame.draw.rect(text_surf, WHITE, text_rect)

    text_surf, text_rect = text_objects("Use the arrow keys on your keyboard to control the snake",
                                        SMALL_TEXT, LIGHT_GREY)
    text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.85)
    screen.blit(text_surf, text_rect)
    pygame.draw.rect(text_surf, WHITE, text_rect)

    text_surf, text_rect = text_objects("Speed is increased every 10 points gained", SMALL_TEXT,
                                        LIGHT_GREY)
    text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.85 + 25)
    screen.blit(text_surf, text_rect)
    pygame.draw.rect(text_surf, WHITE, text_rect)
    pygame.display.flip()

# Initiate game start countdown sequence
if window_was_closed is False:
    screen.fill(BLACK)
    pygame.draw.rect(screen, RED, food)
    player.draw()
    draw_border()
    start_sequence("3")
    screen.fill(BLACK)
    pygame.draw.rect(screen, RED, food)
    player.draw()
    draw_border()
    start_sequence("2")
    screen.fill(BLACK)
    pygame.draw.rect(screen, RED, food)
    player.draw()
    draw_border()
    start_sequence("1")

# The main game loop
while running:
    clock.tick(FPS)
    # Arrow keys presses events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and player.direction != 0:
                player.direction = 2
            elif event.key == pygame.K_LEFT and player.direction != 2:
                player.direction = 0
            elif event.key == pygame.K_UP and player.direction != 3:
                player.direction = 1
            elif event.key == pygame.K_DOWN and player.direction != 1:
                player.direction = 3

    screen.fill(BLACK)
    draw_border()
    text_surf, text_rect = text_objects("Score: " + str(score), EXTRA_LARGE_TEXT, GREY)
    text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    screen.blit(text_surf, text_rect)
    pygame.draw.rect(text_surf, WHITE, text_rect)

    # Collision of the snake's head and the fruit
    if food.x == player.head[0] and food.y == player.head[1]:
        score += 1
        food_eaten = True
        pygame.mixer.Sound.play(arcade_beep)
        pygame.mixer.music.stop()
        player.body_parts.append([food.x, food.y])
        food.x = get_random_x_position()
        food.y = get_random_y_position()
        if player.direction == 0:
            player.head[0] -= TILE_SIZE
        elif player.direction == 1:
            player.head[1] -= TILE_SIZE
        elif player.direction == 2:
            player.head[0] += TILE_SIZE
        elif player.direction == 3:
            player.head[1] += TILE_SIZE
    else:
        player.move()
    pygame.draw.rect(screen, RED, food)
    player.draw()
    pygame.display.flip()
    time.sleep(MOVEMENT_DELAY)
    if player.detect_collision():
        running = False
    # 0.02 seconds will be deducted from MOVEMENT_DELAY every 10 points gained and thus increasing the speed of the game
    if len(player.body_parts) > 0 and MOVEMENT_DELAY > 0.04:
        if len(player.body_parts) % 10 == 0 and food_eaten:
            MOVEMENT_DELAY -= 0.02
            food_eaten = False
# Showing the game of sequence before exiting the game
if window_was_closed is False:
    game_over_sequence()
pygame.quit()
