'''
Driver for OOP Network-based Stratego in Python.
'''

from typing import List
import sys
from stratego.gui import StrategoGUI


def main(_: List[str]) -> int:
    '''
    Main function which drives Stratego.

    :param argv: The command-line arguments.
    :returns: 0 on success, non-zero on error.
    '''

    __debug: bool = True

    if __debug:
        print('Running in debug mode: Errors will not be caught.')
        StrategoGUI()

    else:
        # Call the GUI
        try:
            StrategoGUI()

        # Recover from caught errors
        except Exception as e:
            print(f'Unrecoverable error occurred: {e}')
            return 255

    return 0


# Call the main function, launching the game.
if __name__ == '__main__':
    sys.exit(main(sys.argv))
