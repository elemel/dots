from dots.Dot import Dot

class DotsImage(object):
    def __init__(self, dots):
        self.dots = tuple(dots)

    @staticmethod
    def generate(dot_count, random):
        return DotsImage(Dot.generate(random) for _ in xrange(dot_count))

    def mutate(self, random):
        mutation = random.choice([self.move_or_replace_dot, self.mutate_dot])
        return mutation(random)

    def move_or_replace_dot(self, random):
        dots = list(self.dots)
        i = random.randrange(len(dots))
        j = random.randrange(len(dots))
        dot = dots.pop(i)
        if random.randrange(2):
            dot = Dot.generate(random)
        dots.insert(j, dot)
        return DotsImage(dots)

    def mutate_dot(self, random):
        dots = list(self.dots)
        i = random.randrange(len(dots))
        dots[i] = dots[i].mutate(random)
        return DotsImage(dots)
