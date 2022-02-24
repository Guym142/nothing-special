import numpy as np
from project import Project
from file_handling import write_file


class Algorithm:
    def __init__(self, people_dict, projects_dict, example, write_every=10):
        self.example = example
        self.time = 0
        self.schedule = []
        self.projects = set([Project(name, p) for name, p in projects_dict.items()])

        self.write_every = write_every
        self.available_people = np.ones(projects_dict)
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
        skill_idx = self.people.skill_index(skill)  # return skill index
        available_people = self.people[:, self.available_people]
        relevant_people = available_people[:, available_people[skill_idx, :] > skill[1]]
        effective_skills = np.divide(relevant_people[skill_idx, :], sum(relevant_people, axis=1))

        selected_person_idx = np.argmin(effective_skills)
        return self.people.person_by_index(selected_person_idx)

    def set_working_people(self, project):
        for person in project.persons_in_project:
            self.available_people[person.idx] = 0

    def calculate(self, top_k=1, iters=1):
        self.schedule = []
        self.time = 0

        while True:
            self.update_available_people()

            sorted_projects = self.sort_projects_by_effective_score_desc()  # also remove 0 scores
            if len(sorted_projects):
                break

            for i in range(min(iters, len(sorted_projects) // top_k)):
                top_k_projects = sorted_projects[i*top_k:(i+1)*top_k]
                sorted_skills = self.sort_skills_of_k_projects(top_k_projects)  # {name, level, project}

                for skill in sorted_skills:
                    person = self.find_fitting_person(skill)
                    skill.projects.add_person(person)

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
