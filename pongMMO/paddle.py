import pygame
from game_config import PADDLE_WIDTH, PADDLE_HEIGHT

class PlayerPaddle:
    def __init__(self, play_area_rect):
        self.position = pygame.Vector2(play_area_rect.centerx, play_area_rect.bottom - PADDLE_HEIGHT)
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.play_area_rect = play_area_rect

    def move(self, dx):
        self.position.x += dx
        self.position.x = max(self.play_area_rect.left + self.width / 2, min(self.position.x, self.play_area_rect.right - self.width / 2))

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.position.x - self.width / 2, self.position.y - self.height / 2, self.width, self.height))

class AIPaddle:
    def __init__(self, play_area_rect):
        self.position = pygame.Vector2(play_area_rect.centerx, play_area_rect.top + PADDLE_HEIGHT)
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.speed = 5
        self.play_area_rect = play_area_rect

    def move(self, ball):
        if ball.position.x > self.position.x:
            self.position.x += self.speed
        elif ball.position.x < self.position.x:
            self.position.x -= self.speed

        self.position.x = max(self.play_area_rect.left + self.width / 2, min(self.position.x, self.play_area_rect.right - self.width / 2))

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.position.x - self.width / 2, self.position.y - self.height / 2, self.width, self.height))