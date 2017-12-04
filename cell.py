class Cell:
    """One cell of the grid, contains agent or None, GUI things take place mainly here"""
    def __init__(self, row, col, size, model = None):
        self.model = model
        self.row, self.col = row, col
        self.w_row, self.w_col = size / model.nb_row, size / model.nb_col # for GUI
        self.y, self.x = self.row * self.w_row + 4, self.col * self.w_col + 4 # GUI positions
        self.aff, self.fields_input, self.agent = None, {}, None
        # fields_input will have the form : {var_name : sum of value of fields produced by this variable on this cell}

    def reset_fields_input(self):
        """Reset all fields inputs"""
        for name in self.fields_input: self.fields_input[name] = 0

    @property
    def agent(self):
        """We define the agent as a property"""
        return self.agent_

    @agent.setter
    def agent(self, agent):
        """setter for agent, update GUI when agent is updated"""
        self.agent_ = agent
        # Each time the agent of a cell changes, we delete the previous represntation on the canvas
        self.model.can.delete(self.aff)
        # Then if the new agent is not None
        if agent is not None:
            agent.cell = self # We pass the cell he is in to the agent
            # We update the canvas
            if agent.img is None:
                self.aff = self.model.can.create_rectangle(
                    self.x + 1, self.y + 1,
                    self.x + self.w_col - 2, self.y + self.w_row - 2,
                    fill=agent.bg, width=0)
            else:
                self.aff = self.model.can.create_image(
                    self.x + self.w_col // 2, self.y + self.w_row // 2,
                    image=agent.img)


    def make_neighbours(self):
        """Determine all the neighbours of the cells

        neighbours will have the form {0:self, 1:[all neighbours with 1-case distance], 
                                        2: [all neighbours with 2-cas distance], etc..}"""
        self.neighbours = {0: [self,]}
        for a in range(1, max(self.model.nb_row,  self.model.nb_col)):
            neighbours = []
            for _col in [b for b in range(-a, a+1) if 0<=self.col+b<self.model.nb_col]:
                for _row in [b for b in [a, -a] if 0<=self.row+b<self.model.nb_row]:
                    neighbours.append(self.model.world[self.row + _row][self.col + _col])
            for _row in [b for b in range(-a+1, a) if 0<=self.row+b<self.model.nb_row]:
                for _col in [b for b in [a, -a] if 0<=self.col+b<self.model.nb_col]:
                    neighbours.append(self.model.world[self.row + _row][self.col + _col])
            self.neighbours[a] = neighbours
