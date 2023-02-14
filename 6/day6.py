import sys

def main(input_file):
    try:
        with open(input_file) as f:
            buffer = f.read().rstrip()
            signal_found = False
            for i in range(len(buffer) - 3):
                last_four = buffer[i:i+4]
                last_fourteen = buffer[i:i+14]
                if len(set(last_four)) == 4 and not signal_found:
                    print('The first signal marker is after character', i + 4)
                    signal_found = True
                if len(set(last_fourteen)) == 14:
                    print('The first message marker is after character', i + 14)
                    break

    except OSError as err:
        print('Error while opening file:', err)
    except ValueError as err:
        print('Error while parsing file:', err)

if __name__ == '__main__':
    default_file = '6/input.txt'
    if len(sys.argv) != 2:
        print('Using default file')
    else:
        default_file = sys.argv[1]
    main(default_file)