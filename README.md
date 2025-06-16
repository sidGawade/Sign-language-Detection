# Sign Language Detection with Text-to-Speech

This project detects simple sign language gestures using your webcam, interprets them using MediaPipe's hand tracking, and provides audio feedback using text-to-speech (TTS) via the `pyttsx3` library.

## Features

- Real-time hand gesture recognition using MediaPipe
- Supports gestures like:
  - 👋 Hello (open hand)
  - 👍 Yes (thumbs up)
  - 👎 No (thumbs down)
  - 🤟 I Love You (one hand "ILY" + one open hand)
  - 🙏 Thank You (both hands open)
  - 👋 Goodbye (both hands in "ILY" gesture)
- Speaks out the recognized gesture using a threaded TTS engine
- Skips frames to improve performance on lower-end systems

## Requirements

- Python 3.7 or above
- pip packages:
  - `opencv-python`
  - `mediapipe`
  - `pyttsx3`

## Installation

1. Clone the repository:

git clone https://github.com/yourusername/sign-language-detection.git
cd sign-language-detection.

2. Create and activate a virtual environment (optional but recommended):

python -m venv venv
venv\Scripts\activate    # On Windows #
source venv/bin/activate # On macOS/Linux #

3. Install the required packages:

pip install opencv-python mediapipe pyttsx3

4. Run

Notes:
1. Make sure your hand is clearly visible to the webcam with good lighting.
2. Frame skipping is used to enhance performance. You can modify the skip_frames variable in the code for more responsiveness.

License:
This project is licensed under the MIT License.

Acknowledgements:
1. MediaPipe by Google for hand tracking
2. pyttsx3 for offline text-to-speech functionality
