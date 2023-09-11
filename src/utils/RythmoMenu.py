import pygame
import sys
import math

pygame.init()

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
BLEU = (0, 0, 255)

# Dimensions de la fenêtre
largeur, hauteur = 800, 600
taille_fenetre = (largeur, hauteur)

# Création de la fenêtre
fenetre = pygame.display.set_mode(taille_fenetre)
pygame.display.set_caption("Menu Principal")

# Paramètres du cercle principal
rayon_cercle_principal = 100
position_cercle_principal = [largeur // 2, hauteur // 2]
vitesse_animation = 0.1
temps = 0

# Paramètres des boutons
nombre_boutons = 6
rayon_boutons = rayon_cercle_principal + 40  # Rayon extérieur des boutons
angles_boutons = [i * (2 * math.pi / nombre_boutons) for i in range(nombre_boutons)]
positions_boutons = [(int(position_cercle_principal[0] + rayon_boutons * math.cos(angle)),
                   int(position_cercle_principal[1] + rayon_boutons * math.sin(angle))) for angle in angles_boutons]
bouton_actif = None

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            bouton_actif = None  # Réinitialiser le bouton actif
            for i, (pos_x, pos_y) in enumerate(positions_boutons):
                distance_souris_bouton = ((x - pos_x) ** 2 + (y - pos_y) ** 2) ** 0.5
                if distance_souris_bouton <= rayon_cercle_principal:
                    bouton_actif = i

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for i, (pos_x, pos_y) in enumerate(positions_boutons):
                distance_souris_bouton = ((x - pos_x) ** 2 + (y - pos_y) ** 2) ** 0.5
                if distance_souris_bouton <= rayon_cercle_principal:
                    # Effectuer l'action correspondante au bouton (à personnaliser)
                    print(f"Action du bouton {i + 1} activée.")

    # Mise à jour du temps
    temps += vitesse_animation

    # Utilisation de la fonction sinus pour animer le cercle principal
    facteur_sinus = math.sin(temps)
    agrandissement_cercle_principal = 1 + 0.1 * facteur_sinus

    # Effacer l'écran
    fenetre.fill(BLANC)

    # Dessiner le cercle principal
    pygame.draw.circle(fenetre, BLEU, position_cercle_principal, int(rayon_cercle_principal * agrandissement_cercle_principal))

    # Dessiner les boutons
    for i, (pos_x, pos_y) in enumerate(positions_boutons):
        agrandissement_bouton = 1.1 if bouton_actif == i else 1.0
        pygame.draw.circle(fenetre, NOIR, (pos_x, pos_y), int(rayon_cercle_principal * agrandissement_bouton))

    # Mettre à jour l'affichage
    pygame.display.flip()

    clock.tick(60)  # Limiter les FPS à 60

# Quitter Pygame
pygame.quit()
sys.exit()
