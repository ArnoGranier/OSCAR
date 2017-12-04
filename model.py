import tkinter as tk
from classes import Mineral, Vegetal, Animal
import random as rd


class Model:
    """High-level model"""
    def __init__(self, args):
        self.win = tk.Tk()
        self.win.title('OSCAR')
        self.can = tk.Canvas(self.win, width=args.size, height=args.size)
        self.can.pack()
        self.nb_tick, self.tickrate, self.delay = args.nb_tick, args.tickrate, args.delay

    def all_cells(self):
        """return all the cells"""
        return [cell for line in self.world for cell in line]

    def all_agents(self, order=(Mineral, Vegetal, Animal)):
        """return all agents wich belong to any order specified in order"""
        l = [cell.agent for line in self.world for cell in line
             if type(cell.agent) in order]
        rd.shuffle(l) # We don't want to take agents in any particular order
        return l

    def create_agent(self, name):
        """return an instance of the right agent"""
        if name == 'end' : self.stop() ; return None
        if name == 'death' or name is None: return None
        return self.dict_agents[name]['order'](self.dict_agents[name])

    def tick(self):
        """One time step"""
        agents = self.all_agents()

        # 1. Reset all old fields value
        for cell in self.all_cells(): cell.reset_fields_input()

        # 2. Propagate all fields
        for agent in agents: agent.all_field_activate()

        # 3. Update all sensors
        for agent in agents: agent.all_sensor_get()

        # 4. Make all animals that need to move
        for agent in self.all_agents(order=(Animal,)): agent.move()

        # 5. Make all animals and vegetals that need to give birth
        for agent in self.all_agents(order=(Vegetal,Animal)): agent.all_birth_make()

        # 7. Change all status that need to be changed (stop if any is end)
        for agent in agents: agent.all_status_change()

        # 6. Increment all vars that need to be incremented
        for agent in agents: agent.var_time_step()





    def start(self):
        """Main function"""

        # make neighbours, initialize fields_input
        for cell in self.all_cells():
            cell.make_neighbours()
            for champ in self.champs: cell.fields_input[champ] = 0

        # Put agents in the world
        for ((x, y), dict_start) in self.dict_start.items():
            self.world[x][y].agent = self.create_agent(dict_start)
        self.win.update()

        # Loop through time with a delay of delay, nb_tick times, 
        # waiting tickrate between each step
        self.afters = []
        for i in range(self.delay, self.nb_tick + self.delay):
            self.afters.append(self.win.after(i*self.tickrate, self.tick))
            
        self.win.mainloop()

    def stop(self):
        """Stop the loop"""
        print('ab')
        for after in self.afters:
            self.win.after_cancel(after)