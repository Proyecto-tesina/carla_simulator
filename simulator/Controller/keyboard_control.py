import carla
try:
    import pygame
    from pygame.locals import KMOD_CTRL
    from pygame.locals import KMOD_SHIFT
    from pygame.locals import K_0
    from pygame.locals import K_9
    from pygame.locals import K_BACKQUOTE
    from pygame.locals import K_BACKSPACE
    from pygame.locals import K_COMMA
    from pygame.locals import K_DOWN
    from pygame.locals import K_ESCAPE
    from pygame.locals import K_F1
    from pygame.locals import K_LEFT
    from pygame.locals import K_PERIOD
    from pygame.locals import K_RIGHT
    from pygame.locals import K_SPACE
    from pygame.locals import K_TAB
    from pygame.locals import K_UP
    from pygame.locals import K_a
    from pygame.locals import K_c
    from pygame.locals import K_d
    from pygame.locals import K_h
    from pygame.locals import K_m
    from pygame.locals import K_p
    from pygame.locals import K_q
    from pygame.locals import K_r
    from pygame.locals import K_s
    from pygame.locals import K_w
    from pygame.locals import K_MINUS
    from pygame.locals import K_EQUALS
except ImportError:
    raise RuntimeError(
        'cannot import pygame, make sure pygame package is installed')


class KeyboardControl(object):
    def __init__(self, world, start_in_autopilot):
        self._autopilot_enabled = start_in_autopilot
        self._control = carla.VehicleControl()
        world.player.set_autopilot(self._autopilot_enabled)
        self._steer_cache = 0.0

        self.simple_key_events = {
            K_BACKQUOTE: world.camera_manager.next_sensor,
            K_BACKSPACE: world.restart,
            K_F1: world.hud.toggle_info,
            K_TAB: world.camera_manager.toggle_camera,
            K_c: world.next_weather,
            K_h: world.hud.help.toggle,
        }
        world.hud.notification("Press 'H' or '?' for help.", seconds=4.0)

    def check_events(self, client, world, clock):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYUP:
                escape = event.key == K_ESCAPE
                ctrl_q = event.key == K_q and pygame.key.get_mods() & KMOD_CTRL
                if escape or ctrl_q:
                    return True
            self.check_controller_keys(event, client, world)

        if not self._autopilot_enabled:
            self._parse_vehicle_keys(clock.get_time())
            self._control.reverse = self._control.gear < 0
            world.player.apply_control(self._control)

    def check_controller_keys(self, event, client, world):
        if event.type == pygame.KEYUP:
            try:
                self.simple_key_events[event.key]()
            except KeyError:
                pass

            self.parse_world_events(event, world)
            self.parse_recording_events(event, client, world)
            self.parse_vehicle_events(event, world)

    def parse_world_events(self, event, world):
        if event.key == K_c and pygame.key.get_mods() & KMOD_SHIFT:
            world.next_weather(reverse=True)
        elif event.key > K_0 and event.key <= K_9:
            world.camera_manager.set_sensor(event.key - 1 - K_0)
        elif event.key == K_p and not (pygame.key.get_mods() & KMOD_CTRL):
            self._autopilot_enabled = not self._autopilot_enabled
            world.player.set_autopilot(self._autopilot_enabled)
            world.hud.notification('Autopilot %s' % (
                'On' if self._autopilot_enabled else 'Off'))

    def parse_recording_events(self, event, client, world):
        if event.key == K_r and not (pygame.key.get_mods() & KMOD_CTRL):
            world.camera_manager.toggle_recording()
        elif event.key == K_r and (pygame.key.get_mods() & KMOD_CTRL):
            if (world.recording_enabled):
                client.stop_recorder()
                world.recording_enabled = False
                world.hud.notification("Recorder is OFF")
            else:
                client.start_recorder("manual_recording.rec")
                world.recording_enabled = True
                world.hud.notification("Recorder is ON")
        elif event.key == K_p and (pygame.key.get_mods() & KMOD_CTRL):
            # stop recorder
            client.stop_recorder()
            world.recording_enabled = False
            # work around to fix camera at start of replaying
            currentIndex = world.camera_manager.index
            world.destroy_sensors()
            # disable autopilot
            self._autopilot_enabled = False
            world.player.set_autopilot(self._autopilot_enabled)
            world.hud.notification(
                "Replaying file 'manual_recording.rec'")
            # replayer
            client.replay_file("manual_recording.rec",
                               world.recording_start, 0, 0)
            world.camera_manager.set_sensor(currentIndex)
        elif event.key == K_MINUS and (pygame.key.get_mods() & KMOD_CTRL):
            if pygame.key.get_mods() & KMOD_SHIFT:
                world.recording_start -= 10
            else:
                world.recording_start -= 1
            world.hud.notification(
                "Recording start time is %d" % (world.recording_start))
        elif event.key == K_EQUALS and (pygame.key.get_mods() & KMOD_CTRL):
            if pygame.key.get_mods() & KMOD_SHIFT:
                world.recording_start += 10
            else:
                world.recording_start += 1
            world.hud.notification(
                "Recording start time is %d" % (world.recording_start))

    def parse_vehicle_events(self, event, world):
        if event.key == K_q:
            self._control.gear = 1 if self._control.reverse else -1
        elif self._control.manual_gear_shift and event.key == K_COMMA:
            self._control.gear = max(-1, self._control.gear - 1)
        elif self._control.manual_gear_shift and event.key == K_PERIOD:
            self._control.gear = self._control.gear + 1
        elif event.key == K_m:
            self._control.manual_gear_shift = not self._control.manual_gear_shift
            self._control.gear = world.player.get_control().gear
            world.hud.notification('%s Transmission' % (
                'Manual' if self._control.manual_gear_shift else 'Automatic'))

    def _parse_vehicle_keys(self, milliseconds):
        keys = pygame.key.get_pressed()
        self._control.throttle = 1.0 if keys[K_UP] or keys[K_w] else 0.0
        steer_increment = 5e-4 * milliseconds
        if keys[K_LEFT] or keys[K_a]:
            self._steer_cache -= steer_increment
        elif keys[K_RIGHT] or keys[K_d]:
            self._steer_cache += steer_increment
        else:
            self._steer_cache = 0.0
        self._steer_cache = min(0.7, max(-0.7, self._steer_cache))
        self._control.steer = round(self._steer_cache, 1)
        self._control.brake = 1.0 if keys[K_DOWN] or keys[K_s] else 0.0
        self._control.hand_brake = keys[K_SPACE]

    def register_event(self, key, callback):
        self.simple_key_events.update({key: callback})
