import sys
from games.hill_climb import run_hill_climb
from games.tic_tac_toe import run_tic_tac_toe

def display_menu():
    print("\n=== Game Selection Menu ===")
    print("1. Hill Climb Racing (Hand Gesture Control)")
    print("2. Tic-Tac-Toe (Hand Gesture Control)")
    print("3. Exit")
    return input("Enter your choice (1-3): ")

def main():
    while True:
        choice = display_menu()
        if choice == '1':
            print("Starting Hill Climb Racing control...")
            run_hill_climb()
        elif choice == '2':
            print("Starting Tic-Tac-Toe...")
            run_tic_tac_toe()
        elif choice == '3':
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()