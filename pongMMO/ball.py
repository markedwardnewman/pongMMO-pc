# ball.py
import pygame
from game_config import BALL_RADIUS, BALL_SPEED

class Ball:
    def __init__(self, play_area_rect, hit_sound):
        self.position = pygame.Vector2(play_area_rect.centerx, play_area_rect.centery)
        self.velocity = pygame.Vector2(BALL_SPEED, BALL_SPEED)
        self.radius = BALL_RADIUS
        self.play_area_rect = play_area_rect
        self.hit_sound = hit_sound

    def move(self):
        self.position += self.velocity

    def check_bounds(self, player_paddle, ai_paddle):
        # Check collision with play area boundaries
        if self.position.x - self.radius <= self.play_area_rect.left or self.position.x + self.radius >= self.play_area_rect.right:
            self.velocity.x = -self.velocity.x
            self.hit_sound.play()
        if self.position.y - self.radius <= self.play_area_rect.top:
            self.velocity.y = -self.velocity.y
            self.hit_sound.play()
        
        # Check collision with player paddle
        if (player_paddle.position.y - player_paddle.height / 2 <= self.position.y + self.radius <= player_paddle.position.y + player_paddle.height / 2 and
            player_paddle.position.x - player_paddle.width / 2 <= self.position.x <= player_paddle.position.x + player_paddle.width / 2):
            self.velocity.y = -self.velocity.y
            self.hit_sound.play()

        # Check collision with AI paddle
        if (ai_paddle.position.y - ai_paddle.height / 2 <= self.position.y - self.radius <= ai_paddle.position.y + ai_paddle.height / 2 and
            ai_paddle.position.x - ai_paddle.width / 2 <= self.position.x <= ai_paddle.position.x + ai_paddle.width / 2):
            self.velocity.y = -self.velocity.y
            self.hit_sound.play()

    def reset_position(self):
        self.position = pygame.Vector2(self.play_area_rect.centerx, self.play_area_rect.centery)
        self.velocity = pygame.Vector2(BALL_SPEED, BALL_SPEED)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), self.radius)
