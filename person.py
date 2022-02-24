

class Person:
    count = 0

    def __init__(self, name, skills):
        self.idx = Person.count
        self.name = name
        self.skills = skills
        Person.count += 1
