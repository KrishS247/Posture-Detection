import cv2
import mediapipe as mp
import numpy as np
import threading
from playsound import playsound
import subprocess
import os

alertPlaying = False

def play_alert_sound():
    global alertPlaying
    alertPlaying = True
    playsound('./beeper.mp3')
    alertPlaying = False

# Initialize Mediapipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Open the webcam
cap = cv2.VideoCapture(0)



while True:
    ret, frame = cap.read()

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with Mediapipe Pose model
    results = pose.process(rgb_frame)

    # Check if landmarks are detected
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        # Extract key points for the side view (you may need to adjust these based on your needs)
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]

        # Open the text file for writing pose data
        pose_data_file = open('pose_data.txt', 'w')
        # Save pose data to the text file
        pose_data_file.write(
            f"{left_shoulder.x} {left_shoulder.y} {right_shoulder.x} {right_shoulder.y} "
            f"{left_hip.x} {left_hip.y} {right_hip.x} {right_hip.y}\n"
        )

        # Close the pose data file
        pose_data_file.close()


        # Run the pre-compiled C++ program
        subprocess.run(["main.exe"])

        # Read result from the result file
        with open("result.txt", "r") as result_file:
            result = result_file.readline().strip()

        # Check if the result indicates bad posture
        if result == "Bad Posture!":
            # Display result on the OpenCV window
            cv2.putText(frame, result, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            # Check if the alert sound is not currently playing
            if not alertPlaying:
                # Start a new thread to play the alert sound
                threading.Thread(target=play_alert_sound).start()
        else:
            # Display result on the OpenCV window
            cv2.putText(frame, result, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            

        # Draw landmarks on the frame (optional)
        mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Display the frame
    cv2.imshow("Posture Detection", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()


