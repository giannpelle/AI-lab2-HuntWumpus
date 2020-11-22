import os, sys
sys.path.insert(1, os.path.abspath("modules/"))

import math
import random
from typing import Iterable

from queue import PriorityQueue

import wumpus as wws

from modules.hunt_wumpus_model import HuntWumpusResult
from modules.hunt_wumpus_model import HuntWumpusProblem, HuntWumpusNode

class UCSPlayer(wws.InformedPlayer, wws.UserPlayer):
    """Informed player demonstrating the use of the start episode method to inspect the world."""

    def ucs_search(self, problem):
        """
        Implementation of the pseudocode UCS AIMA4e found on:
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Uniform-Cost-Search.md
        """

        if (problem.is_goal_state(problem.initial_state)):
            self.counter += 1
            return HuntWumpusResult([], 0)

        frontier = PriorityQueue()
        frontier.put(HuntWumpusNode(problem.initial_state))
        reached = {} # {state: int}
        solution = HuntWumpusNode(problem.initial_state, math.inf)
    
        while not frontier.empty() and (node := frontier.get()).path_cost < solution.path_cost:
            childs = [problem.get_child_from(node, with_action= action) for action in problem.get_best_actions_for(node.state)]
            self.counter += 1
            for child in childs:
                if (child.state not in reached) or (child.path_cost < reached[child.state]):
                    reached[child.state] = child.path_cost
                    frontier.put(child)
                    if problem.is_goal_state(child.state) and child.path_cost < solution.path_cost:
                        solution = child

        sequence_actions = problem.unwrap_solution(solution)
        if sequence_actions:
            return HuntWumpusResult(sequence_actions, solution.reward - solution.path_cost)  
        else:
            return HuntWumpusResult([], 0)
    
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

        def heuristic_func(state):
            return 0

        hunt_wumpus_problem = HuntWumpusProblem(world, wws.Hunter.Actions, heuristic_func)
        self.reward = 0
        self.counter = 0

        result = self.ucs_search(hunt_wumpus_problem)

        if not result.sequence_actions:
            self.result_reward = -1
            self.result_sequence_actions = [wws.Hunter.Actions.CLIMB]
        else:
            self.result_reward = result.total_reward
            self.result_sequence_actions = result.sequence_actions
        
        print("")
        print("".join(["*" for i in range(25)] + [f" [ UCS search algorithm ] "] + ["*" for i in range(25)]))
        print(f"visited nodes: {self.counter} nodes (minimum possible is {len(self.result_sequence_actions)})\n")
        print(f"Action sequence: \n{list(map(lambda x: x.name, self.result_sequence_actions))}\n")
        print(f"total reward for the found solution: {self.result_reward}")
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
    world.run_episode(UCSPlayer())


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
