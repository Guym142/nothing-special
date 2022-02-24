import numpy as np
from file_handling import write_file


class Algorithm:
    def __init__(self, people_dict, projects_dict, example, write_every=10):
        self.example = example
        self.time = 0
        self.schedule = []
        self.projects = set(projects_dict.values())
        self.working_people = np.zeros(len(projects_dict))
        self.write_every = write_every

    def update_available_people(self):
        pass

    def sort_projects_by_effective_score_desc(self):

        pass

    def sort_skills_of_k_projects(self, top_k_projects):
        pass

    def find_fitting_person(self, skill):
        pass

    def set_working_people(self, project):
        pass

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
