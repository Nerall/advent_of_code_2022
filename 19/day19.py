import sys
import re
import numpy as np

class Blueprint:
    def __init__(self, line):
        values = re.findall('\d+', line)
        self.recipe = np.zeros((4, 3), dtype=np.uint8)
        # Each ore robot costs _ ore.
        self.recipe[0][0] = values[1]
        # Each clay robot costs _ ore.
        self.recipe[1][0] = values[2]
        # Each obsidian robot costs _ ore and _ clay.
        self.recipe[2][0], self.recipe[2][1] = values[3], values[4]
        # Each geode robot costs _ ore and _ obsidian.
        self.recipe[3][0], self.recipe[3][2] = values[5], values[6]

"""class State:
    def __init__(self, resources, robots):
        self.resources = resources
        self.robots = robots

    def __hash__(self):
        return hash(str(np.concatenate((self.resources, self.robots))))

    def __eq__(self, other):
        return isinstance(other, State) and (self.resources == other.resources).all() and (self.robots == other.robots).all()"""

class BlueprintSolver:
    def __init__(self, blueprint, max_minutes=20):
        # First 4 digits for resources types
        # Last 4 digits for robot types active

        initial_resources = np.array((0, 0, 0, 0), dtype=np.int16)
        initial_robots = np.array((1, 0, 0, 0), dtype=np.int16)  # Starting with 1 ore robot
        initial_state = np.concatenate((initial_resources, initial_robots))
        initial_skipped = np.array((0, 0, 1, 1), dtype=bool)  # By default, obsidian robot and geode robot are skipped
        self.states_processing = {tuple(initial_state):initial_skipped}
        self.states_tb_processed = {}

        self.blueprint = blueprint

        self.cur_robots = None
        self.cur_skipped = None

        self.max_geodes = self.solve_blueprint(max_minutes)

    def solve_blueprint_build(self, resources, tb_constructed, cur_i=0):
        resources, tb_constructed = np.array(resources), np.array(tb_constructed)
        # Iterate over materials
        for i in range(cur_i, 4):
            if self.cur_skipped[i]:
                # No need to build current robot as it was skipped in previous state
                continue
            # Tries to build resource ['ore', 'clay', 'obsidian', 'geode'][i]
            while (resources[:3] >= self.blueprint.recipe[i]).all():
                # New branch without building
                self.solve_blueprint_build(resources=resources, tb_constructed=tb_constructed, cur_i=i + 1)
                resources[:3] -= self.blueprint.recipe[i]
                tb_constructed[i] += 1
        self.solve_blueprint_enqueue(resources=resources, tb_constructed=tb_constructed)

    def solve_blueprint_enqueue(self, resources, tb_constructed):
        # Mark skipped parts, reset if something was built
        if (tb_constructed > self.cur_skipped).any():
            obsidian_production = self.cur_robots[1] or tb_constructed[1]
            geode_production = self.cur_robots[2] or tb_constructed[2]
            new_skipped = np.array((False, False, not(obsidian_production), not(geode_production)))
        else:
            new_skipped = np.array(self.cur_skipped)
        for i in range(4):
            if not new_skipped[i] and (resources[:3] >= self.blueprint.recipe[i]).all():
                new_skipped[i] = True
        # Add new state in queue
        if not new_skipped.all():
            # Active robots produce resources, new robots under construction
            new_state = tuple(np.concatenate((resources + self.cur_robots,
                                              self.cur_robots + tb_constructed)))
            if new_state not in self.states_tb_processed:
                self.states_tb_processed[new_state] = new_skipped
            else:
                self.states_tb_processed[new_state] |= new_skipped


    def solve_blueprint(self, max_minutes):
        max_geodes = 0
        for minute in range(max_minutes):
            print(minute, len(self.states_processing))
            for i, (cur_state, cur_skipped) in enumerate(self.states_processing.items()):
                if i % 10000 == 9999:
                    print(i+1)
                # Build (ore, clay, obsidian, geode) is useless in last (4, 3, 2, 1) min. Max() ensures no negative slicing
                cur_skipped[:max(0, minute - max_minutes + 5)] = True
                self.cur_robots = np.array(cur_state[4:8], dtype=np.int16)
                self.cur_skipped = cur_skipped
                self.solve_blueprint_build(resources=cur_state[:4],
                                           tb_constructed=np.array((0, 0, 0, 0), dtype=np.int16))
            self.states_processing = self.states_tb_processed
            self.states_tb_processed = {}
        for cur_state in self.states_processing.keys():
            if cur_state[3] > self.max_geodes: # Geode resource
                max_geodes = cur_state[3]
                print("found")
                exit()
        return max_geodes

def main(input_file):
    try:
        with open(input_file) as f:
            # Skip first separator
            blueprints = [Blueprint(line) for line in f.read().splitlines()]
            max_geodes = [0] * len(blueprints)
            for i, blueprint in enumerate(blueprints):
                blueprint_solver = BlueprintSolver(blueprint)
                print("max_geode", blueprint_solver.max_geodes)
                max_geodes[i] = blueprint_solver.max_geodes
            print(max_geodes)

    except OSError as err:
        print('Error while opening file:', err)
    #except ValueError as err:
    #    print('Error while parsing file:', err)

if __name__ == '__main__':
    default_file = '19/input.txt'
    if len(sys.argv) != 2:
        print('Using default file')
    else:
        default_file = sys.argv[1]
    main(default_file)