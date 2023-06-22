import sys
import numpy as np
def main(input_file):
    try:
        with open(input_file) as f:
            lines = f.read().splitlines()
            result = [1]
            for line in lines:
                result.append(result[-1])
                if line[:4] == 'addx':
                    value = int(line[5:])
                    result.append(result[-1] + value)
            total = 0
            for i in range(20, min(221, len(result)), 40):
                total += i * result[i - 1]
            print(total)

    except OSError as err:
        print('Error while opening file:', err)
    except ValueError as err:
        print('Error while parsing file:', err)

if __name__ == '__main__':
    default_file = '10/input.txt'
    if len(sys.argv) != 2:
        print('Using default file')
    else:
        default_file = sys.argv[1]
    main(default_file)