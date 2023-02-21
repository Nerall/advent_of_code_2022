import sys

def compute(line):
    (first_min, first_max), (second_min, second_max) = ((int(el) for el in ss.split('-')) for ss in line.split(','))
    first_set = set(range(first_min, first_max + 1))
    second_set = set(range(second_min, second_max + 1))
    overlapping_range = first_set.issubset(second_set) or second_set.issubset(first_set)
    overlapping_pair = bool(first_set.intersection(second_set))
    return overlapping_range, overlapping_pair

def main(input_file):
    try:
        with open(input_file) as f:
            lines = f.read().splitlines()
            ranges_sum, pairs_sum = map(sum, zip(*[compute(line) for line in lines]))
            print(f'There are {ranges_sum} overlapping ranges and {pairs_sum} overlapping pairs')


    except OSError as err:
        print('Error while opening file:', err)
    except ValueError as err:
        print('Error while parsing file:', err)

if __name__ == '__main__':
    default_file = '4/input.txt'
    if len(sys.argv) != 2:
        print('Using default file')
    else:
        default_file = sys.argv[1]
    main(default_file)