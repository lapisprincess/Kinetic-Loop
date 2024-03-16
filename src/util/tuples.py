""" simple tuple operation methods """

def multiply_tuples(tup1, tup2):
    """ """
    if len(tup1) != len(tup2):
        return None
    out = ()
    for i in range(len(tup1)):
        out += (tup1[i] * tup2[i],)
    return out

def divide_tuples(tup1, tup2):
    """ """
    if len(tup1) != len(tup2):
        return None
    out = ()
    for i in range(len(tup1)):
        out += (round(tup1[i] / tup2[i]),)
    return out
