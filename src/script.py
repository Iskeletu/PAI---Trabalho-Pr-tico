"""
Fábio Gandini - 01/12/2025

Main script file, runs the project.
"""

# Internal Modules:
import PSE.problem_solving_environment as PSE


def main() -> None:
    """
    Starts GUI, all other functionalities are called from within the GUI implementation.
    """

    PSE.start()


# This is a script file and should NOT be imported:
if __name__ == '__main__':
    main()