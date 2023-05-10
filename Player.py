# Import the necessary modules.

class Player:
    """The Player object"""
    def __init__(self):
        # Positions are in x, y, z
        self.__position = (0, 0, 0)  # The current position of the player. (Private Attribute)
        self.inventory = []  # List of the items currently in the player's inventory.
        self.inventory_names = []  # List of the names of the items currently in the player's inventory.
        self.name = input("What is your name?\n> ").title()  # Asks the user what their name and sets it as the title.
        # Displays a greeting to the user after they input their name.
        print(f"Greetings {self.name}!\nYour epic quest begins now...")
        pause = input("Press \"Enter\" to continue!")
        print()

    @property
    def position(self):
        """Getter for the private "position" attribute."""
        return tuple(self.__position)

    @position.setter
    def position(self, new):
        """Setter for the private "position" attribute."""
        self.__position += new


# Initialize the Player object.
player = Player()
