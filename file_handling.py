import os
import argparse

from random import shuffle
from pprint import pprint


def write_file():
    output = f""
    if not os.path.exists('outputs'):
        os.makedirs('outputs')
    file_path = os.path.join('outputs', f'.txt')
    with open(file_path, 'w') as f:
        f.write(output)


def load_example(example_letter):
    examples = {
        'a': '',
        'b': '',
        'c': '',
        'd': '',
        'e': '',
    }

    file_name = examples[example_letter]

    return load_file(file_name)


def load_file(file_name):
    input_path = os.path.join('input', file_name + ".txt")

    with open(input_path, 'r') as f:
        total = int(f.readline())
        for i in range(total):
            pass
            # like_line = f.readline().rstrip('\n')
            # dislike_line = f.readline().rstrip('\n')
            #
            # like_ingr = like_line.split(' ')[1:]
            # dislike_ingr = dislike_line.split(' ')[1:]
            #
            # customers.append({
            #     'like': set(like_ingr),
            #     'dislike': set(dislike_ingr)
            # })

    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--example", help="Example Letter", type=str)
    args = parser.parse_args()
    print(args.example)


if __name__ == "__main__":
    main()
