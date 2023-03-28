# Import necessary libraries
import cv2
import numpy as np
import pyautogui
import keyboard
import time
import os
import winsound
from pathlib import Path
from threading import Timer

# Define constants
VIDEO_DIR = str(Path.home() / "Videos")  # Save videos to user's home Videos directory
CLIP_DURATION = 60  # 1 minute clip duration
DELETE_INTERVAL = 300  # Delete clips older than 5 minutes
RESOLUTION = (2560, 1440)  # Video resolution
FPS = 60  # Set FPS to 60


# Function to capture the screen
def capture_screen():
    screenshot = pyautogui.screenshot()  # Take a screenshot
    frame = np.array(screenshot)  # Convert the screenshot to a numpy array
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert the frame to BGR format
    return frame


# Function to save the captured frames as a video clip
def save_clip(frames):
    timestamp = time.strftime("%Y%m%d-%H%M%S")  # Get current timestamp
    file_path = os.path.join(VIDEO_DIR, f"clip-{timestamp}.mp4")  # Generate video file path
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Define codec
    out = cv2.VideoWriter(file_path, fourcc, FPS, RESOLUTION)  # Create video writer

    for frame in frames:
        out.write(frame)  # Write each frame to the video file
    out.release()

    # Play a beep sound after saving the clip
    winsound.Beep(1000, 200)


# Function to delete old video clips
def delete_old_clips():
    now = time.time()  # Get current time
    for file in os.listdir(VIDEO_DIR):
        file_path = os.path.join(VIDEO_DIR, file)
        if os.path.isfile(file_path) and file.startswith("clip-") and file.endswith(".mp4"):
            creation_time = os.path.getctime(file_path)  # Get file creation time
            if (now - creation_time) // 60 >= DELETE_INTERVAL:
                os.remove(file_path)  # Remove the file if it's older than DELETE_INTERVAL
    Timer(DELETE_INTERVAL, delete_old_clips).start()  # Schedule the next deletion


# Main function
def main():
    frames = []  # List to store captured frames
    max_frames = FPS * CLIP_DURATION  # Maximum number of frames for a clip

    delete_old_clips()  # Delete old video clips

    while True:
        start_time = time.time()  # Record start time
        frame = capture_screen()  # Capture the screen
        frames.append(frame)  # Add the frame to the list

        if len(frames) > max_frames:  # Remove the oldest frame if list is full
            frames.pop(0)

        # Save the clip when Alt+F10 is pressed
        if keyboard.is_pressed("alt+f10"):
            save_clip(frames)

        end_time = time.time()  # Record end time
        time_spent = end_time - start_time
        sleep_duration = max(1 / FPS - time_spent, 0)  # Calculate sleep duration
        time.sleep(sleep_duration)  # Sleep for the remaining frame time


# Run the main function
if __name__ == "__main__":
    main()
