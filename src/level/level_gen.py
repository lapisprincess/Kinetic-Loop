import util.bsp as bsp
from util.pathfind import pathfind

# generate a full dungeon floor
def generate_floor(level, complexity, floor, wall):

    # run bsp and build rooms in the partitions,
    # connections keeps track of groups of connected rooms
    groups = []
    for partition in bsp.bsp(level, complexity):
        room = partition.build_room(floor, wall, 16, 5, 10)
        groups.append([room])

    limit = 5
    tries = 0
    while (len(groups) > 1):
        if _merge_groups(level, groups) == False: tries += 1
        if limit >= limit: break

    # reached limit, so we gotta keep biggest group and toss the rest
    if (len(groups) > 1):
        biggest = groups[0]
        for group in groups:
            if len(group) > len(biggest): biggest = group
        groups = [biggest]
    


def _merge_groups(level, groups):
    success = False

    # 
    for group1 in groups:
        for group2 in groups:
            if group1 in groups and len(group1) == 0: 
                groups.remove(group1)
            if group2 in groups and len(group2) == 0: 
                groups.remove(group2)
            if group1 == group2: continue
            # four levels of recursion means fun stuff 🤠
            for room1 in group1:
                for room2 in group2:
                    if level.are_connected(room1, room2): continue
                    if level.connect_rooms(room1, room2):
                        success = True
                        group1.append(room2)
                        group2.remove(room2)

    for group in groups:
        if len(group) == 0: groups.remove(group)

    return success

def _verify_connectivity(level, groups):
    for group1 in groups:
        for room1 in group1:
            center1 = room1.center_tile_coord
            for group2 in groups:
                for room2 in group2:
                    center2 = room2.center_tile_coord
                    if (room1 == room2): continue
                    path = pathfind(center1, center2, level)
                    if path == None or len(path) == 0: 
                        return False
    return True
