import numpy as np

class WristTracker:
    def __init__(self, fps, alpha=0.5):
        self.alpha = alpha
        self.x_filtered = None
        self.y_filtered = None
        self.velocity_x = 0
        self.velocity_y = 0
        self.previous_time = None
        self.dt = 1/fps

    def update(self, x, y, score):
        # Initialize filtered positions if they haven't been already
        if self.x_filtered is None or self.y_filtered is None:
            self.x_filtered, self.y_filtered = x, y

        # Apply alpha filter for smoothing
        self.x_filtered = self.alpha * x + (1 - self.alpha) * self.x_filtered
        self.y_filtered = self.alpha * y + (1 - self.alpha) * self.y_filtered

        # Calculate velocity if time is provided
        self.velocity_x = (x - self.x_filtered) / self.dt
        self.velocity_y = (y - self.y_filtered) / self.dt

    def get_position(self):
        return np.round(self.x_filtered, 2), np.round(self.y_filtered,2)

    def get_velocity(self):
        return np.round(self.velocity_x,2), np.round(self.velocity_y, 2)
