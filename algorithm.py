import numpy as np
from project import Project
from file_handling import write_file, load_example
import argparse

from people import People
from person import Person
from random import randint, shuffle


class Algorithm:
    def __init__(self, persons_dict, projects_dict, skills_set, example, time_step=10):
        self.example = example
        self.time = 0
        self.schedule = []
        self.expected_score = 0
        self.time_step = time_step

        self.projects = set([Project(name, p) for name, p in projects_dict.items()])

        person_list = []
        for people_name, skills_dict in persons_dict.items():
            person_list.append(Person(people_name, skills_dict))
        self.people = People(person_list, skills_set)

        self.available_people_indicator = np.ones(len(persons_dict), dtype=bool)
        self.running_projects = set()

    def update_ending_projects(self):
        ending_projects = []
        for running_project in self.running_projects:
            running_project.days -= self.time_step
            if running_project.days <= 0:
                for working_person in running_project.contributors_set:
                    person_idx = working_person.idx
                    self.available_people_indicator[person_idx] = True
                ending_projects.append(running_project)

        # remove ending project from running projects
        self.running_projects.difference_update(ending_projects)

    def sort_projects_by_effective_score_desc(self):
        zero_scoring_projects = []
        for project in self.projects:
            project.update_effective_score(self.time)
            if project.effective_score <= 0:
                zero_scoring_projects.append(project)

        # remove zero_scoring_projects from projects
        self.projects.difference_update(zero_scoring_projects)

        projects_list = list(self.projects)
        shuffle(projects_list)
        return projects_list
        # return sorted(self.projects, key=lambda p: p.effective_score, reverse=True)

    @staticmethod
    def sort_skills_of_k_projects_desc(top_k_projects):
        skill_list = []
        for project in top_k_projects:
            for skill, level in project.skills.items():
                skill_list.append((skill, level, project))

        shuffle(skill_list)
        return skill_list
        # return sorted(skill_list, key=lambda s: s[1], reverse=True)

    def find_fitting_person(self, skill):
        available_people = self.people.mat.loc[self.available_people_indicator]
        relevant_people = available_people.loc[available_people[skill[0]] >= skill[1]]
        if len(relevant_people) == 0:
            return None

        # effective_skills = np.divide(relevant_people[skill[0]], relevant_people.sum(axis=1))
        # selected_person = effective_skills.argmin()
        rand_idx = randint(0, len(relevant_people) - 1)
        chosen_person_name = relevant_people.index[rand_idx]
        return self.people.name_to_person(chosen_person_name)

    def set_available_people(self, project, value):
        for person in project.contributors_set:
            self.available_people_indicator[person.idx] = False

    def calculate(self, top_k=1, iters=10):
        self.schedule = []
        self.time = 0

        while True:
            print(f'{self.example} | t={self.time:5d} | running projects: {len(self.running_projects)} | projects: {len(self.projects)} | score: {self.expected_score}')
            self.update_ending_projects()

            sorted_projects = self.sort_projects_by_effective_score_desc()  # also remove 0 scores
            if len(sorted_projects) == 0:
                print('no more projects. stopping!')
                break

            added_projects_count = 0
            for i in range(min(iters, len(sorted_projects) // top_k)):
                top_k_projects = sorted_projects[i*top_k:(i+1)*top_k]
                sorted_skills = self.sort_skills_of_k_projects_desc(top_k_projects)  # {name, level, project}

                for skill in sorted_skills:
                    person = self.find_fitting_person(skill)
                    if person is None:
                        continue
                    skill[2].assign_role(person, skill[0])
                    self.available_people_indicator[person.idx] = False # set as unavailable

                for project in top_k_projects:
                    if project.is_full():
                        print(f'\t- adding project with score {project.effective_score}')
                        added_projects_count += 1
                        self.expected_score += project.effective_score
                        self.schedule.append(project)
                        self.running_projects.add(project)

                        project.apply_learning()
                        self.projects.remove(project)
                    else:
                        self.set_available_people(project, True) # set as available again
                        project.clean()

            if added_projects_count > 0:
                print(f't={self.time}: added {added_projects_count} projects. expected score: {self.expected_score}')
                write_file(self.schedule, self.example, self.expected_score)

            self.time += self.time_step

        return self.schedule


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--example", help="Example Letter", type=str)
    args = parser.parse_args()

    example = 'c' # args.example

    people_dict, projects_dict, skills_set = load_example(example)

    Algorithm(people_dict, projects_dict, skills_set, example).calculate()
    # print("done!")


if __name__ == "__main__":
    main()
