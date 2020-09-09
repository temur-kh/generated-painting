from service.methods import *

import copy

import cv2
import matplotlib.pyplot as plt


def generate_painting(config):
    random.seed(config.seed)
    epochs = config.epochs
    n = config.population_size
    m = n // 3
    o = config.n_mutations

    original_image = cv2.imread(config.input)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    population = generate_population(config, n, original_image)

    best_painting = None
    for epoch in range(1, epochs + 1):
        selection = select(population, m, MAX_SELECTION)
        children = crossover(config, selection, original_image)
        population.extend(children)

        selection = select(population, o, RAND_SELECTION)
        mutate(config, selection, original_image)

        painting = select(population, 1, MAX_SELECTION)[0]
        best_score = painting.score
        img = painting_to_image(painting)
        plt.imshow(img)
        plt.title(best_score)
        plt.show()

        if not best_painting or best_painting.score < population[0].score:
            best_painting = copy.deepcopy(population[0])

        population = ageing_algorithm(config, population, n)
        population = select(population, n, MAX_SELECTION)
        if config.logging_every != -1 and epoch % config.logging_every == 0:
            print(f'Epoch #{epoch}: Evolution Best Score = {best_painting.score}, Population Best Score = {best_score}')

    painting_image = painting_to_image(best_painting)
    painting_image = cv2.cvtColor(painting_image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(config.output, painting_image)
