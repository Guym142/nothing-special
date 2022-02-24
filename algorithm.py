import numpy as np
from project import Project
from file_handling import write_file, load_example
import argparse

from People import People
from file_handling import write_file
from person import Person


class Algorithm:
    def __init__(self, persons_dict, projects_dict, skills_set, example, write_every=1):
        self.example = example
        self.time = 0
        self.schedule = []
        self.projects = set([Project(name, p) for name, p in projects_dict.items()])
        person_list = []
        for people_name, skills_dict in persons_dict.items():
            person_list.append(Person(people_name, skills_dict))
        self.people = People(person_list, skills_set)
        self.write_every = write_every
        self.available_people = np.ones(len(projects_dict), dtype=bool)
        self.running_projects = set()

    def update_available_people(self):
        for running_project in self.running_projects:
            running_project.days -= 1
            if running_project.days == 0:
                for working_person in running_project.working_persons:
                    person_idx = working_person.idx
                    self.available_people[person_idx] = 1
                self.running_projects.remove(running_project)

    def sort_projects_by_effective_score_desc(self):
        return sorted(self.projects, key=lambda p: min(0, p.best_before - (self.time + p.days)))

    def sort_skills_of_k_projects(self, top_k_projects):
        skill_list = []
        for project in top_k_projects:
            skill_list += project.skills

        return sorted(skill_list, key=lambda skill: skill[1])

    def find_fitting_person(self, skill):

        tmp = self.people.mat.loc[self.available_people]
        relevant_people = tmp.loc[tmp[skill[0]] > skill[1]]
        if len(relevant_people) == 0:
            return None

        # effective_skills = np.divide(relevant_people[skill[0]], relevant_people.sum(axis=1))
        # selected_person = effective_skills.argmin()
        bla = relevant_people.iloc[0].index
        return self.people.name_to_person(bla)

    def set_working_people(self, project):
        for person in project.persons_in_project:
            self.available_people[person.idx] = 0

    def calculate(self, top_k=1, iters=1):
        self.schedule = []
        self.time = 0

        while True:
            self.update_available_people()

            sorted_projects = self.sort_projects_by_effective_score_desc()  # also remove 0 scores
            if len(sorted_projects) == 0:
                break

            for i in range(min(iters, len(sorted_projects) // top_k)):
                top_k_projects = sorted_projects[i*top_k:(i+1)*top_k]
                sorted_skills = self.sort_skills_of_k_projects(top_k_projects)  # {name, level, project}

                for skill in sorted_skills:
                    person = self.find_fitting_person(skill)
                    if person is None:
                        continue
                    skill[2].add_person(person)

                for project in top_k_projects:
                    if project.is_full():
                        self.schedule.append(project)
                        self.running_projects.add(project)

                        self.set_working_people(project)
                        project.add_one_to_peoples_skills()
                        self.projects.remove(project)
                    else:
                        project.clean()

            if (self.time + 1) % self.write_every == 0:
                write_file(self.schedule, self.example)

            self.time += 1

        return self.schedule


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--example", help="Example Letter", type=str)
    args = parser.parse_args()

    example = 'a' # args.example

    people_dict, projects_dict, skills_set = load_example(example)

    Algorithm(people_dict, projects_dict, skills_set, example).calculate()
    print("done!")


if __name__ == "__main__":
    main()
