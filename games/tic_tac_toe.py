import cv2
import numpy as np
import sys
import os
# Add parent directory to sys.path to resolve utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.hand_detector import HandDetector
import time

def draw_board(image, board, cell_size=100, offset_x=150, offset_y=100, selected_cell=None):
    h, w, _ = image.shape
    for i in range(3):
        for j in range(3):
            x1 = offset_x + j * cell_size
            y1 = offset_y + i * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            color = (0, 255, 0) if selected_cell == (i, j) else (255, 255, 255)  # Green for selection
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 5)  # Thicker selection line
            if board[i][j] != " ":
                # Different colors for X and O
                text_color = (255, 0, 0) if board[i][j] == "X" else (0, 0, 255)  # Red for X, Blue for O
                cv2.putText(image, board[i][j], (x1 + 25, y1 + 70), cv2.FONT_HERSHEY_SIMPLEX, 2, text_color, 4)
    return image

def check_winner(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2-i] == player for i in range(3)):
        return True
    return False

def is_board_full(board):
    return all(cell != " " for row in board for cell in row)

def get_empty_cells(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]

def minimax(board, depth, is_maximizing):
    if check_winner(board, "O"):
        return 1
    if check_winner(board, "X"):
        return -1
    if is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i, j in get_empty_cells(board):
            board[i][j] = "O"
            score = minimax(board, depth + 1, False)
            board[i][j] = " "
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i, j in get_empty_cells(board):
            board[i][j] = "X"
            score = minimax(board, depth + 1, True)
            board[i][j] = " "
            best_score = min(score, best_score)
        return best_score

def ai_move(board):
    best_score = -float("inf")
    best_move = None
    for i, j in get_empty_cells(board):
        board[i][j] = "O"
        score = minimax(board, 0, False)
        board[i][j] = " "
        if score > best_score:
            best_score = score
            best_move = (i, j)
    return best_move

def get_grid_position(cx, cy, cell_size=100, offset_x=150, offset_y=100):
    if offset_x <= cx < offset_x + 3 * cell_size and offset_y <= cy < offset_y + 3 * cell_size:
        col = (cx - offset_x) // cell_size
        row = (cy - offset_y) // cell_size
        return int(row), int(col)
    return None

def is_thumb_index_touching(lm_list):
    if lm_list:
        thumb_tip = lm_list[4][1:3]  # Thumb tip (x, y)
        index_tip = lm_list[8][1:3]  # Index tip (x, y)
        distance = ((thumb_tip[0] - index_tip[0]) ** 2 + (thumb_tip[1] - index_tip[1]) ** 2) ** 0.5
        return distance < 30  # Adjust threshold as needed
    return False

def run_tic_tac_toe():
    detector = HandDetector(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    video = cv2.VideoCapture(0)
    
    # Set camera resolution to 640x480 for consistency
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    board = [[" " for _ in range(3)] for _ in range(3)]
    cell_size = 100
    offset_x, offset_y = 170, 90  # Adjusted to center in 640x480 resolution
    last_move_time = 0
    game_over = False
    result_text = ""
    
    # Set window size to match camera resolution
    cv2.namedWindow("Tic-Tac-Toe", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Tic-Tac-Toe", 640, 480)

    try:
        while True:
            ret, image = video.read()
            if not ret:
                break

            image, fingers, lm_list = detector.process_frame_with_landmarks(image)
            selected_cell = None
            if lm_list:
                cx, cy = lm_list[8][1], lm_list[8][2]  # Index finger tip
                pos = get_grid_position(cx, cy, cell_size, offset_x, offset_y)
                if pos:
                    selected_cell = pos

            image = draw_board(image, board, cell_size, offset_x, offset_y, selected_cell)

            if not game_over and fingers and lm_list:
                total = fingers.count(1)
                if total == 0 and game_over:  # Closed fist to reset
                    board = [[" " for _ in range(3)] for _ in range(3)]
                    game_over = False
                    result_text = ""
                elif is_thumb_index_touching(lm_list) and time.time() - last_move_time > 1:  # Thumb + Index to select
                    cx, cy = lm_list[8][1], lm_list[8][2]
                    pos = get_grid_position(cx, cy, cell_size, offset_x, offset_y)
                    if pos:
                        row, col = pos
                        if board[row][col] == " ":
                            board[row][col] = "X"
                            last_move_time = time.time()
                            if check_winner(board, "X"):
                                result_text = "You Win!"
                                game_over = True
                            elif is_board_full(board):
                                result_text = "Tie!"
                                game_over = True
                            else:
                                ai_row, ai_col = ai_move(board)
                                board[ai_row][ai_col] = "O"
                                if check_winner(board, "O"):
                                    result_text = "AI Wins!"
                                    game_over = True
                                elif is_board_full(board):
                                    result_text = "Tie!"
                                    game_over = True

            if result_text:
                cv2.putText(image, result_text, (offset_x - 50, offset_y + 350), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4)
                if game_over and fingers:
                    total = fingers.count(1)
                    if total == 0:  # Closed fist to reset after game over
                        board = [[" " for _ in range(3)] for _ in range(3)]
                        game_over = False
                        result_text = ""

            cv2.imshow("Tic-Tac-Toe", image)
            if cv2.waitKey(1) == ord('q'):
                break

    finally:
        video.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    run_tic_tac_toe()