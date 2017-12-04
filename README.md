# OSCAR
[2017][Python 3+] Behavioural Simulation Tool by Attraction - Repulsion

Project proposed by Christophe Schlick, see [his site](http://www.labri.fr/perso/schlick/prog2/prog2.pro2017.html) (in french).
Title of the simulator come from the french : "Outil de Simulation Comportementale par Attraction-répulsion", (actually BSTAR (Behavioural Simulation Tool by Attraction - Repulsion) is also a cool name.)
The goal of this project is to allow anybody to make a simple multi-agent simulation based on the concept of attraction-repulsion. 
Interactions between the user and the code, ie defining all the agents and their interactions, is done by txt configuration files. Format of this file will be describe later, but is intended to be as easy and "noob-friendly" as possible.

# WORK IN PROGRESS, WILL WRITE SOME DOC LATER !

# Examples

To run your simulation with OSCAR, use the command prompt, go to where oscar's file are, and run :
```
python oscar.py forestfire
```
Replace forestfire by the name of your file.

There are some parameters you can tune here (namely tickrate (-v), number of ticks (-n), size of the window (-t), delay before starting (-d)), you can type 
```
python oscar.py -h
```
to get help.


## Forestfire

### Configuration file
```
% -----------------------------------------------------------------------------
% ForestFire : simulates fire propagation
%
% Description :
% - ForestFire is based on 3-state mineral agents: 'tree', 'fire', 'ash'
% - 'fire' agents generate a 'flame' field on their 8 neighbouring cells
% - 'flame' field is captured by 'tree' agents
% - 'tree' turns into 'fire' when surrounded by at least 2 'fire' agents
% - with rules given below, 'fire' turns into 'ash' within two time steps,
%   but this delay can be increased by additional transition rules
% -----------------------------------------------------------------------------

world 32 32 #FFF

mineral tree #0F0
var hot                % default: InitValue=0 TimeStepValue=0
sensor hot flame 2    % 'flame' field is scale by 1 and stored in 'hot'
status hot<2 tree    % 'tree' -> 'tree' when 'hot' < 2
status hot>1 fire    % 'tree' -> 'fire' when 'hot' > 1

mineral fire #F00
var flame 2            % default: TimeStepValue=0
field flame -1         % 'flame' field is reduced by 1 for each distance step
                       % remember that negative field values are replaced by 0
status ash             % 'fire' -> 'ash' without condition

mineral ash #777       % no rules, so 'ash' -> 'ash' without condition
% -----------------------------------------------------------------------------

agent choice(tree,tree,empty, empty, empty) all
agent fire   (16,16) 

END
```

### Output

![alt text](https://user-images.githubusercontent.com/27825602/33574319-ee91264a-d938-11e7-8cfe-c5a9c340ac2b.gif)

## Wireworld

### Configuration file

```
% -----------------------------------------------------------------------------
% WireWorld : Wireworld cellular automata
%             https://en.wikipedia.org/wiki/Wireworld
%
% Description :
% - WireWorld is based on 3-state mineral agents: 'conductor', 'head', 'tail'
% - 'conductor' simulates path for moving electrons
% - 'head' and 'tail' are the two adjacent parts of a moving electron
% - 'head' generates an 'electric' field only captured by 'conductor'
% -----------------------------------------------------------------------------

world 16 16 #000

mineral conductor #FF0
var active                   % default: InitValue=0 TimeStepValue=0
sensor active electric 1
status active<1 conductor
status 0<active<3 head       % 'conductor' -> 'head' only when 'active' == 1 or 2
status active>2 conductor

mineral tail #F00
status conductor             % 'tail' -> 'conductor' without condition

mineral head #00F
var electric 2               % default: TimeStepValue=0
field electric -1
status tail                  % 'head' -> 'tail' without condition

% set two electrons moving on a single horizontal wire (use slice notation)

agent head (8,0) (8,8)
agent conductor (8,1:7) (8,9:15)
agent conductor (1:8,5)

% -----------------------------------------------------------------------------

END
```

### Output

![alt text](https://user-images.githubusercontent.com/27825602/33574320-f008de1e-d938-11e7-94b0-da5cef0afc33.gif)

## Lifegame

### Configuration file
```
% -----------------------------------------------------------------------------
% LifeGame : Conway's Game of Life
%            http://en.wikipedia.org/wiki/Conway's_Game_of_Life
%
% Description :
% - LifeGame is based on 2-state mineral agents: 'live' and 'dead'
% - 'live' agents generate a 'life' field on their 8 neighbouring cells
% - 'dead' and 'live' agents have a 'neighbour' sensor for this 'life' field
% -----------------------------------------------------------------------------

world 16 16 #BBB

mineral dead #FFF
var neighbour               % default: InitValue=0 TimeStepValue=0
status neighbour<3 dead   % status lines are evaluated in given order
status neighbour=3 live   % 'dead' -> 'live' only when 'neighbour' == 3
status neighbour>3 dead
sensor neighbour life 1     % 'life' field is scale by 1 and stored in 'neighbour'

mineral live #000
var life 2                  % default: TimeStepValue=0
var neighbour               % default: InitValue=0 TimeStepValue=0
status neighbour<2 dead
status 1<neighbour<4 live   % 'live' -> 'live' only when 'neighbour' == 2 or 3
status neighbour>3 dead
field life -1
sensor neighbour life 1

% initial configuration for the pentadecathlon oscillator (period 15)
agent dead all
agent live (8,3) (8,4) (7,5) (9,5) (8,6) (8,7)
age
nt live (8,8) (8,9) (7,10) (9,10) (8,11) (8,12)
% -----------------------------------------------------------------------------

END
```

### Output

![alt text](https://user-images.githubusercontent.com/27825602/33574323-f2692b8c-d938-11e7-9c05-65ca677d3cfa.gif)

## Phototropism

### Configuration file
```
% -----------------------------------------------------------------------------
% PhotoTropism : Growth of plants with photophilia or photophobia behaviors
%
% Description :
% - PhotoTropism is based on 1 mineral + 2 vegetal agents
% - 'light' agent generates a standard distance field also called 'light'
% - 'photophilia' plants put their seeds in cells with maximum light field
% - 'photophobia' plants put their seeds in cells with minimum light field
% - with the rules given below, each 'photophilia' agent generates only one
%   seed, whereas 'photophobia' agent generates a new seed each 2 time steps
% -----------------------------------------------------------------------------

world 32 32 #FFF

mineral sun #FF0
var light 99                % 'light' field broadcasts up to distance 99
field light -1

vegetal photophilia #0F0
var seed 4 -1               % photophilia germination requires 4 time steps 
birth seed=0 photophilia % germination when seed = 0
var photo
sensor photo light 1        % 'photo' stores 'light' field sensor (positive)

vegetal photophobia #060
var seed 2 -1               % photophobia germination requires 2 time steps
birth seed<1 photophobia % germination when seed < 1
status seed<1 photophobia % reset photophobia status to generate next seed
var photo
sensor photo light -1       % 'photo' stores 'light' field sensor (negative)

% initial configuration
agent sun (0,16)
agent photophilia (31,0) (31,11) (31,20) (31,31)
agent photophobia (31,10) (31,15) (31,16) (31,21)
% -----------------------------------------------------------------------------

END
```

### Output

![alt text](https://user-images.githubusercontent.com/27825602/33574321-f14b6b70-d938-11e7-9a52-3a26052ba1ae.gif)

## Segregation

### Configuration file
```
% -----------------------------------------------------------------------------
% Segregation : Shelling's model of segregation
%             http://nifty.stanford.edu/2014/mccown-schelling-model-segregation
% Description :
% - Segregation is based on 2-state animal agents: 'red' and 'blue'
% - 'red' agents generate a 'red' field on the 8 neighbouring cells
% - 'blue' agents generate a 'blue' field on the 8 neighbouring cells
% - 'red' agents try to move toward maximal 'red' field and minimal 'blue' field
% - 'blue' agents try to move toward maximal 'blue' field and minimal 'red' field
% - stronger/weaker segregation is observed when changing sensitivity values
% - stronger/weaker segregation is observed when changing field distance
% -----------------------------------------------------------------------------

world 32 32 #FFF

animal red #F00
var red 2
field red -1                % 'red' field is limited to 8 neighbouring cells
sensor discomfort blue -0.3  % 'comfort' is decreased by 'blue' field'
sensor comfort red 0.7 % 'comfort' is increased by 'red' field'

animal blue #00F
var blue 2
field blue -1           % 'blue' field is limited to 8 neighbouring cells
sensor comfort blue 0.7  % 'comfort' is increased by 'blue' field'
sensor discomfort red -0.3 % 'comfort' is decreased by 'red' field'

% initial configuration (using random choice between 'empty', 'red', 'blue')
agent choice(empty,red,blue) (0:31,0:31)
% -----------------------------------------------------------------------------

END
```

### Output

![alt text](https://user-images.githubusercontent.com/27825602/33574326-f3d27c30-d938-11e7-926e-fa412b6853bc.gif)

## Sugarscape

### Configuration file
```
% -----------------------------------------------------------------------------
% Sugarscape : Simplified implementation of the Sugarscape system
%              https://en.wikipedia.org/wiki/Sugarscape
% Description :
% - This version of Sugarscape is based on 1 vegetal and 2 animal states:
% - 'grass' agents grow by germination every 3 time steps
% - 'sheep' agents start with 40 'grass' points and loose 1 point per time step
% - 'sheep' agents have random movements as long as they are not 'hungry'
% - 'hungry' agents move on neighbouring cell with maximal 'grass' field
% - 'hungry' agents eat all 'grass' agents they met
% - 'hungry' agents go back to 'sheep' state when they eat enough 'grass'
% -----------------------------------------------------------------------------

world 32 32 #FFF

vegetal grass imgs/grass.png
eatenby hungry
var grass 6     % 'grass' field broadcasts up to distance 5
field grass -2
status grass<1 death      % 'grass' agent disapears when eated by a 'sheep'
var seed 3 -1               % 'grass' germination requires 3 time steps
birth seed=0 grass

animal sheep imgs/sheep.png
var grass 40 -1             % sheep starts with 40 initial 'grass' points
status grass<30 hungry    % sheep becomes hungry when 'grass' < 30

animal hungry imgs/hungry_sheep.png
eat grass
var grass 30 -1
sensor comfort grass 1        % hungry sheep tries to find grass
status grass=0 death      % sheep dies when 'grass' drops to 0
status grass>40 sheep     % back to 'sheep' state when 'grass' > 40

% initial configuration (4 blocks of grass, and 2 lines of sheep)
agent grass (0:4,0:4) (0:4,27:31) (27:31,0:4) (27:31,27:31)
agent sheep (8,14:18) (24,14:18)
% -----------------------------------------------------------------------------

END
```

### Output

![alt text](https://user-images.githubusercontent.com/27825602/33574327-f51d64ce-d938-11e7-97d6-84025be562dc.gif)

## Reproduction

### Configuration file

```
% -----------------------------------------------------------------------------
% Reprod : Reproduction of animals
%
% Description :
% - Reprod is based on 5 main type of agents : female sheep, male sheep
%   pregnant sheep, baby sheep, teenager sheep
% - male sheep + female sheep -> male sheep + pregnant sheep
% - male are attracted by females and repulsed by pregnant, female are 
%   attracted by males, pregnant are attracted by nothing
% - pregant sheep + time -> birth of 1 or 2 baby sheep
% - baby sheeps are attracted by female sheeps
% - baby sheep + time -> teen sheep
% - teen sheep repulsed by other sheeps
% - teen sheep + time -> male sheep or female sheep with 1/2 probability
% -----------------------------------------------------------------------------

world 16 16 #FFF

animal sheep_f #F00
males sheep_m
var age 30 -1
status age<0 death
var preg 
var pheromone_f 5
field pheromone_f -1
sensor sexappeal pheromone_m 1
status preg>0 pregnant_sheep

animal sheep_mere #F00
males sheep_m
var age 15 -1
status age<0 death
var preg 
var pheromone_f 5
field pheromone_f -1
sensor sexappeal pheromone_m 1
status preg>0 pregnant_sheep

animal sheep_m #00F
females sheep_f,sheep_mere
var pheromone_m 5
field pheromone_m -1
var age 30 -1
status age<0 death
sensor sexappeal pheromone_f 1
sensor alreadypreg big -1

animal pregnant_sheep #700
var time 6 -1
var big 5
field big -1
birth 0<time<2 babysheep choice(1,1,2)
status time<1 choice(sheep_mere,sheep_mere,sheep_mere,death,death)

animal babysheep #0F0
var time 7 -1
status time<1 teen
sensor mom pheromone_f 1

animal teen #070
var time 5 -1
status time<1 choice(sheep_m,sheep_f)
sensor trodarkf pheromone_f -1
sensor trodarkm pheromone_m -1

% -----------------------------------------------------------------------------

agent sheep_m (5,10) (10,10) (15,15)
agent sheep_f (10,5) (5,5) (1,1)

END
```

## Output

![alt text](https://user-images.githubusercontent.com/27825602/33574330-f7d707d8-d938-11e7-8e7c-16d3f506a8e4.gif)

