# Filename: bullet_prediction.py

import math
import random

def calculate_bullet_trajectory(start_pos, target_pos, bullet_speed, gravity=9.81):
    """
    Calculate the bullet trajectory given the start position, target position, bullet speed, and gravity.
    Returns the angle required to hit the target.
    """
    dx = target_pos[0] - start_pos[0]
    dy = target_pos[1] - start_pos[1]
    dz = target_pos[2] - start_pos[2]

    distance = math.sqrt(dx**2 + dy**2 + dz**2)

    # Calculate the angle using the physics formula for projectile motion
    angle = math.atan2(dz, distance)
    
    return angle

def predict_best_limb(limb_positions, target_limb, bullet_speed, precision_vars, limb_size):
    """
    Predict the best limb to hit based on limb positions, target limb, bullet speed, precision variables, and limb size.
    """
    best_limb = None
    best_score = float('inf')
    
    for limb, position in limb_positions.items():
        if limb == target_limb:
            trajectory = calculate_bullet_trajectory((0, 0, 0), position, bullet_speed)
            score = trajectory + random_jitter((trajectory, trajectory), precision_vars.get('smoothness', 10))[0]
            if score < best_score:
                best_score = score
                best_limb = limb

    return best_limb

def move_to_best_limb(current_pos, best_limb, keypoints, precision_vars, limb_size):
    """
    Move to the best limb position in a human-like manner.
    """
    if best_limb in keypoints:
        target_position = keypoints[best_limb]
        for pos in simulate_human_movement(current_pos, target_position, precision_vars):
            # Simulate moving to the target position
            pass
        return target_position
    return current_pos

def simulate_human_movement(current_pos, target_pos, precision_vars):
    """
    Simulate smooth human-like movement to the target position.
    """
    steps = precision_vars.get('smoothness', 10)
    delta = ((target_pos[0] - current_pos[0]) / steps, 
             (target_pos[1] - current_pos[1]) / steps)
    
    for _ in range(steps):
        current_pos[0] += delta[0]
        current_pos[1] += delta[1]
        if occasional_mistake(precision_vars.get('miss_chance', 0.1)):
            yield current_pos

def random_jitter(position, amount=5):
    """
    Add random jitter to the position to avoid detection.
    """
    jittered_position = (position[0] + random.uniform(-amount, amount),
                         position[1] + random.uniform(-amount, amount))
    return jittered_position

def occasional_mistake(success_rate=0.95):
    """
    Occasionally make a mistake to mimic human behavior.
    """
    return random.random() < success_rate
