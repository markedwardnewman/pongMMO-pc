import pygame
from game_config import BALL_SPEED_X, BALL_SPEED_Y

class Ball:
    def __init__(self, play_area_rect, hit_sound):
        self.position = pygame.Vector2(play_area_rect.centerx, play_area_rect.centery)
        self.rect = pygame.Rect(self.position.x - 10, self.position.y - 10, 20, 20)  # Assuming the ball is 20x20 px
        self.hit_sound = hit_sound
        self.velocity = pygame.Vector2(BALL_SPEED_X, BALL_SPEED_Y)  # Use configured ball speed
        self.play_area_rect = play_area_rect

    def move(self):
        self.position += self.velocity
        self.rect.x = self.position.x
        self.rect.y = self.position.y

    def check_bounds(self, play_area_rect, player_paddle, ai_paddle):
        # Example collision detection logic
        if self.rect.left <= play_area_rect.left or self.rect.right >= play_area_rect.right:
            self.velocity.x = -self.velocity.x
        if self.rect.top <= play_area_rect.top:
            self.velocity.y = -self.velocity.y
        if self.rect.colliderect(player_paddle.rect) or self.rect.colliderect(ai_paddle.rect):
            self.hit_sound.play()
            self.velocity.y = -self.velocity.y

    def reset(self):
        self.position = pygame.Vector2(self.play_area_rect.centerx, self.play_area_rect.centery)
        self.velocity = pygame.Vector2(BALL_SPEED_X, BALL_SPEED_Y)
        self.rect.topleft = (self.position.x - 10, self.position.y - 10)

    def draw(self, screen):
        pygame.draw.ellipse(screen, (255, 255, 255), self.rect)
