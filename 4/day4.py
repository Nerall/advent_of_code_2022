import sys

def compute(lines):
    overlapping_ranges = 0
    overlapping_pairs = 0
    for line in lines:
        (first_min, first_max), (second_min, second_max) = ((int(el) for el in ss.split('-')) for ss in line.split(','))
        first_set = set(range(first_min, first_max + 1))
        second_set = set(range(second_min, second_max + 1))
        if first_set.issubset(second_set) or second_set.issubset(first_set):
            overlapping_ranges += 1
        if first_set.intersection(second_set):
            overlapping_pairs += 1
    print(f'There are {overlapping_ranges} overlapping ranges and {overlapping_pairs} overlapping pairs')

def main(input_file):
    try:
        with open(input_file) as f:
            compute(f.read().splitlines())

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