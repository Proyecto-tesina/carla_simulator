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
            self.client = carla.Client(args.host, args.port)
            self.client.set_timeout(2.0)

            self.display = pygame.display.set_mode(
                (args.width, args.height),
                pygame.HWSURFACE | pygame.DOUBLEBUF)

            self.hud = Hud(args.width, args.height)

            self.world = World(
                self.client.get_world(),
                self.hud,
                args
            )

            self.controller = args.controller(
                self.world,
                args.autopilot
            )

            self.clock = pygame.time.Clock()
            self.start()
        finally:
            self.stop()

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
