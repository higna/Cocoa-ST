# Import Libraries
import cv2
import numpy as np
from ultralytics import YOLO
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon


def select_polygon(video_path):
    """Define polygon area on a video frame."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return []

    cap.set(cv2.CAP_PROP_POS_FRAMES, 30)  # Start from frame 30

    # Read first frame
    success, frame = cap.read()
    if not success:
        print("Error: Could not read frame.")
        return []

    # Fullscreen window mode
    window_name = "Define restricted Area - Press 'ESC' when finished"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Create a copy of the frame for drawing
    display_frame = frame.copy()
    points = []

    # Function to update display
    def update_display():
        nonlocal display_frame, frame, points
        display_frame = frame.copy()

        # Draw instructions
        instructions = [
            "instructions:",
            "1. Click to add polygon vertices",
            "2. Press 'd' to delete last point",
            "3. Press 'c' to clear all points",
            "4. Press Enter when finished",
            "5. Press ESC to quit",
        ]

        for i, text in enumerate(instructions):
            cv2.putText(
                display_frame,
                text,
                (10, 30 + i * 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
            )

        # Draw polygon lines
        if len(points) > 0:
            for i, (px, py) in enumerate(points):
                cv2.circle(display_frame, (px, py), 5, (0, 0, 255), -1)
                cv2.putText(
                    display_frame,
                    str(i + 1),
                    (px + 15, py - 15),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 225),
                    2,
                )

            if len(points) > 1:
                cv2.polylines(display_frame, [np.array(points)], False, (0, 255, 0), 2)

    # Mouse callback function
    def mouse_callback(event, x, y, flags, param):
        nonlocal points
        if event == cv2.EVENT_LBUTTONDOWN:
            points.append((x, y))
            update_display()

    cv2.setMouseCallback(window_name, mouse_callback)
    # Initial display
    update_display()

    while True:
        key = cv2.waitKey(1)

        if key == 13 or key == 10:
            if len(points) >= 3:
                break
            else:
                print("Please select at least 3 points to form a polygon.")
        elif key == ord("d"):  # Delete last point
            if points:
                points.pop()
                update_display()
        elif key == ord("c"):  # Clear all
            points = []
            update_display()
        elif key == 27:  # ESC key(Quit)
            points = []
            break
    cap.release()
    cv2.destroyAllWindows()
    return points

if __name__ == "__main__":
    print("MAIN STARTED")

    video_path = "/"
    polygon = select_polygon(video_path)

    print("Selected points:", polygon)