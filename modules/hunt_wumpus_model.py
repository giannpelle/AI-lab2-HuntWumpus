from typing import NamedTuple, Iterable
from copy import deepcopy

from wumpus import Hunter, Pit, Wumpus, Gold, Exit
from linear_space import SmartCoordinate, SmartVector

class HuntWumpusState(object):
    """
    Represent a state of the Hunt the Wumpus game with: 
    - agent_location: SmartCoordinate
            represents the current location of the agent in the world
    - agent_orientation: SmartVector
            represents the current orientation of the agent in the world 
    - is_agent_alive: bool
            tells wether the agent is still alive
    - is_arrow_available: bool
            represents the availability of the arrow to the agent
    - has_agent_climbed_out: bool
            tells whether the agent has climbed out of the world
    - wumpus_locations: [SmartCoordinate]
            the list of wumpuses locations in the world
    - gold_locations: [SmartCoordinate]
            the list of golds locations in the world
    - heuristic_cost: number
            the value of the heuristic associated to this state

    @static properties
    - world_size: (number, number) 
            represents the sizes (width, height) of the grid map representing the world
    - block_locations: [SmartCoordinate]
            the list of block locations in the world
    - pit_locations: [SmartCoordinate]
            the list of pit_locations in the world
    - exit_locations: [SmartCoordinate] 
            the list of locations where the agent can escape from the game
    """
    world_size = (0, 0)
    block_locations = []
    pit_locations = []
    exit_locations = SmartCoordinate(0,0)

    def __init__(self, agent_location=SmartCoordinate(0,0), 
                       agent_orientation=SmartVector(0,1), 
                       is_agent_alive=True, 
                       is_arrow_available=True, 
                       has_agent_climbed_out=False, 
                       wumpus_locations=[], 
                       gold_locations=[], 
                       heuristic_cost=0):

        self.agent_location = agent_location
        self.agent_orientation = agent_orientation
        self.is_agent_alive = is_agent_alive
        self.is_arrow_available = is_arrow_available
        self.has_agent_climbed_out = has_agent_climbed_out
        self.wumpus_locations = wumpus_locations
        self.gold_locations = gold_locations
        self.heuristic_cost = heuristic_cost

    def __eq__(self, other):
        return self.agent_location == other.agent_location and \
               self.agent_orientation == other.agent_orientation and \
               self.is_agent_alive == other.is_agent_alive and \
               self.is_arrow_available == other.is_arrow_available and \
               self.has_agent_climbed_out == other.has_agent_climbed_out and \
               self.wumpus_locations == other.wumpus_locations and \
               self.gold_locations == other.gold_locations
               
    def __hash__(self):
        return hash((self.agent_location.x, self.agent_location.y, self.agent_orientation.x, 
                     self.agent_orientation.y, self.is_agent_alive, self.is_arrow_available, 
                     self.has_agent_climbed_out, str(self.wumpus_locations), 
                     str(self.gold_locations)))
    
    def __str__(self):
        return f"HuntWumpusState: (agent_location = {self.agent_location}," \
               + f"\n\tagent_orientation = {self.agent_orientation}," \
               + f"\n\tis_agent_alive = {self.is_agent_alive}," \
               + f"\n\tis_arrow_available = {self.is_arrow_available}," \
               + f"\n\thas_agent_climbed_out = {self.has_agent_climbed_out}," \
               + f"\n\t(wumpus_locations = {self.wumpus_locations}," \
               + f"\n\tgold_locations = {self.gold_locations}," \
               + f"\n\theuristic_cost = {self.heuristic_cost}," \
               + f"\n\tworld_size = {HuntWumpusState.world_size}," \
               + f"\n\tblock_locations = {HuntWumpusState.block_locations}," \
               + f"\n\tpit_locations = {HuntWumpusState.pit_locations}," \
               + f"\n\texit_locations = {HuntWumpusState.exit_locations})"

    def __repr__(self):
        return f"HuntWumpusState: (agent_location = {self.agent_location}," \
               + f"\n\tagent_orientation = {self.agent_orientation}," \
               + f"\n\tis_agent_alive = {self.is_agent_alive}," \
               + f"\n\tis_arrow_available = {self.is_arrow_available}," \
               + f"\n\thas_agent_climbed_out = {self.has_agent_climbed_out}," \
               + f"\n\t(wumpus_locations = {self.wumpus_locations}," \
               + f"\n\tgold_locations = {self.gold_locations}," \
               + f"\n\theuristic_cost = {self.heuristic_cost}," \
               + f"\n\tworld_size = {HuntWumpusState.world_size}," \
               + f"\n\tblock_locations = {HuntWumpusState.block_locations}," \
               + f"\n\tpit_locations = {HuntWumpusState.pit_locations}," \
               + f"\n\texit_locations = {HuntWumpusState.exit_locations})"

    @staticmethod
    def setup_static_properties(world_size, block_locations, pit_locations, exit_locations):
        HuntWumpusState.world_size = world_size
        HuntWumpusState.block_locations = block_locations
        HuntWumpusState.pit_locations = pit_locations
        HuntWumpusState.exit_locations = exit_locations


class HuntWumpusResult(NamedTuple):
    """
    represents the result of the search showing:
    - sequence_actions: [Hunter.Action]
            represents the sequence of actions needed to reach the solution of the problem
    - total_reward: number
            represents the total reward of the agent after performing all actions in the 
            list of sequence actions
    """
    sequence_actions: Iterable[Hunter.Actions]
    total_reward: int


class HuntWumpusNode(object):
    """
    Represents a node of the problem with:
    - state: HuntWumpusState
            represents the state of the node
    - path_cost: number
            is the cost it takes to get to the node from the initial node applying 
            all previous_action defined in node parents
    - reward: number
            is the reward gained by the agent while performing previous actions
    - previous_action: Hunter.Action
            the action that was applied to the parent node to get to this node
    - parent: HuntWumpusNode
            parent node of the actual node
    """

    def __init__(self, state, path_cost=0, reward=0, previous_action=None, parent=None):
        self.state = state
        self.path_cost = path_cost
        self.reward = reward
        self.previous_action = previous_action
        self.parent = parent

    def __hash__(self):
        """
        Determines the uniqueness of an  HuntWumpusNode object. 
        Nodes should have same hash if they represent same state, meanwhile other attributes 
        can differ.
        """
        return self.state.__hash__()

    def __eq__(self, other):
        """
        It's been called every time there is the need to compare 2 objects of type 
        HuntWumpusNode. 
        It is used to prevent the search algorithm from exploring the nodes that have 
        already been visited. 
        (This avoids infinite loops while searching)
        """
        return self.state == other.state

    def __lt__(self, other):
        """
        It's been called to define an order between 2 objects of type HuntWumpusNode
        in the PriorityQueue.
        Order is determined by the sum of path cost, reward and heuristic cost. 
        If both nodes have the same (cost + heuristic) value, we defined the 
        following Breaking Ties:
            Level 1) if nodes have different heuristic_cost values, then we choose the 
                     one with lower one
            Level 2) if nodes have different agent_location values, then we choose the 
                     nearest one to the goal location (using manhattan distance)
            Level 3) if nodes have different orientations, then we defined the 
                     hierarchy N > E > W > S
            Level 4) we return the node with the lowest orientation.y
        """
        if self.get_cost_heuristic_sum() == other.get_cost_heuristic_sum():
            if self.state.heuristic_cost == other.state.heuristic_cost:
                if self.state.agent_location == other.state.agent_location:
                    if self.state.agent_orientation == other.state.agent_orientation:
                        return self.state.agent_orientation.y < other.state.agent_orientation.y 
                    else:
                        if self.state.agent_orientation.y != other.state.agent_orientation.y:
                            return self.state.agent_orientation.y > other.state.agent_orientation.y  
                        else:
                            self.state.agent_orientation.x > other.state.agent_orientation.x
                else:
                    self_goal_location = (self.state.gold_locations[0] if self.state.gold_locations 
                                         else self.state.exit_locations[0])
                    other_goal_location = (other.state.gold_locations[0] if other.state.gold_locations
                                          else self.state.exit_locations[0])
                    return (abs(self_goal_location.x - self.state.agent_location.x) 
                           + abs(self_goal_location.y - self.state.agent_location.y) 
                           <= abs(other_goal_location.x - other.state.agent_location.x) 
                           + abs(other_goal_location.y - other.state.agent_location.y))
            else:
                return self.state.heuristic_cost < other.state.heuristic_cost
        else:
            return self.get_cost_heuristic_sum() <= other.get_cost_heuristic_sum()

    def __str__(self):
        return f"HuntWumpusNode: (id = {id(self)}," \
               + f"\n\tstate = {str(self.state)}," \
               + f"\n\tparent = {id(self.parent)}," \
               + f"\n\tprevious_actions = {self.unwrap_previous_actions()}," \
               + f"\n\tpath_cost = {self.path_cost}," \
               + f"\n\treward = {self.reward}," \
               + f"\n\tvalue_in_priority_queue = {self.get_cost_heuristic_sum()}," \
               + f"\n\tparent_heuristic - current_heuristic: " \
               + f"{self.parent.state.heuristic_cost - self.state.heuristic_cost if self.parent is not None else 0} " \
               + f"<= {self.previous_action}"

    def __repr__(self):
        return f"HuntWumpusNode: (id = {id(self)}," \
               + f"\n\tstate = {str(self.state)}," \
               + f"\n\tparent = {id(self.parent)}," \
               + f"\n\tprevious_actions = {self.unwrap_previous_actions()}," \
               + f"\n\tpath_cost = {self.path_cost}," \
               + f"\n\treward = {self.reward}," \
               + f"\n\tvalue_in_priority_queue = {self.get_cost_heuristic_sum()}," \
               + f"\n\tparent_heuristic - current_heuristic: " \
               +f"{self.parent.state.heuristic_cost - self.state.heuristic_cost if self.parent is not None else 0} " \
               + f"<= {self.previous_action}"

    def get_cost_heuristic_sum(self):
        """
        This func is used to calculate the priority of nodes in the Priority Queue used by the 
        A* algorithm, lower values will result in a high priority
        """
        return self.path_cost + self.state.heuristic_cost

    def unwrap_previous_actions(self):
        """
        returns all actions performed from the initial_node to the given node
        """
        if self.parent is None:
            return []
        
        return self.parent.unwrap_previous_actions() + [self.previous_action]
    

class HuntWumpusProblem(object):
    """
    Is the formal representation of the hunt the wumpus problem in general:
    - initial_state: HuntWumpusState
            the initial state of the problem
    - possible_actions: [Hunter.Actions]
            is the list of possible actions that can be performed by the agent 
    - heuristic_func: (HuntWumpusNode) -> number
            is a function that calculates the heuristic of the current node against 
            the goal of the problem
    - action_costs: { Hunter.Actions: lambda (state, action, next_state) -> number }
            is a mapping between each possible action available to the agent and the 
            associated function which can be used to calculate its cost
    - action_rewards: { Hunter.Actions: lambda (state, action, next_state) -> number }
            is a mapping between each possible action available to the agent and the 
            associated function which can be used to calculate its reward
    """
  
    def __init__(self, world, possible_actions, heuristic_func=lambda x: 0):
        # world info unwrapping
        world_info = {k: [] for k in ('Hunter', 'Pits', 'Wumpus', 'Gold', 
                                      'Exits', 'Hunter_orientation')}
        world_info['Size'] = (world.size.x, world.size.y)
        world_info['Blocks'] = [(c.x, c.y) for c in world.blocks]

        for obj in world.objects:
            if isinstance(obj, Hunter):
                world_info['Hunter_orientation'].append(SmartVector(obj.orientation.value[0], 
                                                                    obj.orientation.value[1]))
                world_info['Hunter'].append(SmartCoordinate(obj.location.x, obj.location.y))
            elif isinstance(obj, Pit):
                world_info['Pits'].append(SmartCoordinate(obj.location.x, obj.location.y))
            elif isinstance(obj, Wumpus):
                world_info['Wumpus'].append(SmartCoordinate(obj.location.x, obj.location.y))
            elif isinstance(obj, Exit):
                world_info['Exits'].append(SmartCoordinate(obj.location.x, obj.location.y))
            elif isinstance(obj, Gold):
                world_info['Gold'].append(SmartCoordinate(obj.location.x, obj.location.y))
        
        world_size = (world.size.x, world.size.y)
        block_locations = world_info["Blocks"]
        pit_locations = world_info["Pits"]
        wumpus_locations = world_info["Wumpus"]
        gold_locations = world_info["Gold"]
        exit_locations = world_info["Exits"]
        agent_location = world_info["Hunter"][0]
        agent_orientation = world_info['Hunter_orientation'][0]

        self.initial_state = HuntWumpusState(agent_location, 
                                             agent_orientation, 
                                             wumpus_locations=wumpus_locations, 
                                             gold_locations=gold_locations)

        HuntWumpusState.setup_static_properties(world_size, block_locations, 
                                                pit_locations, exit_locations)
        
        self.possible_actions = possible_actions
        self.heuristic_func = heuristic_func
        self.initial_state.heuristic_cost = self.heuristic_func(self.initial_state)

        # Action costs:
        # Shooting (using the arrow) -> 10 (otherwise 1)
        # All other -> 1
        self.action_costs = {
            Hunter.Actions.LEFT: lambda state, action, next_state: 1,
            Hunter.Actions.RIGHT: lambda state, action, next_state: 1,
            Hunter.Actions.MOVE: lambda state, action, next_state: 1,
            Hunter.Actions.SHOOT: lambda state, action, next_state: 10 if (state.is_arrow_available == True) 
                                                                          and (next_state.is_arrow_available == False)
                                                                    else 1,
            Hunter.Actions.GRAB: lambda state, action, next_state: 1,
            Hunter.Actions.CLIMB: lambda state, action, next_state: 1
        }

        # Action rewards:
        # Grabbing the gold -> 1000
        # Falling down in a pit -> -1000 (also end of game)
        self.action_rewards = {
            Hunter.Actions.LEFT: lambda state, action, next_state: 0,
            Hunter.Actions.RIGHT: lambda state, action, next_state: 0,
            Hunter.Actions.MOVE: lambda state, action, next_state: 0 if next_state.is_agent_alive 
                                                                   else -1000,
            Hunter.Actions.SHOOT: lambda state, action, next_state: 0,
            Hunter.Actions.GRAB: lambda state, action, next_state: 1000 if (len(state.gold_locations) > len(next_state.gold_locations))
                                                                   else 0,
            Hunter.Actions.CLIMB: lambda state, action, next_state: 0
        }
        
    def is_legal(self, location, *, for_state):
        """
        returns a boolean indicating if the given location is inside the world and it is not a block
        """
        state = for_state

        is_location_inside_grid_map = (location.x in range(HuntWumpusState.world_size[0]) 
                                      and location.y in range(HuntWumpusState.world_size[1]))
        is_not_a_block = location not in HuntWumpusState.block_locations
        return is_location_inside_grid_map and is_not_a_block

    def get_available_actions_for(self, state):
        if state.has_agent_climbed_out or not state.is_agent_alive:
           return []
    
        return self.possible_actions

    # effective actions (ones that do change the state of the problem)
    def get_effective_actions_for(self, state):
        """
        filters out all actions (from all the available ones) that do not change the state of 
        the world (wasteful actions)
        """
        available_actions = self.get_available_actions_for(state)

        # func definitions for switch statement that is used in next for loop
        def is_MOVE_effective_for(state):
            new_location = (state.agent_location + state.agent_orientation)
            return self.is_legal(new_location, for_state=state)
            
        def is_SHOOT_effective_for(state):
            return state.is_arrow_available

        def is_GRAB_effective_for(state):
            return (state.agent_location in state.gold_locations)

        def is_CLIMB_effective_for(state):
            return (state.agent_location in HuntWumpusState.exit_locations)

        switcher = {
            Hunter.Actions.MOVE: is_MOVE_effective_for,
            Hunter.Actions.SHOOT: is_SHOOT_effective_for,
            Hunter.Actions.GRAB: is_GRAB_effective_for,
            Hunter.Actions.CLIMB: is_CLIMB_effective_for,
        }

        effective_actions = []

        for action in available_actions:
            if action == Hunter.Actions.LEFT or action == Hunter.Actions.RIGHT:
                effective_actions.append(action)
                continue

            is_action_effective_for = switcher.get(action, lambda x: False)
            if is_action_effective_for(state):
                effective_actions.append(action)
        
        return effective_actions

    def get_best_actions_for(self, state):
        """
        calculate the best rotation actions for the current state, improving the efficiency 
        of the rotation of the agent
        """
        if state.gold_locations and state.gold_locations[0] in HuntWumpusState.pit_locations:
            return []

        effective_actions = set(self.get_effective_actions_for(state))
        useless_actions = set()

        # no shoot if there is no wumpus to kill
        if state.agent_location + state.agent_orientation not in state.wumpus_locations:
            useless_actions.add(Hunter.Actions.SHOOT)

        # no climb out if we haven't grabbed the gold
        if state.gold_locations:
            useless_actions.add(Hunter.Actions.CLIMB)

        # no move into a pit
        if state.agent_location + state.agent_orientation in HuntWumpusState.pit_locations:
            useless_actions.add(Hunter.Actions.MOVE)
        
        # best rotation moves to get around obstacles
        agent_orientation = state.agent_orientation
        perpendicular_orientation = state.agent_orientation.get_perpendicular_vector_clockwise()

        east_location = state.agent_location + perpendicular_orientation
        south_location = state.agent_location - agent_orientation
        west_location = state.agent_location - perpendicular_orientation

        if (not self.is_legal(west_location, for_state=state) 
           or west_location in HuntWumpusState.pit_locations): # WEST is a block
            if (not self.is_legal(east_location, for_state=state) 
               or east_location in HuntWumpusState.pit_locations): # EAST is a block
                if (not self.is_legal(south_location, for_state=state) 
                   or south_location in HuntWumpusState.pit_locations): # SOUTH is a block
                    useless_actions = useless_actions.union(set([Hunter.Actions.RIGHT, Hunter.Actions.LEFT]))
                else: # SOUTH not a block
                    useless_actions = useless_actions.union(set([Hunter.Actions.LEFT]))
            else: # EAST not a block
                useless_actions = useless_actions.union(set([Hunter.Actions.LEFT]))
        else: #WEST not a block
            if (not self.is_legal(east_location, for_state=state) 
                or east_location in HuntWumpusState.pit_locations): # EAST is a block
                useless_actions = useless_actions.union(set([Hunter.Actions.RIGHT]))

        return effective_actions - useless_actions

    def get_successor_state_from(self, state, *, with_action):
        """
        returns the successor HuntWumpusState resulting from applying the given action
        on the given state
        """
        action = with_action

        if action not in self.get_effective_actions_for(state):
            return deepcopy(state)

        def get_LEFT_successor_from(state):
            return HuntWumpusState(state.agent_location, 
                                   -state.agent_orientation.get_perpendicular_vector_clockwise(), 
                                   state.is_agent_alive, 
                                   state.is_arrow_available, 
                                   state.has_agent_climbed_out, 
                                   state.wumpus_locations, 
                                   state.gold_locations)

        def get_RIGHT_successor_from(state):
            return HuntWumpusState(state.agent_location, 
                                   state.agent_orientation.get_perpendicular_vector_clockwise(), 
                                   state.is_agent_alive, 
                                   state.is_arrow_available, 
                                   state.has_agent_climbed_out, 
                                   state.wumpus_locations, 
                                   state.gold_locations)

        def get_MOVE_successor_from(state):
            new_location = (state.agent_location + state.agent_orientation)
            if not(self.is_legal(new_location, for_state=state)):
                new_location = state.agent_location

            has_agent_survived = (new_location not in state.wumpus_locations 
                                 and new_location not in HuntWumpusState.pit_locations)

            return HuntWumpusState(new_location, 
                                   state.agent_orientation, 
                                   has_agent_survived, 
                                   state.is_arrow_available, 
                                   state.has_agent_climbed_out, 
                                   state.wumpus_locations,
                                   state.gold_locations)

        def get_SHOOT_successor_from(state):
            remaining_wumpus = list(filter(lambda element: element != (state.agent_location + state.agent_orientation), state.wumpus_locations))
            return HuntWumpusState(state.agent_location, 
                                   state.agent_orientation, 
                                   state.is_agent_alive, 
                                   False, 
                                   state.has_agent_climbed_out, 
                                   remaining_wumpus, 
                                   state.gold_locations)

        def get_GRAB_successor_from(state):
            remaining_golds = list(filter(lambda element: element != state.agent_location, state.gold_locations))
            return HuntWumpusState(state.agent_location, 
                                   state.agent_orientation, 
                                   state.is_agent_alive, 
                                   state.is_arrow_available, 
                                   state.has_agent_climbed_out, 
                                   state.wumpus_locations, 
                                   remaining_golds)

        def get_CLIMB_successor_from(state):
            return HuntWumpusState(state.agent_location, 
                                   state.agent_orientation, 
                                   state.is_agent_alive, 
                                   state.is_arrow_available, 
                                   state.agent_location in HuntWumpusState.exit_locations, 
                                   state.wumpus_locations, state.gold_locations)

        switcher = {
            Hunter.Actions.LEFT: get_LEFT_successor_from,
            Hunter.Actions.RIGHT: get_RIGHT_successor_from,
            Hunter.Actions.MOVE: get_MOVE_successor_from,
            Hunter.Actions.SHOOT: get_SHOOT_successor_from,
            Hunter.Actions.GRAB: get_GRAB_successor_from,
            Hunter.Actions.CLIMB: get_CLIMB_successor_from
        }

        get_successor_state_from = switcher.get(action, lambda x: deepcopy(state))
        successor = get_successor_state_from(state)
        successor.heuristic_cost = self.heuristic_func(successor)
        return successor

    def is_goal_state(self, state):
        """
        returns True if the agent has grabbed the gold and climbed out of the world
        """
        return state.has_agent_climbed_out and not state.gold_locations and state.is_agent_alive

    def get_child_from(self, node, *, with_action):
        """
        returns the child HuntWumpusNode resulting from applying the given action on 
        the given node
        """   
        action = with_action

        next_state = self.get_successor_state_from(node.state, with_action=action)

        get_action_cost_from = self.action_costs.get(action, lambda x, y, z: 1)
        action_cost = get_action_cost_from(node.state, action, next_state)

        get_action_reward_from = self.action_rewards.get(action, lambda x, y, z: 0)
        action_reward = get_action_reward_from(node.state, action, next_state)

        return HuntWumpusNode(next_state, node.path_cost + action_cost, 
                              node.reward + action_reward, action, node)

    def unwrap_solution(self, node):
        """
        returns all actions performed from the initial_node to the given node
        """
        if node.parent is None:
            return []
        
        return self.unwrap_solution(node.parent) + [node.previous_action]