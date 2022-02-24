import numpy as np

from People import People
from file_handling import write_file
from person import Person


class Algorithm:
    def __init__(self, persons_dict, projects_dict, skills_set, example, write_every=10):
        self.example = example
        self.time = 0
        self.schedule = []
        self.projects = set(projects_dict.values())
        person_list = []
        for people_name, skills_dict in persons_dict:
            person_list.append(Person(people_name, skills_dict))
        self.people = People(person_list, skills_set)
        self.write_every = write_every
        self.available_people = np.ones(projects_dict)

    def update_available_people(self):
        for running_project in running_projects:
            if (running_project.days == 0):
                for working_person in running_project.working_persons:
                    person_idx = working_person.idx
                    self.available_people[person_idx] = 1

    def sort_projects_by_effective_score_desc(self):

        pass

    def sort_skills_of_k_projects(self, top_k_projects):
        skill_list = []
        for project in top_k_projects:
            skill_list += project.skills

        return sorted(skill_list, key=lambda skill: skill[1])

    def find_fitting_person(self, skill):

        available_people = self.people.mat.loc[self.available_people]
        relevant_people = available_people.loc[available_people[skill[0], :] > skill[1]]
        effective_skills = np.divide(relevant_people.iloc[skill[0]], relevant_people.sum(axis=1))
        selected_person = effective_skills.argmin()

        return self.people.name_to_person(selected_person)

    def set_working_people(self, project):
        for persons in projects.working_persons:
            self.available_people[persons.idx] = 0

    def remove_project(self, project):
        pass

    def calculate(self, top_k=1):
        self.schedule = []
        self.time = 0

        while True:
            self.update_available_people()

            sorted_projects = self.sort_projects_by_effective_score_desc()  # also remove 0 scores
            if len(sorted_projects):
                break

            top_k_projects = sorted_projects[:top_k]

            sorted_skills = self.sort_skills_of_k_projects(top_k_projects)  # {name, level, project}

            for skill in sorted_skills:
                person = self.find_fitting_person(skill)
                skill.projects.add_person(person)

            for project in top_k_projects:
                if project.is_full():
                    self.schedule.append(project)
                    self.set_working_people(project)
                    project.add_one_to_peoples_skills()
                    self.remove_project(project)
                else:
                    project.clean()

            if (self.time + 1) % self.write_every == 0:
                write_file(self.schedule, self.example)

            self.time += 1

        return self.schedule
