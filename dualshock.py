import evdev

BTN_CROSS = evdev.ecodes.BTN_SOUTH
BTN_SQUARE = evdev.ecodes.BTN_WEST
BTN_TRIANGLE = evdev.ecodes.BTN_NORTH
BTN_CIRCLE = evdev.ecodes.BTN_EAST
BTN_L1 = evdev.ecodes.BTN_TL
BTN_R1 = evdev.ecodes.BTN_TR
BTN_L2 = evdev.ecodes.BTN_TL2
BTN_R2 = evdev.ecodes.BTN_TR2
BTN_SHARE = evdev.ecodes.BTN_SELECT
BTN_OPTIONS = evdev.ecodes.BTN_START
BTN_L3 = evdev.ecodes.BTN_THUMBL
BTN_R3 = evdev.ecodes.BTN_THUMBR
BTN_PS = evdev.ecodes.BTN_MODE
BTN_TOUCHPAD = evdev.ecodes.BTN_TOUCH

_SUPPORTED_BUTTONS = [BTN_CROSS, BTN_SQUARE, BTN_TRIANGLE, BTN_CIRCLE, BTN_L1, BTN_R1, BTN_L2, BTN_R2, BTN_SHARE, BTN_OPTIONS, BTN_L3, BTN_R3, BTN_PS, BTN_TOUCHPAD]

class Dualshock:
    """
    Represents a Dualshock controller.

    Attributes:
        threshold (float): Ignore stick values below this threshold.
        left (tuple): Current position of the left stick (x, y).
        right (tuple): Current position of the right stick (x, y).
        l2 (float): Current value of the left trigger (L2).
        r2 (float): Current value of the right trigger (R2).
        buttons (dict): Dictionary of button states.
    """

    threshold = 0.11
    
    @classmethod
    def find_compatible_devices(cls):
        def is_compatible_device(device):
            return device.name == "Sony Interactive Entertainment Wireless Controller" or device.name == "Wireless Controller"
        
        return list(filter(is_compatible_device, map(evdev.InputDevice, evdev.list_devices())))

    def __init__(self, on_button_press=None, on_report_sync=None):
            """
            Initializes a Dualshock controller instance.

            Args:
                on_button_press (function, optional): Callback function to handle button press events. It will pass the button code and the button value as arguments.
                on_report_sync (function, optional): Callback function to handle report sync events. It will pass the left stick position, the right stick position, the left trigger value and the right trigger value as arguments.

            Raises:
                RuntimeError: If no compatible devices are found or if too many compatible devices are found.
            """
            devices = Dualshock.find_compatible_devices()
            if len(devices) == 0:
                raise RuntimeError("No compatible devices found")
            if len(devices) > 1:
                raise RuntimeError("Too many compatible devices found")
            self._device = devices[0]
            self.left = (0, 0)
            self.right = (0, 0)
            self.l2 = 0
            self.r2 = 0
            self.buttons = {k: 0 for k in _SUPPORTED_BUTTONS}
            self._on_button_press = on_button_press
            self._on_report_sync = on_report_sync
    
    def scale(self, val):
        """
        Scales a value from the range [0, 255] to the range [0, 1].

        Args:
            val (int): The value to scale.

        Returns:
            float: The scaled value.
        """
        return float(val)/255
    
    def center(self, val):
        """
        Centers a value in the [0, 1] range to the [-1, 1] range.

        Args:
            val (float): The value to center.

        Returns:
            float: The centered value.
        """
        centered = (val - 0.5) * 2
        if abs(centered) < self.threshold:
            centered = 0
        return centered

        
    def listen(self):
        """
        Starts listening for events from the Dualshock controller.

        This method runs in an infinite loop and calls the appropriate callback functions
        when button press events or report sync events occur.
        """
        for event in self._device.read_loop():
            if event.type == evdev.ecodes.EV_KEY and event.code in _SUPPORTED_BUTTONS:
                if self._on_button_press:
                    self._on_button_press(event.code, event.value)
            elif event.type == evdev.ecodes.EV_ABS:
                if event.code == evdev.ecodes.ABS_X:
                    self.left = (self.center(self.scale(event.value)), self.left[1])
                elif event.code == evdev.ecodes.ABS_Y:
                    self.left = (self.left[0], self.center(self.scale(event.value)))
                elif event.code == evdev.ecodes.ABS_Z:
                    self.l2 = self.scale(event.value)
                elif event.code == evdev.ecodes.ABS_RX:
                    self.right = (self.center(self.scale(event.value)), self.right[1])
                elif event.code == evdev.ecodes.ABS_RY:
                    self.right = (self.right[0], self.center(self.scale(event.value)))
                elif event.code == evdev.ecodes.ABS_RZ:
                    self.r2 = self.scale(event.value)
            elif event.type == evdev.ecodes.EV_SYN:
                if self._on_report_sync:
                    self._on_report_sync(self.left, self.right, self.l2, self.r2)
