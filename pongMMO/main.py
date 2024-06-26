import pygame
import sys
from ball import Ball
from paddle import PlayerPaddle, AIPaddle
from game_config import SCREEN_WIDTH, SCREEN_HEIGHT, PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT
import pyttsx3
import random
import os
from chat_init import get_openai_client
from chat_history import load_history, save_history

# Initialize OpenAI client
openai = get_openai_client()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

class PongGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pong MMO")

        self.play_area_rect = pygame.Rect(
            (SCREEN_WIDTH - PLAY_AREA_WIDTH) / 2,
            (SCREEN_HEIGHT - PLAY_AREA_HEIGHT) / 2,
            PLAY_AREA_WIDTH,
            PLAY_AREA_HEIGHT
        )

        # Load sound effect
        self.hit_sound = pygame.mixer.Sound('sounds/hit_sound.wav')
        
        self.ball = Ball(self.play_area_rect, self.hit_sound)
        self.player_paddle = PlayerPaddle(self.play_area_rect)
        self.ai_paddle = AIPaddle(self.play_area_rect)

        self.score = 0  # Start score at 0
        self.misses = 0
        self.max_misses = 3
        self.conversation_history = load_history()
        self.game_over = False

        # Generate and speak welcome message
        self.welcome_message = self.generate_welcome_message()
        self.speak(self.welcome_message)

    def generate_welcome_message(self):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Welcome to PongMMO'"},
            ],
            max_tokens=10
        )
        return response['choices'][0]['message']['content'].strip()

    def save_history(self):
        save_history(self.conversation_history)

    def draw_play_area(self):
        pygame.draw.rect(self.screen, (0, 0, 255), self.play_area_rect)

    def speak(self, message):
        engine.say(message)
        engine.runAndWait()

    def reset_game(self):
        self.ball = Ball(self.play_area_rect, self.hit_sound)
        self.player_paddle = PlayerPaddle(self.play_area_rect)
        self.ai_paddle = AIPaddle(self.play_area_rect)
        self.score = 0  # Reset score to 0
        self.misses = 0
        self.game_over = False

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        misses_text = font.render(f'Misses: {self.misses}', True, (255, 255, 255))
        self.screen.blit(score_text, (20, 20))
        self.screen.blit(misses_text, (20, 60))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_history()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    self.player_paddle.move(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player_paddle.move((self.player_paddle.rect.centerx - self.player_paddle.speed, 0))
                    elif event.key == pygame.K_RIGHT:
                        self.player_paddle.move((self.player_paddle.rect.centerx + self.player_paddle.speed, 0))
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_over:
                        if self.play_again_button.collidepoint(event.pos):
                            self.reset_game()
                        elif self.exit_game_button.collidepoint(event.pos):
                            self.save_history()
                            pygame.quit()
                            sys.exit()

            if not self.game_over:
                self.ai_paddle.move(self.ball)  # AI paddle follows the ball

                self.screen.fill((139, 69, 19))  # Brown background
                self.draw_play_area()
                self.ball.move()
                self.ball.check_bounds(self.play_area_rect, self.player_paddle, self.ai_paddle)
                self.player_paddle.draw(self.screen)
                self.ai_paddle.draw(self.screen)
                self.ball.draw(self.screen)
                self.draw_score()

                self.check_game_over()

            if self.game_over:
                self.display_game_over()

            pygame.display.flip()

    def check_game_over(self):
        if self.ball.position.y > self.play_area_rect.bottom:
            self.misses += 1
            if self.misses >= self.max_misses:
                self.game_over = True
                self.speak(random.choice(["Ha ha! You lost!", "Better luck next time!", "I win!"]))
            else:
                self.ball.reset()
        elif self.ball.position.y < self.play_area_rect.top:
            self.score += 1
            self.ball.reset()

        if self.misses >= self.max_misses:
            self.game_over = True
            self.speak(random.choice(["Ha ha! You lost!", "Better luck next time!", "I win!"]))

    def display_game_over(self):
        font = pygame.font.Font(None, 74)
        game_over_text = font.render('Game Over', True, (255, 0, 0))
        self.screen.blit(game_over_text, ((SCREEN_WIDTH / 2) - (game_over_text.get_width() / 2), (SCREEN_HEIGHT / 2) - 100))

        button_font = pygame.font.Font(None, 36)
        play_again_text = button_font.render('Play Again', True, (0, 255, 0))
        exit_game_text = button_font.render('Exit Game', True, (0, 255, 0))

        self.play_again_button = pygame.Rect((SCREEN_WIDTH / 2) - 100, (SCREEN_HEIGHT / 2), 200, 50)
        self.exit_game_button = pygame.Rect((SCREEN_WIDTH / 2) - 100, (SCREEN_HEIGHT / 2) + 60, 200, 50)

        pygame.draw.rect(self.screen, (0, 0, 0), self.play_again_button)
        pygame.draw.rect(self.screen, (0, 0, 0), self.exit_game_button)

        self.screen.blit(play_again_text, (self.play_again_button.x + 50, self.play_again_button.y + 10))
        self.screen.blit(exit_game_text, (self.exit_game_button.x + 60, self.exit_game_button.y + 10))

if __name__ == "__main__":
    game = PongGame()
    game.run()
