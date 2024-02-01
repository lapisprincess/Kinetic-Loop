controls_path = "controls.txt"
needed_controls = [
    'north', 'south', 'east', 'west',
    'north-east', 'north-west',
    'south-east', 'south-west',
    'menu_main', 'menu_inventory', 'menu_player'
]
def define_controls(data_path):
    return define(data_path, controls_path, needed_controls, True)

settings_path = "settings.txt"
needed_settings = ['screen_width', 'screen_height']
def define_settings(data_path):
    return define(data_path, settings_path, needed_settings)

def define(data_path, file_path, options, lists = False):
    file = open(data_path + file_path, 'r')
    out = {}
    for line in file:
        line = line.split()
        if (('#' in line) or (len(line) == 0)
            or (line[0] not in options)): continue # comment line
        command = line[0]
        if lists:
            mapped_keys = [line[line.index('=')+1]]
            while '&' in line: # parse multiple values
                line = line[line.index('&')+1:]
                if '&' in line: mapped_keys.append(line[line.index('&')-1])
                else: mapped_keys.append(line[0])
        else: mapped_keys = line[line.index('=')+1]
        out[command] = mapped_keys
    file.close()
    return out
