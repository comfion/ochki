#!/bin/python

import argparse
import cv2
import datetime
import os
import subprocess
import threading
import time

def record_cam(cam_index, output_path, duration_seconds, resolution=(1280, 720)):
    cap = cv2.VideoCapture(cam_index)
    if not cap.isOpened():
        print(f"Error: Could not open webcam {cam_index}.")
        return

    # Attempt to set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0  # Default to 30 if not available

    # FFmpeg command to save as 720p MP4
    cmd = [
        'ffmpeg',
        '-y',  # Overwrite output
        '-f', 'rawvideo',
        '-vcodec', 'rawvideo',
        '-s', f'{resolution[0]}x{resolution[1]}',
        '-pix_fmt', 'bgr24',  # OpenCV default
        '-r', str(fps),
        '-i', '-',  # Input from stdin
        '-c:v', 'libx264',
        '-preset', 'ultrafast',
        '-pix_fmt', 'yuv420p',
        output_path
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    start_time = time.time()
    while time.time() - start_time < duration_seconds:
        ret, frame = cap.read()
        if not ret:
            break
        # Resize if not already 720p
        frame = cv2.resize(frame, resolution)
        proc.stdin.write(frame.tobytes())

    proc.stdin.close()
    proc.wait()
    cap.release()

def main():
    parser = argparse.ArgumentParser(description="Record videos from two webcams.")
    parser.add_argument('minutes', type=int, help="Duration in minutes")
    args = parser.parse_args()

    duration_seconds = args.minutes * 60

    # Create timestamp-based directory
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    dir_path = os.path.join(os.getcwd(), timestamp)
    os.makedirs(dir_path, exist_ok=True)

    left_path = os.path.join(dir_path, 'l.mp4')
    right_path = os.path.join(dir_path, 'r.mp4')

    thread_left = threading.Thread(target=record_cam, args=(0, left_path, duration_seconds))
    thread_right = threading.Thread(target=record_cam, args=(2, right_path, duration_seconds))

    thread_left.start()
    thread_right.start()

    thread_left.join()
    thread_right.join()

    print(f"Recordings saved in: {dir_path}")

if __name__ == "__main__":
    main()
