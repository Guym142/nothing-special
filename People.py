from typing import List

from person import Person

import pandas as pd


class People:
    def __init__(self, people: List[Person], skills_set: set):
        self.people = people
        self.skills_list = list(skills_set)
        self.persons_names = [p.name for p in people]
        self.person_to_ind_dict = {p: i for i, p in enumerate(self.persons_names)}
        self.mat = pd.DataFrame({p.name: self._skills_dict_to_list(p.skills) for p in people},
                                columns=self.skills_list).set_index(
            self.persons_names)

    def _skills_dict_to_list(self, skills_dict: dict) -> list:
        return [skills_dict[skill] for skill in self.skills_list]

    def name_to_person(self, name: str):
        return self.people[self.person_to_ind_dict[name]]
