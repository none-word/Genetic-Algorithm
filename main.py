import numpy as np

import random
import cv2

PICTURE_SIZE = 512
POPULATION_SIZE = 64

sourceImage = cv2.imread("./me.JPG")


# function for mutation a chromosome
# return mutated chromosome
def mutate(chromosome):
    # the coordinate of new square
    square = (
        random.randint(0, 511), random.randint(0, 511)
    )

    # getting the color of the pixel with coordinate 'square' from source picfture
    color = sourceImage[square[1], square[0]]
    color = (
        int(color[0]),
        int(color[1]),
        int(color[2])
    )

    # generation of square size
    size = random.randint(5, 50)
    # drawing the square on picture
    chromosome[1] = cv2.rectangle(chromosome[1], square, (square[0] + size, square[1] + size), color, -1)
    # updating the difference from source image
    diff = get_difference(chromosome[1])
    chromosome[0] = diff
    return chromosome


# function for creation initial population
# return initial population
def create_init_population():
    # creation the clear image (just black background)
    _image = np.zeros((PICTURE_SIZE, PICTURE_SIZE, 3), np.uint8)
    # counting the difference from source image
    difference = get_difference(_image)
    # creation population of 64 identity chromosomes
    _population = np.array([[difference, _image] for _ in range(POPULATION_SIZE)], dtype="object")
    return _population


# updating the population by getting the 8 best ones and copying them 8 times
# return updated population
def selector(_population):
    # cutting of the population, remaining the best 8 ones
    _population = _population[_population[:, 0].argsort()][0:8]
    # copying the bests 8 times
    for i in range(56):
        diff = _population[i % 8][0]
        _image = _population[i % 8][1].copy()
        _population = np.append(_population, np.array([[diff, _image]], dtype="object"), axis=0)
    return _population


# fitness function
# return the difference _image from source image
def get_difference(_image):
    return np.sum((np.array(sourceImage) - np.array(_image)) **
                  2)/float(PICTURE_SIZE ** 2)


# making the mutation for whole population
# return mutated population
def mutate_population(_population):
    # updating each chromosome in population one by one
    for k in range(16):
        i = random.randint(0, 63)
        chromosome = mutate(_population[i])
        _population[i] = chromosome
    return _population


population = create_init_population()
# input of the number of iterations
x = int(input("Write the number of evolutions "))
image = []
# executing the iterations
while x != -1:
    # executing the proper number of iterations
    for i in range(x):
        # mutation and choosing the best ones
        population = mutate_population(population)
        population = selector(population)
    # show the result
    image = population[0][1]
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    x = int(input("Write the number of evolutions "))
# saving the result image
cv2.imwrite("result.jpg", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
