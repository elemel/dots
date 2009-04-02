class DotsImage(object):
    def __init__(self, dots):
        self.dots = tuple(dots)

    @staticmethod
    def generate(count, factory, random):
        return DotsImage(factory(random) for _ in xrange(count))

    def mutate(self, factory, random):
        mutation = random.choice([self.move_or_replace_dot, self.mutate_dot])
        return mutation(factory, random)

    def move_or_replace_dot(self, factory, random):
        dots = list(self.dots)
        i = random.randrange(len(dots))
        j = random.randrange(len(dots))
        dot = dots.pop(i)
        if random.randrange(2):
            dot = factory(random)
        dots.insert(j, dot)
        return DotsImage(dots)

    def mutate_dot(self, factory, random):
        dots = list(self.dots)
        i = random.randrange(len(dots))
        dots[i] = dots[i].mutate(random)
        return DotsImage(dots)
