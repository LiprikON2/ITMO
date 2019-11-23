# Game of life (1970)
The Game of Life (sometimes known simply as Life) is an example of a cellular automaton and a zero-player game. It takes place on an infinite two-dimensional grid in which cells can be ‘on’ (alive) or ‘off’ (dead), and is defined by a set of rules that jointly determine the state of a cell given the state of its neighbours. Following specification of an initial configuration, patterns evolve over time across the grid requiring no further user input (thus ‘zero-player’). First popularized in 1970 in the Scientific American (Gardner, 1970), the Game of Life has attracted lasting appeal among both scientific and amateur communities. One reason for its appeal is that it is very simple to program, yet at the same time it appears to exemplify emergent and self-organized behaviour. Even though its (simple) rules are specified at the level of individual cells, one sees entities at coarse-grained ‘higher’ levels of description, whose behaviors are better described by rules at these higher levels.


## GUI Version use

```
life-gui.py [-h] [--width] [--height] [--cell_size] [--max-generations] [--speed]

optional arguments:
  -h, --help            show this help message and exit
  --width              Width of a window in px. Default: 500
  --height             Height of a window in px. Default: 500
  --cell_size          Size of a single cell in px. Default: 20
  --max-generations    Maximum amount of generation. Default: 500
  --speed SPEED        Speed in pygame ticks. Default: 1
```

## CLI Version use


```
life-console.py [-h] [--rows ] [--cols] [--max-generations]

optional arguments:
  -h, --help           show this help message and exit
  --rows               Amount of rows. Default: 20
  --cols               Amount of columns. Default: 20
  --max-generations    Maximum amount of generation. Default: 20
```

## Setup

1. `pip install requirements.txt`


### Unittests
```
python -m unittest discover
```