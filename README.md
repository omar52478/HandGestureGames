Hand Gesture Games
Overview
This project implements a hand gesture-based gaming system using a webcam. It includes two games:

Hill Climb Racing: Control the game using hand gestures (closed fist for brake, open hand for accelerate, two fingers to pause).
Tic-Tac-Toe: Play against an AI using hand gestures to select cells (index finger to select, thumb + index to confirm).

Requirements

Python 3.6+
Libraries (install using pip install -r requirements.txt):
opencv-python
mediapipe
numpy
pynput

Installation

    Clone the repository:git clone https://github.com/omar52478/HandGestureGames.git
    cd hand_gesture_games

Install the required libraries:pip install -r requirements.txt

Run the project:python main.py

How to Play
Hill Climb Racing

    Ensure the Hill Climb Racing game window is open on your computer.
    Use the following gestures:
    Closed fist: Brake (left arrow).
    Open hand: Accelerate (right arrow).
    Two fingers: Pause (spacebar).

Press q to exit.

Tic-Tac-Toe

    Use the following gestures:
    Index finger: Move to select a cell.
    Thumb + Index touching: Confirm selection.
    Closed fist (after game over): Reset the game.
    Open palm for 3 seconds: Exit the game.

Buttons:
Reset: Click the green "Reset" button to start a new game.
Exit: Click the red "Exit" button to quit.

Press q to exit.

Difficulty Levels (Tic-Tac-Toe)

    Easy: AI makes random moves.
    Medium: AI uses limited-depth Minimax with random moves.
    Hard: AI uses full Minimax with Alpha-Beta Pruning (default).

Notes

    Ensure good lighting and a clear background for better hand detection.
    The project works on Windows, Linux, and macOS (uses pynput for keyboard simulation).

Future Improvements

    Add more games (e.g., Snake).
    Improve hand detection in low-light conditions.
    Add sound effects and animations for a better user experience.
