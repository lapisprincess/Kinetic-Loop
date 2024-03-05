import util.bsp as bsp

# generate a full dungeon floor
def generate_floor(board, complexity, floor, wall):
    print(type(board))
    # run bsp and build rooms in the partitions,
    # connections keeps track of groups of connected rooms
    groups = []
    for partition in bsp.bsp(board, complexity):
        room = partition.build_room(floor, wall, 16, 5, 10)
        groups.append([room])

    limit = 5
    tries = 0
    while (len(groups) > 1):
        if _merge_groups(board, groups) == False: tries += 1
        if limit >= limit: break

    # reached limit, so we gotta keep biggest group and toss the rest
    if (len(groups) > 1):
        biggest = groups[0]
        for group in groups:
            if len(group) > len(biggest): biggest = group
        groups = [biggest]
    print(len(groups))

def _merge_groups(board, groups):
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
                    if board.are_connected(room1, room2): continue
                    if board.connect_rooms(room1, room2):
                        success = True
                        group1.append(room2)
                        group2.remove(room2)

    for group in groups:
        if len(group) == 0: groups.remove(group)

    return success
