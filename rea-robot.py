"""
rea-robot.py

Simulates a little toy robot on a table.

Usage
=====
To run commands from an example file (see example.in, included):
rea-robot.py -i <input file>

Otherwise, the program will read commands from stdin until ctrl-d (ctrl-z on
windows) is input.

Additional Commands
===================
Beyond the spec, for testing purposes, I added two additional 'valid' inputs,
the program accepts blank lines, and also accepts any line starting with 
'RESET'. When given a 'RESET' line, the program sets the state back to the
initial state, (None, None)

"""

import argparse
import sys

from robot import process_command as command

def cmdline_args():
    """
    Create command line parameters and parse the current command line.
    """
    parser = argparse.ArgumentParser(description='Toy Robot Simulator')
    parser.add_argument('--input', '-i', type=argparse.FileType('r'),
                        default=sys.stdin,
                        help="Input file containing robot commands, "
                        "one per line.")
    parser.parse_args()

def main():
    """
    Get commands from stdin or input file, and run the toy robot.
    """
    args = cmdline_args()
    state = None,None
    
    for line in args.input.readlines():
        # For testing purposes
        if line.upper().startswith("RESET"):
            print(">>> Reset <<<")
            state = None,None
        elif line.isspace():
            continue
        else:
            state = command(line, *state)
    

if __name__ == "__main__":
    # doctest.testmod()
    main()
