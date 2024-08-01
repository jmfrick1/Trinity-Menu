import unittest
from unittest.mock import patch, MagicMock
from src.menu import Menu

class TestMenu(unittest.TestCase):

    def setUp(self):
        # Setup any necessary resources or initializations
        self.mock_menu = Menu()

    def tearDown(self):
        # Clean up after each test if necessary
        pass

    def test_menu_initialization(self):
        # Test case for menu initialization
        self.assertIsInstance(self.mock_menu, Menu, "Menu should be an instance of the Menu class")
        self.assertEqual(self.mock_menu.current_selection, 0, "Initial selection should be 0")
        self.assertEqual(len(self.mock_menu.items), 0, "Menu items should be empty initially")

    def test_add_item_to_menu(self):
        # Test case for adding items to the menu
        self.mock_menu.add_item("Item 1", MagicMock())
        self.assertEqual(len(self.mock_menu.items), 1, "Menu should have 1 item after adding")
        self.assertEqual(self.mock_menu.items[0][0], "Item 1", "First item should be 'Item 1'")

    def test_menu_navigation(self):
        # Test case for menu navigation
        self.mock_menu.add_item("Item 1", MagicMock())
        self.mock_menu.add_item("Item 2", MagicMock())
        self.mock_menu.navigate_down()
        self.assertEqual(self.mock_menu.current_selection, 1, "Current selection should move down to index 1")
        self.mock_menu.navigate_up()
        self.assertEqual(self.mock_menu.current_selection, 0, "Current selection should move up to index 0")

if __name__ == '__main__':
    unittest.main()
