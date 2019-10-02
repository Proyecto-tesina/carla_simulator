class FifoStrategy:
    """
    Args:
        carousel: the carousel on which the strategy operates
    """
    def __init__(self, carousel):
        self.carousel = carousel
        self.pos = -1

    def next_image(self):
        self.pos += 1
        if self.pos > len(self.carousel.images_to_roll) - 1:
            self.pos = 0
        return self.pos

    def prev_image(self):
        self.pos -= 1
        if self.pos < 0:
            self.pos = len(self.carousel.images_to_roll) - 1
        return self.pos
