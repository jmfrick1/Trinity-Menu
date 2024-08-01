import unittest
from src.bullseye import pick_color

class TestColorPicker(unittest.TestCase):

    def test_pick_color(self):
        # Mock input values for testing
        image_path = "test_image.jpg"
        x, y = 100, 200
        
        # Call the function and get the picked color
        picked_color = pick_color(image_path, x, y)
        
        # Assuming the function returns a tuple (r, g, b) of picked color
        self.assertEqual(picked_color, (255, 0, 0))  # Example assertion

if __name__ == '__main__':
    unittest.main()
