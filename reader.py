import math
import random as rd
from classes import Mineral, Vegetal, Animal
import tkinter as tk
from PIL import Image, ImageTk


def if_possible_float(expr):
    try:
        return float(expr)
    except:
        return expr


class Parser:
    def __init__(self, model, Var, Sensor, Status, Field, Birth, taille):
        self.nb_row, self.nb_col = 0, 0
        self.dico_start, self.dico_agents, self.champs = {}, {}, []
        self.dico_order = {'mineral': Mineral,
                           'vegetal': Vegetal,
                           'animal': Animal}
        self.dico_range = {'mineral': 0, 'vegetal': 1, 'animal': 1}
        self.model = model
        self.Var, self.Sensor, self.Status = Var, Sensor, Status
        self.Field, self.Birth = Field, Birth
        self.taille = taille

    def treatement(self, line_):
        line_ = line_.replace(', ', ',')
        line_ = line_.replace('\n', '')
        line_ = line_.replace('\t', '')
        line = line_.split('%')[0]
        line = line.split()
        if line == []:
            return ['']
        return line

    def condition_parser(self, condi):
        if '=' in condi:
            condi = condi.split('=')
            condi = [if_possible_float(expr) for expr in condi]
            if isinstance(condi[0], float):
                thresholdinf, thresholdsup = condi[0] - 1, condi[0] + 1
                varname = condi[1]
            else:
                thresholdinf, thresholdsup = condi[1] - 1, condi[1] + 1
                varname = condi[0]
        elif '<' in condi:
            condi = condi.split('<')
            condi = [if_possible_float(expr) for expr in condi]
            if len(condi) == 2:
                if isinstance(condi[0], float):
                    thresholdinf, thresholdsup = condi[0], math.inf
                    varname = condi[1]
                else:
                    thresholdsup, thresholdinf = condi[1], -math.inf
                    varname = condi[0]
            elif len(condi) == 3:
                thresholdinf, thresholdsup = condi[0], condi[2]
                varname = condi[1]
        elif '>' in condi:
            condi = condi.split('>')
            condi = [if_possible_float(expr) for expr in condi]
            if len(condi) == 2:
                if isinstance(condi[0], float):
                    thresholdsup, thresholdinf = condi[0], -math.inf
                    varname = condi[1]
                else:
                    thresholdinf, thresholdsup = condi[1], math.inf
                    varname = condi[0]
            elif len(condi) == 3:
                thresholdsup, thresholdinf = condi[0], condi[2]
                varname = condi[1]
        return varname, thresholdinf, thresholdsup

    def check_choice(self, line):
        if 'choice' not in line:
            return line
        else:
            line = line[7:-1].split(',')
            choice_ = rd.choice(line)
            if choice_ == 'empty':
                return None
            return choice_

    def check_choice_rand(self, line):
        if 'choice' not in line:
            return lambda line=line : line
        else:
            line = line[7:-1].split(',')
            return lambda line=line: rd.choice(line)

    def parse_color_image(self, line):
        if line[0] == '#' and len(line) == 4:
            return line, None
        else:
            width = int(self.taille / self.nb_row - self.taille / (100 * self.nb_row)) - 4
            height = int(self.taille / self.nb_col - self.taille / (100 * self.nb_col)) - 4
            img = Image.open(line)
            img = img.resize((height, width))
            return None, ImageTk.PhotoImage(img)

    def read(self, file):
        line = self.treatement(file.readline())
        while True:
            if line == ['']:
                line = self.treatement(file.readline())
            if 'END' in line:
                break
            elif line[0] == 'world':
                self.nb_row = int(line[1])
                self.nb_col = int(line[2])
                self.world_color = self.parse_color_image(line[3])[0]
                for row in range(self.nb_row):
                    for col in range(self.nb_col):
                        self.dico_start[(row, col)] = None
                line = self.treatement(file.readline())
            elif line[0] == 'agent':
                if 'all' in line[2:]:
                    for row in range(self.nb_row):
                        for col in range(self.nb_col):
                            self.dico_start[(row, col)] = self.check_choice(
                                                                    line[1])
                else:
                    for tuple_ in line[2:]:
                        if ':' in tuple_:
                            tuple_ = tuple_[1:-1].split(',')
                            if ':' in tuple_[0] and ':' in tuple_[1]:
                                tuple1 = tuple_[0].split(':')
                                tuple2 = tuple_[1].split(':')
                                for row in range(int(tuple1[0]),
                                                 int(tuple1[1]) + 1):
                                    for col in range(int(tuple2[0]),
                                                     int(tuple2[1]) + 1):
                                        self.dico_start[(row, col)] = \
                                         self.check_choice(line[1])
                            elif ':' in tuple_[0]:
                                tuple1 = tuple_[0].split(':')
                                for row in range(int(tuple1[0]),
                                                 int(tuple1[1])+1):
                                    self.dico_start[(row, int(tuple_[1]))] = \
                                     self.check_choice(line[1])
                            elif ':' in tuple_[1]:
                                tuple1 = tuple_[1].split(':')
                                for col in range(int(tuple1[0]),
                                                 int(tuple1[1])+1):
                                    self.dico_start[(int(tuple_[0]), col)] = \
                                     self.check_choice(line[1])
                        else:
                            self.dico_start[eval(tuple_)] = \
                             self.check_choice(line[1])
                line = self.treatement(file.readline())

            elif (line[0] == 'mineral' or
                  line[0] == 'vegetal' or
                  line[0] == 'animal'):
                name, order = line[1], line[0]
                eat, eatenby, males, females = [], [], [], []
                color, img = self.parse_color_image(line[2])
                self.dico_agents[name] = {'name':name,
                                          'bg': color,
                                          'img': img,
                                          'order': self.dico_order[order],
                                          'eat' : eat,
                                          'eatenby' : eatenby,
                                          'males' : males,
                                          'females' : females,
                                          'vars': [],
                                          'status': [],
                                          'sensors': [],
                                          'fields': [],
                                          'births': []}
                line_ = self.treatement(file.readline())
                while line_[0] in ['eat', 'eatenby', 'males', 'females']:
                    if line_[0] == 'eat':
                        for name_ in line_[1].split(','):
                            eat.append(name_)
                    elif line_[0] == 'eatenby':
                        for name_ in line_[1].split(','):
                            eatenby.append(name_)
                    elif line_[0] == 'males':
                        for name_ in line_[1].split(','):
                            males.append(name_)
                    elif line_[0] == 'females':
                        for name_ in line_[1].split(','):
                            females.append(name_)
                    line_ = self.treatement(file.readline())
                line2 = line_   
                while line2[0] not in ['mineral', 'vegetal', 'animal', 'agent',
                                       'END']:
                    if line2 == ['']:
                        pass
                    elif line2[0] == 'var':
                        var_name = line2[1]
                        if len(line2) == 2:
                            self.dico_agents[name]['vars'].append(
                                self.Var(name=var_name))
                        elif len(line2) == 3:
                            self.dico_agents[name]['vars'].append(
                                self.Var(
                                    name=var_name,
                                    initvalue=float(line2[2]))
                                )
                        else:
                            self.dico_agents[name]['vars'].append(
                                self.Var(
                                    name=var_name,
                                    initvalue=float(line2[2]),
                                    timestepvalue=float(line2[3]))
                                )

                    elif line2[0] == 'sensor':
                        self.dico_agents[name]['sensors'].append(
                            self.Sensor(
                                sensor_name=line2[1],
                                var_name=line2[2],
                                coeff=float(line2[3]),
                                range_=self.dico_range[order])
                            )

                    elif line2[0] == 'status':
                        if len(line2) == 2:
                            new_status_name = self.check_choice_rand(line2[1])
                            self.dico_agents[name]['status'].append(
                                 self.Status(
                                     new_status_name=new_status_name,
                                     create_agent_func=self.model.create_agent)
                                )
                        else:
                            varname, thresholdinf, thresholdsup = \
                             self.condition_parser(line2[1])
                            new_status_name = self.check_choice_rand(line2[2])
                            self.dico_agents[name]['status'].append(
                                self.Status(
                                    var_name=varname,
                                    thresholdsup=thresholdsup,
                                    thresholdinf=thresholdinf,
                                    new_status_name=new_status_name,
                                    create_agent_func=self.model.create_agent)
                                )

                    elif line2[0] == 'field':
                        self.champs.append(line2[1])
                        self.dico_agents[name]['fields'].append(
                            self.Field(
                                var_name=line2[1],
                                decrease=float(line2[2]),
                                max_range = max(self.nb_row, self.nb_col),
                                self_included = True if eatenby+males+females != [] else False)
                            )

                    elif line2[0] == 'birth':
                        n = lambda:1
                        if len(line2) == 4: 
                            n = self.check_choice_rand(line2[3])
                        varname, thresholdinf, thresholdsup = \
                         self.condition_parser(line2[1])
                        child_name = self.check_choice_rand(line2[2])
                        self.dico_agents[name]['births'].append(
                            self.Birth(
                                var_name=varname,
                                thresholdinf=thresholdinf,
                                thresholdsup=thresholdsup,
                                child_name=child_name,
                                create_agent_func=self.model.create_agent,
                                nb_of_births=n)
                            )
                    line2 = self.treatement(file.readline())
                line = line2

        return {'nb_row': self.nb_row, 'nb_col': self.nb_col,
                'world_color': self.world_color,
                'dict_agents': self.dico_agents,
                'dict_start': self.dico_start,
                'champs': self.champs}
