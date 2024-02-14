def debug():
    # prompt user
    prompt = input("\n> ") + " "
    command = prompt.split()
    params, command = command[1:], command[0]
    for val in params:
        try: val = int(val)
        except: None

    match command:

        case "build_room":
            if len(params) < 4:
                print("not enough params!")
                return
            cond = board.build_room(
                (params[0], params[1]), 
                (params[2], params[3]), 
                tile.cobble_floor, tile.cobble_wall
            )
            if cond: print("success!")
            else: print("failed to build room!")

        case "kill":
            if len(params) < 1:
                print("not enough params!")
                return
            for entity in board.entities.sprites():
                if entity.id == params[0]: entity.kill()
                else: # no suitable command
                    print("unrecognized command!")

'''
List of debug commands:
    - build_room <x> <y> <width> <height>
    - kill <entity_id>
'''
