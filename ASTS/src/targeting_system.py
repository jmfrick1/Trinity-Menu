import logging
import numpy as np
import time

logger = logging.getLogger(__name__)

class Aimbot:
    def __init__(self):
        self.enabled = False
        self.aim_key = None
        self.aim_fov = 90
        self.smoothness = 1.0
        self.aim_bone = 'head'
        self.aim_priority = 'distance'
        self.max_distance = 1000
        self.triggerbot_enabled = False
        self.rapid_fire_enabled = False
        self.headshot_percentage = 100
        self.limb_targeting_enabled = False
        self.excluded_groups = []
        self.humanization_enabled = True
        self.last_shot_time = 0

    def toggle_aimbot(self):
        self.enabled = not self.enabled
        logger.info(f"Aimbot {'enabled' if self.enabled else 'disabled'}")

    def set_aim_key(self, key):
        self.aim_key = key
        logger.info(f"Aim key set to {key}")

    def set_aim_fov(self, fov):
        self.aim_fov = fov
        logger.info(f"Aim FOV set to {fov} degrees")

    def set_smoothness(self, smoothness):
        self.smoothness = smoothness
        logger.info(f"Aim smoothness set to {smoothness}")

    def set_aim_bone(self, bone):
        self.aim_bone = bone
        logger.info(f"Aim bone set to {bone}")

    def set_aim_priority(self, priority):
        self.aim_priority = priority
        logger.info(f"Aim priority set to {priority}")

    def set_max_distance(self, distance):
        self.max_distance = distance
        logger.info(f"Max aim distance set to {distance}")

    def toggle_triggerbot(self):
        self.triggerbot_enabled = not self.triggerbot_enabled
        logger.info(f"Triggerbot {'enabled' if self.triggerbot_enabled else 'disabled'}")

    def toggle_rapid_fire(self):
        self.rapid_fire_enabled = not self.rapid_fire_enabled
        logger.info(f"Rapid fire {'enabled' if self.rapid_fire_enabled else 'disabled'}")

    def set_headshot_percentage(self, percentage):
        self.headshot_percentage = percentage
        logger.info(f"Headshot percentage set to {percentage}%")

    def enable_limb_targeting(self, enabled):
        self.limb_targeting_enabled = enabled
        logger.info(f"Limb targeting {'enabled' if self.limb_targeting_enabled else 'disabled'}")

    def exclude_group(self, group):
        self.excluded_groups.append(group)
        logger.info(f"Group {group} excluded from targeting")

    def include_group(self, group):
        if group in self.excluded_groups:
            self.excluded_groups.remove(group)
            logger.info(f"Group {group} included for targeting")

    def aim_at_target(self, player_position, target_position):
        direction = target_position - player_position
        distance = np.linalg.norm(direction)
        if distance == 0:
            return player_position

        direction /= distance
        smooth_direction = player_position + direction * self.smoothness
        return smooth_direction

    def update(self, player_position, targets):
        if not self.enabled:
            return None

        best_target = None
        best_distance = float('inf')
        
        for target in targets:
            target_position = target['position']
            if self._is_valid_target(target, player_position):
                distance = np.linalg.norm(target_position - player_position)
                if distance < best_distance:
                    best_distance = distance
                    best_target = target

        if best_target:
            new_aim_position = self.aim_at_target(player_position, best_target['position'])
            if self.triggerbot_enabled:
                self.triggerbot(new_aim_position)
            return new_aim_position
        return None

    def _is_valid_target(self, target, player_position):
        if target['group'] in self.excluded_groups:
            return False
        distance = np.linalg.norm(target['position'] - player_position)
        if distance > self.max_distance:
            return False
        return True

    def triggerbot(self, aim_position):
        current_time = time.time()
        if current_time - self.last_shot_time > 0.1:  # Simulate firing delay
            logger.info(f"Firing at position {aim_position}")
            self.last_shot_time = current_time

    def rapid_fire(self):
        while self.rapid_fire_enabled:
            self.triggerbot()
            time.sleep(0.05)  # Simulate rapid firing rate

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    aimbot = Aimbot()
    aimbot.toggle_aimbot()
    aimbot.set_aim_key('VK_XBUTTON1')  # Example key, replace with actual key code
    aimbot.set_aim_fov(90)
    aimbot.set_smoothness(1.0)
    aimbot.set_aim_bone('head')
    aimbot.set_aim_priority('distance')
    aimbot.set_max_distance(1000)
    aimbot.toggle_triggerbot()
    aimbot.toggle_rapid_fire()
    aimbot.set_headshot_percentage(100)
    aimbot.enable_limb_targeting(True)
    aimbot.exclude_group('team')

    # Example player and target positions
    player_position = np.array([50, 50, 50])
    targets = [{'position': np.array([100, 50, 50]), 'group': 'enemy'}]

    new_aim_position = aimbot.update(player_position, targets)
    if new_aim_position is not None:
        logger.info(f"New aim position: {new_aim_position}")
