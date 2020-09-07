import random

import numpy as np
import matplotlib.pyplot as plt


class Painting:
    def __init__(self, img_size, strokes):
        self.img_size = img_size
        self.strokes = strokes
        self.score = None

    @staticmethod
    def generate(config, original_image):
        n_strokes = config.n_strokes
        h, w, c = original_image.shape
        img_size = (h, w)
        n_pxs = h * w
        strokes = []
        for i in range(n_strokes):
            position = random.randint(0, n_pxs - 1)
            y = position // w
            x = position % w
            color = tuple(int(val) for val in original_image[y, x])
            stroke = Stroke.generate(config, img_size, color=color, position=(x, y))
            strokes.append(stroke)
        return Painting(img_size, strokes)


class Stroke:
    def __init__(self, config, img_size, color, length, width, position, degrees):
        self.img_size = img_size
        self.color = color
        self.length = length
        self.width = width
        self.position = position
        self.degrees = degrees

        self.color_max_step = config.color_max_step
        self.length_max_step = config.length_max_step
        self.length_range = (config.length_min, config.length_max)
        self.width_max_step = config.width_max_step
        self.width_range = (config.width_min, config.width_max)
        self.position_max_step = config.position_max_step
        self.degrees_max_step = config.degrees_max_step

    @staticmethod
    def generate(config, img_size, color=None, length=None, width=None, position=None, degrees=None):
        if not color:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        if not length:
            length = random.randint(config.length_min, config.length_max)
        if not width:
            width = random.randint(config.width_min, config.width_max)
        if not position:
            position = (random.randint(0, img_size[1] - 1), random.randint(0, img_size[0] - 1))
        if not degrees:
            degrees = random.randint(0, 359)
        return Stroke(config, img_size, color, length, width, position, degrees)

    def mutate_color(self):
        new_r, new_g, new_b = self.color
        choice = random.randint(1, 3)
        if choice == 1:
            d_r = random.randint(-self.color_max_step, self.color_max_step)
            new_r = min(255, max(0, self.color[0] + d_r))
        elif choice == 2:
            d_g = random.randint(-self.color_max_step, self.color_max_step)
            new_g = min(255, max(0, self.color[1] + d_g))
        else:
            d_b = random.randint(-self.color_max_step, self.color_max_step)
            new_b = min(255, max(0, self.color[2] + d_b))
        self.color = (new_r, new_g, new_b)

    def mutate_length(self):
        d_l = random.randint(-self.length_max_step, self.length_max_step)
        new_length = min(self.length_range[1], max(self.length_range[0], d_l))
        self.length = new_length

    def mutate_width(self):
        d_w = random.randint(-self.width_max_step, self.width_max_step)
        new_width = min(self.width_range[1], max(self.width_range[0], d_w))
        self.width = new_width

    def mutate_position(self):
        new_x, new_y = self.position
        choice = random.randint(1, 2)
        if choice == 1:
            d_x = random.randint(-self.position_max_step, self.position_max_step)
            new_x = min(self.img_size[1] - 1, max(0, self.position[0] + d_x))
        else:
            d_y = random.randint(-self.position_max_step, self.position_max_step)
            new_y = min(self.img_size[0] - 1, max(0, self.position[1] + d_y))
        self.position = (new_x, new_y)

    def mutate_degrees(self):
        d_a = random.randint(-self.degrees_max_step, self.degrees_max_step)
        self.degrees = (self.degrees + d_a) % 360

    @property
    def end_point(self):
        angle = self.degrees / 180 * np.pi
        d_x = int(self.length * np.cos(angle))
        d_y = int(self.length * np.sin(angle))
        x = min(self.img_size[1] - 1, max(0, self.position[0] + d_x))
        y = min(self.img_size[0] - 1, max(0, self.position[1] + d_y))
        return x, y
