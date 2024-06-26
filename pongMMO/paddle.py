import pygame
from game_config import PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED

class PlayerPaddle:
    def __init__(self, play_area_rect):
        """ Initialize the player's paddle within the specified play area.
        
        Args:
            play_area_rect (pygame.Rect): The rectangular area of the play field.
        """
        self.rect = pygame.Rect(play_area_rect.centerx - PADDLE_WIDTH // 2, 
                                play_area_rect.bottom - PADDLE_HEIGHT, 
                                PADDLE_WIDTH, PADDLE_HEIGHT)
        self.play_area_rect = play_area_rect  # Save the play area rect
        self.speed = PADDLE_SPEED

    def move(self, pos):
        """ Update the paddle's horizontal position based on mouse movement.
        
        Args:
            pos (tuple): The (x, y) position of the mouse or calculated position for keyboard input.
        """
        new_centerx = max(self.play_area_rect.left + self.rect.width // 2,
                          min(pos[0], self.play_area_rect.right - self.rect.width // 2))
        self.rect.centerx = new_centerx

    def draw(self, screen):
        """ Draw the paddle on the screen.
        
        Args:
            screen (pygame.Surface): The surface on which to draw the paddle.
        """
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

class AIPaddle:
    def __init__(self, play_area_rect):
        """ Initialize the AI paddle within the specified play area.
        
        Args:
            play_area_rect (pygame.Rect): The rectangular area of the play field.
        """
        self.rect = pygame.Rect(play_area_rect.centerx - PADDLE_WIDTH // 2, 
                                play_area_rect.top, 
                                PADDLE_WIDTH, PADDLE_HEIGHT)
        self.play_area_rect = play_area_rect  # Save the play area rect
        self.speed = PADDLE_SPEED

    def move(self, ball):
        """ Move the paddle based on the ball's position to simulate AI.
        
        Args:
            ball (Ball): The ball object the AI is tracking.
        """
        if ball.position.x < self.rect.centerx:
            self.rect.centerx = max(self.rect.centerx - self.speed, self.play_area_rect.left)
        elif ball.position.x > self.rect.centerx:
            self.rect.centerx = min(self.rect.centerx + self.speed, self.play_area_rect.right)

    def draw(self, screen):
        """ Draw the AI paddle on the screen.
        
        Args:
            screen (pygame.Surface): The surface on which to draw the AI paddle.
        """
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
