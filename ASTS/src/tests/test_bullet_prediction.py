import unittest
from src.bullet_prediction import predict_bullet_path

class TestBulletPrediction(unittest.TestCase):

    def test_predict_bullet_path(self):
        # Mock input values for testing
        initial_position = (0, 0)
        initial_velocity = (10, 5)
        time = 2
        
        # Call the function and get the predicted position
        predicted_position = predict_bullet_path(initial_position, initial_velocity, time)
        
        # Assuming the function returns a tuple (x, y) of predicted position
        self.assertEqual(predicted_position, (20, 10))

if __name__ == '__main__':
    unittest.main()
