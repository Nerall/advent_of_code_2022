import sys

def rucksack_priority(line):
    first, second = line[:len(line) // 2], line[len(line) // 2:]
    letter = next(iter(set(first).intersection(second)))
    if 'a' <= letter <= 'z':
        priority = ord(letter) - ord('a') + 1
    elif 'A' <= letter <= 'Z':
        priority = ord(letter) - ord('A') + 27
    return priority

def elves_priority(elves):
    letter = next(iter(set(elves[0]).intersection(elves[1]).intersection(elves[2])))
    if 'a' <= letter <= 'z':
        priority = ord(letter) - ord('a') + 1
    elif 'A' <= letter <= 'Z':
        priority = ord(letter) - ord('A') + 27
    return priority

def main(input_file):
    try:
        with open(input_file) as f:
            lines = f.read().splitlines()
            rucksack_sum = sum([rucksack_priority(line) for line in lines])
            elves_sum = sum([elves_priority(lines[i:i+3]) for i in range(0, len(lines), 3)])
            print('The sum of priorities of rucksack items is', rucksack_sum)
            print('The sum of priorities of elf groups is', elves_sum)


    except OSError as err:
        print('Error while opening file:', err)
    except ValueError as err:
        print('Error while parsing file:', err)

if __name__ == '__main__':
    default_file = '3/input.txt'
    if len(sys.argv) != 2:
        print('Using default file')
    else:
        default_file = sys.argv[1]
    main(default_file)