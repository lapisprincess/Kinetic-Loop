all_directions = ['north', 'south', 'west', 'east']
all_directions += ['north-west', 'north-east', 'south-west', 'south-east']
def necessary_movement(direction):
    match direction:
        case 'north': x, y = 0, -1
        case 'south': x, y = 0, 1
        case 'west': x, y = -1, 0
        case 'east': x, y = 1, 0
        case 'north-west': x, y = -1, -1
        case 'north-east': x, y = 1, -1
        case 'south-west': x, y = -1, 1
        case 'south-east': x, y = 1, 1
    return (x, y)


