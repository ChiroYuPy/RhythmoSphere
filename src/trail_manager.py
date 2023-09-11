import pygame


class TrailManager:
    def __init__(self, trail_duration, trail_size, trail_color):
        self.trails = []  # Liste pour stocker les traînées
        self.trail_duration = trail_duration
        self.trail_size = trail_size
        self.trail_color = trail_color

    def update_position(self, position):
        if self.trails:
            # Obtenir la position précédente de la traînée
            prev_position = self.trails[-1][0]

            # Calculer la distance entre les positions
            distance = ((position[0] - prev_position[0]) ** 2 + (position[1] - prev_position[1]) ** 2) ** 0.5

            # Définir le nombre de points intermédiaires pour lisser le trait
            num_intermediate_points = int(distance / 2)  # Vous pouvez ajuster ce facteur selon vos besoins

            # Interpoler les positions intermédiaires
            for i in range(num_intermediate_points):
                t = (i + 1) / (num_intermediate_points + 1)
                intermediate_x = int(prev_position[0] + t * (position[0] - prev_position[0]))
                intermediate_y = int(prev_position[1] + t * (position[1] - prev_position[1]))
                self.trails.append(((intermediate_x, intermediate_y), self.trail_duration))

        # Ajouter la nouvelle position à la liste
        self.trails.append((position, self.trail_duration))

    def update(self, delta_time):
        new_trails = []  # Liste temporaire pour stocker les traînées actives
        for position, duration in self.trails:
            duration -= delta_time  # Réduire la durée de vie de chaque traînée
            if duration > 0:
                new_trails.append((position, duration))  # Ajouter les traînées actives à la liste temporaire
        self.trails = new_trails  # Remplacer les traînées par les traînées actives

    def draw(self, screen):
        for position, _ in self.trails:
            pygame.draw.circle(screen, self.trail_color, position, self.trail_size)

    def get_trails(self):
        return self.trails  # Renvoie la liste des traînées actives