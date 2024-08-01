import json
import logging

logger = logging.getLogger(__name__)

class ConfigManager:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = {}

    def load_config(self):
        try:
            with open(self.config_file, 'r') as file:
                self.config = json.load(file)
                logger.info("Configuration loaded successfully")
        except FileNotFoundError:
            logger.warning("Configuration file not found, loading defaults")
            self.config = self.default_config()
        except json.JSONDecodeError:
            logger.error("Error decoding configuration file, loading defaults")
            self.config = self.default_config()

    def save_config(self):
        try:
            with open(self.config_file, 'w') as file:
                json.dump(self.config, file, indent=4)
                logger.info("Configuration saved successfully")
        except IOError as e:
            logger.error(f"Error saving configuration: {e}")

    def default_config(self):
        return {
            "aimbot": {
                "enabled": False,
                "aim_key": "VK_XBUTTON1",
                "aim_fov": 90,
                "smoothness": 1.0,
                "aim_bone": "head",
                "aim_priority": "distance",
                "max_distance": 1000,
                "triggerbot_enabled": False,
                "rapid_fire_enabled": False,
                "headshot_percentage": 100,
                "limb_targeting_enabled": False,
                "excluded_groups": []
            },
            "esp": {
                "enabled": True,
                "player_color": [255, 0, 0],
                "item_color": [0, 255, 0],
                "skeleton_color": [255, 255, 0]
            }
        }

    def get(self, key, default=None):
        keys = key.split('.')
        value = self.config
        for k in keys:
            value = value.get(k, default)
            if value is None:
                return default
        return value

    def set(self, key, value):
        keys = key.split('.')
        d = self.config
        for k in keys[:-1]:
            d = d.setdefault(k, {})
        d[keys[-1]] = value

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    config_manager = ConfigManager()
    config_manager.load_config()
    aimbot_enabled = config_manager.get('aimbot.enabled')
    config_manager.set('aimbot.enabled', True)
    config_manager.save_config()
    logger.info(f"Aimbot enabled: {aimbot_enabled}")
