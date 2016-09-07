"""
robot.py

Contains methods for managing the state of the robot as described in 
PROBLEM.md.

"""
from __future__ import print_function
import sys
import re
    
faces = {
    "NORTH" : {"LEFT" : "WEST", "RIGHT" : "EAST"},
    "EAST" : {"LEFT" : "NORTH", "RIGHT" : "SOUTH"},
    "SOUTH" : {"LEFT" : "EAST", "RIGHT" : "WEST"},
    "WEST" : {"LEFT" : "SOUTH", "RIGHT" : "NORTH"}
    }
    
moves = {
    "NORTH" : (0, 1),
    "EAST" : (1, 0),
    "SOUTH" : (0, -1),
    "WEST" : (-1, 0)
    }
    
    
def out_of_bounds(position, bounds):
    """
    Determines if a position is out of bounds on the table.
    
    >>> out_of_bounds((0,0), (1,1))
    False
    
    >>> out_of_bounds((1,1), (1,1))
    True
    
    >>> out_of_bounds((0,1), (5,1))
    True
    
    >>> out_of_bounds((1,0), (1,5))
    True
    
    """
    return (position[0] < 0 or position[0] >= bounds[0] 
            or position[1] < 0 or position[1] >= bounds[1])
    
    
def place(place_pos, place_facing, curr_pos, curr_facing, bounds):
    """
    Place the robot on a legal space on the table.
    
    >>> place((1,2), "EAST", None, None, (5,5))
    ((1, 2), 'EAST')
    
    >>> place((1,2), "EAST", (4,4), "SOUTH", (5,5))
    ((1, 2), 'EAST')
    
    >>> place((5,5), "NORTH", None, None, (5,5))
    (None, None)
     
    """    
    # If we're trying to place the robot out of bounds, do nothing.
    if out_of_bounds(place_pos, bounds):
        return curr_pos, curr_facing
    
    return place_pos, place_facing
    
    
def move(position, facing, bounds):
    """
    Move one unit in the currently facing direction.
    
    >>> move((0,0), "NORTH", (2,2))
    (0, 1)
    
    >>> move((0,0), "SOUTH", (2,2))
    (0, 0)
    
    >>> move((0,1), "NORTH", (2,2))
    (0, 1)
    
    """
    new_pos = (position[0] + moves[facing][0], position[1] + moves[facing][1])
    
    if out_of_bounds(new_pos, bounds):
        return position
    
    return new_pos
    
    
def turn(direction, facing):
    """
    Turn the robot, changing the direction it's facing.
    
    >>> turn("LEFT", "NORTH")
    'WEST'
    
    >>> turn("RIGHT", turn("RIGHT", "WEST"))
    'EAST'
    
    >>> turn("BANANA", "EAST")
    'EAST'
    
    """
    new_face = faces[facing].get(direction, None)
    if new_face is not None:
        return new_face
    
    return facing
    
    
def report(position, facing):
    """
    Reports the current location of the robot
    
    >>> report((0,0), "EAST")
    Pos: 0,0 Face: EAST
    
    """
    print("Pos: {0},{1} Face: {2}".format(position[0], position[1], facing))
    

def process_command(line, position=None, facing=None, bounds=(5,5)):
    """
    Takes a robot and a command, and processes it if able. If the command 
    cannot be processed, the current position and facing is returned unchanged.
    
    >>> process_command("PLACE zero zero NORTH", None, None)
    (None, None)
    
    >>> process_command("PLACE 1 2 UP", (0,0), "EAST", (5,5))
    ((0, 0), 'EAST')
    
    >>> process_command("JUMP", (0,0), "NORTH")
    ((0, 0), 'NORTH')
    
    """
    line = line.strip().upper()
    default = position, facing
    
    if line.startswith("PLACE"):
        # Split on comma or whitespace, remove empty items, and take everything
        # after "PLACE"
        line = [x for x in re.split(r"\s|,", line) if len(x) > 0][1:]
        
        if line[-1] not in faces.keys():
            return default
        else:
            place_facing = line[-1]
            
        try:
            place_pos = int(line[0]), int(line[1])
        except ValueError:
            print("Unable to parse position in PLACE command - ({0}, {1})"
                .format(line[0], line[1]), file=sys.stderr)
            return default
            
        return place(place_pos, place_facing, position, facing, bounds)
    
    # Only accept PLACE commands until position and facing have a value.    
    elif(position is not None and facing is not None):            
        if line == "MOVE":
            return move(position, facing, bounds), facing
            
        elif line == "LEFT" or line == "RIGHT":
            return position, turn(line, facing)
            
        elif line == "REPORT":
            report(position, facing)
            return default
    
    return default
    
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()