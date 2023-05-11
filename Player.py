# Import the necessary modules.
# Import numpy.array() and numpy.add() so that I can store and update the player's position.
from numpy import array, add


# Defines the Player class that will be used to generate player objects.
class Player:
    """The Player object"""
    def __init__(self):
        # Positions are in x, y, z
        self.__position = array([0, 0, 0])  # The current position of the player. (Private Attribute)
        self.inventory = []  # List of the items currently in the player's inventory.
        self.inventory_names = []  # List of the names of the items currently in the player's inventory.
        self.name = input("What is your name?\n> ").title()  # Asks the user what their name and sets it as the title.
        self.won = False  # Stores if the player has beaten the game or not.
        # Displays a greeting to the user after they input their name.
        print(f"Greetings {self.name}!\nYour epic quest begins now...")
        pause = input("Press \"Enter\" to continue!")

    def __str__(self):
        """Purely for debugging purposes."""
        return "\n\nPLAYER\n"\
               f"Current Position: {self.__position} | {self.position}\n" \
               f"Inventory: {self.inventory}\n" \
               f"Inventory Names: {self.inventory_names}\n" \
               f"Name: {self.name}\n" \
               f"Won: {self.won}"

    @property
    def position(self):
        """Getter for the private "position" attribute."""
        return tuple(self.__position)

    @position.setter
    def position(self, new):
        """Setter for the private "position" attribute."""
        self.__position = add(self.__position, new)


# Initialize the Player object.
player = Player()
