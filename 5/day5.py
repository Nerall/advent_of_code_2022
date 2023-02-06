import sys

def build_stack(head):
    # Last index
    head_size = int(head[-1][-2])
    stacks = [[] for _ in range(head_size)]
    for j in range(head_size):
        for i in range(len(head) - 2, -1, -1):
            # Access from the bottom of the stack
            char = head[i][j * 4 + 1]
            if char == ' ':
                # No more element in stack
                break
            stacks[j].append(char)
    return stacks

def build_instructions(tail):
    instructions = []
    for line in tail:
        instructions.append([int(s) for s in line.split() if s.isdigit()])
    return instructions

def parse_instructions_cratemover9000(stacks, instructions):
    # Copy stack
    stacks = [stack[:] for stack in stacks]
    for (move_, from_, to_) in instructions:
        for _ in range(move_):
            crate = stacks[from_ - 1].pop()
            stacks[to_ - 1].append(crate)
    message = ''.join(stack[-1] for stack in stacks)
    print('With a CrateMover 9000, the message formed by the top of each stack is', message)

def parse_instructions_cratemover9001(stacks, instructions):
    # Copy stack
    stacks = [stack[:] for stack in stacks]
    for (move_, from_, to_) in instructions:
        crates = stacks[from_ - 1][-move_:]
        stacks[from_ - 1] = stacks[from_ - 1][:-move_]
        stacks[to_ - 1] += crates
    message = ''.join(stack[-1] for stack in stacks)
    print('With a CrateMover 9001, the message formed by the top of each stack is', message)

def main(input_file):
    try:
        with open(input_file) as f:
            head, tail = (buffer.splitlines() for buffer in f.read().split('\n\n'))
            stacks = build_stack(head)
            instructions = build_instructions(tail)
            parse_instructions_cratemover9000(stacks, instructions)
            parse_instructions_cratemover9001(stacks, instructions)

    except OSError as err:
        print('Error while opening file:', err)
    except ValueError as err:
        print('Error while parsing file:', err)

if __name__ == '__main__':
    default_file = '5/input.txt'
    if len(sys.argv) != 2:
        print('Using default file')
    else:
        default_file = sys.argv[1]
    main(default_file)