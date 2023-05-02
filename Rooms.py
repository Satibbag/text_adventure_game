# Import the necessary modules.
# Import the Item class so that Items can be generated.
from Items import Item
# Importing numpy.array() so that I can do matrix math.
from numpy import array

# Define the possible movement commands and their
# respective arrays.
MOVEMENT = {"north": array([0 , 1]),
            "south": array([0 ,-1]),
            "east" : array([1 , 0]),
            "west" : array([-1, 0])}


# Define the Room class that will be used to generate
# rooms.
class Room():
	"""Base Room Object"""
	def __init__(self, room_items=[], usable_items=[],
              		allowed_movements=[], descriptions={}):
		self.room_items = room_items  # Items that are in the room.
		self.usable_items = usable_items  # Usable items
		self.allowed_movements = allowed_movements  # The possible valid movement directions
		self.descriptions = descriptions  # (room_items,usable_items) : description text
	
	def __str__(self):
		pass

	def get_item(self, item, player):
		"""Gets an item from the room and adds it to the player's inventory."""
		# Checks to see if there are items in the current room.
		if self.room_items:
			# Asks the user which item they would like to pickup.
			picked_item = input("What item would you like to pick up? | >").lower()
			# Checks to see if the inputted item is a valid item in the room.
			if picked_item in self.room_items:
				# Displays the pickup_text for the item that the player picked up.
				print(picked_item.pickup_text)
				# Adds the picked up item to the player's inventory.
				player.inventory.append(picked_item)
				# Removes the picked up item from the list of items in the room.
				self.room_items.remove(picked_item)
			else:
				# Displays a message if the inputted item isn't a valid item.
				print(f"Couldn't find the {picked_item} item in the room.")
		else:
			# Displays a message if there aren't any items to pickup in the room.
			print("There aren't any items to pick up.")
	
	def use_item(self, player):
		"""Use an item from the player's inventory."""
		# Checks to see if there are items in the player's inventory.
		if player.inventory:
			# Displays the player's current inventory as a bulleted list.
			print(f"Your current inventory:")
			for item in player.inventory:
				print(f"\n* {item}")
			# Asks the user which item they would like to use.
			used_item = input("What item would you like to use? | >").lower()
			# Checks to see if the inputted item is a valid item in the player's inventory
			if used_item in player.inventory:
				# Checks to see if the inputted item is a valid usable item.
				if used_item in self.usable_items:
					# Displays the use_text for the item that the player used.
					print(used_item.use_text)
					# Removes the used item from the player's inventory.
					player.inventory.remove(used_item)
					# Deletes the used item from the list of usable items in the room.
					del self.usable_items[used_item]
					# Runs a special action depending on the type of object that was used.
					used_item.special(self)
