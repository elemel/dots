import math

class ShadedTriangle(object):
    # chromosome = xyrgbaxyrgbaxyrgba

    def __init__(self, chromosome):
        self.chromosome = tuple(chromosome)

    @staticmethod
    def generate(random):
        x, y = random.random(), random.random()
        radius = random.random() ** 3
        color = tuple(random.random() for _ in xrange(4))
        chromosome = []
        for _ in xrange(3):
            angle = 2 * math.pi * random.random()
            chromosome.append(x + radius * math.cos(angle))
            chromosome.append(y + radius * math.sin(angle))
            chromosome.extend(color)
        return ShadedTriangle(chromosome)

    def mutate(self, random):
        chromosome = list(self.chromosome)
        i = random.randrange(len(chromosome))
        chromosome[i] += random.choice([-1, 1]) * random.random() ** 3
        chromosome[i] = max(0, min(chromosome[i], 1))
        return ShadedTriangle(chromosome)

    def draw(self, graphics):
        graphics.draw_shaded_triangle(self.chromosome)
