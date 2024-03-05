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
        case _: return None
    return (x, y)

# direction from coord1 to coord2
def match_direction(coord1: tuple[int, int], coord2: tuple[int, int]) -> str:
    # scan for cadinal directions
    vert = ''
    if   (coord1[1] > coord2[1]): vert = 'north'
    elif (coord1[1] < coord2[1]): vert = 'south'
    horz = ''
    if   (coord1[0] > coord2[0]): horz = 'west'
    elif (coord1[0] < coord2[0]): horz = 'east'

    # construct output string
    if (horz == '') and (vert == ''): return ''
    elif (horz == ''): return vert
    elif (vert == ''): return horz
    return (vert + '-' + horz)

def get_random_neighbor(tile_coord, board, poss_directions = all_directions):
    if poss_directions == []: return None

    tentative_dir = random.randint(0, len(poss_directions) - 1)
    mov = necessary_movement(tentative_dir)
    tile = board.get_tile(tile_coord[0] + mov[0], tile_coord[1] + mov[1])
    
    if tile == None:
        poss_directions.remove(tentative_dir)
        return get_random_neighbor(tile_coord, board, poss_directions)

    return tile

def get_all_neighbors(tile_coord):
    neighbors = []
    for direction in all_directions:
        mod = necessary_movement(direction)
        neighbors.append((
            tile_coord[0] + mod[0], 
            tile_coord[1] + mod[1]
        ))

    return neighbors
