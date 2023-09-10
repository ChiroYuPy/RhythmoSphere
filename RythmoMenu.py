import pygame
import pygame_menu
import json
import os

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
WIDTH, HEIGHT = 800, 600
WINDOW_SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Menu de jeu de musique")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Charger les données de carte depuis le fichier JSON
def load_maps_from_json():
    map_list = []
    with open("config.json", "r") as json_file:
        data = json.load(json_file)
        for map_data in data["maps"]:
            map_list.append(map_data)
    return map_list

maps = load_maps_from_json()

# Créer le menu déroulant scrollable
menu = pygame_menu.Menu("Menu de jeu de musique", WIDTH, HEIGHT, theme=pygame_menu.themes.THEME_DEFAULT)

map_names = [map_data["name"] for map_data in maps]

# Paramètres du menu déroulant personnalisé
dropdown_height = 300  # Hauteur du menu déroulant
item_height = 40       # Hauteur de chaque élément de menu

scroll_value = 0      # Valeur de défilement actuelle
selected_map = None   # Carte sélectionnée

def on_select_map(map_name):
    global selected_map
    selected_map = map_name
    print("Lancer le jeu avec la carte :", selected_map)

def update_dropdown_position():
    for i, map_name in enumerate(map_names):
        item_y = HEIGHT // 2 - dropdown_height // 2 + i * item_height + scroll_value
        item_rect = pygame.Rect(WIDTH // 2 - 100, item_y, 200, item_height)
        if item_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (100, 100, 100), item_rect)
        pygame.draw.rect(screen, BLACK, item_rect, 2)
        item_text = menu.add.button(map_name, on_select_map, map_name, align=pygame_menu.locals.ALIGN_CENTER)
        item_text.set_position(WIDTH // 2, item_y + item_height // 2)

# Ajouter les éléments du menu déroulant personnalisé
menu.add.label("Sélectionnez une carte :")

menu.add.button("Quitter", pygame_menu.events.EXIT)

# Boucle principale
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Molette vers le haut
                scroll_value = max(0, scroll_value - item_height)
            elif event.button == 5:  # Molette vers le bas
                max_scroll = max(0, len(map_names) * item_height - dropdown_height)
                scroll_value = min(max_scroll, scroll_value + item_height)

    # Afficher le menu
    screen.fill(WHITE)
    update_dropdown_position()  # Mettre à jour la position du menu déroulant

    menu.update(pygame.event.get())

    menu.draw(screen)

    pygame.display.flip()

# Quitter Pygame
pygame.quit()
