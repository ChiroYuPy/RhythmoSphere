import pygame
import sys
import math

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
largeur, hauteur = 800, 600

# Création de la fenêtre
fenetre = pygame.display.set_mode((largeur, hauteur))

# Couleur de l'arc (en RVB)
couleur_arc = (0, 0, 255)  # Bleu

# Position du centre du cercle
centre_cercle = (400, 300)

# Rayon du cercle
rayon = 100

# Angle de départ et angle de fin (en radians)
angle_debut = 0  # Angle de départ (0 radians)
angle_fin = math.pi  # Angle de fin (180 degrés en radians)

# Épaisseur de la ligne
epaisseur_ligne = 50

# Boucle principale
en_cours = True
while en_cours:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False

    # Efface l'écran avec une couleur de fond
    fenetre.fill((0, 0, 0))  # Noir

    # Dessine l'arc de cercle sur l'écran
    pygame.draw.arc(fenetre, couleur_arc, (centre_cercle[0] - rayon, centre_cercle[1] - rayon, 2 * rayon, 2 * rayon), angle_debut, angle_fin, epaisseur_ligne)

    # Met à jour l'affichage
    pygame.display.flip()

# Quitte Pygame
pygame.quit()
sys.exit()
