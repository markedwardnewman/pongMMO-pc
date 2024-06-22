import pygame
import sys
from ball import Ball
from paddle import PlayerPaddle, AIPaddle
from game_config import SCREEN_WIDTH, SCREEN_HEIGHT, PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT

class PongGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Pong MMO')
        self.clock = pygame.time.Clock()

        # Calculate the play area rectangle
        self.play_area_rect = pygame.Rect(
            (SCREEN_WIDTH - PLAY_AREA_WIDTH) / 2,
            (SCREEN_HEIGHT - PLAY_AREA_HEIGHT) / 2,
            PLAY_AREA_WIDTH,
            PLAY_AREA_HEIGHT
        )

        self.ball = Ball(self.play_area_rect)
        self.player_paddle = PlayerPaddle(self.play_area_rect)
        self.ai_paddle = AIPaddle(self.play_area_rect)

    def draw_play_area(self):
        # Draw the blue play area
        pygame.draw.rect(self.screen, (0, 0, 255), self.play_area_rect)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((139, 69, 19))  # Brown background

            self.draw_play_area()  # Draw the blue play area

            self.ball.move()
            self.ball.check_bounds(self.player_paddle, self.ai_paddle)
            self.ai_paddle.move(self.ball)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player_paddle.move(-5)
            if keys[pygame.K_RIGHT]:
                self.player_paddle.move(5)

            self.ball.draw(self.screen)
            self.player_paddle.draw(self.screen)
            self.ai_paddle.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == '__main__':
    game = PongGame()
    game.run()