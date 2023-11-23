
# wumpus_kb.py (original)
# Source: http://www.sista.arizona.edu/~clayton/courses/ai/projects/wumpus/docs/wumpus_kb.html

# the Work Distribution is written as "*** ${Name} Code Here ***"


# wumpus_kb.py
# ------------
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

import utils

#-------------------------------------------------------------------------------
# Wumpus Propositions
#-------------------------------------------------------------------------------

### atemporal variables

proposition_bases_atemporal_location = ['P', 'W', 'S', 'B']

def pit_str(x, y):
    "There is a Pit at <x>,<y>"
    return 'P{0}_{1}'.format(x, y)
def wumpus_str(x, y):
    "There is a Wumpus at <x>,<y>"
    return 'W{0}_{1}'.format(x, y)
def stench_str(x, y):
    "There is a Stench at <x>,<y>"
    return 'S{0}_{1}'.format(x, y)
def breeze_str(x, y):
    "There is a Breeze at <x>,<y>"
    return 'B{0}_{1}'.format(x, y)

### fluents (every proposition who's truth depends on time)

proposition_bases_perceptual_fluents = ['Stench', 'Breeze', 'Glitter', 'Bump', 'Scream']

def percept_stench_str(t):
    "A Stench is perceived at time <t>"
    return 'Stench{0}'.format(t)
def percept_breeze_str(t):
    "A Breeze is perceived at time <t>"
    return 'Breeze{0}'.format(t)
def percept_glitter_str(t):
    "A Glitter is perceived at time <t>"
    return 'Glitter{0}'.format(t)
def percept_bump_str(t):
    "A Bump is perceived at time <t>"
    return 'Bump{0}'.format(t)
def percept_scream_str(t):
    "A Scream is perceived at time <t>"
    return 'Scream{0}'.format(t)

proposition_bases_location_fluents = ['OK', 'L']

def state_OK_str(x, y, t):
    "Location <x>,<y> is OK at time <t>"
    return 'OK{0}_{1}_{2}'.format(x, y, t)
def state_loc_str(x, y, t):
    "At Location <x>,<y> at time <t>"
    return 'L{0}_{1}_{2}'.format(x, y, t)

def loc_proposition_to_tuple(loc_prop):
    """
    Utility to convert location propositions to location (x,y) tuples
    Used by HybridWumpusAgent for internal bookkeeping.
    """
    parts = loc_prop.split('_')
    return (int(parts[0][1:]), int(parts[1]))

proposition_bases_state_fluents = ['HeadingNorth', 'HeadingEast',
                                   'HeadingSouth', 'HeadingWest',
                                   'HaveArrow', 'WumpusAlive']

def state_heading_north_str(t):
    "Heading North at time <t>"
    return 'HeadingNorth{0}'.format(t)
def state_heading_east_str(t):
    "Heading East at time <t>"
    return 'HeadingEast{0}'.format(t)
def state_heading_south_str(t):
    "Heading South at time <t>"
    return 'HeadingSouth{0}'.format(t)
def state_heading_west_str(t):
    "Heading West at time <t>"
    return 'HeadingWest{0}'.format(t)
def state_have_arrow_str(t):
    "Have Arrow at time <t>"
    return 'HaveArrow{0}'.format(t)
def state_wumpus_alive_str(t):
    "Wumpus is Alive at time <t>"
    return 'WumpusAlive{0}'.format(t)

proposition_bases_actions = ['Forward', 'Grab', 'Shoot', 'Climb',
                             'TurnLeft', 'TurnRight', 'Wait']

def action_forward_str(t=None):
    "Action Forward executed at time <t>"
    return ('Forward{0}'.format(t) if t != None else 'Forward')
def action_grab_str(t=None):
    "Action Grab executed at time <t>"
    return ('Grab{0}'.format(t) if t != None else 'Grab')
def action_shoot_str(t=None):
    "Action Shoot executed at time <t>"
    return ('Shoot{0}'.format(t) if t != None else 'Shoot')
def action_climb_str(t=None):
    "Action Climb executed at time <t>"
    return ('Climb{0}'.format(t) if t != None else 'Climb')
def action_turn_left_str(t=None):
    "Action Turn Left executed at time <t>"
    return ('TurnLeft{0}'.format(t) if t != None else 'TurnLeft')
def action_turn_right_str(t=None):
    "Action Turn Right executed at time <t>"
    return ('TurnRight{0}'.format(t) if t != None else 'TurnRight')
def action_wait_str(t=None):
    "Action Wait executed at time <t>"
    return ('Wait{0}'.format(t) if t != None else 'Wait')


def add_time_stamp(prop, t): return '{0}{1}'.format(prop, t)

proposition_bases_all = [proposition_bases_atemporal_location,
                         proposition_bases_perceptual_fluents,
                         proposition_bases_location_fluents,
                         proposition_bases_state_fluents,
                         proposition_bases_actions]


#-------------------------------------------------------------------------------
# Axiom Generator: Current Percept Sentence
#-------------------------------------------------------------------------------


# def make_percept_sentence(t, tvec):
def axiom_generator_percept_sentence(t, tvec):
    """
    ROGUE FUNCTION: The inputs are neglected and replaced with phyiscal percept
    Asserts that each percept proposition is True or False at time t.

    t := time
    tvec := a boolean (True/False) vector with entries corresponding to
            percept propositions, in this order:
                (<stench>,<breeze>,<glitter>,<bump>,<scream>)

    Name: Aharnish Pithva
    id: AU2040022

    Example:
        Input:  [False, True, False, False, True]
        Output: '~Stench0 & Breeze0 & ~Glitter0 & ~Bump0 & Scream0'
    """
    # FIXME:
    # old_tvec = tvec
    # tvec = wumpus_colour_and_move.get_real_tvec()
    # tvec[3]=old_tvec[3]

    # input("Enter current detected colour: ")

    old_tvec = tvec
    tvec = wumpus_colour_and_move.get_input_tvec()
    tvec[3]=old_tvec[3]

    props = []
    percepts = ['Stench','Breeze','Glitter','Bump','Scream']
    for index in range(len(tvec)):
        if tvec[index]:
            props.append(percepts[index] + str(t))
        else:
            props.append('~' + percepts[index] + str(t))
    axiom_str = ' & '.join(props)
    return axiom_str



#-------------------------------------------------------------------------------
# Axiom Generators: Initial Axioms
#-------------------------------------------------------------------------------

def axiom_generator_initial_location_assertions(x, y):
    """
    Assert that there is no Pit and no Wumpus in the location

    x,y := the location

    Name: Freya Shah
    id: AU2120184

    ---> Test input:
    axiom= axiom_generator_initial_location_assertions(1,1)
    print(axiom)
    ---> Test output:
    (~P1_1) & (~W1_1)
    """
    axiom_str = '(~{0}) & (~{1})'.format(pit_str(x,y),wumpus_str(x,y)) #asserts that there is no pit and wumpus at the given location by calling the previously defined pit and wumpus functions
    return axiom_str

def axiom_generator_pits_and_breezes(x, y, xmin, xmax, ymin, ymax):
    """
    Assert that Breezes (atemporal) are only found in locations where
    there are one or more Pits in a neighboring location (or the same location!)

    x,y := the location
    xmin, xmax, ymin, ymax := the bounds of the environment; you use these
           variables to 'prune' any neighboring locations that are outside
           of the environment (and therefore are walls, so can't have Pits).
    
    Name: Freya Shah
    id: AU2120184

    ---> Test input:
    axiom= axiom_generator_pits_and_breezes(2,1,0,5,0,5)
    print(axiom)
    ---> Test output:
    B2_1 <=> (P1_1 | P2_0 | P3_1 | P2_2 | P2_1)
    """
    axiom_str = ''

    pits = []
    for (xVal,yVal) in [((x-1),y),(x,(y-1)),((x+1),y),(x,(y+1))]: #picking the locations up, below, right and left
        if xVal >= xmin and xVal <= xmax and yVal >= ymin and yVal <= ymax: # if the location is in the bound of the environment then append in pits list
            pits.append(pit_str(xVal,yVal))
    pits.append('P'+str(x)+'_'+str(y)) #append the the given location
    axiom_str += '{0} <=> ({1})'.format(breeze_str(x,y),(' | ').join(pits)) #axiom that asserts breezes are found in location where there are one or more Pits in a neighboring location (or the same location!)

    return axiom_str

def generate_pit_and_breeze_axioms(xmin, xmax, ymin, ymax):
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_pits_and_breezes(x, y, xmin, xmax, ymin, ymax))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_pits_and_breezes')
    return axioms

def axiom_generator_wumpus_and_stench(x, y, xmin, xmax, ymin, ymax):
    """
    Assert that Stenches (atemporal) are only found in locations where
    there are one or more Wumpi in a neighboring location (or the same location!)

    (Don't try to assert here that there is only one Wumpus;
    we'll handle that separately)

    x,y := the location
    xmin, xmax, ymin, ymax := the bounds of the environment; you use these
           variables to 'prune' any neighboring locations that are outside
           of the environment (and therefore are walls, so can't have Wumpi).

    Name: Freya Shah
    id: AU2120184

    ---> Test input:
    axiom= axiom_generator_wumpus_and_stench(2,1,0,5,0,5)
    print(axiom)
    ---> Test output:
    S2_1 <=> (W1_1 | W2_0 | W3_1 | W2_2 | W2_1)
    """
    axiom_str = ''
    wumpus = []
    for (xVal, yVal) in [((x - 1), y), (x, (y - 1)), ((x + 1), y), (x, (y + 1))]: #picking the locations up, below, right and left
        if xVal >= xmin and xVal <= xmax and yVal >= ymin and yVal <= ymax: # if the location is in the bound of the environment then append in wumpus list
            wumpus.append(wumpus_str(xVal, yVal))
    wumpus.append('W'+str(x)+'_'+str(y))
    axiom_str = '{0} <=> ({1})'.format(stench_str(x, y), (' | ').join(wumpus)) #axiom that asserts that Stenches (atemporal) are only found in locations where there are one or more Wumpi in a neighboring location (or the same location!)
    return axiom_str


def generate_wumpus_and_stench_axioms(xmin, xmax, ymin, ymax):
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_wumpus_and_stench(x, y, xmin, xmax, ymin, ymax))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_wumpus_and_stench')
    return axioms

def axiom_generator_at_least_one_wumpus(xmin, xmax, ymin, ymax):    # assuming inclusive range 
    """
    Assert that there is at least one Wumpus.

    xmin, xmax, ymin, ymax := the bounds of the environment.

    Name: Aharnish Pithva
    id: AU2040022

    ---> Test input:
    axiom= axiom_generator_at_least_one_wumpus(0,3,0,3)
    print(axiom)
    ---> Test output:
    W0_0 | W0_1 | W0_2 | W0_3 | W1_0 | W1_1 | W1_2 | W1_3 | W2_0 | W2_1 | W2_2 | W2_3 | W3_0 | W3_1 | W3_2 | W3_3
    """
    axiom_str = ''
    possible_wumpus_pos = []

    for y in range(ymin,ymax+1):
        for x in range(xmin, xmax + 1):
            possible_wumpus_pos.append([x,y])

    for indx, this_pos in iter(possible_wumpus_pos):
        if(indx != 0):
            axiom_str += " | "
        axiom_str += wumpus_str(this_pos[0],this_pos[1])

    # Comment or delete the next line once this function has been implemented.
    # utils.print_not_implemented()
    return axiom_str

def axiom_generator_at_most_one_wumpus(xmin, xmax, ymin, ymax):
    """
    Assert that there is at at most one Wumpus.

    xmin, xmax, ymin, ymax := the bounds of the environment.



    Name: Aharnish Pithva
    id: AU2040022

    ---> Test input:
    axiom= axiom_generator_at_most_one_wumpus(0,2,0,2)
    print(axiom)
    ---> Test output:
    (~W0_0 & ~W1_0 & ~W2_0 & ~W0_1 & ~W1_1 & ~W2_1 & ~W0_2 & ~W1_2 & ~W2_2) | (W0_0 & ~W0_1 & ~W0_2 & ~W1_0 & ~W1_1 & ~W1_2 & ~W2_0 & ~W2_1 & ~W2_2) | (~W0_0 & ~W0_1 & ~W0_2 & W1_0 & ~W1_1 & ~W1_2 & ~W2_0 & ~W2_1 & ~W2_2) | (~W0_0 & ~W0_1 & ~W0_2 & ~W1_0 & ~W1_1 & ~W1_2 & W2_0 & ~W2_1 & ~W2_2) | (~W0_0 & W0_1 & ~W0_2 & ~W1_0 & ~W1_1 & ~W1_2 & ~W2_0 & ~W2_1 & ~W2_2) | (~W0_0 & ~W0_1 & ~W0_2 & ~W1_0 & W1_1 & ~W1_2 & ~W2_0 & ~W2_1 & ~W2_2) | (~W0_0 & ~W0_1 & ~W0_2 & ~W1_0 & ~W1_1 & ~W1_2 & ~W2_0 & W2_1 & ~W2_2) | (~W0_0 & ~W0_1 & W0_2 & ~W1_0 & ~W1_1 & ~W1_2 & ~W2_0 & ~W2_1 & ~W2_2) | (~W0_0 & ~W0_1 & ~W0_2 & ~W1_0 & ~W1_1 & W1_2 & ~W2_0 & ~W2_1 & ~W2_2) | (~W0_0 & ~W0_1 & ~W0_2 & ~W1_0 & ~W1_1 & ~W1_2 & ~W2_0 & ~W2_1 & W2_2)
    """
    axiom_str = ''

    # initially insert a case when there is no wumpus on the board, because the function is for at most one qumpus
    axiom_str += '('
    for y in range(ymin,ymax+1):
        for x in range(xmin, xmax + 1):
            if(x != 0 or y != 0):
                axiom_str += " & "
            axiom_str += "~" + wumpus_str(x,y)

    axiom_str += ') | '

    # array such that there is exactly one wumpus on the board for every grid positions on the board.
    array_single_wumpus = []

    for y in range(ymin,ymax+1):
        for x in range(xmin, xmax + 1):
            if(x != 0 or y != 0):
                axiom_str += " | "
            axiom_str += "("

            # inner loop to generate a single state where there is wumpus at exactly single position on the board
            for xi in range(xmin, xmax + 1):
                for yi in range(ymin,ymax+1):
                    if(xi != 0 or yi != 0):
                        axiom_str += " & "
                    if(x == xi and y == yi):    # this state represents wumpus at position (xi, yi)
                        axiom_str += wumpus_str(xi,yi)
                    else:                       # this state represents wumpus not at (xi, yi)
                        axiom_str += "~" +wumpus_str(xi,yi)

            axiom_str += ")"
            
    

    return axiom_str

def axiom_generator_only_in_one_location(px, py, xmin, xmax, ymin, ymax, t = 0):
    """
    Assert that the Agent can only be in one (the current xi,yi) location at time t.

    xi,yi := the current location.
    xmin, xmax, ymin, ymax := the bounds of the environment.
    t := time; default=0
    """
    """
    Name: Aharnish Pithva
    id: AU2040022
    """
    axiom_str = ''


    # inner loop to generate a single state where there is wumpus at exactly single position on the board
    for xi in range(xmin, xmax + 1):
        for yi in range(ymin,ymax+1):
            if(xi != 0 or yi != 0):
                axiom_str += " & "
            if(px == xi and py == yi):    # this state represents wumpus at position (xi, yi)
                axiom_str += state_loc_str(xi,yi,t=t)
            else:                       # this state represents wumpus not at (xi, yi)
                axiom_str += "~" + state_loc_str(xi,yi,t=t)
                
    # axiom_str += ")"

    return axiom_str


def axiom_generator_only_one_heading(heading = 'north', t = 0):
    """
    Assert that Agent can only head in one direction at a time.

    heading := string indicating heading; default='north';
               will be one of: 'north', 'east', 'south', 'west'
    t := time; default=0
    """
    """
    Name: Aharnish Pithva
    id: AU2040022
    """

    legal_headings = ["north", 'east', 'south', 'west']

    axiom_str = ''

    for indx in range(len(legal_headings)):
        this_heading = legal_headings[indx]
        if(indx != 0):
            axiom_str += " & "
        if(heading.lower() == this_heading.lower()):
            axiom_str += "Heading_" + this_heading
        else:
            axiom_str += "~" + "Heading_" + this_heading
        
        # insert current time to the knowledge state
        axiom_str += str(t)

    return axiom_str

def axiom_generator_have_arrow_and_wumpus_alive(t = 0):
    """
    Asserts that Agent has the arrow and the Wumpus is alive at time t.

    t := time; default=0

    Name: Freya Shah
    id: AU2120184
    """
    axiom_str = '{0} & {1}'.format(state_have_arrow_str(t),state_wumpus_alive_str(t))
    return axiom_str


def initial_wumpus_axioms(xi, yi, width, height, heading='east'):
    """
    Generate all of the initial wumpus axioms
    
    xi,yi = initial location
    width,height = dimensions of world
    heading = str representation of the initial agent heading
    """
    axioms = [axiom_generator_initial_location_assertions(xi, yi)]
    axioms.extend(generate_pit_and_breeze_axioms(1, width, 1, height))
    axioms.extend(generate_wumpus_and_stench_axioms(1, width, 1, height))
    
    axioms.append(axiom_generator_at_least_one_wumpus(1, width, 1, height))
    axioms.append(axiom_generator_at_most_one_wumpus(1, width, 1, height))

    axioms.append(axiom_generator_only_in_one_location(xi, yi, 1, width, 1, height))
    axioms.append(axiom_generator_only_one_heading(heading))

    axioms.append(axiom_generator_have_arrow_and_wumpus_alive())
    
    return axioms


#-------------------------------------------------------------------------------
# Axiom Generators: Temporal Axioms (added at each time step)
#-------------------------------------------------------------------------------



def axiom_generator_location_OK(x, y, t):
    """
    Name:  Bhargav Kargatiya
    ID:  AU2140121
    Assert the conditions under which a location is safe for the Agent.
    (Hint: Are Wumpi always dangerous?)

    x, y := location
    t := time
    Example Input: x=2, y=3, t=1
    Example Output: OK2_3_1 <=> ((~P2_3 & ~W2_3) | (~P2_3 & ~WumpusAlive1))

     {0}: Represents the state condition for a safe location.
    ~{1}: Ensures there is no pit at the location.
    ~{2}: Represents the state of the Wumpus being alive at time t.
    ~{3}: Ensures there is no Wumpus at the location.
    """
    # The overall logical proposition can be read as follows:
    # The location is safe if and only if there is no pit and either there is no Wumpus or the Wumpus is dead.
    axiom_str = '{0} <=> ((~{1} & ~{3}) | (~{1} & ~{2}))'.format(
        state_OK_str(x, y, t),
        pit_str(x, y),
        state_wumpus_alive_str(t),
        wumpus_str(x, y)
    )

    return axiom_str


def generate_square_OK_axioms(t, xmin, xmax, ymin, ymax):
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_location_OK(x, y, t))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_location_OK')
    return filter(lambda s: s != '', axioms)


#-------------------------------------------------------------------------------
# Connection between breeze / stench percepts and atemporal location properties

def axiom_generator_breeze_percept_and_location_property(x, y, t):
    """
    Name: Bhargav Kargatiya
    ID: AU2140121
    Assert that when in a location at time t, then perceiving a breeze
    at that time (a percept) means that the location is breezy (atemporal)

    x, y := location
    t := time
    Example Input: x=2, y=3, t=1
    Example Output: L2_3_1 >> (Breeze1 <==> B2_3)

    # {0}: Represents the state of being in a particular location at a specific time.
    # {1}: Represents the perception of a breeze at a given time.
    # {2}: Represents the atemporal property of the location being breezy.
    """
    # Logical expression: If in a specific location at a specific time, perceiving a breeze is equivalent to the location being breezy.
    axiom_str = '{0} >> ({1} <==> {2})'.format(state_loc_str(
        x, y, t), percept_breeze_str(t), breeze_str(x, y))
    return axiom_str

def generate_breeze_percept_and_location_axioms(t, xmin, xmax, ymin, ymax):
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_breeze_percept_and_location_property(x, y, t))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_breeze_percept_and_location_property')
    return filter(lambda s: s != '', axioms)

def axiom_generator_stench_percept_and_location_property(x, y, t):
    """
    Name: Bhargav Kargatiya
    ID: AU2140121

    Assert that when in a location at time t, then perceiving a stench
    at that time (a percept) means that the location has a stench (atemporal)

    x,y := location
    t := time

    Example Input: x=2, y=3, t=1
    Example Output: L2_3_1 >> (Stench1 <==> S2_3)

    # {0}: Represents the state of being in a particular location at a specific time.
    # {1}: Represents the perception of a stench at a given time.
    # {2}: Represents the atemporal property of the location having a stench.

    """
    # Logical expression: If in a specific location at a specific time, perceiving a stench is equivalent to the location having a stench.
    axiom_str = '{0} >> ({1} <==> {2})'.format(state_loc_str(
        x, y, t), percept_stench_str(t), stench_str(x, y))
    return axiom_str

def generate_stench_percept_and_location_axioms(t, xmin, xmax, ymin, ymax):
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_stench_percept_and_location_property(x, y, t))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_stench_percept_and_location_property')
    return filter(lambda s: s != '', axioms)


#-------------------------------------------------------------------------------
# Transition model: Successor-State Axioms (SSA's)
# Avoid the frame problem(s): don't write axioms about actions, write axioms about
# fluents!  That is, write successor-state axioms as opposed to effect and frame
# axioms
#
# The general successor-state axioms pattern (where F is a fluent):
#   F^{t+1} <=> (Action(s)ThatCause_F^t) | (F^t & ~Action(s)ThatCauseNot_F^t)

# NOTE: this is very expensive in terms of generating many (~170 per axiom) CNF clauses!
def axiom_generator_at_location_ssa(t, x, y, xmin, xmax, ymin, ymax):
    """

    Name: Aaditya Yadav
    Id: AU2140094
    
    Assert the condidtions at time t under which the agent is in
    a particular location (state_loc_str: L) at time t+1, following
    the successor-state axiom pattern.

    See Section 7. of AIMA.  However...
    NOTE: the book's version of this class of axioms is not complete
          for the version in Project 3.
    
    x,y := location
    t := time
    xmin, xmax, ymin, ymax := the bounds of the environment.
    """
    axiom_str = ''
    moves = ['({0} & (~{1} | {2} | {3} | {4} | {5} | {6}))'.format(
        state_loc_str(x,y,t),
        action_forward_str(t),
        percept_bump_str(t+1),
        action_grab_str(t),
        action_shoot_str(t),
        action_turn_left_str(t),
        action_turn_right_str(t))]

    for ((xVal,yVal),move) in [(((x-1),y),'E'),((x,(y-1)),'N'),(((x+1),y),'W'),((x,(y+1)),'S')]:
        if xVal >= xmin and xVal <= xmax and yVal >= ymin and yVal <= ymax:
            if move == 'N':
                moves.append('({0} & ({1} & {2}))'.format(state_loc_str(x,y-1,t),state_heading_north_str(t),action_forward_str(t)))
            if move == 'E':
                moves.append('({0} & ({1} & {2}))'.format(state_loc_str(x - 1, y, t), state_heading_east_str(t), action_forward_str(t)))
            if move == 'W':
                moves.append('({0} & ({1} & {2}))'.format(state_loc_str(x + 1, y, t), state_heading_west_str(t), action_forward_str(t)))
            if move == 'S':
                moves.append('({0} & ({1} & {2}))'.format(state_loc_str(x,y+1,t),state_heading_south_str(t),action_forward_str(t)))

    sucLoc = state_loc_str(x,y,t+1)  
    axiom_str = f"{sucLoc} <=> ({' | '.join(moves)})"
    return axiom_str

def generate_at_location_ssa(t, x, y, xmin, xmax, ymin, ymax, heading):
    """
    The full at_location SSA converts to a fairly large CNF, which in
    turn causes the KB to grow very fast, slowing overall inference.
    We therefore need to restric generating these axioms as much as possible.
    This fn generates the at_location SSA only for the current location and
    the location the agent is currently facing (in case the agent moves
    forward on the next turn).
    This is sufficient for tracking the current location, which will be the
    single L location that evaluates to True; however, the other locations
    may be False or Unknown.
    """
    axioms = [axiom_generator_at_location_ssa(t, x, y, xmin, xmax, ymin, ymax)]
    if heading == 'west' and x - 1 >= xmin:
        axioms.append(axiom_generator_at_location_ssa(t, x-1, y, xmin, xmax, ymin, ymax))
    if heading == 'east' and x + 1 <= xmax:
        axioms.append(axiom_generator_at_location_ssa(t, x+1, y, xmin, xmax, ymin, ymax))
    if heading == 'south' and y - 1 >= ymin:
        axioms.append(axiom_generator_at_location_ssa(t, x, y-1, xmin, xmax, ymin, ymax))
    if heading == 'north' and y + 1 <= ymax:
        axioms.append(axiom_generator_at_location_ssa(t, x, y+1, xmin, xmax, ymin, ymax))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_at_location_ssa')
    return filter(lambda s: s != '', axioms)

#----------------------------------

def axiom_generator_have_arrow_ssa(t):
    """
    Name: Bhargav Kargatiya
    ID: AU2140121
    Assert the conditions at time t under which the Agent
    has the arrow at time t+1

    t := time
    Example Input:  t=2
    Example Output: HaveArrow3 <=> (HaveArrow2 & ~Shoot2)

    # {0}: Represents the state of having the arrow at time t+1.
    # {1}: Represents the state of having the arrow at time t.
    # {2}: Represents the action of shooting at time t.
    """
    # Logical expression: The Agent has the arrow at time t+1 if and only if
    # the Agent has the arrow at time t and does not shoot at time t.
    axiom_str = '{0} <=> ({1} & ~{2})'.format(state_have_arrow_str(t+1),
                                              state_have_arrow_str(t), action_shoot_str(t))
    return axiom_str

def axiom_generator_wumpus_alive_ssa(t):
    """
    Assert the conditions at time t under which the Wumpus
    is known to be alive at time t+1

    (NOTE: If this axiom is implemented in the standard way, it is expected
    that it will take one time step after the Wumpus dies before the Agent
    can infer that the Wumpus is actually dead.)

    t := time

    Name: Raiyan Diwan
    ID: AU2140111
    """
    axiom_str = '{0} <=> ({1} & ~{2})'.format(state_wumpus_alive_str(t+1),state_wumpus_alive_str(t),percept_scream_str(t+1))
    return axiom_str

#----------------------------------


def axiom_generator_heading_north_ssa(t):
    """
    Specify the conditions at time t for the
    Agent to be oriented North at time t+1.

    t := time
    
    Name: Raiyan Diwan
    ID: AU2140111
    """

    no_move = '({0} & ({1} | {2} | {3} | {4} | {5}))'.format(state_heading_north_str(t),action_wait_str(t),action_grab_str(t),action_shoot_str(t),percept_bump_str(t+1),action_forward_str(t))
    turn_left = '({0} & {1})'.format(state_heading_east_str(t),action_turn_left_str(t))
    turn_right = '({0} & {1})'.format(state_heading_west_str(t),action_turn_right_str(t))
    axiom_str = '{0} <=> ({1} | {2} | {3})'.format(state_heading_north_str(t+1),no_move,turn_left,turn_right)
    return axiom_str

def axiom_generator_heading_east_ssa(t):
    """
    Specify the conditions at time t for the
    Agent to be oriented East at time t+1.

    t := time
    
    Name: Raiyan Diwan
    ID: AU2140111
    """
    no_move = '({0} & ({1} | {2} | {3} | {4} | {5}))'.format(state_heading_east_str(t),action_wait_str(t),action_grab_str(t),action_shoot_str(t),percept_bump_str(t+1),action_forward_str(t))
    turn_left = '({0} & {1})'.format(state_heading_south_str(t),action_turn_left_str(t))
    turn_right = '({0} & {1})'.format(state_heading_north_str(t),action_turn_right_str(t))
    axiom_str = '{0} <=> ({1} | {2} | {3})'.format(state_heading_east_str(t+1),no_move,turn_left,turn_right)
    return axiom_str

def axiom_generator_heading_south_ssa(t):
    """
    Specify the conditions at time t for the
    Agent to be oriented South at time t+1.

    t := time
    
    Name: Raiyan Diwan
    ID: AU2140111
    """
    no_move = '({0} & ({1} | {2} | {3} | {4} | {5}))'.format(state_heading_south_str(t),action_wait_str(t),action_grab_str(t),action_shoot_str(t),percept_bump_str(t+1),action_forward_str(t))
    turn_left = '({0} & {1})'.format(state_heading_west_str(t),action_turn_left_str(t))
    turn_right = '({0} & {1})'.format(state_heading_east_str(t),action_turn_right_str(t))
    axiom_str = '{0} <=> ({1} | {2} | {3})'.format(state_heading_south_str(t+1),no_move,turn_left,turn_right)
    return axiom_str

def axiom_generator_heading_west_ssa(t):
    """
    Specify the conditions at time t for the
    Agent to be oriented West at time t+1.

    t := time
    
    Name: Raiyan Diwan
    ID: AU2140111
    """
    no_move = '({0} & ({1} | {2} | {3} | {4} | {5}))'.format(state_heading_west_str(t),action_wait_str(t),action_grab_str(t),action_shoot_str(t),percept_bump_str(t+1),action_forward_str(t))
    turn_left = '({0} & {1})'.format(state_heading_north_str(t),action_turn_left_str(t))
    turn_right = '({0} & {1})'.format(state_heading_south_str(t),action_turn_right_str(t))
    axiom_str = '{0} <=> ({1} | {2} | {3})'.format(state_heading_west_str(t+1),no_move,turn_left,turn_right)
    return axiom_str

def generate_heading_ssa(t):
    """
    Generates all of the heading SSAs.
    """
    return [axiom_generator_heading_north_ssa(t),
            axiom_generator_heading_east_ssa(t),
            axiom_generator_heading_south_ssa(t),
            axiom_generator_heading_west_ssa(t)]

def generate_non_location_ssa(t):
    """
    Generate all non-location-based SSAs
    """
    axioms = [] # all_state_loc_ssa(t, xmin, xmax, ymin, ymax)
    axioms.append(axiom_generator_have_arrow_ssa(t))
    axioms.append(axiom_generator_wumpus_alive_ssa(t))
    axioms.extend(generate_heading_ssa(t))
    return filter(lambda s: s != '', axioms)



#----------------------------------

# Written by Aryan Prajapati

# q.)
# q.1)
def axiom_generator_heading_only_north(t):
    """
    Name: Aryan Prajapati [AU2140090]

    Here, we are generating an axiom which ensures that agent is only heading in north direction at a given time t. 
    In the code we are using already defined functions. 
    state_heading_north_str(t), state_heading_east_str(t), state_heading_south_str(t), and state_heading_west_str(t) are functions that return string representations of different heading states at a specific time t. 
    
    --> Axiom Form: 
        (north_t <=> (negated direction_t list)) 

    --> Test Input:
    t=1
    print(axiom_generator_heading_only_north(t)) 

    --> Output:
    (HeadingNorth1 <=> (~HeadingEast1 & ~HeadingSouth1 & ~HeadingWest1))
    
    --> Explanation:
     If the agent is heading north at time 1, it must not be heading in any other direction, and if the agent is not heading east, south, or west, it must be heading north.
     The 1 is appended to direction to represent the time index t. 
    """
    """
    Assert that when heading is North, the agent is not heading any other direction.
    t := time
    """
    negated_directions= '~{0} & ~{1} & ~{2}'.format(state_heading_east_str(t), state_heading_south_str(t),state_heading_west_str(t))        #left side's direction in eq. (north_t <=> (negated direction_t list)) 
    #print(negated_directions)
    axiom_str= '({0} <=> ({1}))'.format(state_heading_north_str(t), negated_directions)                                                    #whole equation formatting
    return axiom_str

    """
    OR

    negated_directions= ['~'+direction+str(t) for direction in proposition_bases_state_fluents[1:4]]
    axiom_str= '({0}{1} <=> ({2}))'.format(proposition_bases_state_fluents[0],str(t)," & ".join(negated_directions))

    *** Note - here we are directly using proposition fluents list to get the output and not using the state functions ***
    proposition_bases_state_fluents = ['HeadingNorth', 'HeadingEast',
                                       'HeadingSouth', 'HeadingWest',
                                       'HaveArrow', 'WumpusAlive']
    """

# Written by Aryan Prajapati
# q.2)
def axiom_generator_heading_only_south(t):
    """
    Name: Aryan Prajapati [AU2140090]

    Here, we are generating an axiom which ensures that agent is heading only in south direction at a given time t. 
    
    --> Axiom Form: 
        (south_t <=> (negated direction_t list)) 

    --> Test Input:
    t=1
    print(axiom_generator_heading_only_south(t)) 

    --> Output:
    (HeadingSouth1 <=> (~HeadingEast1 & ~HeadingNorth1 & ~HeadingWest1))
    
    --> Explanation:
     If the agent is heading south at time 1, it must not be heading in any other direction, and if the agent is not heading east, north or west, it must be heading south.
     The 1 is appended to direction to represent the time index t. 
    """
    negated_directions= '~{0} & ~{1} & ~{2}'.format(state_heading_east_str(t),state_heading_north_str(t),state_heading_west_str(t))
    axiom_str ='({0} <=> ({1}))'.format(state_heading_south_str(t), negated_directions)
    return axiom_str


# Written by Aryan Prajapati
# q.3)
def axiom_generator_heading_only_east(t):
    """
    Name: Aryan Prajapati
    Roll no.: AU2140090

    Here, we are generating an axiom which ensures that agent is heading only in east direction at a given time t. 
    
    --> Axiom Form: 
        (east_t <=> (negated direction_t list)) 

    --> Test Input:
    t=1
    print(axiom_generator_heading_only_east(t)) 

    --> Output:
    (HeadingEast1 <=> (~HeadingNorth1 & ~HeadingSouth1 & ~HeadingWest1))
    
    --> Explanation:
     If the agent is heading east at time 1, it must not be heading in any other direction, and if the agent is not heading north,south or west, it must be heading east.
     The 1 is appended to direction to represent the time index t. 
    """
    """
    Assert that when heading is east, the agent is not heading any other direction.
    t := time
    """
    negated_directions= '~{0} & ~{1} & ~{2}'.format(state_heading_north_str(t), state_heading_south_str(t),state_heading_west_str(t))
    axiom_str= '({0} <=> ({1}))'.format(state_heading_east_str(t), negated_directions)
    return axiom_str


# Written by Aryan Prajapati
# q.4)
def axiom_generator_heading_only_west(t):
    """
    Name: Aryan Prajapati [AU2140090]

    Here, we are generating an axiom which ensures that agent is heading only in west direction at a given time t. 
    
    --> Axiom Form: 
        (west_t <=> (negated direction_t list)) 

    --> Test Input:
    t=1
    print(axiom_generator_heading_only_west(t)) 

    --> Output:
    (HeadingWest1 <=> (~HeadingNorth1 & ~HeadingSouth1 & ~HeadingEast1))
    
    --> Explanation:
     If the agent is heading west at time 1, it must not be heading in any other direction, and if the agent is not heading north,south or west, it must be heading east.
     The 1 is appended to direction to represent the time index t. 
    """
    negated_directions= '~{0} & ~{1} & ~{2}'.format(state_heading_north_str(t), state_heading_south_str(t),state_heading_east_str(t))
    axiom_str= '({0} <=> ({1}))'.format(state_heading_west_str(t), negated_directions)
    return axiom_str



def generate_heading_only_one_direction_axioms(t):
    return [axiom_generator_heading_only_north(t),
            axiom_generator_heading_only_east(t),
            axiom_generator_heading_only_south(t),
            axiom_generator_heading_only_west(t)]


# Written by Aryan Prajapati
# r.)
def axiom_generator_only_one_action_axioms(t):
    """
    Name: Aryan Prajapati [AU2140090]

    Here, we are generating axioms which ensures that only one action can be executed at a given time t.
    
    --> Axiom Form: 
        (action_t <=> (negated action_t list))    {action_t is not in the negated action_t list, <=> (if and only if) operator}

    --> Test Input:
    t = 1
    axioms_str = axiom_generator_only_one_action_axioms(t)
    print(axioms_str)                  
        
    --> Output:
    (TurnRight1 <=> (~TurnLeft1 & ~Forward1 & ~Grab1 & ~Climb1 & ~Shoot1 & ~Wait1)) & (TurnLeft1 <=> (~TurnRight1 & ~Forward1 & ~Grab1 & ~Climb1 & ~Shoot1 & ~Wait1)) & (Forward1 <=> (~TurnRight1 & ~TurnLeft1 & ~Grab1 & ~Climb1 & ~Shoot1 & ~Wait1)) & (Grab1 <=> (~TurnRight1 & ~TurnLeft1 & ~Forward1 & ~Climb1 & ~Shoot1 & ~Wait1)) & (Climb1 <=> (~TurnRight1 & ~TurnLeft1 & ~Forward1 & ~Grab1 & ~Shoot1 & ~Wait1)) & (Shoot1 <=> (~TurnRight1 & ~TurnLeft1 & ~Forward1 & ~Grab1 & ~Climb1 & ~Wait1)) & (Wait1 <=> (~TurnRight1 & ~TurnLeft1 & ~Forward1 & ~Grab1 & ~Climb1 & ~Shoot1))
    
    i.e we get a conjuction of 7 axiom of the form mentioned above.

    --> Explanation:

    It means that if "TurnRight" is true at time 1, then all other actions must be false at time 1, and if all other actions are false at time 1, then "TurnRight" must be true. 
    The 1 is appended to the action names (e.g., Forward1, Grab1) to represent the time index t. This indicates that the actions are associated with a specific time step.

    """
    """
    Assert that only one axion can be executed at a time.
    t := time
    """

    axiom_str = ""
    actions  = ['TurnRight', 'TurnLeft', 'Forward', 'Grab', 'Climb', 'Shoot', 'Wait'] #from wumpus.py file

    length=len(actions)

    for i in range(0,length):                                                   #loop is used to generate negated action list by using array slicing. And to form the axiom equation. 
        a=actions[i]                                                            #left side single action in the eq. (action_t <=> (negated action_t list)) 
        b=actions[0:i] + actions[i+1:length]                                    #right side's negated actions in the eq. (action_t <=> (negated action_t list)) 
        negated_actions= ["~"+ action+str(t) for action in b]                   #loop is used to place '~' sign before every action elemnt in the list.
        axiom_str = axiom_str + '({0}{1} <=> ({2}))'.format(a,str(t),' & '.join(negated_actions)) +" & "        #combining everything here using '+' operator and string formatting

    axiom_str = axiom_str.rstrip(' & ')                                         #removing extra " & " from the right side of the string

    return axiom_str



def generate_mutually_exclusive_axioms(t):
    """
    Generate all time-based mutually exclusive axioms.
    """
    axioms = []
    
    # must be t+1 to constrain which direction could be heading _next_
    axioms.extend(generate_heading_only_one_direction_axioms(t + 1))

    # actions occur in current time, after percept
    axioms.append(axiom_generator_only_one_action_axioms(t))

    return filter(lambda s: s != '', axioms)

#-------------------------------------------------------------------------------

    

