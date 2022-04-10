import cv2
import mediapipe as mp
import numpy as np
import argparse
import pyttsx3
import vlc
import time
import threading

# setup agrparse
ap = argparse.ArgumentParser()
ap.add_argument("-t",
                "--exercise_type",
                type=str,
                help='Type of activity to do',
                required=True)

args = vars(ap.parse_args())

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
engine = pyttsx3.init()


def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - \
        np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle > 180.0:
        angle = 360-angle

    return angle


def beep():
    p = vlc.MediaPlayer("beep-02.mp3")
    p.play()
    time.sleep(60)
    p.stop()


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    # Curl counter variables
    counter = 0
    stage = None
    headDrop = True
    slump = True
    leanForward = True
    current_message = ""

    # Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()

            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark

                # Get coordinates
                lshoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                lelbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                lwrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                rshoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                             landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                relbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                rwrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                lhip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                rhip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                lknee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                rknee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                lankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                rankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                lear = [landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].y]
                rear = [landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value].y]
                leye = [landmarks[mp_pose.PoseLandmark.LEFT_EYE.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_EYE.value].y]
                reye = [landmarks[mp_pose.PoseLandmark.RIGHT_EYE.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_EYE.value].y]
                nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x,
                        landmarks[mp_pose.PoseLandmark.NOSE.value].y]
                neck = [(lshoulder[0]+rshoulder[0])/2,
                        (lshoulder[1]+rshoulder[1])/2]

                # Curl counter logic
                if(args['exercise_type'] == 'Curls'):
                    # Calculate angle
                    angle = calculate_angle(rshoulder, relbow, rwrist)

                    if angle > 160:
                        stage = "Down"
                    if angle < 30 and stage == 'Down':
                        stage = "Up"
                        counter += 1
                        # engine.say(str(counter))
                        # engine.runAndWait()
                        threading.Thread(target=beep, daemon=True).start()
                        print(counter)

                    # Visualize angle
                    cv2.putText(image, str(angle),
                                tuple(np.multiply(
                                    lelbow, [640, 480]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (
                                255, 255, 255), 2, cv2.LINE_AA
                                )

                # Squats counter logic
                elif(args['exercise_type'] == 'Squats'):
                    # Calculate angle
                    langle = calculate_angle(lhip, lknee, lankle)
                    rangle = calculate_angle(rhip, rknee, rankle)
                    avg_leg_angle = (langle + rangle) // 2

                    if avg_leg_angle > 160:
                        stage = "Up"
                    if avg_leg_angle < 70 and stage == 'Up':
                        stage = "Down"
                        counter += 1
                        # beep()
                        # engine.say(str(counter))
                        # engine.runAndWait()
                        threading.Thread(target=beep, daemon=True).start()
                        print(counter)

                    # Visualize angle
                    cv2.putText(image, str(avg_leg_angle),
                                tuple(np.multiply(
                                    lknee, [640, 480]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (
                                255, 255, 255), 2, cv2.LINE_AA
                                )

                elif(args['exercise_type'] == 'Lunges'):
                    # Calculate angle
                    langle = calculate_angle(lhip, lknee, lankle)
                    rangle = calculate_angle(rhip, rknee, rankle)
                    avg_leg_angle = (langle + rangle) // 2

                    if avg_leg_angle > 160:
                        stage = "Up"
                    if (langle < 70 and rangle > 160) or (rangle < 70 and langle > 160) and stage == 'Up':
                        stage = "Down"
                        counter += 1
                        # beep()
                        # engine.say(str(counter))
                        # engine.runAndWait()
                        threading.Thread(target=beep, daemon=True).start()
                        print(counter)

                    # Visualize angle
                    cv2.putText(image, str(avg_leg_angle),
                                tuple(np.multiply(
                                    lknee, [640, 480]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (
                                255, 255, 255), 2, cv2.LINE_AA
                                )

                # pushups counter logic
                elif(args['exercise_type'] == 'PushUps'):
                    # Calculate angle
                    langle = calculate_angle(lshoulder, lelbow, lwrist)
                    rangle = calculate_angle(rshoulder, relbow, rwrist)
                    avg_arm_angle = (langle + rangle) // 2

                    if avg_arm_angle > 160:
                        stage = "Up"
                    if avg_arm_angle < 100 and stage == 'Up':
                        stage = "Down"
                        counter += 1
                        # beep()
                        # engine.say(str(counter))
                        # engine.runAndWait()
                        threading.Thread(target=beep, daemon=True).start()
                        print(counter)

                    # Visualize angle
                    cv2.putText(image, str(avg_arm_angle),
                                tuple(np.multiply(
                                    lknee, [640, 480]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (
                                255, 255, 255), 2, cv2.LINE_AA
                                )

                # pushups counter logic
                elif(args['exercise_type'] == 'PostureCorrector'):

                    if (leye[0] < 0.5 and lear[0] < 0.5):
                        headDrop = False
                        threading.Thread(target=beep, daemon=True).start()
                    else:
                        headDrop = True
                    if(lshoulder[1] > rshoulder[1] + 0.3 or lshoulder[1] + 0.3 < rshoulder[1]):
                        slump = False
                        threading.Thread(target=beep, daemon=True).start()
                    else:
                        slump = True
                    if lshoulder[0] >= (lear[0] + 150) or rshoulder[0] > (rear[0] + 150):
                        leanForward = False
                    else:
                        leanForward = True

                    print(headDrop, slump, leanForward)

                    if not headDrop:
                        current_message = "Lift up your head!\n"
                    if not leanForward:
                        current_message = "Lean back!\n"
                    if not slump:
                        current_message = "Sit up in your chair, you're slumping!\n"

            except:
                pass

            if(args['exercise_type'] == 'PostureCorrector'):
                cv2.rectangle(image, (10, 10), (400, 100), (255, 255, 255), -1)
                # Rep data
                cv2.putText(image, args['exercise_type'], (15, 35),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, current_message, (15, 65),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)

                if(headDrop or leanForward or slump):
                    current_message = ''

            else:
                # Render curl counter
                # Setup status box
                cv2.rectangle(image, (10, 10), (350, 130), (255, 255, 255), -1)
                cv2.circle(image, (650, 600),
                           80, (255, 255, 255), -1)

                # Rep data
                cv2.putText(image, 'EXERCISE TYPE - ', (15, 35),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, args['exercise_type'], (195, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, str(counter),
                            (620, 630),
                            cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 3, cv2.LINE_AA)

                # Stage data
                cv2.putText(image, 'STATE - ', (15, 95),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, stage,
                            (100, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 1, cv2.LINE_AA)

            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(
                                          color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(
                                          color=(245, 66, 230), thickness=2, circle_radius=2)
                                      )

            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
