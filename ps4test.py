import evdev

devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
devices = [dev for dev in devices if dev.name == "Sony Interactive Entertainment Wireless Controller"]

if len(devices) == 0:
    raise RuntimeError("No hay mando")
if len(devices) > 1:
    raise RuntimeError("Demasiados mandos")

gamepad = devices[0]

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


def scaleInt(val):
    return float(val)/255-0.5

def scaleUint(val):
    return float(val)/255

def btn_state():
    return "Buttons ({:1s}{:1s}{:1s}{:1s})".format(
        "⮾" if btn_cross == 1 else " ",
        "□" if btn_square == 1 else " ",
        "○" if btn_circle == 1 else " ",
        "△" if btn_triangle == 1 else " ",
    )

for event in gamepad.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        if event.code == 304:
            btn_cross = event.value
        elif event.code == 305:
            btn_circle = event.value
        elif event.code == 307:
            btn_triangle = event.value
        elif event.code == 308:
            btn_square = event.value 
    if event.type == evdev.ecodes.EV_ABS:
        if event.code == 0:
            left_x = scaleInt(event.value)
        elif event.code == 1:
            left_y = scaleInt(event.value)
        elif event.code == 2:
            l2 = scaleUint(event.value)
        elif event.code == 3:
            right_x = scaleInt(event.value)
        elif event.code == 4:
            right_y = scaleInt(event.value)
        elif event.code == 5:
            r2 = scaleUint(event.value)
    print("Left: ({:5.2f}, {:5.2f}) L2 ({:.2f}) Right: ({:5.2f}, {:5.2f}) R2 ({:.2f}) {}".format(left_x, left_y, l2, right_x, right_y, r2, btn_state()))


