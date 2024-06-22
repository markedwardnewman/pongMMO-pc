# main.py
import os
import sys
import pygame
import pyttsx3
from ball import Ball
from paddle import PlayerPaddle, AIPaddle
from game_config import SCREEN_WIDTH, SCREEN_HEIGHT, PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT

class PongGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()  # Initialize the sound mixer
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Pong MMO')
        self.clock = pygame.time.Clock()
        
        # Initialize the text-to-speech engine
        self.engine = pyttsx3.init()
        
        # Load sound effects
        self.hit_sound = pygame.mixer.Sound(os.path.join('sounds', 'hit_sound.wav'))
        self.score_sound = pygame.mixer.Sound(os.path.join('sounds', 'score_sound.wav'))

        # Calculate the play area rectangle
        self.play_area_rect = pygame.Rect(
            (SCREEN_WIDTH - PLAY_AREA_WIDTH) / 2,
            (SCREEN_HEIGHT - PLAY_AREA_HEIGHT) / 2,
            PLAY_AREA_WIDTH,
            PLAY_AREA_HEIGHT
        )

        self.ball = Ball(self.play_area_rect, self.hit_sound)
        self.player_paddle = PlayerPaddle(self.play_area_rect)
        self.ai_paddle = AIPaddle(self.play_area_rect)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.Font(None, 74)
        self.game_over = False

    def draw_play_area(self):
        pygame.draw.rect(self.screen, (0, 0, 255), self.play_area_rect)
        
    def draw_scores(self):
        player_text = self.font.render(str(self.player_score), True, (255, 255, 255))
        ai_text = self.font.render(str(self.ai_score), True, (255, 255, 255))
        self.screen.blit(player_text, (self.play_area_rect.left + 20, 10))
        self.screen.blit(ai_text, (self.play_area_rect.right - 40, 10))
        
    def check_game_over(self):
        if self.player_score >= 3 or self.ai_score >= 3:
            self.game_over = True
            self.say_good_game()

    def say_good_game(self):
        self.engine.say("Good game")
        self.engine.runAndWait()

    def draw_game_over(self):
        if self.game_over:
            over_text = self.font.render("Game Over", True, (255, 0, 0))
            self.screen.blit(over_text, (self.screen.get_width() / 2 - 100, self.screen.get_height() / 2 - 50))
            pygame.display.flip()
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKQUOTE:  # Check for the tilde key
                        pygame.quit()
                        sys.exit()

            if not self.game_over:
                self.screen.fill((139, 69, 19))  # Brown background

                self.draw_play_area()  # Draw the blue play area

                self.ball.move()
                if self.ball.position.y + self.ball.radius >= self.play_area_rect.bottom:
                    self.ai_score += 1
                    self.score_sound.play()
                    self.ball.reset_position()
                elif self.ball.position.y - self.ball.radius <= self.play_area_rect.top:
                    self.player_score += 1
                    self.score_sound.play()
                    self.ball.reset_position()
                
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
                self.draw_scores()
                self.check_game_over()
            else:
                self.draw_game_over()

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == '__main__':
    game = PongGame()
    game.run()
