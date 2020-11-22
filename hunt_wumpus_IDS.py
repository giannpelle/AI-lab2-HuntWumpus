import os, sys
sys.path.insert(1, os.path.abspath("modules/"))

import random
from typing import Iterable

import wumpus as wws

from modules.hunt_wumpus_model import HuntWumpusResult
from modules.hunt_wumpus_model import HuntWumpusProblem, HuntWumpusNode

# DISCLAIMER: 
# this is the implementation of the uninformed search algorithm Iterative Deepening Search (IDS) 
# which was developed just for testing and comparison purposes
class IDSPlayer(wws.InformedPlayer, wws.UserPlayer):
    """Informed player demonstrating the use of the start episode method to inspect the world."""

    def iterative_deepening_search(self, problem):
        """
        Implementation of the pseudocode found on: 
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Iterative-Deepening-Search.md
        
        cutoff flag is [-1]
        no admissible solution flag is [-2]    
        """
        depth = 0

        while True:
            result = self.depth_limited_search(problem, depth)
            
            print(f"nodes explored: {self.counter}")
            self.counter = 0
            
            if result != [-1]: #-1 is cutoff
                return result if result != [-2] else HuntWumpusResult([], 0)

            depth += 1
            

    def depth_limited_search(self, problem, depth):
        """
        Implementation of the pseudocode AIMA3e found on:
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Depth-Limited-Search.md
        """
        print("".join(["-" for i in range(40)]), f"Limit Depth ({depth})", "".join(["-" for i in range(40)]))
        
        return self.recursive_dls(HuntWumpusNode(problem.initial_state), problem, depth, set([HuntWumpusNode(problem.initial_state)]))
    
    def recursive_dls(self, node, problem, limit, explored_nodes):
        self.counter += 1
        self.total_counter += 1
        
        if problem.is_goal_state(node.state):
            return HuntWumpusResult(problem.unwrap_solution(node), node.reward - node.path_cost)
        elif limit == 0:
            return [-1]
        else:
            cutoff_occured = False
            childs = [problem.get_child_from(node, with_action= action) for action in problem.get_best_actions_for(node.state)]
            clean_childs = list(filter(lambda child: child not in explored_nodes, childs))
            
            new_explored_nodes = explored_nodes.copy()
            new_explored_nodes.add(node)
            
            for child in clean_childs:
                result = self.recursive_dls(child, problem, limit - 1, new_explored_nodes)
                
                if result == [-1]:
                    cutoff_occured = True
                elif result != [-2]:
                    return result
            
            if cutoff_occured:
                return [-1]
            else:
                return [-2]

    
    def _say(self, text: str):
        print(self.name + ' says: ' + text)

    def start_episode(self, world: wws.WumpusWorld):
        """Print the description of the world before starting."""

        world_info = {k: [] for k in ('Hunter', 'Pits', 'Wumpus', 'Gold', 'Exits')}
        world_info['Size'] = (world.size.x, world.size.y)
        world_info['Blocks'] = [(c.x, c.y) for c in world.blocks]

        for obj in world.objects:
            if isinstance(obj, wws.Hunter):
                world_info['Hunter'].append((obj.location.x, obj.location.y))
            elif isinstance(obj, wws.Pit):
                world_info['Pits'].append((obj.location.x, obj.location.y))
            elif isinstance(obj, wws.Wumpus):
                world_info['Wumpus'].append((obj.location.x, obj.location.y))
            elif isinstance(obj, wws.Exit):
                world_info['Exits'].append((obj.location.x, obj.location.y))
            elif isinstance(obj, wws.Gold):
                world_info['Gold'].append((obj.location.x, obj.location.y))

        print('World details:')
        for k in ('Size', 'Pits', 'Wumpus', 'Gold', 'Exits', 'Blocks'):
            print('  {}: {}'.format(k, world_info.get(k, None)))

        self.counter = 0
        self.total_counter = 0
        self.reward = 0
        self.result_sequence_actions = []
        self.result_reward = 0
        hunt_wumpus_problem = HuntWumpusProblem(world, wws.Hunter.Actions)

        result = self.iterative_deepening_search(hunt_wumpus_problem)
        
        if not result.sequence_actions:
            self.result_reward = -1
            self.result_sequence_actions = [wws.Hunter.Actions.CLIMB]
        else:
            self.result_reward = result.total_reward
            self.result_sequence_actions = result.sequence_actions

        if result.sequence_actions == []:
            print("There is no solution for the problem")
            return
        
        print("")
        print("".join(["*" for i in range(100)]))
        print(f"The counter of nodes explored is {self.total_counter} (counting from LIMIT = 0)\n")
        print(f"Action sequence: \n{list(map(lambda x: x.name, self.result_sequence_actions))}\n")
        print(f"The total reward of the search is {self.result_reward}")
        print("".join(["*" for i in range(100)]))
        print("")

    def end_episode(self, outcome: int, alive: bool, success: bool):
        """Method called at the when an episode is completed."""
        self._say('Episode completed, my reward is {}'.format(outcome))

    # random player
    def play(self, turn: int, percept: wws.Hunter.Percept, actions: Iterable[wws.Hunter.Actions]) -> wws.Hunter.Actions:
        return self.result_sequence_actions[turn]

    def feedback(self, action: wws.Hunter.Actions, reward: int, percept: wws.Hunter.Percept):
        """Receive in input the reward of the last action and the resulting state. The function is called right after the execution of the action."""
        #self._say('Moved to {} with reward {}'.format(percept.position, reward))
        self.reward += reward




WUMPUS_WORLD = '''
    {
        "id": "simple wumpus world",
        "size": [7, 7],
        "hunters": [[0, 0]],
        "pits": [[4, 0], [3, 1], [2, 2], [6, 2], [4, 4], [3, 5], [4, 6], [5, 6]],
        "wumpuses": [[1, 2]],
        "exits": [[0, 0]],
        "golds": [[6, 3]],
        "blocks": []
    }
'''


def play_fixed_informed(world_json: str = WUMPUS_WORLD):
    """Play on a given world described in JSON format."""
    # create the world
    world = wws.WumpusWorld.from_JSON(world_json)

    # Run a player with knowledge about the world
    world.run_episode(IDSPlayer())


EXAMPLES = (play_fixed_informed)


def main(*args):
    ex_names = {ex.__name__.lower(): ex for ex in EXAMPLES}
    ex = None
    if len(args) > 0:
        ex_name = args[0]
        if ex_name.lower() in ex_names:
            ex = ex_names[ex_name.lower()]
        else:
            print('Example {} not among the available {}'.format(ex_name, list(ex_names.keys())))
            return -1
    else:
        # Randomly play one of the examples
        ex = random.choice(EXAMPLES)

    print('Example {}:'.format(ex.__name__))
    print('  ' + ex.__doc__)
    ex()

    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
