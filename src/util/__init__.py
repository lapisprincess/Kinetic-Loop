# general definition method.
# lists decides whether settings can have multiple associated values
def define(data_path, file_path: str, lists = False):
    file = open(data_path + file_path, 'r')
    out = {}
    for line in file:
        line = line.split()

        # disregard comment lines
        if ('#' in line) or ('=' not in line) or (len(line) == 0): continue

        key = line[0]
        # multiple values
        if lists == True:
            value = [line[line.index('=')+1]]
            while '&' in line: # parse multiple values
                line = line[line.index('&')+1:]
                if '&' in line: value.append(line[line.index('&')-1])
                else: value.append(line[0])
        # single value
        else: value = line[line.index('=')+1]

        out[key] = value

    file.close()
    return out


### CONTROLS ###
controls_path = "controls.txt"
def define_controls(data_path):
    return define(data_path, controls_path, True)


### SETTINGS ###
settings_path = "settings.txt"
needed_settings = ['screen_width', 'screen_height']
def define_settings(data_path):
    return define(data_path, settings_path)
