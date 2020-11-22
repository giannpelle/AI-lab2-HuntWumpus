import os, sys
sys.path.insert(1, os.path.abspath("modules/"))

from modules.linear_space import SmartCoordinate, SmartVector
from modules.hunt_wumpus_model import HuntWumpusState

# HELPER FUNCTIONS

def _manhattan_distance_between(start, destination):
    """
    the traditional manhattan distance
    """
    return abs(destination.x - start.x) + abs(destination.y - start.y)

def _get_orientations_to_reach(to_location, *, from_location):
    """
    rerturns the list of vectors aligned to to the destination, from the from_location
    """
    #list of vectors reaching the destination                
    reaching_destination_orientations = []

    if from_location == to_location:
        return []
    elif to_location.x == from_location.x: # goal and agent on same row (axes Y)
        if to_location.y > from_location.y:
            reaching_destination_orientations.append(SmartVector(0, 1))
        else:
            reaching_destination_orientations.append(SmartVector(0, -1))
    elif to_location.y == from_location.y:
        if to_location.x > from_location.x:
            reaching_destination_orientations.append(SmartVector(1, 0))
        else:
            reaching_destination_orientations.append(SmartVector(-1, 0))
    else:
        y_component = 1 if to_location.y > from_location.y else -1
        x_component = 1 if to_location.x > from_location.x else -1
        reaching_destination_orientations.extend([SmartVector(x_component, 0), 
                                                  SmartVector(0, y_component)])

    return reaching_destination_orientations

def _get_orientations_to_move_away_from(to_location, *, from_location):
    """
    rerturns the list of vectors that take you away from the destination
    """       
    all_vectors = [SmartVector(1, 0), SmartVector(0, 1), SmartVector(0, -1), SmartVector(-1, 0)]
    return [vec for vec in all_vectors if vec not in _get_orientations_to_reach(to_location, 
                                                                                from_location=from_location)]
def _get_cost_to_orientate_to(to_location, *, from_location, with_orientation):
    """
    returns the minimum cost to orientate the agent to point to the destination location
    """
    from_orientation = with_orientation
               
    reaching_destination_orientations = _get_orientations_to_reach(to_location, from_location=from_location)

    if not reaching_destination_orientations:
        return 0

    if from_orientation not in reaching_destination_orientations:
        return (1 if from_orientation.get_perpendicular_vector_clockwise() in reaching_destination_orientations 
                    or -from_orientation.get_perpendicular_vector_clockwise() in reaching_destination_orientations
               else 2)
    else:
        return 0

def _get_orientation_overhead_to_reach(to_location, *, from_location):
    """
    returns the orientation overhead to reach a location (NOT considering the agent orientation) but only 
    the overhead that will be introduced by the path to follow
    """
    if (to_location.x == from_location.x or to_location.y == from_location.y):
        return 0
    else:
        return 1

# suppose start being oriented in destination direction (either one of them)
def _smart_manhattan_distance(start, *, destination, with_block_locations):
    """
    checks if there is a solution to reach the destination in exactly manhattan distance steps:
    - if there is one, it will return manhattan distance + orientation overhead of the best 
      available path (with value 0-3)
    - otherwise it will return manhattan_distance + 4
    more info about these values is available in the documentation (they are not random values)
    """
    block_locations = with_block_locations
    map_size = (abs(destination.x - start.x) + 1, abs(destination.y - start.y) + 1)

    #early exit if start and destination in the same point
    if start == destination:
        return 0

    #filtering out all outer blocks from the smallest grid containing the start and destination location
    block_max_y = max(start.y, destination.y)
    block_max_x = max(start.x, destination.x)
    block_min_y = min(start.y, destination.y)
    block_min_x = min(start.x, destination.x)
    filtered_blocks = list(filter(lambda block: (block_min_x <= block.x <= block_max_x) 
                                                and (block_min_y <= block.y <= block_max_y), block_locations))

    ax_orientation = SmartVector(start.x - destination.x, start.y - destination.y)

    # we are in the \ situation and we have to consider top_left_location and bottom_right_location
    if ax_orientation == SmartVector(1, -1) or ax_orientation == SmartVector(-1, 1):
        top_left_location = SmartCoordinate()
        bottom_right_location = SmartCoordinate()

        if start.y > destination.y:
            top_left_location = start
            bottom_right_location = destination
        else:
            top_left_location = destination
            bottom_right_location = start

        translation_vector = -bottom_right_location
        start = start + translation_vector
        destination = destination + translation_vector
        filtered_blocks = list(map(lambda block: block + translation_vector, filtered_blocks))
        filtered_blocks = list(map(lambda block: SmartCoordinate(-block.x, block.y), filtered_blocks))

    #we are in the / situation on the positive quadrant and can consider top_right_location and bottom_left_location
    else:
        top_right_location = SmartCoordinate()
        bottom_left_location = SmartCoordinate()

        if start.y > destination.y:
            top_right_location = start
            bottom_left_location = destination
        else:
            top_right_location = destination
            bottom_left_location = start

        translation_vector = -bottom_left_location
        start = start + translation_vector
        destination = destination + translation_vector
        filtered_blocks = list(map(lambda block: block + translation_vector, filtered_blocks))
        

    # mapping the grid world into a binary matrix to performing some calculations 
    # (read documentation for better explanation )
    grid_map = [[0 for i in range(map_size[0])] for j in range(map_size[1])]    

    for block_location in filtered_blocks:
        grid_map[block_location.y][block_location.x] = 1

    base_manhattan_distance = _manhattan_distance_between(start, destination)

    result_indexes = []

    previous_bitmap_row = grid_map[0]
    previous_mapping_indexes_right = []

    for index, value in enumerate(previous_bitmap_row):
        if value == 0:
            previous_mapping_indexes_right.append(index)
        else:
            break

    result_indexes.append(previous_mapping_indexes_right)

    for bitmap_row_index, bitmap_row in enumerate(grid_map[1:]):
        legal_row = [value if index in previous_mapping_indexes_right else 1 for index, value in enumerate(bitmap_row)] 
        
        indexes = [index for index, value in enumerate(legal_row) 
                   if value == 0 and previous_bitmap_row[index] == 0] #if index < len(previous_row) else False)]

        mapping_right = set()

        for index in indexes:
            for row_index, value in enumerate(bitmap_row[index:]):
                if value == 0:
                    mapping_right.add(row_index + index)
                else:
                    break

        if not mapping_right:
            # no solution with manhattan distance
            return base_manhattan_distance + 1 + 3
            # 1 because there is no way to reach destination with a straight manhattan path, 
            #   so also manhattan needs at least one rotation
            # 2 because it need to one step farther and one step to recover that step distance 
            # 1 for minimum orientation overhead (manhattan from farther location)
        
        result_indexes.append(sorted(list(mapping_right)))
        previous_bitmap_row = bitmap_row
        previous_mapping_indexes_right = mapping_right
    

    if not (map_size[0] - 1 in result_indexes[-1]):
        # no solution with manhattan distance
        return base_manhattan_distance + 1 + 3
        # 1 because there is no way to reach destination with a straight manhattan path, 
        #   so also manhattan needs at least one rotation
        # 2 because it need to one step farther and one step to recover that step distance 
        # 1 for minimum orientation overhead (manhattan from farther location)

    else:
        # there is a straight path to the goal with no blocks
        if len(result_indexes) == 1 or all([len(mapping_right) == 1 for mapping_right in result_indexes]):
            return base_manhattan_distance

        # straight right then up is available
        elif (len(result_indexes[0]) == map_size[0]
             and all([map_size[0] - 1 in mapping_right for mapping_right in result_indexes])):
            return base_manhattan_distance + 1 # only one orientation needed  EEEEE {LEFT} NNNNN
        # straight up then right is available
        elif (len(result_indexes[-1]) == map_size[0]
             and all([0 in mapping_right for mapping_right in result_indexes])):
            return base_manhattan_distance + 1 # only one orientation needed  NNNNN {RIGHT} EEEEE
        
        # one direction straight, the other can be split up in two
        elif (list(range(map_size[0])) in result_indexes 
             or any([False not in boolean_list for boolean_list in [[i in mapping_right for mapping_right in result_indexes] for i in range(map_size[0])]])):
            return base_manhattan_distance + 2 # maybe only two orientation needed  EE {LEFT} NNNNN {RIGHT} EEE 
                                               # at least an entire segment must be followed straight

        else:
            return base_manhattan_distance + 3 # all other cases


# HEURISTIC FUNCTIONS

def heuristic_func_manhattan(state):
    """
    the traditional manhattan distance from agent location to goal (+ coming back if the agent 
    hasn't grabbed the gold yet)
    """
    goal_location = state.gold_locations[0] if state.gold_locations else state.exit_locations[0]
    base_cost = 0

    if state.gold_locations:
        base_cost = _manhattan_distance_between(state.gold_locations[0], state.exit_locations[0])

    return _manhattan_distance_between(state.agent_location, goal_location) + base_cost


def heuristic_func_manhattan_with_orientation_overhead(state):
    """
    if the goal is aligned to the agent location, then there's no need to rotate, 
    otherwise we need to rotate at least once
    """
    goal_location = state.gold_locations[0] if state.gold_locations else state.exit_locations[0]
    base_cost = 0

    if state.gold_locations:
        base_cost = _manhattan_distance_between(state.gold_locations[0], state.exit_locations[0])

    base_cost += 1 if state.gold_locations else 0
    base_cost += 1 if not state.has_agent_climbed_out else 0

    goal_manhattan_distance = _manhattan_distance_between(state.agent_location, goal_location)
    orientation_cost = _get_cost_to_orientate_to(goal_location, from_location=state.agent_location, with_orientation=state.agent_orientation)

    if state.agent_location.x == goal_location.x or state.agent_location.y == goal_location.y:
        return goal_manhattan_distance + orientation_cost + base_cost
    else:
        return goal_manhattan_distance + orientation_cost + 1 + base_cost # it needs to rotate at least once

def heuristic_func_wumpus_gold_together(state):
    """
    check if the wumpus is in the same location of the gold, 
    then return manhtann distance + 10 if true, manhattan distance otherwise
    """
    goal_location = state.gold_locations[0] if state.gold_locations else state.exit_locations[0]
    base_cost = 0

    if state.gold_locations:
        base_cost = _manhattan_distance_between(state.gold_locations[0], state.exit_locations[0])

    manhattan_distance = _manhattan_distance_between(state.agent_location, goal_location)
    wumpuses_to_be_killed = len(set(state.wumpus_locations) and set(state.gold_locations))
    shoot_cost = 10

    return manhattan_distance + (shoot_cost * wumpuses_to_be_killed) + base_cost

def heuristic_func_best_neighbour(state):
    """
    Check all ortogonally adjacent tiles, then sum up the cost to reach each tile (rotation + movement + shoot?)
    and add it to the manhattan distance of the neighbour to the goal.
    It eventually return the lowest value of all of them.
    """
    goal_location = state.gold_locations[0] if state.gold_locations else state.exit_locations[0]
    pit_block_locations = state.pit_locations + HuntWumpusState.block_locations

    base_cost = 0
    if state.gold_locations:
        orientation_overhead = _get_orientation_overhead_to_reach(state.exit_locations[0], 
                                                                  from_location=state.gold_locations[0])
        base_cost = (_manhattan_distance_between(state.gold_locations[0], state.exit_locations[0]) 
                    + orientation_overhead)

    base_cost += 1 if state.gold_locations else 0
    base_cost += 1 if not state.has_agent_climbed_out else 0

    if state.agent_location == goal_location:
        shoot_cost = 0 if state.agent_location not in state.wumpus_locations else 10
        return base_cost + shoot_cost

    agent_orientation = state.agent_orientation
    perpendicular_orientation = agent_orientation.get_perpendicular_vector_clockwise()

    north_location = state.agent_location + agent_orientation
    east_location = state.agent_location + perpendicular_orientation
    south_location = state.agent_location - agent_orientation
    west_location = state.agent_location - perpendicular_orientation

    neighbour_locations = [north_location, east_location, south_location, west_location]
    neighbour_blocks = []
    
    for neighbour in neighbour_locations:
        if not (neighbour.x in range(HuntWumpusState.world_size[0]) 
                and neighbour.y in range(HuntWumpusState.world_size[1]) 
                and neighbour not in pit_block_locations):
            neighbour_blocks.append(neighbour)

    # never executed since no movement allowed for the agent
    if neighbour_locations == neighbour_blocks:
        return _manhattan_distance_between(state.agent_location, goal_location) + base_cost

    reaching_goal_orientations = _get_orientations_to_reach(goal_location, 
                                                            from_location=state.agent_location)
    
    escape_locations = [exit for exit in neighbour_locations if exit not in neighbour_blocks]

    escape_locations_costs = []
    for escape_location in escape_locations:
        cost_to_orientiate_to_escape_location = _get_cost_to_orientate_to(escape_location, 
                                                                          from_location=state.agent_location, 
                                                                          with_orientation=state.agent_orientation)
        move_cost = 1
        shoot_cost = 0 if escape_location not in state.wumpus_locations else 10
        orientation_cost = _get_cost_to_orientate_to(goal_location, from_location=escape_location, with_orientation=SmartVector.from_coordinate(escape_location - state.agent_location))
        goal_manhattan_distance = _manhattan_distance_between(escape_location, goal_location)
        orientation_overhead = _get_orientation_overhead_to_reach(goal_location, 
                                                                  from_location=escape_location)

        escape_locations_costs.append(cost_to_orientiate_to_escape_location 
                                      + move_cost 
                                      + shoot_cost
                                      + orientation_cost
                                      + goal_manhattan_distance 
                                      + orientation_overhead)

    return base_cost + min(escape_locations_costs)


def heuristic_func_smart_manhattan(state):
    """
    This heuristic uses the smart_manhattan_distance defined at the top of the file to get a very close approximation 
    of the minimum available manhattan distance reaching the goal starting from the agent location, in the case a valid 
    manhattan path is available, otherwise it will return the cheapest non_manhattan alternative path.
    For more information on how this manhattan work look at the documentation.
    """
    goal_location = state.gold_locations[0] if state.gold_locations else state.exit_locations[0]
    pit_block_locations = state.pit_locations + HuntWumpusState.block_locations
    
    base_cost = 0
    if state.gold_locations:
        base_cost = _smart_manhattan_distance(state.gold_locations[0], destination=state.exit_locations[0], with_block_locations=pit_block_locations)

    base_cost += 1 if state.gold_locations else 0
    base_cost += 1 if not state.has_agent_climbed_out else 0

    if state.wumpus_locations:
        if state.gold_locations:
            base_cost += 10 if state.gold_locations[0] in state.wumpus_locations or state.exit_locations[0] in state.wumpus_locations else 0
        else:
            base_cost += 10 if state.exit_locations[0] in state.wumpus_locations else 0

    if state.agent_location == goal_location:
        return base_cost
    
    cost_to_orientiate_to_goal_location = _get_cost_to_orientate_to(goal_location, 
                                                                    from_location=state.agent_location, 
                                                                    with_orientation=state.agent_orientation)

    manhattan_distance_to_goal = _smart_manhattan_distance(state.agent_location, destination=goal_location, with_block_locations=pit_block_locations)
    return cost_to_orientiate_to_goal_location + manhattan_distance_to_goal + base_cost


def heuristic_func_best_neighbour_smart_manhattan(state):
    """
    This is a re-implementation of the heuristic_func_best_neighbour function using the _smart_manhattan_distance 
    helper method defined on the top of the file, for more information about how smart_manhattan_distance calculates
    an approximation of the distance from a starting location to a destination location look at the documentation
    """
    goal_location = state.gold_locations[0] if state.gold_locations else state.exit_locations[0]
    pit_block_locations = state.pit_locations + HuntWumpusState.block_locations
    
    base_cost = 0
    if state.gold_locations:
        base_cost = _smart_manhattan_distance(state.gold_locations[0], destination=state.exit_locations[0], with_block_locations=pit_block_locations)

    base_cost += 1 if state.gold_locations else 0
    base_cost += 1 if not state.has_agent_climbed_out else 0

    if state.wumpus_locations:
        if state.gold_locations:
            base_cost += 10 if state.gold_locations[0] in state.wumpus_locations or state.exit_locations[0] in state.wumpus_locations else 0
        else:
            base_cost += 10 if state.exit_locations[0] in state.wumpus_locations else 0

    if state.agent_location == goal_location:
        return base_cost

    agent_orientation = state.agent_orientation
    perpendicular_orientation = agent_orientation.get_perpendicular_vector_clockwise()

    north_location = state.agent_location + agent_orientation
    east_location = state.agent_location + perpendicular_orientation
    south_location = state.agent_location - agent_orientation
    west_location = state.agent_location - perpendicular_orientation

    neighbour_locations = [north_location, east_location, south_location, west_location]
    neighbour_blocks = []
    
    for neighbour in neighbour_locations:
        if not (neighbour.x in range(HuntWumpusState.world_size[0]) 
                and neighbour.y in range(HuntWumpusState.world_size[1]) 
                and neighbour not in pit_block_locations):
            neighbour_blocks.append(neighbour)

    # never executed since no movement allowed for the agent
    if neighbour_locations == neighbour_blocks:
        return _smart_manhattan_distance(state.agent_location, destination=state.exit_locations[0], with_block_locations=pit_block_locations) + base_cost

    reaching_goal_orientations = _get_orientations_to_reach(goal_location, 
                                                            from_location=state.agent_location)

    escape_locations = [exit for exit in neighbour_locations if exit not in neighbour_blocks]
    
    escape_locations_costs = []
    for escape_location in escape_locations:
        cost_to_orientiate_to_escape_location = _get_cost_to_orientate_to(escape_location, 
                                                                              from_location=state.agent_location, 
                                                                              with_orientation=state.agent_orientation)
        move_cost = 1

        shoot_cost = 0
        # if it is the goal location the cost has already been taken care in the base_cost
        if escape_location != goal_location:
            shoot_cost = 0 if escape_location not in state.wumpus_locations else 10
        
        manhattan_distance_to_goal = _smart_manhattan_distance(escape_location, destination=goal_location, with_block_locations=pit_block_locations)
        orientation_cost = _get_cost_to_orientate_to(goal_location, from_location=escape_location, with_orientation=SmartVector.from_coordinate(escape_location - state.agent_location))

        escape_locations_costs.append(cost_to_orientiate_to_escape_location
                                      + move_cost
                                      + shoot_cost
                                      + manhattan_distance_to_goal
                                      + orientation_cost)

    return min(escape_locations_costs) + base_cost

