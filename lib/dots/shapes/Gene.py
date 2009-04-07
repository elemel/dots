def Gene(index):
    def get(self):
        return self.chromosome[index]
    return property(get)
