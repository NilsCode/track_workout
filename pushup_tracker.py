import numpy as np

class PushupCounter:
    def __init__(self, threshold):
        self.threshold = threshold
        self.is_up = True
        self.pushup_count = 0
        self.avg_y_position_previous = None
        self.start_top_pos = None
        self.start_bottom_pos = None
        self.pushup_state = "UP"
        self.time_track = []
        self.travel_track = []
        self.pushup_start_time = None
        self.last_pushup_time = None
        self.top_shoulder_position = []
    
    def update(self, left_shoulder, right_shoulder, dt):
        """
        Update the counter based on new shoulder positions.
        
        Args:
        left_shoulder (tuple): (x, y) position of the left shoulder.
        right_shoulder (tuple): (x, y) position of the right shoulder.
        """
        # Calculate the average y-position using the y-coordinates
        avg_y_position = (left_shoulder[0] + right_shoulder[0]) / 2
        
        # Initialize start positions if not set
        if self.start_top_pos is None:
            self.start_top_pos = avg_y_position
            self.start_bottom_pos = avg_y_position
            self.pushup_start_time = 0
            self.last_pushup_time = 0
            self.top_shoulder_position.append(self.start_top_pos)
        
        # Update the top and bottom positions
        self.start_top_pos = min(self.start_top_pos, avg_y_position)
        self.start_bottom_pos = max(self.start_bottom_pos, avg_y_position)
        self.pushup_start_time += dt
        
        # Handle transition from up to down
        if self.is_up and avg_y_position > self.start_top_pos + self.threshold:
            self.is_up = False
            self.pushup_state = "DOWN"
            self.start_bottom_pos = avg_y_position  # Update the bottom position as we move down
            self.top_shoulder_position.append(self.start_top_pos)
                
        # Handle transition from down to up
        elif not self.is_up and avg_y_position < self.start_bottom_pos - self.threshold:
            self.is_up = True
            self.pushup_count += 1
            self.pushup_state = "UP"
            
            cycle_time = self.pushup_start_time - self.last_pushup_time
            self.time_track.append(cycle_time)
            
            travel = self.start_bottom_pos - self.start_top_pos
            self.travel_track.append(travel)
            
            self.last_pushup_time = self.pushup_start_time
            self.start_top_pos = avg_y_position  # Update the top position as we move up
            
        self.avg_y_position_previous = avg_y_position
    
    def get_count(self):
        """
        Returns the current pushup count.
        
        Returns:
        int: The total number of pushups counted.
        """
        return self.pushup_count

    def get_cycle_time(self):
        """
        Return latest cycle time
        
        Returns:
        float: Time for last pushup in seconds
        None: If pushup count is 0
        """
        
        if len(self.time_track):
            return np.round(self.time_track[-1], 2)
        else:
            return None
    
    def get_travel(self):
        """
        Return latest cycle time
        
        Returns:
        float: Time for last pushup in seconds
        None: If pushup count is 0
        """
        
        if len(self.travel_track):
            return np.round(self.travel_track[-1], 2)
        else:
            return None

    def get_top_postion(self):
        return np.round(np.mean(self.top_shoulder_position), 4), np.std(self.top_shoulder_position)