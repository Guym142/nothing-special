import os
import argparse

from random import shuffle
from pprint import pprint
from collections import defaultdict


def write_file(schedule, example, score):
    output_lines = [str(len(schedule))]

    for project in schedule:
        output_lines.append(project.name)
        output_lines.append(' '.join(project.get_contributors_names_in_order()))

    output = '\n'.join(output_lines)

    if not os.path.exists('outputs'):
        os.makedirs('outputs')
    file_path = os.path.join('outputs', f'{example}_len={len(schedule)}_score={score}.txt')
    with open(file_path, 'w') as f:
        f.write(output)


def load_example(example_letter):
    examples = {
        'a': 'a_an_example.in',
        'b': 'b_better_start_small.in',
        'c': 'c_collaboration.in',
        'd': 'd_dense_schedule.in',
        'e': 'e_exceptional_skills.in',
        'f': 'f_find_great_mentors.in'
    }

    file_name = examples[example_letter]

    return load_file(file_name)


def load_file(file_name):
    input_path = os.path.join('inputs', file_name + ".txt")

    contributors_dict = dict()
    projects_dict = dict()
    skills_set = set()

    with open(input_path, 'r') as f:
        # first line of file
        contributors_num, projects_num = [int(n) for n in f.readline().rstrip('\n').split(' ')]

        # contributors (people)
        for c in range(contributors_num):
            # contributor first line
            cont_first_line = f.readline().rstrip('\n').split(' ')
            cont_name, cont_skill_num = cont_first_line[0], int(cont_first_line[1])

            # contributor's skills
            skills_dict = defaultdict(int)
            for s in range(cont_skill_num):
                skill_line = f.readline().rstrip('\n').split(' ')
                skill_name, skill_level = skill_line[0], int(skill_line[1])

                skills_dict[skill_name] = skill_level
                skills_set.add(skill_name)

            # append contributor
            contributors_dict[cont_name] = skills_dict

        # projects
        for p in range(projects_num):
            project_first_line = f.readline().rstrip('\n').split(' ')
            project_name, project_days, project_score, project_best_before, project_number_of_roles = \
                project_first_line[0], int(project_first_line[1]), int(project_first_line[2]), \
                int(project_first_line[3]), int(project_first_line[4])

            # project's skills (roles)
            project_skills_dict = {}
            for r in range(project_number_of_roles):
                skills_line = f.readline().rstrip('\n').split(' ')
                skill_name, skill_level = skills_line[0], int(skills_line[1])

                project_skills_dict[skill_name] = skill_level

            # append project
            projects_dict[project_name] = {
                'days': project_days,
                'score': project_score,
                'best_before': project_best_before,
                'skills': project_skills_dict
            }

    return contributors_dict, projects_dict, skills_set


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--example", help="Example Letter", type=str)
    args = parser.parse_args()

    people_dict, projects_dict, skills_set = load_example(args.example)

    pprint(people_dict)


if __name__ == "__main__":
    main()
