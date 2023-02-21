import sys
import numpy as np

class Knots():
    def __init__(self, size=2, dtype=np.int8):
        self.knots = np.zeros((size, 2), dtype=np.int8)
        self.enum = {'U':(-1, 0), 'D':(1, 0), 'L':(0, -1), 'R':(0, 1)}
        self.history = set([(0, 0)])

    def distance(self, direction):
        self.knots[0] += self.enum[direction]
        for i in range(len(self.knots) - 1):
            if not (np.abs(self.knots[i] - self.knots[i+1]) >= 2).any():
                # No changes
                break
            # -2 -1 0 1 2 -> -1 -1 0 1 1
            self.knots[i+1] += np.sign(self.knots[i] - self.knots[i+1])
        self.history.add(tuple(self.knots[-1]))

    # Unused method
    def print_knots(self):
        printer = [['.' for _ in range(26)] for _ in range(16)]
        for i, (x, y) in enumerate(self.knots):
            printer[x + 10][y + 11] = str(i)
        printer[10][11] = 's'
        for line in printer:
            print(''.join(line))

    # Unused method
    def print_history(self):
        printer = [['.' for _ in range(26)] for _ in range(16)]
        for x, y in self.history:
            printer[x + 10][y + 11] = '#'
        printer[10][11] = 's'
        for line in printer:
            print(''.join(line))

def main(input_file):
    try:
        with open(input_file) as f:
            knots2 = Knots(2)
            knots10 = Knots(10)
            lines = f.read().splitlines()
            for line in lines:
                direction, value = line.split(' ')
                for _ in range(int(value)):
                    knots2.distance(direction)
                    knots10.distance(direction)
            print(f"The 2-knots rope's tail visited {len(knots2.history)} positions")
            print(f"The 10-knots rope's tail visited {len(knots10.history)} positions")

    except OSError as err:
        print('Error while opening file:', err)
    except ValueError as err:
        print('Error while parsing file:', err)

if __name__ == '__main__':
    default_file = '9/input.txt'
    if len(sys.argv) != 2:
        print('Using default file')
    else:
        default_file = sys.argv[1]
    main(default_file)