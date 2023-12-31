
# wumpus_planners.py (original)
# Source: http://www.sista.arizona.edu/~clayton/courses/ai/projects/wumpus/docs/wumpus_planners.html

# the Work Distribution is written as "*** ${Name} Code Here ***"


# wumpus_planners.py
# ------------------
# Licensing Information:
# Please DO NOT DISTRIBUTE OR PUBLISH solutions to this project.
# You are free to use and extend these projects for EDUCATIONAL PURPOSES ONLY.
# The Hunt The Wumpus AI project was developed at University of Arizona
# by Clay Morrison (clayton@sista.arizona.edu), spring 2013.
# This project extends the python code provided by Peter Norvig as part of
# the Artificial Intelligence: A Modern Approach (AIMA) book example code;
# see http://aima.cs.berkeley.edu/code.html
# In particular, the following files come directly from the AIMA python
# code: ['agents.py', 'logic.py', 'search.py', 'utils.py']
# ('logic.py' has been modified by Clay Morrison in locations with the
# comment 'CTM')
# The file ['minisat.py'] implements a slim system call wrapper to the minisat
# (see http://minisat.se) SAT solver, and is directly based on the satispy
# python project, see https://github.com/netom/satispy .

from wumpus_environment import *
from wumpus_kb import *
import search

#-------------------------------------------------------------------------------
# Distance fn
#-------------------------------------------------------------------------------

def manhattan_distance_with_heading(current, target):
    """
    Return the Manhattan distance + any turn moves needed
        to put target ahead of current heading
    current: (x,y,h) tuple, so: [0]=x, [1]=y, [2]=h=heading)
    heading: 0:^:north 1:<:west 2:v:south 3:>:east
    """
    md = abs(current[0] - target[0]) + abs(current[1] - target[1])
    if current[2] == 0:   # heading north
        # Since the agent is facing north, "side" here means
        # whether the target is in a row above or below (or
        # the same) as the agent.
        # (Same idea is used if agent is heading south)
        side = (current[1] - target[1])
        if side > 0:
            md += 2           # target is behind: need to turns to turn around
        elif side <= 0 and current[0] != target[0]:
            md += 1           # target is ahead but not directly: just need to turn once
        # note: if target straight ahead (curr.x == tar.x), no turning required
    elif current[2] == 1: # heading west
        # Now the agent is heading west, so "side" means
        # whether the target is in a column to the left or right
        # (or the same) as the agent.
        # (Same idea is used if agent is heading east)
        side = (current[0] - target[0])
        if side < 0:
            md += 2           # target is behind
        elif side >= 0 and current[1] != target[1]:
            md += 1           # target is ahead but not directly
    elif current[2] == 2: # heading south
        side = (current[1] - target[1])
        if side < 0:
            md += 2           # target is behind
        elif side >= 0 and current[0] != target[0]:
            md += 1           # target is ahead but not directly
    elif current[2] == 3: # heading east
        side = (current[0] - target[0])
        if side > 0:
            md += 2           # target is behind
        elif side <= 0 and current[1] != target[1]:
            md += 1           # target is ahead but not directly
    return md


#-------------------------------------------------------------------------------
# Plan Route
#-------------------------------------------------------------------------------

def plan_route(current, heading, goals, allowed):
    """
    Given:
       current location: tuple (x,y)
       heading: integer representing direction
       gaals: list of one or more tuple goal-states
       allowed: list of locations that can be moved to
    ... return a list of actions (no time stamps!) that when executed
    will take the agent from the current location to one of (the closest)
    goal locations
    You will need to:
    (1) Construct a PlanRouteProblem that extends search.Problem
    (2) Pass the PlanRouteProblem as the argument to astar_search
        (search.astar_search(Problem)) to find the action sequence.
        Astar returns a node.  You can call node.solution() to exract
        the list of actions.
    NOTE: represent a state as a triple: (x, y, heading)
          where heading will be an integer, as follows:
          0='north', 1='west', 2='south', 3='east'
    """

    # Ensure heading is a in integer form
    if isinstance(heading,str):
        heading = Explorer.heading_str_to_num[heading]

    if goals and allowed:
        prp = PlanRouteProblem((current[0], current[1], heading), goals, allowed)
        # NOTE: PlanRouteProblem will include a method h() that computes
        #       the heuristic, so no need to provide here to astar_search()
        node = search.astar_search(prp)
        if node:
            return node.solution()
    
    # no route can be found, return empty list
    return []

#-------------------------------------------------------------------------------

class PlanRouteProblem(search.Problem):
    def __init__(self, initial, goals, allowed):
        """ Problem defining planning of route to closest goal
        Goal is generally a location (x,y) tuple, but state will be (x,y,heading) tuple
        initial = initial location, (x,y) tuple
        goals   = list of goal (x,y) tuples
        allowed = list of state (x,y) tuples that agent could move to """
        self.initial = initial # initial state
        self.goals = goals     # list of goals that can be achieved
        self.allowed = allowed # the states we can move into

    # Written by Aryan Prajapati
    def h(self,node):
        #heuristic for A * search using Manhattan distance 
        """
        Name: Aryan Prajapati [AU2140090]
    
        Here the 'h' method uses the manhattan_distance_with_heading func. to calculate the distances with heading for each goal state. It returns the minimum calculated distance from the list.
        
        --> Test Input:
        i_state=(0,0,0)
        g_states=[(3,3,0),(1,2,1),(0,0,2)]
        a_states=[(0,0),(0,1),(1,0),(1,1),(2,2),(3,3)]
        instance_1 = PlanRouteProblem(i_state,g_states,a_states)
        example_node = Node((1, 1, 0)) # assuming node with a state
        print("Heuristic value:", instance_1.h(example_node))
    
        --> Output:
            Heuristic value: 1
            {calc_distance list -- [5, 1, 4]}
        """
        current_state= node.state
        calc_distance=[]
        g_arr=self.goals
        for goal_state in g_arr:                                                    #traversing through goal state array 
            distance =manhattan_distance_with_heading(current_state, goal_state)    #calculating distances using predefined func.
            calc_distance.append(distance)
        #print(calc_distance)
        h_value= min(calc_distance)                                                 #returning the minimum dist value
        return h_value

    
    # Written by Aryan Prajapati
    def actions(self, state):
        #Return list of allowed actions that can be made in state
        """
        Name: Aryan Prajapati [AU2140090]

        Here, we are checking the heading and next state to determine whether moving forward is allowed. A dictionary (next_position) is used to map the possible next positions. 

        --> Test Input:
        i_state=(0,0,0)
        g_states=[(3,3,0),(1,2,1),(0,0,2)]
        a_states=[(0,0),(0,1),(1,0),(1,1),(2,2),(3,3)]
        problem_instance = PlanRouteProblem(i_state, g_states, a_states)

        current_state = (0, 0, 1)   # i.e. agent is at (0,0) facing west
        possible_actions = problem_instance.actions(current_state)
        print(possible_actions)

        --> Output:
        ['TurnRight', 'TurnLeft']    
        *(neighbouring allowed states are (0,1) and (1,0) but it is facing west so it can't go directly forward. Thus a disallowed_actions list is returned)

        for current_state=(0,0,3) # i.e. agent is at (0,0) facing east
        --> Output:
        ['Forward', 'TurnRight', 'TurnLeft']
        """
        allowed_actions = ['Forward','TurnRight','TurnLeft']
        disallowed_actions = ['TurnRight','TurnLeft']

        #possible next positions based on the current heading
        next_position = {
            0: (state[0], state[1] + 1),  # heading north
            1: (state[0] - 1, state[1]),  # heading west
            2: (state[0], state[1] - 1),  # heading south
            3: (state[0] + 1, state[1]),  # heading east
        }
        #print(next_position)
        # checking if moving forward is allowed based on the current heading and allowed states
        if state[2] in next_position and next_position[state[2]] in self.allowed:
            return allowed_actions                  # allow forward movement
        else:
            return disallowed_actions               # no forward movement




    def result(self, state, action):
        """
        Return the new state after applying action to state

        Name: Bhargav Kargatiya
        Number:AU2140121
        """
        "*** Bhargav CODE HERE ***"
         if action == 'TurnRight':
            new_heading = (state[2] + 3) % 4
            return (state[0], state[1], new_heading)

        if action == 'TurnLeft':
            new_heading = (state[2] + 1) % 4
            return (state[0], state[1], new_heading)

        if action == 'Forward':
            direction_changes = [(0, 1), (-1, 0), (0, -1), (1, 0)]
            x_change, y_change = direction_changes[state[2]]
            return (state[0] + x_change, state[1] + y_change, state[2])

    def goal_test(self, state):
        """
        Return True if state is a goal state

        Name: Bhargav Kargatiya
        Number:AU2140121
        """
        "*** Bhargav CODE HERE ***"
        if (state[0:2] in self.goals):
            return True
        return False


#-------------------------------------------------------------------------------

def test_PRP(initial):
    """
    The 'expected initial states and solution pairs' below are provided
    as a sanity check, showing what the PlanRouteProblem soluton is
    expected to produce.  Provide the 'initial state' tuple as the
    argument to test_PRP, and the associate solution list of actions is
    expected as the result.
    The test assumes the goals are [(2,3),(3,2)], that the heuristic fn
    defined in PlanRouteProblem uses the manhattan_distance_with_heading()
    fn above, and the allowed locations are:
        [(0,0),(0,1),(0,2),(0,3),
        (1,0),(1,1),(1,2),(1,3),
        (2,0),            (2,3),
        (3,0),(3,1),(3,2),(3,3)]
    
    Expected intial state and solution pairs:
    (0,0,0) : ['Forward', 'Forward', 'Forward', 'TurnRight', 'Forward', 'Forward']
    (0,0,1) : ['TurnRight', 'Forward', 'Forward', 'Forward', 'TurnRight', 'Forward', 'Forward']
    (0,0,2) : ['TurnLeft', 'Forward', 'Forward', 'Forward', 'TurnLeft', 'Forward', 'Forward']
    (0,0,3) : ['Forward', 'Forward', 'Forward', 'TurnLeft', 'Forward', 'Forward']
    """
    return plan_route((initial[0],initial[1]), initial[2],
                      # Goals:
                      [(2,3),(3,2)],
                      # Allowed locations:
                      [(0,0),(0,1),(0,2),(0,3),
                       (1,0),(1,1),(1,2),(1,3),
                       (2,0),            (2,3),
                       (3,0),(3,1),(3,2),(3,3)])


#-------------------------------------------------------------------------------
# Plan Shot
#-------------------------------------------------------------------------------

def plan_shot(current, heading, goals, allowed):
    """ Plan route to nearest location with heading directed toward one of the
    possible wumpus locations (in goals), then append shoot action.
    NOTE: This assumes you can shoot through walls!!  That's ok for now. """
    if goals and allowed:
        psp = PlanShotProblem((current[0], current[1], heading), goals, allowed)
        node = search.astar_search(psp)
        if node:
            plan = node.solution()
            plan.append(action_shoot_str(None))
            # HACK:
            # since the wumpus_alive axiom asserts that a wumpus is no longer alive
            # when on the previous round we perceived a scream, we
            # need to enforce waiting so that itme elapses and knowledge of
            # "dead wumpus" can then be inferred...
            plan.append(action_wait_str(None))
            return plan

    # no route can be found, return empty list
    return []

#-------------------------------------------------------------------------------

class PlanShotProblem(search.Problem):
    def __init__(self, initial, goals, allowed):
        """ Problem defining planning to move to location to be ready to
              shoot at nearest wumpus location
        NOTE: Just like PlanRouteProblem, except goal is to plan path to
              nearest location with heading in direction of a possible
              wumpus location;
              Shoot and Wait actions is appended to this search solution
        Goal is generally a location (x,y) tuple, but state will be (x,y,heading) tuple
        initial = initial location, (x,y) tuple
        goals   = list of goal (x,y) tuples
        allowed = list of state (x,y) tuples that agent could move to """
        self.initial = initial # initial state
        self.goals = goals     # list of goals that can be achieved
        self.allowed = allowed # the states we can move into

    def h(self, node):
        """
        A heuristic function designed for use in search.astar_search()

        Args:
            self: The instance of the class containing this method.
        node: The current node in the search space.

        Returns:
            int: The calculated heuristic value.
        Name: Freya Shah
        id: AU2120184 
        """
        # Extract possible Wumpus locations and explorer locations
        possible_wumpus_locations = self.goals
        explorer_locations = self.allowed
        shot_spots = []

        # Identify spots where the Wumpus can be shot based on their coordinates
        for wumpus_loc in possible_wumpus_locations:
            for explorer_loc in explorer_locations:
                # If either the x or y coordinate matches, the Wumpus can be shot from this location
                if wumpus_loc[0] == explorer_loc[0] or wumpus_loc[1] == explorer_loc[1]:
                    shot_spots.append(explorer_loc)

        current_state= node.state
        calc_distance=[]
        for goal_state in shot_spots: #traversing through shot spots
            distance =manhattan_distance_with_heading(current_state, goal_state)    #calculating distances using predefined func.
            calc_distance.append(distance)
    
        h_value= min(calc_distance)        
    # Return the minimum distance as the heuristic value
    return h_value

    def actions(self, state):
        """
        Return a list of allowed actions that can be made in the given state.

        Args:
            self: The instance of the class containing this method.
            state: The current state of the agent.

        Returns:
            list: A list of allowed actions based on the current state.

        Name: Freya Shah
        id: AU2120184
        """
        allowed_Forward = ['Forward', 'TurnRight', 'TurnLeft']
        not_Forward = ['TurnRight', 'TurnLeft']
        if state[2] == 0 and (state[0], state[1] + 1) in self.allowed:
            return allowed_Forward
        if state[2] == 1 and (state[0] - 1, state[1]) in self.allowed:
            return allowed_Forward
        if state[2] == 2 and (state[0], state[1] - 1) in self.allowed:
            return allowed_Forward
        if state[2] == 3 and (state[0] + 1, state[1]) in self.allowed:
            return allowed_Forward
        return not_Forward


    def result(self, state, action):
        """
        Name : Aaditya Yadav
        Id : AU2140094
        Return the new state after applying action to state
        """
        if action == 'TurnRight':
            new_heading = (state[2] + 3) % 4
            return (state[0], state[1], new_heading)
        if action == 'TurnLeft':
            new_heading = (state[2] + 1) % 4
            return (state[0], state[1], new_heading)
        if action == 'Forward':
            direction_changes = [(0, 1), (-1, 0), (0, -1), (1, 0)]
            x_change, y_change = direction_changes[state[2]]
            return (state[0] + x_change, state[1] + y_change, state[2])
        pass

    def goal_test(self, state):
        """
        Name : Aaditya Yadav
        Id : AU2140094
        Return True if state is a goal state
        """
        possibleWumpusLocations = self.goals

        if state in self.goals:
            return False

        for location in possibleWumpusLocations:
            if location[0] == state[0]:
                if ((location[1] > state[1]) and state[2] == 0):
                    return True
                if ((location[1] < state[1]) and state[2] == 2):
                    return True
            if location[1] == state[1]:
                if ((location[0] < state[0]) and state[2] == 1):
                    return True
                if ((location[0] > state[0]) and state[2] == 3):
                    return True
        return False

#-------------------------------------------------------------------------------

def test_PSP(initial = (0,0,3)):
    """
    The 'expected initial states and solution pairs' below are provided
    as a sanity check, showing what the PlanShotProblem soluton is
    expected to produce.  Provide the 'initial state' tuple as the
    argumetn to test_PRP, and the associate solution list of actions is
    expected as the result.
    The test assumes the goals are [(2,3),(3,2)], that the heuristic fn
    defined in PlanShotProblem uses the manhattan_distance_with_heading()
    fn above, and the allowed locations are:
        [(0,0),(0,1),(0,2),(0,3),
        (1,0),(1,1),(1,2),(1,3),
        (2,0),            (2,3),
        (3,0),(3,1),(3,2),(3,3)]
    
    Expected intial state and solution pairs:
    (0,0,0) : ['Forward', 'Forward', 'TurnRight', 'Shoot', 'Wait']
    (0,0,1) : ['TurnRight', 'Forward', 'Forward', 'TurnRight', 'Shoot', 'Wait']
    (0,0,2) : ['TurnLeft', 'Forward', 'Forward', 'Forward', 'TurnLeft', 'Shoot', 'Wait']
    (0,0,3) : ['Forward', 'Forward', 'Forward', 'TurnLeft', 'Shoot', 'Wait']
    """
    return plan_shot((initial[0],initial[1]), initial[2],
                     # Goals:
                     [(2,3),(3,2)],
                     # Allowed locations:
                     [(0,0),(0,1),(0,2),(0,3),
                      (1,0),(1,1),(1,2),(1,3),
                      (2,0),            (2,3),
                      (3,0),(3,1),(3,2),(3,3)])
    
#-------------------------------------------------------------------------------

    

