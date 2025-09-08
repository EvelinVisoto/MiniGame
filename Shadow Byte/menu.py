from pygame import Rect

class MenuButton:
    def __init__(self, label, position, action):
        self.label = label
        self.rect = Rect(position, (200, 50))
        self.action = action

    def draw(self, screen):
        screen.draw.filled_rect(self.rect, "white")
        screen.draw.text(self.label, center=self.rect.center, fontsize=30, color="black")

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.action()

def create_menu(start_action, toggle_sound_action, exit_action):
    return [
        MenuButton("Start Game", (300, 150), start_action),
        MenuButton("Toggle Sound", (300, 220), toggle_sound_action),
        MenuButton("Exit", (300, 290), exit_action),
    ]
