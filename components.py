import math
import random as rd

class Var:
    """Variables class"""
    def __init__(self, name=None, initvalue=0, timestepvalue=0):
        self.name, self.initvalue, self.timestepvalue = name, initvalue, timestepvalue


class Status:
    """Status class"""
    def __init__(self, var_name=None, thresholdsup=math.inf, thresholdinf=-math.inf,
                 new_status_name=lambda:None, create_agent_func=None):
        # We stock a "new_status_name - generator"
        self.new_status = lambda: create_agent_func(new_status_name())
        # And we also stock a simple-to-call condition-verifier
        if var_name is None: self.condition = lambda self : True
        else: self.condition = lambda self: (thresholdinf < getattr(self, var_name)[0] < thresholdsup)

    def make_status_change(self, agent):
        """check if condition is fulfilled and perform the status change"""
        if self.condition(agent): agent.cell.agent = self.new_status()


class Sensor:
    """Sensors class

    Sensor will have the form {0:value for self.cell, 1: {cell : value for cell in 1-neighbours}, 
                                2 : {cell : value for cell in 2-neighbours}, etc ..}"""
    def __init__(self, sensor_name=None, var_name=None, coeff=1, range_=1):
        self.var_name, self.coeff = var_name, coeff
        self.sensor_name, self.range_ = sensor_name, range_ + 1

    def sensor_get(self, agent):
        """get sensor values and set them as a variale for agent"""
        dict_ = {i : {cell : cell.fields_input[self.var_name] * self.coeff 
                      for cell in agent.cell.neighbours[i]} for i in range(1, self.range_)}
        dict_[0] = agent.cell.fields_input[self.var_name] * self.coeff
        setattr(agent, self.sensor_name, dict_)


class Field:
    """Fields class"""
    def __init__(self, var_name=None, decrease=-1, max_range=None, self_included=False):
        self.var_name, self.decrease = var_name, decrease
        # self_included is set to True if agent can be eaten or is able to reproduce
        self.max_range, self.start_range = max_range, 0 if self_included else 1

    def field_activate(self, agent):
        """set cell.fields_input to the right value for all the relevant cells"""
        value = getattr(agent, self.var_name)[0]
        # On ne va pas plus loin que ce sur quoi on a de l'impact (+1 pour etre sur, pour les decrease non entiers)
        max_revelant_range = min(math.floor(-value/self.decrease)+1, self.max_range)
        for i in range(self.start_range, max_revelant_range):
            for cell in agent.cell.neighbours[i]:
                cell.fields_input[self.var_name] += value + i * self.decrease


class Birth:
    """Births class"""
    def __init__(self, var_name=None, thresholdsup=math.inf, thresholdinf=-math.inf,
                 child_name=lambda:None, create_agent_func=None, nb_of_births=lambda:1):
        # We stock a "new_status_name - generator"
        self.child = lambda: create_agent_func(child_name())
        # Number of childs (random)
        self.nb_of_births = lambda : int(nb_of_births())
        # And we also stock a simple-to-call condition-verifier
        if var_name is None: self.condition = lambda self : True
        else: self.condition = lambda self: (thresholdinf < getattr(self, var_name)[0] < thresholdsup)

    def make_birth(self, agent):
        # Check condition
        if self.condition(agent):

            for _ in range(self.nb_of_births()):
            # Get all possible cells for a birth (ie empty 1-neighbours)
                possible_cells = [cell for cell in agent.cell.neighbours[1] if cell.agent is None]
                if not possible_cells: return None 

                # Build a dict with possibles cells as keys and their attractiveness as values
                relevant_neighbours = {cell : sum([getattr(agent, sensor.sensor_name)[1][cell]
                                                   for sensor in agent.sensors]) for cell in possible_cells}

                # Compute cells that are the most attractive (attractiveness exactly equal to the max)
                max_value = max([relevant_neighbours[cell] for cell in possible_cells])
                possible_birth_cells = [cell for cell in possible_cells if relevant_neighbours[cell] == max_value]

                # Choose randomly from those cells to find the cell we will give birth into
                birth_cell = rd.choice(possible_birth_cells)

                # Acutally give birth
                birth_cell.agent = self.child()

