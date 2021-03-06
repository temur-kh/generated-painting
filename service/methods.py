import random
import copy

import numpy as np
import cv2

from service.painting import Painting

MAX_SELECTION = 1
RAND_SELECTION = 2

PIXEL_MAX_SCORE = 765


def select(population, k, mode):
    if mode == MAX_SELECTION:
        population.sort(key=lambda obj: -obj.score)
        return population[:k]
    elif mode == RAND_SELECTION:
        return random.sample(population, k=k)
    else:
        raise ValueError("Invalid selection mode is provided.")


def ageing_algorithm(config, population, n):
    def age_up(painting):
        painting.age += 1
        return painting

    n_olds = sum([1 for painting in population if painting.age >= config.max_age])
    if n - len(population) > n_olds:
        return [age_up(painting) for painting in population if painting.age < config.max_age]
    else:
        result = [painting for painting in population if painting.age < config.max_age]
        olds = [painting for painting in population if painting.age >= config.max_age]
        random.shuffle(olds)
        i = 0
        while len(result) < n:
            result.append(olds[i])
            i += 1
        return [age_up(painting) for painting in result]


def crossover(config, selection, original_image):
    n_strokes = config.n_strokes
    indices = list(range(len(selection)))
    random.shuffle(indices)
    children = []
    for i in range(1, len(indices), 2):
        parent_1 = selection[indices[i - 1]]
        parent_2 = selection[indices[i]]
        parent_1.strokes.sort(key=lambda stroke: stroke.position)
        parent_2.strokes.sort(key=lambda stroke: stroke.position)
        zero_ones = [0] * (n_strokes // 2 + n_strokes % 2) + [1] * (n_strokes // 2)
        random.shuffle(zero_ones)
        child_strokes = [copy.deepcopy(parent_2.strokes[ix] if val else parent_1.strokes[ix]) for ix, val in
                         enumerate(zero_ones)]
        child = Painting(parent_1.img_size, child_strokes)
        child.score = fitness_function(child, original_image)
        children.append(child)
    return children


def mutate(config, selection, original_image):
    for painting in selection:
        for stroke in painting.strokes:
            prob = random.random()
            if prob <= config.stroke_mut_ratio:
                choice = random.randint(1, 8)
                if choice in [1, 2, 3]:
                    stroke.mutate_color()
                elif choice == 4:
                    stroke.mutate_length()
                elif choice == 5:
                    stroke.mutate_width()
                elif choice in [6, 7]:
                    stroke.mutate_position()
                else:
                    stroke.mutate_degrees()
        score = fitness_function(painting, original_image)
        painting.score = score


def generate_population(config, size, original_image):
    population = []
    for _ in range(size):
        painting = Painting.generate(config, original_image)
        score = fitness_function(painting, original_image)
        painting.score = score
        population.append(painting)
    return population


def fitness_function(painting, original_image):
    img = painting_to_image(painting)
    max_score = PIXEL_MAX_SCORE * painting.img_size[0] * painting.img_size[1]
    loss = np.sum(np.abs(img - original_image))
    return max_score - loss


def painting_to_image(painting, default_val=255):
    size = painting.img_size
    img = default_val * np.ones((size[0], size[1], 3), np.uint8)
    random.shuffle(painting.strokes)
    for stroke in painting.strokes:
        cv2.line(img, stroke.position, stroke.end_point, stroke.color, stroke.width)
    return img
