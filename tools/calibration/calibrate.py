#!/bin/python

import cv2
import numpy as np

def main():
    # Open webcams (assume 0: left, 1: right)
    cap_left = cv2.VideoCapture(0)
    cap_right = cv2.VideoCapture(2)

    if not cap_left.isOpened() or not cap_right.isOpened():
        print("Error: Could not open one or both webcams.")
        return

    # Create ORB detector
    orb = cv2.ORB_create()

    # Create BFMatcher
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    instructions = [
        "Position cameras horizontally ~63 mm apart (average human IPD).",
        "Ensure they are parallel, facing the same direction.",
        "Point at a scene with distinct features.",
        "Adjust until matching lines are mostly horizontal (minimal vertical offset or slant).",
        "This mimics human binocular vision for stereo setup.",
        "Press 'q' to quit."
    ]

    while True:
        ret_left, frame_left = cap_left.read()
        ret_right, frame_right = cap_right.read()

        if not ret_left or not ret_right:
            print("Error: Failed to capture frames.")
            break

        # Convert to grayscale
        gray_left = cv2.cvtColor(frame_left, cv2.COLOR_BGR2GRAY)
        gray_right = cv2.cvtColor(frame_right, cv2.COLOR_BGR2GRAY)

        # Detect keypoints and descriptors
        kp_left, des_left = orb.detectAndCompute(gray_left, None)
        kp_right, des_right = orb.detectAndCompute(gray_right, None)

        if des_left is not None and des_right is not None:
            # Match descriptors
            matches = bf.match(des_left, des_right)
            matches = sorted(matches, key=lambda x: x.distance)

            # Take top matches
            good_matches = matches[:50]

            # Draw matches
            img_matches = cv2.drawMatches(frame_left, kp_left, frame_right, kp_right, good_matches, None,
                                          flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

            # Compute average vertical disparity (dy)
            if good_matches:
                dys = [kp_right[m.trainIdx].pt[1] - kp_left[m.queryIdx].pt[1] for m in good_matches]
                avg_dy = np.mean(dys)
                std_dy = np.std(dys)

                # Overlay alignment feedback
                feedback = f"Avg vertical offset: {avg_dy:.1f} px (std: {std_dy:.1f})"
                if abs(avg_dy) > 5 or std_dy > 10:
                    feedback += " - Adjust tilt/height for better alignment."
                else:
                    feedback += " - Good vertical alignment!"
                cv2.putText(img_matches, feedback, (10, img_matches.shape[0] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # Overlay instructions
            for i, line in enumerate(instructions):
                cv2.putText(img_matches, line, (10, 30 + i * 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            cv2.imshow('Webcam Stereo Calibration Tool', img_matches)
        else:
            # If no descriptors, show side-by-side without matches
            img_combined = np.hstack((frame_left, frame_right))
            for i, line in enumerate(instructions):
                cv2.putText(img_combined, line, (10, 30 + i * 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.imshow('Webcam Stereo Calibration Tool', img_combined)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap_left.release()
    cap_right.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
