import numpy as np

_FIXED_TRESHOLD = 20

class KPTracker:
    def __init__(self, fps, alpha=0.7):
        self.alpha = alpha
        self.x_filtered = 0
        self.y_filtered = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.previous_time = None
        self.dt = 1/fps
        self.position_track = [[0, 0]]
        self.is_moving = True
        self.moving_counter = _FIXED_TRESHOLD

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
        
        self.position_track.append([self.x_filtered ,self.y_filtered])
        if len(self.position_track) > 20:
            self.position_track.pop(0)
        
        pose_variance = self.get_pose_variance()
        if pose_variance > 0.1:
            self.moving_counter +=1 
            if self.moving_counter > _FIXED_TRESHOLD:
                self.moving_counter = _FIXED_TRESHOLD
                self.is_moving = True
        else:
            self.moving_counter -=1 
            if self.moving_counter < 0:
                self.moving_counter = 0
                self.is_moving = False


    def get_position(self):
        return np.round(self.x_filtered, 2), np.round(self.y_filtered,2)

    def get_velocity(self):
        return np.round(self.velocity_x,2), np.round(self.velocity_y, 2)

    def get_pose_variance(self):
        return np.round(np.max(np.var(self.position_track, axis=0)),2)
    
    