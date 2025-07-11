import time
import threading
from pathlib import Path

def clear_screen():
    print("\033c", end="")
    # print("\033[H", end="") 

def cursor_start():
    # print("\033[H", end="") # Doesnt really clear full frames, if some part of the frame is out of the window (if you zoom in)
    print("\033[H\033[3J", end="")

def intro_sequence(fps):
    FPS = fps  # frames per second
    HERE = Path(__file__).parent
    frame_file = HERE / "frames.txt"
    if not frame_file.exists():
        return  # skip animation if file missing

    with frame_file.open("r", encoding="utf-8") as f:
        frames = f.read().strip().split("\n\n")

    stop_flag = {"stop": False}

    def wait_for_enter():
        input() # Due to cursor_start(), this gets cleared away.
        stop_flag["stop"] = True

    threading.Thread(target=wait_for_enter, daemon=True).start()

    cursor_start()
    print(frames[0] + "\nPress <Enter> to end animation…", end="", flush=True)
    # print("\nPress <Enter> to end animation…\n") 

    time.sleep(1 / FPS)

    try:
        while not stop_flag["stop"]:
            for frame in frames[1:]:
                if stop_flag["stop"]:
                    break
                cursor_start()
                print(frame + "\nPress <Enter> to end animation…", end="", flush=True)
                time.sleep(1 / FPS)
    except KeyboardInterrupt:
        pass

    clear_screen()

while True:
    fps = input("Enter FPS for animation: ")
    if fps.isdigit() and int(fps) > 0:
        fps = int(fps)
        break
    else:
        print("❌ Please enter a whole number.")
        
clear_screen()
intro_sequence(fps)