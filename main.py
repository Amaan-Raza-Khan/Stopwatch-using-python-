import time
second = 0
hours = 0
minute = 0
is_pause = True

def update_time():
    global second, minute, hours, is_pause
    if not is_pause:
        second +=1
        if second == 60:
            second = 0
            minute +=1
        elif minute == 60:
            minute = 0
            hours+=1


    return f"{hours:02}:{minute:02}:{second:02}"
def toggle_pause():
    global is_pause
    is_pause = not is_pause
    return is_pause
def reset():
    global second, minute, hours, is_pause
    is_pause = True
    second = 0
    minute =0
    hours = 0
def get_current_time():
    return f"{hours:02}:{minute:02}:{second:02}"