class Shape(object):
    chromosome_len = 0

    def __init__(self, chromosome):
        self.chromosome = tuple(chromosome)

    @classmethod
    def generate(cls, random):
        chromosome = [random.random() for _ in xrange(cls.chromosome_len)]
        return cls(chromosome)

    def mutate(self, random):
        chromosome = list(self.chromosome)
        i = random.randrange(len(chromosome))
        sigma = random.choice([0.001, 0.01, 0.1])
        chromosome[i] = random.normalvariate(chromosome[i], sigma)
        chromosome[i] = max(0, chromosome[i])
        chromosome[i] = min(chromosome[i], 1)
        cls = type(self)
        return cls(chromosome)

