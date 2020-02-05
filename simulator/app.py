#!/usr/bin/env python

# Copyright (c) 2019 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

# Allows controlling a vehicle with a keyboard. For a simpler and more
# documented example, please take a look at tutorial.py.


# ==============================================================================
# -- find carla module ---------------------------------------------------------
# ==============================================================================


import glob
import os
import sys


try:
    sys.path.append(glob.glob('./Carla/PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass


# ==============================================================================
# -- imports -------------------------------------------------------------------
# ==============================================================================


import argparse
import logging

from Controller.wheel_control import WheelControl
from Controller.keyboard_control import KeyboardControl

from Display.resolution import CustomResolution, MultimonitorResolution

import carla

from Hud.hud import Hud

from World.world import World

try:
    import pygame
except ImportError:
    raise RuntimeError(
        'cannot import pygame, make sure pygame package is installed')


class App():

    def __init__(self, args):
        pygame.init()
        pygame.font.init()

        self.world = None

        try:
            self.__init_client(args)

            self.__init_display(args)

            self.__init_hud(args)

            self.__init_world(args)

            self.__init_controller(args)

            self.clock = pygame.time.Clock()
            self.start()
        finally:
            self.stop()

    def __init_client(self, args):
        self.client = carla.Client(args.host, args.port)
        self.client.set_timeout(2.0)

    def __init_display(self, args):
        self.resolution = args.resolution

        self.display = pygame.display.set_mode(
            self.resolution.size(),
            pygame.HWSURFACE | pygame.DOUBLEBUF
        )

    def __init_hud(self, args):
        self.hud = Hud(*self.resolution.size())

    def __init_controller(self, args):
        self.controller = args.controller(
            self.world,
            args.autopilot
        )

    def __init_world(self, args):
        self.world = World(
            self.client.get_world(),
            self.hud,
            args
        )

    def start(self):
        while True:
            self.clock.tick_busy_loop(60)
            if self.controller.parse_events(self.client, self.world, self.clock):
                return
            self.world.tick(self.clock)
            self.world.render(self.display)
            pygame.display.flip()

    def stop(self):
        if (self.world and self.world.recording_enabled):
            self.client.stop_recorder()

        if self.world is not None:
            self.world.destroy()

        pygame.quit()


# ==============================================================================
# -- main() --------------------------------------------------------------------
# ==============================================================================


def main():
    argparser = argparse.ArgumentParser(
        description='CARLA Manual Control Client')
    argparser.add_argument(
        '-v', '--verbose',
        action='store_true',
        dest='debug',
        help='print debug information')
    argparser.add_argument(
        '--host',
        metavar='H',
        default='127.0.0.1',
        help='IP of the host server (default: 127.0.0.1)')
    argparser.add_argument(
        '-p', '--port',
        metavar='P',
        default=2000,
        type=int,
        help='TCP port to listen to (default: 2000)')
    argparser.add_argument(
        '-a', '--autopilot',
        action='store_true',
        help='enable autopilot')
    argparser.add_argument(
        '--filter',
        metavar='PATTERN',
        default='vehicle.*',
        help='actor filter (default: "vehicle.*")')
    argparser.add_argument(
        '--rolename',
        metavar='NAME',
        default='hero',
        help='actor role name (default: "hero")')
    argparser.add_argument(
        '--gamma',
        default=2.2,
        type=float,
        help='Gamma correction of the camera (default: 2.2)')
    argparser.add_argument(
        '-w', '--wheel',
        action='store_true',
        help='Enable manual control steering wheel')
    argparser.add_argument(
        '--res',
        metavar='WIDTHxHEIGHT',
        default='1280x720',
        help='window resolution (default: 1280x720)')
    argparser.add_argument(
        '--multimonitor',
        action='store_true',
        help='Multimonitor window resolution, extends display in all monitors')

    args = argparser.parse_args()

    if args.multimonitor:
        args.resolution = MultimonitorResolution()
    else:
        width, height = [int(x) for x in args.res.split('x')]
        args.resolution = CustomResolution(width, height)

    args.controller = WheelControl if args.wheel else KeyboardControl

    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(format='%(levelname)s: %(message)s', level=log_level)

    logging.info('listening to server %s:%s', args.host, args.port)

    try:
        instructions = open('./simulator/instructions.txt', 'r')
        print(instructions.read())
    except FileNotFoundError:
        logging.warning('Couldn\'t open instructions file')

    try:
        App(args)

    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')


if __name__ == '__main__':

    main()
