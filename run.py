import cv2
import mediapipe as mp
import pyttsx3
import threading

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Variable to store the last spoken gesture
last_spoken_gesture = ""

# Function to speak the detected gesture in a separate thread
def speak_gesture(gesture):
    global last_spoken_gesture
    if gesture != last_spoken_gesture:  # Avoid repeating the same gesture
        def speak():
            engine.say(gesture) 
            engine.runAndWait()
        threading.Thread(target=speak).start()
        last_spoken_gesture = gesture

# Function to check if all fingers are extended
def is_open_hand(landmarks):
    tips = [8, 12, 16, 20]  # Indices of finger tips (excluding thumb)
    mcp = [5, 9, 13, 17]    # Indices of middle finger joints
    return all(landmarks.landmark[tip].y < landmarks.landmark[mcp].y for tip, mcp in zip(tips, mcp))

# Function to check if thumb is up
def is_thumbs_up(landmarks):
    thumb_tip = landmarks.landmark[4]
    thumb_ip = landmarks.landmark[3]
    return thumb_tip.y < thumb_ip.y

# Function to check if thumb is down
def is_thumbs_down(landmarks):
    thumb_tip = landmarks.landmark[4]
    thumb_ip = landmarks.landmark[3]
    return thumb_tip.y > thumb_ip.y

# Function to check if hand is in "I Love You" gesture
def is_i_love_you(landmarks):
    # Thumb, index, and pinky extended; middle and ring fingers folded
    thumb_tip = landmarks.landmark[4]
    index_tip = landmarks.landmark[8]
    middle_tip = landmarks.landmark[12]
    ring_tip = landmarks.landmark[16]
    pinky_tip = landmarks.landmark[20]
    
    thumb_extended = thumb_tip.y < landmarks.landmark[3].y
    index_extended = index_tip.y < landmarks.landmark[6].y
    middle_folded = middle_tip.y > landmarks.landmark[9].y
    ring_folded = ring_tip.y > landmarks.landmark[13].y
    pinky_extended = pinky_tip.y < landmarks.landmark[17].y
    
    return thumb_extended and index_extended and middle_folded and ring_folded and pinky_extended

# Function to check if both hands are flat (Thank You)
def is_thank_you(landmarks_list):
    if len(landmarks_list) != 2:
        return False
    return all(is_open_hand(landmarks) for landmarks in landmarks_list)

# Function to check if one hand is "ILY" and the other is open (I Love You)
def is_i_love_you_one_hand(landmarks_list):
    if len(landmarks_list) != 2:
        return False
    # Check if one hand is "ILY" and the other is open
    hand1_ily = is_i_love_you(landmarks_list[0])
    hand2_open = is_open_hand(landmarks_list[1])
    hand2_ily = is_i_love_you(landmarks_list[1])
    hand1_open = is_open_hand(landmarks_list[0])
    return (hand1_ily and hand2_open) or (hand2_ily and hand1_open)

# Function to check if both hands are in "ILY" gesture (Goodbye)
def is_goodbye(landmarks_list):
    if len(landmarks_list) != 2:
        return False
    return all(is_i_love_you(landmarks) for landmarks in landmarks_list)


# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set width to 640 pixels
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Set height to 480 pixels

frame_counter = 0
skip_frames = 2  # Process every 3rd frame

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_counter += 1
    if frame_counter % skip_frames != 0:
        continue  # Skip this frame

    # Convert the frame to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    # Process the frame with MediaPipe Hands
    results = hands.process(image)

    # Convert the frame back to BGR for display
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Initialize phrase as empty
    phrase = ""

    if results.multi_hand_landmarks:
        landmarks_list = results.multi_hand_landmarks

        # Draw hand landmarks
        for landmarks in landmarks_list:
            mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)

        # Detect gestures
        if len(landmarks_list) == 1:
            if is_open_hand(landmarks_list[0]):
                phrase = "Hello"
            elif is_thumbs_up(landmarks_list[0]):
                phrase = "Yes"
            elif is_thumbs_down(landmarks_list[0]):
                phrase = "No"
        elif len(landmarks_list) == 2:
            if is_thank_you(landmarks_list):
                phrase = "Thank You"
            elif is_i_love_you_one_hand(landmarks_list):
                phrase = "I Love You"
            elif is_goodbye(landmarks_list):
                phrase = "Goodbye"

        # Speak the detected gesture
        if phrase:
            speak_gesture(phrase)

    # Display the phrase
    cv2.putText(image, f"Phrase: {phrase}", (10, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show the frame
    cv2.imshow('Sign Language Detection', image)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()