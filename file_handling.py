import os
import argparse

from random import shuffle
from pprint import pprint
from collections import defaultdict


def write_file(schedule, example):
    output_lines = [len(schedule)]

    for project in schedule:
        output_lines.append(project.name)
        output_lines.append(' '.join(project.get_people()))

    output = '\n'.join(output_lines)

    if not os.path.exists('outputs'):
        os.makedirs('outputs')
    file_path = os.path.join('outputs', f'{example}_{len(schedule)}.txt')
    with open(file_path, 'w') as f:
        f.write(output)


def load_example(example_letter):
    examples = {
        'a': 'a_an_example.in',
        'b': 'b_better_start_small.in',
        'c': 'c_collaboration.in',
        'd': 'd_dense_schedule.in',
        'e': 'e_exceptional_skills.in.txt',
        'f': 'f_find_great_mentors.in.txt'
    }

    file_name = examples[example_letter]

    return load_file(file_name)


def load_file(file_name):
    input_path = os.path.join('inputs', file_name + ".txt")

    contributors_dict = dict()
    skills_set = set()
    projects_dict = dict()
    with open(input_path, 'r') as f:
        contributors_num, projects_num = [int(n) for n in f.readline().rstrip('\n').split(' ')]
        for c in range(contributors_num):
            contributor_name, contributor_skill_num = f.readline().rstrip('\n').split(' ')
            contributor_skill_num = int(contributor_skill_num)
            skills_dict = defaultdict(lambda: 0)
            for s in range(contributor_skill_num):
                skill_name, skill_level = f.readline().rstrip('\n').split(' ')
                skill_level = int(skill_level)
                skills_dict[skill_name] = skill_level
                skills_set.add(skill_name)
            contributors_dict[contributor_name] = skills_dict
        for p in range(projects_num):
            project_name, project_days, project_score, project_best_before, project_number_of_roles = f.readline() \
                .rstrip('\n').split(' ')
            project_days, project_score, project_best_before, project_number_of_roles = int(project_days), int(
                project_score), int(project_best_before), int(project_number_of_roles)
            project_skills_list = []
            for r in range(project_number_of_roles):
                skill_name, skill_level = f.readline().rstrip('\n').split(' ')
                skill_level = int(skill_level)
                project_skills_list.append((skill_name, skill_level))
            projects_dict[project_name] = {'project_days': project_days,
                                           'project_score': project_score,
                                           'project_best_before': project_best_before,
                                           'project_number_of_roles': project_number_of_roles,
                                           'project_skills_list': project_skills_list}
    return contributors_dict, projects_dict, skills_set


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--example", help="Example Letter", type=str)
    args = parser.parse_args()

    people_dict, projects_dict, skills_set = load_example(args.example)

    pprint(people_dict)


if __name__ == "__main__":
    main()
