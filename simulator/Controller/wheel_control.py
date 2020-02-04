from Controller.keyboard_control import KeyboardControl

import math

import sys

if sys.version_info >= (3, 0):
    from configparser import ConfigParser
else:
    from ConfigParser import RawConfigParser as ConfigParser

try:
    import pygame
except ImportError:
    raise RuntimeError(
        'cannot import pygame, make sure pygame package is installed')


class WheelControl(KeyboardControl):
    def __init__(self, world, start_in_autopilot):
        super(WheelControl, self).__init__(world, start_in_autopilot)
        pygame.joystick.init()

        joystick_count = pygame.joystick.get_count()
        if joystick_count > 1:
            raise ValueError("Please Connect Just One Joystick")

        self._joystick = pygame.joystick.Joystick(0)
        self._joystick.init()

        self._parser = ConfigParser()
        self._parser.read('wheel_config.ini')
        self._steer_idx = self._parser.getint(
            'G29 Racing Wheel', 'steering_wheel')
        self._throttle_idx = self._parser.getint(
            'G29 Racing Wheel', 'throttle')
        self._brake_idx = self._parser.getint('G29 Racing Wheel', 'brake')
        self._reverse_idx = self._parser.getint('G29 Racing Wheel', 'reverse')
        self._handbrake_idx = self._parser.getint(
            'G29 Racing Wheel', 'handbrake')
        self._drt_action_idx = self._parser.getint(
            'G29 Racing Wheel', 'drt_action')

    def hook_parse_events(self, world, event):
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:
                world.restart()
            elif event.button == 9:
                world.hud.toggle_info()
            elif event.button == 2:
                world.camera_manager.toggle_camera()
            elif event.button == 3:
                world.next_weather()
            elif event.button == self._drt_action_idx:
                world.hud.drt_alert.toggle()
            elif event.button == self._reverse_idx:
                self._control.gear = 1 if self._control.reverse else -1
            elif event.button == 23:
                world.camera_manager.next_sensor()

    def _parse_vehicle(self):
        numAxes = self._joystick.get_numaxes()
        jsInputs = [float(self._joystick.get_axis(i)) for i in range(numAxes)]
        # print (jsInputs)
        jsButtons = [float(self._joystick.get_button(i)) for i in
                     range(self._joystick.get_numbuttons())]

        # Custom function to map range of inputs [1, -1] to outputs [0, 1]
        # i.e 1 from inputs means nothing is pressed
        # For the steering, it seems fine as it is
        K1 = 1.0  # 0.55
        steerCmd = K1 * math.tan(1.1 * jsInputs[self._steer_idx])

        K2 = 1.6  # 1.6
        throttleCmd = K2 + (2.05 * math.log10(
            -0.7 * jsInputs[self._throttle_idx] + 1.4) - 1.2) / 0.92
        if throttleCmd <= 0:
            throttleCmd = 0
        elif throttleCmd > 1:
            throttleCmd = 1

        brakeCmd = 1.6 + (2.05 * math.log10(
            -0.7 * jsInputs[self._brake_idx] + 1.4) - 1.2) / 0.92
        if brakeCmd <= 0:
            brakeCmd = 0
        elif brakeCmd > 1:
            brakeCmd = 1

        self._control.steer = steerCmd
        self._control.brake = brakeCmd
        self._control.throttle = throttleCmd

        # toggle = jsButtons[self._reverse_idx]

        self._control.hand_brake = bool(jsButtons[self._handbrake_idx])
