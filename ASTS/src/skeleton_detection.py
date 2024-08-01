import numpy as np
import cv2
import torch
import torchvision
from torchvision import transforms
from torch import nn
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SkeletonDetectionNet(nn.Module):
    """
    Neural network model for skeleton detection using ResNet18 as the backbone.
    """
    def __init__(self):
        super(SkeletonDetectionNet, self).__init__()
        self.model = torchvision.models.resnet18(pretrained=True)
        self.model.fc = nn.Linear(self.model.fc.in_features, 17 * 2)  # 17 keypoints with (x, y)

    def forward(self, x):
        return self.model(x).view(-1, 17, 2)

def load_model(model_path='path/to/skeleton_model.pth'):
    """
    Loads the pre-trained model for skeleton detection.

    Args:
        model_path (str): Path to the model file.

    Returns:
        SkeletonDetectionNet: The loaded model.
    """
    try:
        model = SkeletonDetectionNet()
        model.load_state_dict(torch.load(model_path))
        model.eval()
        logger.info("Model loaded successfully")
        return model
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise

def preprocess_frame(frame):
    """
    Preprocesses the input frame for the model.

    Args:
        frame (numpy.ndarray): The input frame.

    Returns:
        torch.Tensor: The preprocessed frame tensor.
    """
    try:
        preprocess = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        frame_tensor = preprocess(frame).unsqueeze(0)
        logger.info("Frame preprocessed successfully")
        return frame_tensor
    except Exception as e:
        logger.error(f"Error in frame preprocessing: {e}")
        raise

def detect_skeleton(frame, model):
    """
    Detects skeleton keypoints in the input frame using the model.

    Args:
        frame (numpy.ndarray): The input frame.
        model (SkeletonDetectionNet): The skeleton detection model.

    Returns:
        numpy.ndarray: The detected keypoints.
    """
    try:
        input_tensor = preprocess_frame(frame)
        with torch.no_grad():
            output = model(input_tensor)
        keypoints = output[0].numpy()
        keypoints = (keypoints * [frame.shape[1] / 256, frame.shape[0] / 256]).astype(np.int)
        logger.info("Skeleton detection successful")
        return keypoints
    except Exception as e:
        logger.error(f"Error in skeleton detection: {e}")
        raise

def draw_skeleton(frame, keypoints):
    """
    Draws the detected skeleton on the frame.

    Args:
        frame (numpy.ndarray): The frame to draw on.
        keypoints (numpy.ndarray): The detected keypoints.

    Returns:
        None
    """
    try:
        for x, y in keypoints:
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)  # Draw keypoints in green
        for pair in [(0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (5, 6), (6, 7), (7, 8), (0, 9), (9, 10), (10, 11), (11, 12), (0, 13), (13, 14), (14, 15), (15, 16)]:
            partA = keypoints[pair[0]]
            partB = keypoints[pair[1]]
            cv2.line(frame, tuple(partA), tuple(partB), (255, 0, 0), 2)  # Draw limbs in blue
        logger.info("Skeleton drawn successfully")
    except Exception as e:
        logger.error(f"Error in drawing skeleton: {e}")
        raise

def main():
    """
    Main function to demonstrate skeleton detection and drawing.

    Returns:
        None
    """
    try:
        model = load_model('path/to/skeleton_model.pth')
        
        # Example frame loading (replace with actual frame capture code)
        frame = cv2.imread('path/to/frame.png')
        
        keypoints = detect_skeleton(frame, model)
        draw_skeleton(frame, keypoints)
        
        cv2.imshow('Skeleton Detection', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except Exception as e:
        logger.error(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()
