import numpy as np


class Algorithm():
    def __init__(self, people_dict, projects_dict):
        self.time = 0
        self.projects = set(projects_dict.values())
        self.working_people = np.zeros(len(projects_dict))
        self.available_people = np.ones(projects_dict)
        self.running_projects = set()

    def update_available_people(self):
        for running_project in running_projects:
            if(running_project.days == 0):
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
        skill_idx = self.people.skill_index(skill)  # return skill index
        available_people = self.people[:, self.available_people]
        relevant_people = available_people[:, available_people[skill_idx, :] > skill[1]]
        effective_skills = np.divide(relevant_people[skill_idx, :], sum(relevant_people, axis=1))

        selected_person_idx = np.argmin(effective_skills)
        return self.people.person_by_index(selected_person_idx)



    def set_working_people(self, project):
        for persons in projects.working_persons:
            self.available_people[persons.idx] = 0

    def remove_project(self, project):
        pass

    def calculate(self, top_k=1):
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
                skill.project.add_person(person)

            for project in top_k_projects:
                if project.is_full():
                    self.set_working_people(project)
                    project.add_one_to_peoples_skills()
                    self.remove_project(project)
                else:
                    project.clean()

            self.time += 1