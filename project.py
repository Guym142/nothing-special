from person import Person


class Project:
    def __init__(self, name: str, project_dict: dict):
        self.name = name
        self.days = project_dict['project_days']
        self.score = project_dict['project_score']
        self.best_before = project_dict['project_best_before']
        self.number_of_roles = project_dict['project_number_of_roles']
        self._skills_list = project_dict['project_skills_list']
        self.skills = [(skill_name, skill_level, self) for skill_name, skill_level in self._skills_list]
        self.persons_in_project = [None] * len(self._skills_list)
        self.skills_name = [s[0] for s in self._skills_list]

    def add_person(self, person: Person, skill: str):
        skill_id = self.skills_name.index(skill)
        if skill_id is None:
            raise ValueError('skill not found')
        # persons_in_project_num = len(self.persons_in_project)
        # if len(self.persons_in_project) >= len(self.skills):
        #     raise IndexError('too many persons in project')
        # if person.skills[self.skills[persons_in_project_num - 1][0]] + 1 < self.skills[persons_in_project_num - 1][1]:
        #     raise IndexError('person is unfit for assignment')
        self.persons_in_project[skill_id] = person

    def is_full(self) -> bool:
        for person in self.persons_in_project:
            if person is None:
                return False
        return True

    def add_one_to_peoples_skills(self):
        for i, person in enumerate(self.persons_in_project):
            if person is None:
                raise ValueError('project not full')
            if (person.skills[self.skills[i][0]] == self.skills[i][1]) or (
                    person.skills[self.skills[i][0]] + 1 == self.skills[i][1]):
                person.skills[self.skills[i][0]] += 1

    def clean(self):
        self.persons_in_project = [None] * len(self._skills_list)
