import pygame


class HelpText(object):
    def __init__(self, font, width, height):
        lines = self._get_help_file().split('\n')
        self.font = font
        self.dim = (1200, len(lines) * 22 + 12)
        self.pos = (0.5 * width - 0.5 *
                    self.dim[0], 0.5 * height - 0.5 * self.dim[1])
        self.seconds_left = 0
        self.surface = pygame.Surface(self.dim)
        self.surface.fill((0, 0, 0, 0))
        for n, line in enumerate(lines):
            text_texture = self.font.render(line, True, (255, 255, 255))
            self.surface.blit(text_texture, (22, n * 22))
            self._render = False
        self.surface.set_alpha(220)

    def _get_help_file(self):
        try:
            with open('./simulator/instructions.txt', 'r') as file:
                return file.read()
        except FileNotFoundError:
            return 'There was an error when looking for the instructions file'

    def toggle(self):
        self._render = not self._render

    def render(self, display):
        if self._render:
            display.blit(self.surface, self.pos)
