'''
directions is a module for dealing with cardinal direction stuff,
translating from coordinates to direction, and direction to coordinates
'''

all_directions = ['north', 'south', 'west', 'east']
all_directions += ['north-west', 'north-east', 'south-west', 'south-east']

# movement modifiers corresponding to given direction
def necessary_movement(direction: str) -> tuple[int, int]:
    match (direction):
        case 'north':      x, y =  0, -1
        case 'south':      x, y =  0,  1
        case 'west':       x, y = -1,  0
        case 'east':       x, y =  1,  0
        case 'north-west': x, y = -1, -1
        case 'north-east': x, y =  1, -1
        case 'south-west': x, y = -1,  1
        case 'south-east': x, y =  1,  1
    return (x, y)

# direction from coord1 to coord2
def match_direction(coord1: tuple[int, int], coord2: tuple[int, int]) -> str:
    # scan for cadinal directions
    vert = ''
    if   (coord1[1] > coord2[1]): vert = 'south'
    elif (coord1[1] < coord2[1]): vert = 'north'
    horz = ''
    if   (coord1[0] > coord2[0]): horz = 'west'
    elif (coord1[0] < coord2[0]): horz = 'east'

    # construct output string
    if (horz == '') and (vert == ''): return ''
    elif (horz == ''): return vert
    elif (vert == ''): return horz
    return (vert + '-' + horz)
