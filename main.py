#!/usr/bin/env python3

from dualshock import Dualshock, BTN_CIRCLE, BTN_CROSS
from pybricks.sound import SoundFile
from ev3dev2.sound import Sound
from ev3dev2.motor import MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, MoveJoystick, SpeedPercent
import threading

left_x = 0
left_y = 0

class MotorThread(threading.Thread):
    def __init__(self):
        self.motor_garra = MediumMotor(OUTPUT_A)
        self.robot = MoveJoystick(OUTPUT_B, OUTPUT_C)
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if left_x == 0 and left_y == 0:
                self.robot.stop()
            else:
                self.robot.on(left_x, -left_y, 1)

    def release(self):
        Sound.play_file(SoundFile.AIR_RELEASE)
        self.motor_garra.on_for_seconds(SpeedPercent(-50), 1)

    def grab(self):
        Sound.play_file(SoundFile.AIRBRAKE)
        self.motor_garra.on_for_seconds(SpeedPercent(50), 1)

motor_thread = MotorThread()
motor_thread.setDaemon(True)
motor_thread.start()

def on_button_press(btn, val):
    if val == 0:
        return
    if btn == BTN_CROSS:
        motor_thread.grab()
    elif btn == BTN_CIRCLE:
        motor_thread.release()

def on_report_sync(left, right, lt, rt):
    global left_x, left_y
    left_x = left[0] if left[0] else 0
    left_y = left[1] if left[1] else 0

gamepad = Dualshock(on_button_press=on_button_press, on_report_sync=on_report_sync)
gamepad.listen()
