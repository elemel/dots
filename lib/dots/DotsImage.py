class DotsImage(object):
    def __init__(self, elements):
        self.elements = tuple(elements)

    @staticmethod
    def generate(count, factory, random):
        return DotsImage(factory(random) for _ in xrange(count))

    def mutate(self, factory, random):
        mutation = random.choice([self.move_or_replace_element,
                                  self.mutate_element])
        return mutation(factory, random)

    def move_or_replace_element(self, factory, random):
        elements = list(self.elements)
        i = random.randrange(len(elements))
        j = random.randrange(len(elements))
        element = elements.pop(i)
        if random.randrange(2):
            element = factory(random)
        elements.insert(j, element)
        return DotsImage(elements)

    def mutate_element(self, factory, random):
        elements = list(self.elements)
        i = random.randrange(len(elements))
        elements[i] = elements[i].mutate(random)
        return DotsImage(elements)
