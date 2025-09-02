#!/bin/python

import cv2
import platform

def list_webcams():
    available_cameras = []
    index = 0
    max_index_to_check = 10  # Check up to 10 indices to avoid excessive probing

    while index < max_index_to_check:
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            available_cameras.append(index)
            cap.release()
        index += 1

    return available_cameras

def main():
    cameras = list_webcams()
    if cameras:
        print("Available webcams found at indices:", cameras)
    else:
        print("No webcams found.")

if platform.system() == "Emscripten":
    main()
else:
    if __name__ == "__main__":
        main()
