from person import Person


class Project:
    def __init__(self, name: str, project_dict: dict):
        self.name = name
        self.days = project_dict['project_days']
        self.score = project_dict['project_score']
        self.best_before = project_dict['project_best_before']
        self.number_of_roles = project_dict['project_number_of_roles']
        self._skills_list = project_dict['project_number_of_roles']
        self.skills = [(skill_name, skill_level, self) for skill_name, skill_level in self._skills_list]
        self.persons_in_project = []
        self.done = False

    def add_person(self, person: Person):
        persons_in_project_num = len(self.persons_in_project)
        if self.len(self.persons_in_project) >= len(self.skills):
            raise IndexError('too many people in project')
        if person.skills[self.skills[persons_in_project_num - 1]][0] <
        self.persons_in_project.append(person)