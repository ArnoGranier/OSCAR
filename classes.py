import random as rd


class Mineral:
	"""Class of a mineral agent"""
	def __init__(self, data):
		# Instanciate data (wich are useful for minerals)
		for attr in ['name', 'bg', 'img', 'vars', 'status', 'fields', 'sensors', 'eatenby']:
			setattr(self, attr, data[attr])
		# To get along with "sensor's datas", all variables will be of the form {0 : value}
		for var in self.vars: setattr(self, var.name, {0: var.initvalue})

	def __str__(self):
		return self.name

	def var_time_step(self):
		"""increment all variale (through time)"""
		for var in self.vars: getattr(self, var.name)[0] += var.timestepvalue
		
	def all_sensor_get(self):
		"""get all sensors values"""
		for sensor in self.sensors: sensor.sensor_get(self)
	def all_sensor_reset(self):
		"""reset all sensors values"""
		for sensor in self.sensors: sensor.sensor_reset(self)
	def all_status_change(self):
		"""change all status"""
		for status in self.status: status.make_status_change(self)
	def all_field_activate(self):
		"""activate (propagate) all fields"""
		for field in self.fields: field.field_activate(self)


class Vegetal(Mineral):
	"""Class of a vegetal (inherit from Mineral)"""
	def __init__(self, data):
		Mineral.__init__(self, data)
		# Compared to minerals, some other variables are useful for vegetals
		for attr in ['births', 'males', 'females']: setattr(self, attr, data[attr])
		if self.females : self.preg = {0: 0} #female must have the preg (for pregnant) variable

	def all_birth_make(self):
		"""make all births"""
		for birth in self.births: birth.make_birth(self)


class Animal(Vegetal):
	"""Class of an animal agent"""
	def __init__(self, data):
		Vegetal.__init__(self, data)
		# Contrary to vegetals, animals can eat
		setattr(self, 'eat', data['eat'])
		# We introduce a variable speed wich specify .. well the speed of the animal
		# (That does not meen it will travel multiple cell as once, but rather one cell every x time step)
		# default is move every time step, 1 would be wait 1 time step each time, etc ..
		if 'speed' not in [var.name for var in self.vars]: self.speed = {0: 0}
		self.temp = self.speed[0]

	def move(self):
		"""Movement function for animals"""
		# Taking speed into account
		if self.temp <= 0:
			self.temp = self.speed[0]

			# Get all possible cells for a movement (ie self.cell and all 1-neighbours cells wich does not
			# contains something that we can't step into)
			possible_cells = [self.cell] + [cell for cell in self.cell.neighbours[1] 
							  if cell.agent == None or cell.agent.name in self.eat+self.males+self.females]
			if not possible_cells: return  

			# Build a dict with possibles cells as keys and their attractiveness as values
			relevant_neighbours = {cell : sum([getattr(self, sensor.sensor_name)[1][cell] if cell != self.cell 
											   else getattr(self, sensor.sensor_name)[0] 
											   for sensor in self.sensors]) for cell in possible_cells}

			# Compute cells that are the most attractive (attractiveness exactly equal to the max)
			max_value = max(relevant_neighbours.values())
			possible_move_cells = [cell for cell in possible_cells if relevant_neighbours[cell] == max_value]

			# Choose randomly from those cells to find the cell we will move into
			move_cell = rd.choice(possible_move_cells)

			# If this cell wasn't empty we still have to do some things ..
			if move_cell != self.cell and move_cell.agent is not None :

				# If we eat something we absorb variables that we share with our food
				if move_cell.agent.name in self.eat:
					all_vars_prev = set([var.name for var in move_cell.agent.vars])
					all_vars_self = set([var.name for var in self.vars])
					to_change = all_vars_prev.intersection(all_vars_self)
					for name in to_change:
						getattr(self, name)[0] += getattr(move_cell.agent, name)[0]

				# If we tried to step into a male, we don't move 
				# (we do that to avoid female to go away when male try to .. do their things)
				elif move_cell.agent.name in self.males:
					return

				# Reproduction ! If tried to step into a female, we set the female preg (for pregnant) variable
				# to 1 (this is a mandatory variable for all females) and we actually don't move
				elif move_cell.agent.name in self.females:
					move_cell.agent.preg = {0:1}
					return

			# Actually perform the movement
			self.cell.agent, move_cell.agent = None, self
		else:
			self.temp -= 1 
