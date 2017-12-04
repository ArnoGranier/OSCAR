# BSTAR
[2017][Python 3+] Behavioural Simulation Tool by Attraction - Repulsion

Project proposed by Christophe Schlick, see [his site](http://www.labri.fr/perso/schlick/prog2/prog2.pro2017.html) (in french).

The goal of this project is to allow anybody to make a simple multi-agent simulation based on the concept of attraction-repulsion. 
Interactions between the user and the code, ie defining all the agents and their interactions, is done by txt configuration files. Format of this file will be describe later, but is intended to be as easy and "noob-friendly" as possible.

# WORK IN PROGRESS, WILL WRITE SOME DOC LATER !

# Examples

## Forestfire
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
## Wireworld

## Lifegame

## Phototropism

## Segregation

## Sugarscape

## Reproduction
