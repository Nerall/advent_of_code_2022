import sys
import os

class Node():
    def __init__(self, name, type, parent=None, size=None, children=None):
        self.name = name
        self.type = type
        self.parent = parent
        self.size = size
        self.children = children

    def from_text(text, parent):
        info, name = text.split(' ')
        if info == 'dir': # Directory
            node = Node(name=name, type='dir', parent=parent, children=[])
        else: # File
            node = Node(name=name, type='file', parent=parent, size=int(info))
        return node

    def set_children(self, children):
        if self.type == 'dir':
            self.children = children

    def compute_size(self):
        if not self.size: # Directory
            self.size = 0
            for child in self.children:
                self.size += child.compute_size()
        return self.size

    def sum_smallests(self):
        if not self.size:
            self.compute_size()

        total = self.size if self.size <= 100000 else 0
        total += sum([child.sum_smallests() for child in self.children if child.type == 'dir'])
        return total

    def smallest_to_delete(self, min_size):
        if not self.size:
            self.compute_size()

        best_size = None
        if self.size == min_size:
            # Optimal
            best_size = min_size
        elif self.size > min_size:
            best_size = self.size
            for child in self.children:
                if child.type == 'dir':
                    child_smallest = child.smallest_to_delete(min_size)
                    if child_smallest and child_smallest < best_size:
                        best_size = child_smallest
        return best_size

class Builder():
    def __init__(self, blocks):
        self.root = Node(name='/', type='dir', parent=None, children=[])
        self.current = self.root
        self.parse_blocks(blocks)

    def parse_blocks(self, blocks):
        for block in blocks:
            command = block[0][:2]
            if command == 'ls':
                self.command_ls(block[1:])
            elif command == 'cd':
                self.command_cd(block[0][3:])

    def command_ls(self, lines):
        children = [Node.from_text(text, self.current) for text in lines]
        self.current.set_children(children)

    def command_cd(self, name):
        if name == '/':
            self.current = self.root
        elif name == '..':
            self.current = self.current.parent
        else:
            for child in self.current.children:
                if child.name == name:
                    self.current = child
                    break

def main(input_file):
    try:
        with open(input_file) as f:
            # Skip first separator
            buffer = f.read()[2:].split('$ ')
            commands = [command.splitlines() for command in buffer]
            builder = Builder(commands)
            sum_smallests = builder.root.sum_smallests()
            needed_space = max(0, 30000000 - (70000000 - builder.root.size))
            smallest_to_delete = builder.root.smallest_to_delete(needed_space)
            print('The sum of all directories smaller than 100ko is', sum_smallests)
            print('The smallest directory that will free enough memory has size', smallest_to_delete)

    except OSError as err:
        print('Error while opening file:', err)
    except ValueError as err:
        print('Error while parsing file:', err)

if __name__ == '__main__':
    default_file = '7/input.txt'
    if len(sys.argv) != 2:
        print('Using default file')
    else:
        default_file = sys.argv[1]
    main(default_file)