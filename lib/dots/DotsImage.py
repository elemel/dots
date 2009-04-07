class DotsImage(object):
    def __init__(self, shapes):
        self.shapes = tuple(shapes)

    @staticmethod
    def generate(count, factory, random):
        return DotsImage(factory(random) for _ in xrange(count))

    def mutate(self, factory, random):
        mutation = random.choice([self.move_or_replace_shape,
                                  self.mutate_shape])
        return mutation(factory, random)

    def move_or_replace_shape(self, factory, random):
        shapes = list(self.shapes)
        i = random.randrange(len(shapes))
        j = random.randrange(len(shapes))
        shape = shapes.pop(i)
        if random.randrange(2):
            shape = factory(random)
            if random.randrange(2):
                j = len(shapes)
        shapes.insert(j, shape)
        return DotsImage(shapes)

    def mutate_shape(self, factory, random):
        shapes = list(self.shapes)
        i = random.randrange(len(shapes))
        shapes[i] = shapes[i].mutate(random)
        return DotsImage(shapes)
