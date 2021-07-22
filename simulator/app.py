#!/usr/bin/env python

import sys
import requests as rq
from datetime import datetime

try:
    sys.path.append("../carla_API/carla-linux-x86_64.egg")
except IndexError:
    raise ImportError(
        'cannot import carla module, make sure the path to ".egg" \
        file is correct'
    )

import argparse
import logging

from Controller.wheel_control import WheelControl
from Controller.keyboard_control import KeyboardControl
from Display.resolution import CustomResolution, MultimonitorResolution
from Hud.hud import Hud
from World.world import World
from Monitors.player_monitor import PlayerMonitor
from Signals.Drt.light import AlertLight

import carla
import pygame
from pygame.locals import K_b
from pygame.locals import K_n


class App:
    BASE_URL = "http://127.0.0.1:8000"

    def __init__(self, args):
        pygame.init()
        pygame.font.init()

        self.world = None
        self.EXPERIMENT_TARGET_ID = None
        self.HAS_CONNECTION = False

        try:
            self._init_client(args)
            self._init_display(args)
            self._init_hud(args)
            self._init_world(args)
            self._init_controller(args)
            self._init_components()
            self.clock = pygame.time.Clock()
            self.start()
        finally:
            self.stop()

    def _init_client(self, args):
        self.client = carla.Client(args.host, args.port)
        self.client.set_timeout(2.0)
        try:
            experiment = rq.post(
                f"{self.BASE_URL}/experiments/",
                data={"started_at": datetime.now().isoformat()},
            )
            self.EXPERIMENT_TARGET_ID = experiment.json()["id"]
        except rq.exceptions.ConnectionError:
            self.HAS_CONNECTION = False
        else:
            self.HAS_CONNECTION = True

    def _init_display(self, args):
        self.resolution = args.resolution

        self.display = pygame.display.set_mode(
            self.resolution.size(), self.resolution.mode()
        )

    def _init_hud(self, args):
        self.hud = Hud(*self.resolution.size())

    def _init_controller(self, args):
        self.controller = args.controller(self.world, args.autopilot)

    def _init_world(self, args):
        self.world = World(self.client.get_world(), self.hud, args)

    def _init_components(self):
        player_monitor = PlayerMonitor()
        alert_light = AlertLight(*self.resolution.size())

        self.world.add_tick_subscriber(player_monitor)
        self.world.add_render_subscriber(alert_light)

        self.controller.register_event(K_n, alert_light.turn_on_by_user)
        self.controller.register_event(K_b, alert_light.turn_off_by_user)

        # Add these if playing with joystick
        # self.controller.register_button(1, alert_light.turn_on_by_user)
        # self.controller.register_button(6, alert_light.turn_on_by_user)

    def start(self):
        while True:
            self.clock.tick_busy_loop(60)
            if self.controller.check_events(self.client, self.world, self.clock):
                return
            self.world.tick(self.clock)
            self.world.render(self.display)
            pygame.display.flip()

    def stop(self):
        if self.world and self.world.recording_enabled:
            self.client.stop_recorder()

        if self.world is not None:
            self.world.destroy()

        if self.HAS_CONNECTION:
            rq.patch(f"{self.BASE_URL}/experiments/{self.EXPERIMENT_TARGET_ID}/end/")
        pygame.quit()


def main():
    argparser = argparse.ArgumentParser(description="CARLA Manual Control Client")
    argparser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        dest="info",
        help="print experiment information",
    )
    argparser.add_argument(
        "--host",
        metavar="H",
        default="127.0.0.1",
        help="IP of the host server (default: 127.0.0.1)",
    )
    argparser.add_argument(
        "-p",
        "--port",
        metavar="P",
        default=2000,
        type=int,
        help="TCP port to listen to (default: 2000)",
    )
    argparser.add_argument(
        "-a", "--autopilot", action="store_true", help="enable autopilot"
    )
    argparser.add_argument(
        "--rolename",
        metavar="NAME",
        default="hero",
        help='actor role name (default: "hero")',
    )
    argparser.add_argument(
        "--gamma",
        default=2.2,
        type=float,
        help="Gamma correction of the camera (default: 2.2)",
    )
    argparser.add_argument(
        "-w",
        "--wheel",
        action="store_true",
        help="Enable manual control steering wheel",
    )
    argparser.add_argument(
        "--res",
        metavar="WIDTHxHEIGHT",
        default="1280x720",
        help="window resolution (default: 1280x720)",
    )
    argparser.add_argument(
        "--multimonitor",
        action="store_true",
        help="Multimonitor window resolution, extends display in all monitors",
    )

    args = argparser.parse_args()

    if args.multimonitor:
        args.resolution = MultimonitorResolution()
    else:
        width, height = [int(x) for x in args.res.split("x")]
        args.resolution = CustomResolution(width, height)

    args.controller = WheelControl if args.wheel else KeyboardControl

    log_level = logging.INFO if args.info else logging.WARNING
    logging.basicConfig(format="%(levelname)s: %(message)s", level=log_level)

    logging.info("listening to server %s:%s", args.host, args.port)

    try:
        with open("./instructions.txt", "r") as file:
            print(file.read())
    except FileNotFoundError:
        logging.warning("Couldn't open instructions file")

    try:
        App(args)
    except KeyboardInterrupt:
        print("\nCancelled by user. Bye!")


if __name__ == "__main__":

    main()
