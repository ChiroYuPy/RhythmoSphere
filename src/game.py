import csv
import random
import sys
import time
from src.particle import Particle
import pygame

from src import CircleManager, TrailManager
from src.exceptions import InvalidLevelException
from src.settings import *
from src.utils.CreateRythmo import play_map_music


class Game:
    def __init__(self, beatmap_name):
        self.beatmap_name = beatmap_name
        self.map_duration = 0
        self.current_time = 0
        self.progress_bar_color = (0, 255, 0)
        self.fps = 1000
        self.is_paused = None
        self.clock = pygame.time.Clock()
        self.load_assets()
        self.init_display()
        self.init_game_data()
        self.circle_manager = CircleManager()
        self.trail_manager = TrailManager(trail_duration, trail_size, trail_color)

    def calculate_accuracy(self):
        total_notes = self.score_300 + self.score_100 + self.score_50 + self.missed_circles
        if total_notes != 0:
            accuracy = ((self.score_300 * 1) + (self.score_100 * (1 / 3)) + (self.score_50 * (1 / 6))) / total_notes
            return accuracy * 100
        return 0

    def load_assets(self):
        self.cursor_image = pygame.image.load(cursor_image)
        self.circle_image = pygame.image.load(circle_image)
        self.aproach_circle_image = pygame.image.load(aproach_circle_image)
        pygame.mouse.set_visible(False)

    def init_display(self):
        self.screen = pygame.display.set_mode((window[0], window[1]))
        pygame.display.set_caption(window_name)

    def init_game_data(self):
        self.tempo_bpm = 123.05
        self.tempo_multiplicator = self.tempo_bpm / 60
        self.circle_data = []
        self.score_50 = 0
        self.score_100 = 0
        self.score_300 = 0
        self.approach_circle = None
        self.running = True
        self.current_circle_index = 0
        self.missed_circles = 0
        self.clicked_circles = 0
        self.score = 0
        self.combo = 1
        self.map_start_time = time.time()
        self.font = pygame.font.Font("assets/fonts/SCF.ttf", 36)
        self.mouse_prev_state = False
        self.clicked = False
        self.precision_duration = 4
        self.active_precisions = []

    def load_map(self, filename):
        try:
            with open(filename, 'r') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if len(row) == 3:
                        time, circle_x, circle_y = map(float, row)
                        self.circle_data.append([time, circle_x, circle_y, False])
                        if time > self.map_duration:
                            self.map_duration = time + 2
        except FileNotFoundError:
            raise InvalidLevelException("File not found")

    def BeatMapRun(self):
        pygame.init()
        pygame.mixer.init()
        play_map_music(self.beatmap_name, pygame)
        while self.running:
            self.handle_events()
            if not self.is_paused:
                self.update()
            self.fps = self.clock.get_fps()
            self.clock.tick(1000)

            self.render()

            pygame.time.delay(10)

        pygame.quit()
        sys.exit()

    def handle_events(self):
        if not self.is_paused:  # Vérifiez si le jeu n'est pas en pause
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.toggle_pause()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.clicked = False  # Désactivez les clics de souris lorsque le jeu est en pause
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.toggle_pause()

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def update(self):
        map_current_time = (time.time() - self.map_start_time) * self.tempo_multiplicator
        self.current_time = map_current_time

        self.check_circles(map_current_time)
        self.update_precision()
        self.trail_manager.update(1 / FPS)  # Met à jour les traînées avec le temps écoulé depuis la dernière frame

    def check_circles(self, map_current_time):
        for i in range(len(self.circle_data) - 1, self.current_circle_index - 1, -1):
            circle = self.circle_data[i]
            if map_current_time >= circle[0] and not circle[3] and not self.clicked:
                circle_image_resized = pygame.transform.scale(self.circle_image, (2 * CIRCLE_RADIUS, 2 * CIRCLE_RADIUS))
                self.screen.blit(circle_image_resized, (int(circle[1]) - CIRCLE_RADIUS, int(circle[2]) - CIRCLE_RADIUS))
                if pygame.mouse.get_pressed()[0] and not self.mouse_prev_state:
                    self.handle_circle_click(circle, map_current_time)
                if map_current_time - circle[0] >= 2:
                    self.handle_missed_circle(circle)

    def handle_circle_click(self, circle, map_current_time):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        distance = ((mouse_x - circle[1]) ** 2 + (mouse_y - circle[2]) ** 2) ** 0.5
        if distance < CIRCLE_RADIUS:
            precision = abs(circle[0] - map_current_time)
            self.handle_precision(precision)
            circle[3] = True
            if 1.7 < precision < 2.3:
                self.score_300 += 1
                self.score += 300 * self.combo
                self.combo += 1
                self.approach_circle = None
            elif 1.4 < precision < 2.6:
                self.score_100 += 1
                self.score += 100 * self.combo
                self.combo += 1
                self.approach_circle = None
            elif 1 < precision < 3:
                self.score_50 += 1
                self.score += 50 * self.combo
                self.combo += 1
                self.approach_circle = None

    def handle_missed_circle(self, circle):
        circle[3] = True
        self.missed_circles += 1
        self.combo = 1

    def handle_precision(self, precision):
        precision_x = bar_x + bar_width * (precision / self.precision_duration)
        self.active_precisions.append((precision_x, time.time()))

    def update_precision(self):
        current_time = time.time()
        self.active_precisions = [(x, timestamp) for x, timestamp in self.active_precisions if
                                  current_time - timestamp <= self.precision_duration]

    def render(self):
        self.screen.fill(BLACK)

        self.render_circles()
        self.render_precision()
        self.render_score()

        progress_width = int((self.current_time / self.map_duration) * window[0])
        pygame.draw.rect(self.screen, self.progress_bar_color, (0, 0, progress_width, 10))

        fps_text = self.font24.render(f"FPS: {int(self.fps)}", True, WHITE)
        self.screen.blit(fps_text, (10, 10))

        self.mouse_prev_state = pygame.mouse.get_pressed()[0]

        # Afficher les traînées derrière le curseur
        for position, duration in self.trail_manager.get_trails():
            pygame.draw.circle(self.screen, trail_color, position,
                               int(duration * 8))  # Utilisez la durée de vie pour déterminer la taille

        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.screen.blit(self.cursor_image, (mouse_x - self.cursor_image.get_width() / 2,
                                             mouse_y - self.cursor_image.get_height() / 2))

        # Afficher le chemin du curseur
        self.trail_manager.update_position((mouse_x, mouse_y))
        self.trail_manager.draw(self.screen)

        pygame.display.flip()

        self.mouse_prev_state = pygame.mouse.get_pressed()[0]

    def render_circles(self):
        map_current_time = (time.time() - self.map_start_time) * self.tempo_multiplicator
        for circle in self.circle_data:
            if map_current_time >= circle[0] and not circle[3]:
                # Dessin du premier cercle normal
                circle_image_resized = pygame.transform.scale(self.circle_image, (2 * CIRCLE_RADIUS, 2 * CIRCLE_RADIUS))
                self.screen.blit(circle_image_resized, (int(circle[1]) - CIRCLE_RADIUS, int(circle[2]) - CIRCLE_RADIUS))

                circle_radius = 4 * CIRCLE_RADIUS
                circle_image_double = pygame.transform.scale(self.circle_image, (circle_radius, circle_radius))
                circle_rect = circle_image_double.get_rect()
                circle_rect.center = (int(circle[1]), int(circle[2]))

                # Dessin progressif du deuxième cercle
                time_elapsed = map_current_time - circle[0]
                if time_elapsed < 2:
                    # Calculez la taille intermédiaire
                    intermediate_radius = int(circle_radius - (circle_radius - 2 * CIRCLE_RADIUS) * (time_elapsed / 2))
                    intermediate_image = pygame.transform.scale(self.aproach_circle_image,
                                                                (intermediate_radius, intermediate_radius))
                    intermediate_rect = intermediate_image.get_rect()
                    intermediate_rect.center = (int(circle[1]), int(circle[2]))
                    self.screen.blit(intermediate_image, intermediate_rect)
                else:
                    # Dessinez le cercle à sa taille normale une fois le temps écoulé
                    self.screen.blit(circle_image_double, circle_rect)

                font = pygame.font.Font("assets/fonts/sixty.ttf", 36)
                text = font.render("1", True, WHITE)
                text_rect = text.get_rect()
                text_rect.center = circle_rect.center
                self.screen.blit(text, text_rect)

    def render_precision(self):
        current_time = time.time()
        pygame.draw.rect(self.screen, ORANGE, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(self.screen, GREEN, (bar_x + bar_width * 0.2, bar_y, bar_width * 0.6, bar_height))
        pygame.draw.rect(self.screen, BLUE, (bar_x + bar_width * 0.4, bar_y, bar_width * 0.2, bar_height))
        pygame.draw.rect(self.screen, WHITE, (bar_x + bar_width * 0.5 - 1, bar_y - 12, 2, bar_height + 24))
        for precision_x, timestamp in self.active_precisions:
            remaining_time = current_time - timestamp
            if remaining_time < self.precision_duration:
                opacity = int(255 * (1 - remaining_time / self.precision_duration))
                color = (255, 255, 255, opacity)
                precision_surface = pygame.Surface((4, bar_height + 20), pygame.SRCALPHA)
                pygame.draw.rect(precision_surface, color, (0, 0, 2, bar_height + 20))
                self.screen.blit(precision_surface, (precision_x, bar_y - 10))

    def render_score(self):
        pygame.draw.rect(self.screen, (16, 16, 16), pygame.Rect(stats_x, stats_y, 200, 90), 0, 10)

        pygame.draw.rect(self.screen, GREEN, pygame.Rect(stats_x + 16, stats_y + 76, 30, 10), 0, 10)
        pygame.draw.rect(self.screen, BLUE, pygame.Rect(stats_x + 72, stats_y + 76, 30, 10), 0, 10)
        pygame.draw.rect(self.screen, RED, pygame.Rect(stats_x + 128, stats_y + 76, 30, 10), 0, 10)

        self.font24 = pygame.font.Font("assets/fonts/SCF.ttf", 24)
        self.font48 = pygame.font.Font("assets/fonts/SCF.ttf", 48)
        self.font72 = pygame.font.Font("assets/fonts/SCF.ttf", 72)

        three_hundred_score_text = self.font24.render(f"{self.score_300}", True, WHITE)
        hundred_score_text = self.font24.render(f"{self.score_100}", True, WHITE)
        fifty_score_text = self.font24.render(f"{self.score_50}", True, WHITE)
        miss_score_text = self.font24.render(f"{self.missed_circles}", True, WHITE)
        combo_text = self.font72.render(f"X{self.combo}", True, WHITE)
        total_score_text = self.font48.render(str(self.score).zfill(8), True, WHITE)

        accuracy = self.calculate_accuracy()
        accuracy_text = self.font48.render(f"{accuracy:.2f}%", True, WHITE)
        self.screen.blit(accuracy_text, ((window[0] - accuracy_text.get_width()) // 2, 12))

        self.screen.blit(hundred_score_text, (stats_x + 20, stats_y + 30))
        self.screen.blit(three_hundred_score_text, (stats_x + 300, stats_y + 30))
        self.screen.blit(fifty_score_text, (stats_x + 76, stats_y + 30))
        self.screen.blit(miss_score_text, (stats_x + 132, stats_y + 30))
        self.screen.blit(combo_text, (window[0] * 0.9, window[1] * 0.86))
        self.screen.blit(total_score_text, (window[0] * 0.8, 10))