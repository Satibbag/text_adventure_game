# Defines the Item class that will be used
# to generate the items for the game.
class Item:
	def __init__(self, name="", description_text="", pickup_text="", use_text="", obj_type=""):
		self.name = name
		self.description_text = description_text
		self.pickup_text = pickup_text
		self.use_text = use_text
		self.obj_type = obj_type
	
	# Returns the item's description text as the Item's string representation.
	def __str__(self):
		return self.description_text
	
	# Special function that does a different action depending on the
	# type of object that is defined.
	def special(self, curr_room, **kwargs):
		# Checks to see if the current object is a key.
		if self.obj_type == "key":
			# Loops through the used kwargs.
			for key, value in kwargs:
				# If one of the used kwargs is "unlocked_directions",
				# it adds the new, unlocked directions to the list
				# of valid movements for the player.
				if key == "unlocked_directions":
					new_directions = value
					for direction in new_directions:
						curr_room.allowed_movements.append(direction)
						print(f"You can now move {direction}!")
