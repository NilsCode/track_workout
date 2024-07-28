import numpy as np
import cv2

class StatsOverlay:
    def __init__(self, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=0.5, thickness=2, color=(0, 0, 255)):
        self.font = font
        self.font_scale = font_scale
        self.thickness = thickness
        self.color = color
        self.stats = []

    def add_stats(self, stats_dict):
        """
        Add or update stats in the table.
        :param stats_dict: Dictionary of label-value pairs
        """
        self.stats = list(stats_dict.items())

    def draw(self, frame):
        """
        Draw the stats table on the frame with a fixed starting position,
        ensuring the table occupies 33% of the frame width.
        :param frame: Image frame on which to draw the table
        :return: Frame with the stats table drawn
        """
        if not self.stats:
            return frame

        frame_height, frame_width = frame.shape[:2]
        table_width = int(frame_width * 0.33)  # 33% of the frame width

        # Fixed starting position from the right side of the frame
        start_x = frame_width - table_width

        x_offset, y_offset = 10, 20  # Offsets within the table region

        # Draw each stat
        for i, (label, value) in enumerate(self.stats):
            text = f"{label}: {value}"
            _, text_height = cv2.getTextSize(text, self.font, self.font_scale, self.thickness)[0]
            cv2.putText(frame, text, (start_x + x_offset, y_offset + i * (text_height + 10)), self.font, self.font_scale, self.color, self.thickness)

        return frame