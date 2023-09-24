window = [1280, 720]
window_name = "Affichage des cercles"
FPS = 15

circle_image = "assets/images/circles/circle.png"
aproach_circle_image = "assets/images/circles/approach_circle.png"
cursor_image = "assets/images/cursors/cursor.png"

bar_width = 420
bar_height = 16
bar_x = (window[0] - bar_width) // 2
bar_y = window[1] - 40

stats_x = 10
stats_y = window[1] - 100

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (127, 127, 127)

CIRCLE_RADIUS = 42

trail_duration = 2
trail_size = 1
trail_color = ORANGE


class GameSettings:
    def __init__(self):
        self.window = [1280, 720]
        self.window_name = "Affichage des cercles"
        self.FPS = 15

        self.circle_image = "assets/textures/circles/circle.png"
        self.aproach_circle_image = "assets/textures/circles/approach_circle.png"
        self.cursor_image = "assets/textures/cursor/cursor.png"
        self.pause_menu_image = "assets/textures/ui/pause_menu.png"

        self.bar_width = 420
        self.bar_height = 16
        self.bar_x = (self.window[0] - self.bar_width) // 2
        self.bar_y = self.window[1] - 40

        self.stats_x = 10
        self.stats_y = self.window[1] - 100

        self.CIRCLE_RADIUS = 42

        self.trail_duration = 2
        self.trail_size = 1
        self.trail_color = ORANGE
