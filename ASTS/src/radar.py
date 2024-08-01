# Filename: radar.py

import pygame
import logging

logger = logging.getLogger(__name__)

class Radar:
    def __init__(self, screen, radar_center, radar_size, enemy_color, bot_color, friendly_color):
        self.screen = screen
        self.radar_center = radar_center
        self.radar_size = radar_size
        self.enemy_color = enemy_color
        self.bot_color = bot_color
        self.friendly_color = friendly_color
        self.entities = []

    def update_entities(self, entities):
        """
        Update the list of entities to be displayed on the radar.
        
        Parameters:
        entities (list): List of entities with positions (x, y) and types.
        """
        self.entities = entities

    def draw_radar(self):
        """
        Draw the radar on the screen.
        """
        # Draw radar rectangle
        pygame.draw.rect(self.screen, (0, 255, 0), (*self.radar_center, *self.radar_size), 1)

        # Draw entities on radar
        for entity in self.entities:
            self.draw_entity(entity)

    def draw_entity(self, entity):
        """
        Draw an entity on the radar.
        
        Parameters:
        entity (dict): An entity with 'position' and 'type'.
        """
        pos = entity['position']
        radar_pos = self.convert_to_radar_coords(pos)
        if entity['type'] == 'enemy':
            pygame.draw.circle(self.screen, self.enemy_color, radar_pos, 5)  # Circle for enemies
        elif entity['type'] == 'bot':
            pygame.draw.polygon(self.screen, self.bot_color, [radar_pos, (radar_pos[0] - 5, radar_pos[1] + 10), (radar_pos[0] + 5, radar_pos[1] + 10)])  # Triangle for bots
        elif entity['type'] == 'friend':
            pygame.draw.rect(self.screen, self.friendly_color, (*radar_pos, 10, 10))  # Square for friends

    def convert_to_radar_coords(self, pos):
        """
        Convert game world coordinates to radar coordinates.
        
        Parameters:
        pos (tuple): The (x, y) position in the game world.
        
        Returns:
        tuple: The (x, y) position on the radar.
        """
        # Placeholder for actual conversion logic
        scale = 0.1
        radar_x = self.radar_center[0] + int(pos[0] * scale)
        radar_y = self.radar_center[1] + int(pos[1] * scale)
        return (radar_x, radar_y)

if __name__ == "__main__":
    # Example usage
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    radar = Radar(screen, (50, 50), (200, 200), (255, 0, 0), (0, 255, 0), (0, 0, 255))

    # Sample entities
    entities = [
        {'position': (200, 300), 'type': 'enemy'},
        {'position': (400, 500), 'type': 'bot'},
        {'position': (600, 100), 'type': 'friend'}
    ]

    radar.update_entities(entities)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))  # Clear screen
        radar.draw_radar()
        pygame.display.flip()

    pygame.quit()
