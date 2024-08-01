import cv2
import numpy as np
import pygame
from openpose import pyopenpose as op
import logging

logger = logging.getLogger(__name__)

class ESP:
    def __init__(self, screen):
        self.screen = screen
        params = dict()
        params["model_folder"] = "models/"
        self.opWrapper = op.WrapperPython()
        self.opWrapper.configure(params)
        self.opWrapper.start()

    def detect_keypoints(self, frame):
        datum = op.Datum()
        datum.cvInputData = frame
        self.opWrapper.emplaceAndPop(op.VectorDatum([datum]))
        return datum.poseKeypoints

    def draw_skeleton(self, keypoints):
        targets = []
        for person in keypoints:
            if person is None:
                continue
            for keypoint in person:
                x, y, confidence = keypoint
                if confidence > 0.1:
                    pygame.draw.circle(self.screen, (255, 0, 0), (int(x), int(y)), 3)
                    targets.append({'position': np.array([x, y, 0]), 'group': 'enemy'})
        return targets

    def draw_loot(self, loot_items):
        for item in loot_items:
            position = item['position']
            if item['type'] == 'money':
                pygame.draw.circle(self.screen, (0, 255, 0), position, 10)  # Green circle for money
            elif item['type'] == 'box':
                pygame.draw.rect(self.screen, (255, 0, 0), (*position, 20, 20))  # Red box
            elif item['type'] == 'crate':
                pygame.draw.rect(self.screen, (0, 0, 255), (*position, 30, 30))  # Blue crate

    def draw_entities(self, entities):
        for entity in entities:
            if entity['type'] == 'enemy':
                color = (255, 0, 0)
            elif entity['type'] == 'bot':
                color = (0, 255, 0)
            else:
                color = (0, 0, 255)
            
            x, y = entity['position']
            pygame.draw.circle(self.screen, color, (int(x), int(y)), 10)

    def draw(self, frame, entities, loot_items):
        keypoints = self.detect_keypoints(frame)
        targets = self.draw_skeleton(keypoints)
        self.draw_entities(entities)
        self.draw_loot(loot_items)
        return targets

    def update(self, frame, entities, loot_items):
        self.screen.fill((0, 0, 0))  # Clear the screen
        targets = self.draw(frame, entities, loot_items)
        pygame.display.flip()
        return targets

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    esp = ESP(screen)

    # Example frame and entities
    frame = np.zeros((800, 600, 3), dtype=np.uint8)
    entities = [{'type': 'enemy', 'position': (400, 300)}]
    loot_items = [{'type': 'money', 'position': (200, 150)}]

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        targets = esp.update(frame, entities, loot_items)
        logger.info(f"Detected targets: {targets}")

    pygame.quit()
