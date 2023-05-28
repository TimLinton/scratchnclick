import time
from pynput.mouse import Listener, Button, Controller

mouse = Controller()

def get_mouse_position():
    return mouse.position

def get_direction(prev_position, current_position):
    x1, y1 = prev_position
    x2, y2 = current_position
    return x2 - x1, y2 - y1

def is_direction_changed(prev_direction, current_direction, threshold=5):
    dx1, dy1 = prev_direction
    dx2, dy2 = current_direction
    dot_product = dx1 * dx2 + dy1 * dy2
    return dot_product < threshold

def on_move(x, y):
    global prev_position, prev_direction, direction_change_count, last_move_time, last_change_time
    current_position = (x, y)
    current_direction = get_direction(prev_position, current_position)
    
    current_time = time.time()
    time_since_last_move = current_time - last_move_time
    
    if time_since_last_move < 0.1:  # Only consider direction changes if the time between moves is less than 100ms
        if is_direction_changed(prev_direction, current_direction):
            direction_change_count += 1
            if current_time - last_change_time > 1 and direction_change_count > 5:  # Check for minimum number of direction changes
                mouse.click(Button.left)
                last_change_time = current_time
                direction_change_count = 0
        else:
            last_change_time = current_time
            direction_change_count = 0
            
    last_move_time = current_time
    prev_position = current_position
    prev_direction = current_direction

prev_position = get_mouse_position()
prev_direction = (0, 0)
direction_change_count = 0
last_change_time = time.time()
last_move_time = time.time()

with Listener(on_move=on_move) as listener:
    listener.join()
