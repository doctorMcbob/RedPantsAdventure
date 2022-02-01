from levels import tutorial, l0, l1, l2, l3, l4, fin, hub

levels = {
    "hub": hub.level,
    "tutorial": tutorial.level,
    "l0": l0.level,
    "l1": l1.level,
    "l2": l2.level,
    "l3": l3.level,
    "l4": l4.level,
    "fin": fin.level,
}

def get_level(name):
    return levels[name]
