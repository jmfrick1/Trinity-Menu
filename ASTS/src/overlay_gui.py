import pygame
import logging
import numpy as np
from esp import ESP
from targeting_system import Aimbot
from config_manager import ConfigManager

logger = logging.getLogger(__name__)

class OverlayGUI:
    def __init__(self, width, height, process_name):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('ASTS Overlay')
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize systems
        self.config_manager = ConfigManager()
        self.config_manager.load_config()

        self.esp = ESP(process_name)
        self.aimbot = Aimbot()
        self.apply_config()

    def apply_config(self):
        # Apply aimbot settings
        self.aimbot.enabled = self.config_manager.get('aimbot.enabled', False)
        self.aimbot.set_aim_key(self.config_manager.get('aimbot.aim_key', 'VK_XBUTTON1'))
        self.aimbot.set_aim_fov(self.config_manager.get('aimbot.aim_fov', 90))
        self.aimbot.set_smoothness(self.config_manager.get('aimbot.smoothness', 1.0))
        self.aimbot.set_aim_bone(self.config_manager.get('aimbot.aim_bone', 'head'))
        self.aimbot.set_aim_priority(self.config_manager.get('aimbot.aim_priority', 'distance'))
        self.aimbot.set_max_distance(self.config_manager.get('aimbot.max_distance', 1000))
        self.aimbot.triggerbot_enabled = self.config_manager.get('aimbot.triggerbot_enabled', False)
        self.aimbot.rapid_fire_enabled = self.config_manager.get('aimbot.rapid_fire_enabled', False)
        self.aimbot.set_headshot_percentage(self.config_manager.get('aimbot.headshot_percentage', 100))
        self.aimbot.enable_limb_targeting(self.config_manager.get('aimbot.limb_targeting_enabled', False))
        self.aimbot.excluded_groups = self.config_manager.get('aimbot.excluded_groups', [])

        # Apply ESP settings
        self.esp_enabled = self.config_manager.get('esp.enabled', True)
        self.player_color = tuple(self.config_manager.get('esp.player_color', [255, 0, 0]))
        self.item_color = tuple(self.config_manager.get('esp.item_color', [0, 255, 0]))
        self.skeleton_color = tuple(self.config_manager.get('esp.skeleton_color', [255, 255, 0]))

    def draw_text(self, text, position, color=(255, 255, 255), font_size=24):
        font = pygame.font.SysFont(None, font_size)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, position)

    def draw_box(self, rect, color=(255, 0, 0), width=2):
        pygame.draw.rect(self.screen, color, rect, width)

    def draw_circle(self, position, radius, color=(0, 255, 0), width=2):
        pygame.draw.circle(self.screen, color, position, radius, width)

    def draw_line(self, start_pos, end_pos, color=(0, 0, 255), width=2):
        pygame.draw.line(self.screen, color, start_pos, end_pos, width)

    def update(self):
        player_position = np.array([50, 50, 50])  # Placeholder for player position

        if self.esp_enabled:
            # Fetch targets using ESP
            players = self.esp.get_player_positions()
            items = self.esp.get_item_positions()
            
            # Draw ESP information
            for pos in players:
                self.draw_circle(pos[:2], 5, self.player_color, 2)
            for pos in items:
                self.draw_box((pos[0], pos[1], 10, 10), self.item_color, 2)

        # Update aimbot with new targets
        targets = [{'position': pos, 'group': 'enemy'} for pos in players]
        new_aim_position = self.aimbot.update(player_position, targets)
        if new_aim_position is not None:
            self.draw_circle(new_aim_position[:2], 5, (255, 255, 0), 2)  # Visualize the aim position

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.fill((0, 0, 0))  # Clear the screen
            self.update()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

        # Clean up
        self.esp.close()

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    overlay_gui = OverlayGUI(800, 600, "example_process.exe")
    overlay_gui.run()
