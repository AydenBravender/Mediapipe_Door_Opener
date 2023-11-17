import cv2
import math
import mediapipe as mp
import socket
import time

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Initialize video capture
cap = cv2.VideoCapture(0)

# Initialize Mediapipe hands
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    client_socket = socket.socket()
    
    # Change with your computers ip address
    client_socket.connect(( , ))

    last_processing_time = time.time()
    processing_interval = 0.3  # Process a frame every 0.3 seconds, this way the recieving program doesn't get overloaded with data
    
    while True:
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue
        
        current_time = time.time() # helps the program know when the last time it processed a frame was, and when it needs to
        if current_time - last_processing_time >= processing_interval:
            last_processing_time = current_time

            results = hands.process(image)

            if results.multi_hand_landmarks is not None:
                for hand_landmarks in results.multi_hand_landmarks:
                   # we find the position on the screen of these 4 points: 
                    index_metacarpal = (hand_landmarks.landmark[5].x, hand_landmarks.landmark[5].y, hand_landmarks.landmark[5].z)
                    pinky_metacarpal = (hand_landmarks.landmark[20].x, hand_landmarks.landmark[20].y, hand_landmarks.landmark[20].z)
                    middle_tip = (hand_landmarks.landmark[14].x, hand_landmarks.landmark[14].y, hand_landmarks.landmark[14].z)
                    metacarpal = (hand_landmarks.landmark[10].x, hand_landmarks.landmark[10].y, hand_landmarks.landmark[10].z)

                    # Calculate the 2D distance (ignoring depth)
                    distance_base = math.sqrt((index_metacarpal[0] - pinky_metacarpal[0])**2 + (index_metacarpal[1] - pinky_metacarpal[1])**2)
                    distance_var = math.sqrt((middle_tip[0] - metacarpal[0])**2 + (middle_tip[1] - metacarpal[1])**2)
                    # we measure the width of the hand (distance_base), and distance of the base of the middle finger to the tip
                    # when we divide these 2 numbers we get a value that depending on your hand size determine whether its opened or clenched
                    value = distance_base/distance_var
                    
                    # The number 3 here is what works for my hands, but you'll need to play around with a value that works better for you
                    # you can add 'print(value)' to see what it is when your hand is opened and closed
                    if value > 3:
                        hand = "opened"
                    elif value < 3:
                        hand = "clenched"
                    # This is an optional line of code that draws all of the hand points onto the image
                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    # Also optional, it writes the status of the variable 'hand' onto the screen
                    cv2.putText(image, f'Hand: {hand}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            else:
                hand = "neither"

            data_to_send = hand
            client_socket.send(data_to_send.encode())
           
            cv2.imshow('MediaPipe Hands', image)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

client_socket.close()
