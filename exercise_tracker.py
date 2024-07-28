import numpy as np
from pushup_tracker import PushupCounter
from kp_tracker import KPTracker

KEYPOINT_DICT = {
    'nose': 0,
    'left_eye': 1,
    'right_eye': 2,
    'left_ear': 3,
    'right_ear': 4,
    'left_shoulder': 5,
    'right_shoulder': 6,
    'left_elbow': 7,
    'right_elbow': 8,
    'left_wrist': 9,
    'right_wrist': 10,
    'left_hip': 11,
    'right_hip': 12,
    'left_knee': 13,
    'right_knee': 14,
    'left_ankle': 15,
    'right_ankle': 16
}

class ExerciseTracker:
    def __init__(self,exercise_type) -> None:
        self.exercise_type = exercise_type
        self.init_flag = False
        self.frame_rate = 10
        self.is_ended = False
        self._is_in_position_counter = 0
        
        if exercise_type == "pushup":
            self.left_shoulder = KPTracker(self.frame_rate)
            self.right_shoulder = KPTracker(self.frame_rate)
            self.left_wrist = KPTracker(self.frame_rate)
            self.right_wrist = KPTracker(self.frame_rate)
            self.left_ankle = KPTracker(self.frame_rate)
            self.right_ankle = KPTracker(self.frame_rate)
            self.pushup_counter = PushupCounter(0.1)

    
    def update(self, keypoints):
        if self.exercise_type == "pushup":
            left_shoulder_points = keypoints[KEYPOINT_DICT['left_shoulder']]
            right_shoulder_points = keypoints[KEYPOINT_DICT['right_shoulder']]
            left_wrist_points = keypoints[KEYPOINT_DICT['left_wrist']]
            right_wrist_points = keypoints[KEYPOINT_DICT['right_wrist']]
            left_ankle_points = keypoints[KEYPOINT_DICT['left_ankle']]
            right_ankle_points = keypoints[KEYPOINT_DICT['right_ankle']]
            
            self.left_shoulder.update(*left_shoulder_points)
            self.right_shoulder.update(*right_shoulder_points)
            self.left_wrist.update(*left_wrist_points)
            self.right_wrist.update(*right_wrist_points)
            self.left_ankle.update(*left_ankle_points)
            self.right_ankle.update(*right_ankle_points)
            
            if not self.init_flag:
                is_wrist_moving = self.left_wrist.is_moving
                if not is_wrist_moving:
                    self.init_flag = True
            else:
                if not self.is_ended:
                    ls_point = self.left_shoulder.get_position()
                    rs_point = self.right_shoulder.get_position()
                    self.pushup_counter.update(ls_point, rs_point, 1/self.frame_rate)
                    if self.left_wrist.is_moving:
                        self.is_ended = True
                    
                    top_mean, top_var = self.pushup_counter.get_top_postion()
                    count = self.pushup_counter.get_count()
                    z_value = (top_mean - ls_point[0])/np.sqrt(top_var)
                    if count > 2:
                        if z_value > 1.0:
                            self.is_ended = True
        
    def is_in_pushup_position(self):
        
        ls_point = self.left_shoulder.get_position()
        rs_point = self.right_shoulder.get_position()
        lw_point = self.left_wrist.get_position()
        rw_point = self.right_wrist.get_position()
        la_point = self.left_ankle.get_position()
        ra_point = self.right_ankle.get_position()
        
        