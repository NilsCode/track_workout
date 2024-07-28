import cv2
import numpy as np
import time

from stats_overlay import StatsOverlay
from pushup_tracker import PushupCounter
from kp_tracker import KPTracker

from exercise_tracker import ExerciseTracker

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

def plot_points(frame, current_keypoints):
    for y, x, score in current_keypoints:
        if score > 0.2:
            x, y = int(x * frame.shape[1]), int(y * frame.shape[0])
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)


# Load the video file.
cap = cv2.VideoCapture('vids/vid.mp4')
keypoints = np.load('keypoints.npy')
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640, 480))

num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
image_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
image_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_rate = cap.get(cv2.CAP_PROP_FPS)

left_shoulder = KPTracker(frame_rate)
right_shoulder = KPTracker(frame_rate)
left_wrist = KPTracker(frame_rate)
pushup_tracker = ExerciseTracker("pushup")
overlay = StatsOverlay()
pushup_counter = PushupCounter(0.1)


print(keypoints.shape)
print("Total frames: ", num_frames)
print("Frame rate: ", frame_rate)

for frame_idx in range(num_frames):
    time.sleep(1/frame_rate)
    
    ret, frame = cap.read()
    if not ret:
        break  # Break out of the loop if there are no frames left to read.
    if frame_idx % 3 != 0:
        continue
    frame_resized = cv2.resize(frame, (640, 480))
    current_keypoints = keypoints[frame_idx, 0, 0, :, :]
    
    left_shoulder_points = current_keypoints[KEYPOINT_DICT['left_shoulder']]
    right_shoulder_points = current_keypoints[KEYPOINT_DICT['right_shoulder']]
    left_wrist_points = current_keypoints[KEYPOINT_DICT['left_wrist']]
    left_shoulder.update(*left_shoulder_points)
    right_shoulder.update(*right_shoulder_points)
    left_wrist.update(*left_wrist_points)
    
    
    pushup_counter.update(left_shoulder.get_position(),right_shoulder.get_position() , 1/frame_rate)
    
    pushup_tracker.update(current_keypoints)
    
    stats = {"LS ": str([np.round(x, 2) for x in left_shoulder_points]), "RS ": str([np.round(x, 2) for x in right_shoulder_points])}
    stats["Pushup Init"] = str(pushup_tracker.init_flag)
    stats["Pushup Count"] = str(pushup_tracker.pushup_counter.get_count())
    stats["Exercise end"] = str(pushup_tracker.is_ended)
    stats["Status"] = pushup_counter.pushup_state
    stats["Cycle Time (s)"] = str(pushup_counter.get_cycle_time())
    stats["Travel (%)"] = str(pushup_counter.get_travel())
    stats["LS_score"] = str(np.round(left_shoulder_points[2], 2))
    stats["RS_score"] = str(np.round(right_shoulder_points[2],2))
    stats["LR_score"] = str(left_wrist_points[2])
    
    #print("********************************************")
    #print(left_wrist.is_moving, left_wrist.moving_counter)
    
    overlay.add_stats(stats_dict=stats)
    stats_frame = overlay.draw(frame=frame_resized)
    
    
    plot_points(frame_resized, current_keypoints)
    out.write(frame_resized)
    cv2.imshow('Frame', frame_resized)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
    
# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()