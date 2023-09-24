import pygame

class Particle:
    def __init__(self, x, y, color, text, size, lifetime):
        self.x = x
        self.y = y
        self.color = color
        self.text = text
        self.size = size
        self.lifetime = lifetime
        self.age = 0
        self.active = True  # Flag to track if the particle is active

    def update(self):
        if self.active:
            self.age += 1
            if self.age >= self.lifetime:
                self.active = False  # Deactivate the particle when it reaches its lifetime

    def is_dead(self):
        return not self.active  # Check if the particle is no longer active

    def draw(self, screen):
        if self.active:
            alpha = 255 - int(255 * (self.age / self.lifetime))
            font = pygame.font.Font(None, self.size)
            text_surface = font.render(self.text, True, self.color)
            text_surface.set_alpha(alpha)
            screen.blit(text_surface, (self.x, self.y))
