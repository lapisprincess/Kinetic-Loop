def debug(board, log):
    command = log.type_txt[4:].split()
    params, command = command[1:], command[0]
    for val in params:
        try: val = int(val)
        except: None
    match command:

        case "build_room":
            if len(params) < 4:
                log.add_message("usage: build_room <xcoord> <ycoord> <width> <height>")
                return
            cond = board.build_room(
                (params[0], params[1]), 
                (params[2], params[3]), 
                tile.cobble_floor, tile.cobble_wall
            )
            if cond: log.add_message("success!")
            else: log.add_message("failed to build room!")

        case "kill":
            if len(params) < 1:
                log.add_message("usage: kill <entity>")
                return
            for entity in board.entities.sprites():
                if entity.info["Name"].lower() == params[0].lower(): 
                    entity.kill()
                    log.add_message("hit successful!")
                    return
            log.add_message("not a recognized enemy")

        case _:
            log.add_message("unrecognized command!")

'''
List of debug commands:
    - build_room <x> <y> <width> <height>
    - kill <entity id>
    - birth <entity type>
'''
