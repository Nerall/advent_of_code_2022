import sys

def parser(buffer):
    elves = buffer.split('\n\n')
    calories = [0] * len(elves)

    for i, elf in enumerate(elves):
        calories[i] = sum((int(el) for el in elf.splitlines()))

    top_3 = sorted(calories)[-3:]

    print(f'The elf with the most calories carries a {max(calories)} calories.')
    print(f'The three elves with the most calories carry a total of {sum(top_3)} calories.')

def main(input_file):
    try:
        with open(input_file) as f:
            parser(f.read())

    except OSError as err:
        print('Error while opening file:', err)

    except ValueError as err:
        print('Error while parsing file:', err)

if __name__ == '__main__':
    default_file = '1/input.txt'
    if len(sys.argv) != 2:
        print('Using default file')
    else:
        default_file = sys.argv[1]
    main(default_file)