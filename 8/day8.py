import sys
import numpy as np

class Forest():
    def __init__(self, lines):
        self.trees = np.array([[int(tree) for tree in line] for line in lines],
                                dtype=np.uint8)

        # Unused
        self.visible = np.ones(self.trees.shape, dtype=np.bool_)
        self.visible[1:-1, 1:-1] = False
        self.visited = np.zeros(self.trees.shape, dtype=np.bool_)

    # Unused method
    def _get_visible(self, i, j, max_height):
        w, h = self.trees.shape
        if not self.visible[i, j] and not self.visited[i, j]:
            self.visited[i, j] = True
            for (not_border, (i2, j2)) in zip((i > 0, i + 1 < w, j > 0, j + 1 < h),
                                ((i - 1, j), (i + 1, j), (i, j - 1),  (i, j + 1))):
                if not_border and max_height > self.trees[i2, j2]:
                    if self._get_visible(i2, j2, max_height):
                        return True
        return self.visible[i, j]

    # Unused method
    # _sum_visible sets to visible all trees that have a path to a border with only lower trees in-between
    # The statement asked only to check straight orthogonal lines
    def _sum_visible(self):
        w, _ = self.trees.shape
        # Iterate on all non-border trees
        for (i, j) in np.asarray(np.where(self.visible == False)).T:
            self.visited = np.zeros(self.trees.shape, dtype=np.bool_)
            if self._get_visible(i, j, self.trees[i, j]):
                self.visible[i, j] = True
        return self.visible.sum()

    def get_visible(self, i, j):
        lower_trees = self.trees < self.trees[i, j]
        return lower_trees[i, :j].all() or lower_trees[i, j+1:].all() or \
               lower_trees[:i, j].all() or lower_trees[i+1:, j].all()

    def sum_visible(self):
        return sum([self.get_visible(i, j) for i, j in np.ndindex(self.trees.shape)])

    # Returns index of higher tree's first occurrence in all axes
    def get_distance(self, axis):
        indices = np.where(axis)[0]
        return 1 + indices[0] if indices.size else axis.size

    def get_scenic_score(self, i, j):
        higher_trees = self.trees >= self.trees[i, j]
        axes = (np.flip(higher_trees[i, :j]), higher_trees[i, j+1:], \
                np.flip(higher_trees[:i, j]), higher_trees[i+1:, j])
        return np.product([self.get_distance(axis) for axis in axes if axis.size])

    def best_scenic_score(self):
        return max([self.get_scenic_score(i, j) for i, j in np.ndindex(self.trees.shape)])

def main(input_file):
    try:
        with open(input_file) as f:
            lines = f.read().splitlines()
            forest = Forest(lines)
            sum_visible = forest._sum_visible()  
            best_scenic_score = forest.best_scenic_score()
            print("The number of visible trees is", sum_visible)
            print("The highest scenic score possible is", best_scenic_score)

    except OSError as err:
        print('Error while opening file:', err)
    except ValueError as err:
        print('Error while parsing file:', err)

if __name__ == '__main__':
    default_file = '8/input.txt'
    if len(sys.argv) != 2:
        print('Using default file')
    else:
        default_file = sys.argv[1]
    main(default_file)