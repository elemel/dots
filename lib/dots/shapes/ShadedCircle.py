class ShadedCircle(object):
    def __init__(self, center, radius, color, alphas):
        self.center = tuple(center)
        self.radius = radius
        self.color = tuple(color)
        self.alphas = tuple(alphas)

    @staticmethod
    def decode(chromosome):
        center = chromosome[:2]
        radius = chromosome[2]
        color = chromosome[3:6]
        alphas = chromosome[6:]
        return ShadedCircle(center, radius, color, alphas)

    def encode(self):
        return self.center + (self.radius,) + self.color + self.alphas

    @staticmethod
    def generate(random):
        chromosome = [random.random() for _ in xrange(10)]
        chromosome[2] *= random.choice([0.001, 0.01, 0.1, 1])
        return ShadedCircle.decode(chromosome)

    def mutate(self, random):
        chromosome = list(self.encode())
        i = random.randrange(len(chromosome))
        sigma = random.choice([0.001, 0.01, 0.1, 1])
        chromosome[i] = random.normalvariate(chromosome[i], sigma)
        chromosome[i] = max(0, min(chromosome[i], 1))
        return ShadedCircle.decode(chromosome)

    def draw(self, graphics):
        graphics.draw_shaded_circle(self.center, self.radius, self.color,
                                    self.alphas)
