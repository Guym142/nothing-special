from person import Person


class Project:
    def __init__(self, name: str, project_dict: dict):
        self.name = name
        self.days = project_dict['days']
        self.score = project_dict['score']
        self.best_before = project_dict['best_before']
        self.skills = project_dict['skills']

        self.effective_score = None

        self.skills_assignment = {} # keeps order
        self.contributors_set = set()
        self.clean()

    def update_effective_score(self, time):
        self.effective_score = self.score - min(0, self.best_before - (time + self.days))

    def _is_fit_for_assignment(self, person: Person, skill):
        person_level = person.skills[skill]
        project_level = self.skills[skill]
        if person_level < project_level:
            # person is unfit, check if can be mentored
            if project_level - person_level == 1:
                # only one off from the required skill
                for possible_mentor in self.contributors_set:
                    if possible_mentor[skill] >= project_level:
                        # found mentor
                        return True
        return False

    def assign_role(self, person: Person, skill: str):
        if skill not in self.skills_assignment:
            raise ValueError('role not in project')
        elif self.skills_assignment[skill] is not None:
            raise ValueError('role already assigned')

        if self._is_fit_for_assignment(person, skill):
            raise ValueError('person is unfit for assignment')

        if person in self.contributors_set:
            raise ValueError('person is already assigned to project on a different skill')

        self.skills_assignment[skill] = person
        self.contributors_set.add(person)

    def is_full(self) -> bool:
        for person in self.skills_assignment.values():
            if person is None:
                return False
        return True

    def apply_learning(self):
        for skill, person in self.skills_assignment.items():
            person_level = person.skills[skill]
            project_level = self.skills[skill]

            if person_level - project_level <= 1:
                # person is learning if diff is 0 or 1
                person.skills[skill] += 1

    def clean(self):
        self.skills_assignment = dict.fromkeys(self.skills.keys())
        self.contributors_set = set()

    def get_contributors_names_in_order(self):
        return [cont.name for cont in self.skills_assignment.values()]
