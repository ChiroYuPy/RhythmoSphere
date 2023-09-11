import sys

import pygame

from src.game import Game
from src.exceptions import InvalidLevelException
from src.settings import *


class MainMenu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((window[0], window[1]))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("assets/font/SCF.ttf", 48)
        self.title_font = pygame.font.Font("assets/font/SCF.ttf", 72)
        self.selected_option = 0
        self.options = ["Play", "Quit"]
        self.bpm = 123.05

    def show(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                    elif event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        if self.options[self.selected_option] == "Play":
                            game = Game()
                            try:
                                game.load_map('data/map.csv')
                                game.run()
                            except InvalidLevelException as e:
                                print(e.args[0])

                        elif self.options[self.selected_option] == "Quit":
                            pygame.quit()
                            sys.exit()

            self.screen.fill(BLACK)
            title_text = self.title_font.render("Rythmo Sphere", True, WHITE)
            title_rect = title_text.get_rect(center=(window[0] // 2, 100))
            self.screen.blit(title_text, title_rect)

            for i, option in enumerate(self.options):
                option_text = self.font.render(option, True, WHITE)
                option_rect = option_text.get_rect(center=(window[0] // 2, 300 + i * 100))

                if i == self.selected_option:
                    pygame.draw.polygon(self.screen, WHITE, [(option_rect.left - 40, option_rect.centery),
                                                             (option_rect.left - 10, option_rect.centery - 20),
                                                             (option_rect.left - 10, option_rect.centery + 20)])

                self.screen.blit(option_text, option_rect)

            pygame.display.flip()
            self.clock.tick(60)

    def set_bpm(self, bpm):
        self.bpm = bpm