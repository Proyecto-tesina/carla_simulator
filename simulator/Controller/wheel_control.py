import math
import sys

from Controller.keyboard_control import KeyboardControl

if sys.version_info >= (3, 0):
    from configparser import ConfigParser
else:
    from ConfigParser import RawConfigParser as ConfigParser

import pygame


class WheelControl(KeyboardControl):
    def __init__(self, world, start_in_autopilot):
        super().__init__(world, start_in_autopilot)
        pygame.joystick.init()

        joystick_count = pygame.joystick.get_count()
        if joystick_count > 1:
            raise ValueError("Please Connect Just One Joystick")

        self._joystick = pygame.joystick.Joystick(0)
        self._joystick.init()

        self._parser = ConfigParser()
        self._parser.read("./simulator/wheel_config.ini")
        self._steer_idx = self._parser.getint("G29 Racing Wheel", "steering_wheel")
        self._brake_idx = self._parser.getint("G29 Racing Wheel", "brake")
        self._reverse_idx = self._parser.getint("G29 Racing Wheel", "reverse")
        self._throttle_idx = self._parser.getint("G29 Racing Wheel", "throttle")
        self._handbrake_idx = self._parser.getint("G29 Racing Wheel", "handbrake")

        self.simple_joybuttons_events = {
            0: world.restart,
            9: world.hud.toggle_info,
            2: world.camera_manager.toggle_camera,
            23: world.camera_manager.next_sensor,
            3: world.next_weather,
        }

    def check_controller_keys(self, event, client, world):
        super().check_controller_keys(event, client, world)
        if event.type == pygame.JOYBUTTONDOWN:
            try:
                self.simple_joybuttons_events[event.button]()
            except KeyError:
                pass
            if event.button == self._reverse_idx:
                self._control.gear = 1 if self._control.reverse else -1

    def _parse_vehicle_keys(self, milliseconds):
        super()._parse_vehicle_keys(milliseconds)

        numAxes = self._joystick.get_numaxes()
        jsInputs = [float(self._joystick.get_axis(i)) for i in range(numAxes)]
        jsButtons = [
            float(self._joystick.get_button(i))
            for i in range(self._joystick.get_numbuttons())
        ]

        # Custom function to map range of inputs [1, -1] to outputs [0, 1]
        # i.e 1 from inputs means nothing is pressed
        # For the steering, it seems fine as it is
        K1 = 1.0  # 0.55
        steerCmd = K1 * math.tan(1.1 * jsInputs[self._steer_idx])

        K2 = 1.6  # 1.6
        throttleCmd = (
            K2
            + (2.05 * math.log10(-0.7 * jsInputs[self._throttle_idx] + 1.4) - 1.2)
            / 0.92
        )
        if throttleCmd <= 0:
            throttleCmd = 0
        elif throttleCmd > 1:
            throttleCmd = 1

        brakeCmd = (
            1.6
            + (2.05 * math.log10(-0.7 * jsInputs[self._brake_idx] + 1.4) - 1.2) / 0.92
        )
        if brakeCmd <= 0:
            brakeCmd = 0
        elif brakeCmd > 1:
            brakeCmd = 1

        self._control.steer = steerCmd
        self._control.brake = brakeCmd
        self._control.throttle = throttleCmd
        self._control.hand_brake = bool(jsButtons[self._handbrake_idx])

    def register_button(self, button, callback):
        self.simple_joybuttons_events.update({button: callback})
