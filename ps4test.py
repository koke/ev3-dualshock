import evdev
import dualshock


left_x = 0
left_y = 0
l2 = 0
right_x = 0
right_y = 0
r2 = 0
btn_cross = 0
btn_square = 0
btn_circle = 0
btn_triangle = 0

def btn_state():
    return "Buttons ({:1s}{:1s}{:1s}{:1s})".format(
        "⮾" if btn_cross == 1 else " ",
        "□" if btn_square == 1 else " ",
        "○" if btn_circle == 1 else " ",
        "△" if btn_triangle == 1 else " ",
    )

def print_debug():
        print("Left: ({:5.2f}, {:5.2f}) L2 ({:.2f}) Right: ({:5.2f}, {:5.2f}) R2 ({:.2f}) {}".format(left_x, left_y, l2, right_x, right_y, r2, btn_state()))

def on_button_press(btn, val):
    if btn == dualshock.BTN_CROSS:
        global btn_cross
        btn_cross = val
    elif btn == dualshock.BTN_SQUARE:
        global btn_square
        btn_square = val
    elif btn == dualshock.BTN_CIRCLE:
        global btn_circle
        btn_circle = val
    elif btn == dualshock.BTN_TRIANGLE:
        global btn_triangle
        btn_triangle = val
    print_debug()

def on_report_sync(left, right, lt, rt):
    global left_x, left_y, right_x, right_y, l2, r2
    left_x = left[0] if left[0] else 0
    left_y = left[1] if left[1] else 0
    right_x = right[0] if right[0] else 0
    right_y = right[1] if right[1] else 0
    l2 = lt if lt else 0
    r2 = rt if rt else 0
    print_debug()

gamepad = dualshock.Dualshock(on_button_press=on_button_press, on_report_sync=on_report_sync)
gamepad.listen()
