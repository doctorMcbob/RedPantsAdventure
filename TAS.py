"""
TAS.py
TAS: Tool Assisted Speedrun

a TAS-er for RedPantsAdventure
"""
import sys
import pygame
from pygame.rect import Rect
from pygame.locals import *

import pickle
from copy import deepcopy

pygame.init()
W, H = 960, 640
SCREEN = pygame.display.set_mode((W, H))
pygame.display.set_caption("~~ Level Editor ~~")
HEL16 = pygame.font.SysFont("Helvetica", 16)
HEL32 = pygame.font.SysFont("Helvetica", 32)
HEL64 = pygame.font.SysFont("Helvetica", 64)

import platformer as p
#this is gross
p.CLOCK = pygame.time.Clock()
p.SCREEN = SCREEN
p.HEL32 = HEL32
p.HEL64 = HEL64

STATES = []

BTNS = {
    "LEFT": False,
    "RIGHT": False,
    "UP": False,
    "DOWN": False,
    "SPACE": False,
}
keymap = {
    K_LEFT:"LEFT",
    K_RIGHT:"RIGHT",
    K_UP:"UP",
    K_DOWN:"DOWN",
    K_SPACE:"SPACE",
}

def get_state():
    return (p.PLATFORMS, p.HATS, p.SPIKES, p.SPRINGS, deepcopy(p.ENEMIES), p._ENEMIES, p.FLAGS, p.CHEESE, p.BACK, p.SPAWN,
            p.X, p.Y, p.x_vel, p.y_vel, p.DOOR, p.HAT, p.STATE, p.CROUCH, p.mov, p.hub, p.DIR,
            p.counter, p.dframe, p.IGT, p.endcard)

def set_state(state):
    p.PLATFORMS, p.HATS, p.SPIKES, p.SPRINGS, p.ENEMIES, p._ENEMIES, p.FLAGS, p.CHEESE, p.BACK, p.SPAWN, p.X, p.Y, p.x_vel, p.y_vel, p.DOOR, p.HAT, p.STATE, p.CROUCH, p.mov, p.hub, p.DIR, p.counter, p.dframe, p.IGT, p.endcard = state

class Event():
    def __init__(self, type, key):
        self.type = type
        self.key = key

def bouncer(thing):
    def bounce(): return thing
    return bounce

def read_tas(TAS):
    global STATES
    for i in range(len(TAS)):
        p.advance_frame(bouncer(TAS[i]))
        STATES.append(get_state())

if len(sys.argv) > 1:
    with open(sys.argv[-1], "rb") as f:
        TAS = pickle.load(f)
    read_tas(TAS)
else:
    TAS = []

def flush(n=500):
    global TAS, STATES
    STATES = STATES[:0-n]
    set_state(STATES[-1])
    read_tas(TAS[0-n:])

def get_tas_menu():
    surf = pygame.Surface((W, 16))
    surf.fill((100, 100, 100))
    for i, key in enumerate(["LEFT", "RIGHT", "UP", "DOWN", "SPACE"]):
        if BTNS[key] == KEYDOWN: pygame.draw.rect(surf, (200, 0, 0), Rect((126*i, 0), (126, 16)))
        elif BTNS[key] == KEYUP: pygame.draw.rect(surf, (0, 0, 200), Rect((126*i, 0), (126, 16)))
        surf.blit(HEL16.render(key, 0, (0, 0, 0)), (126*i, 0))
    surf.blit(HEL16.render(str(len(TAS)), 0, (0, 0, 0)), (W-126, 0))
    return surf

EVENTS = []
while __name__ == "__main__":
    for e in pygame.event.get():
        if e.type == QUIT: quit()
        if e.type == KEYDOWN and e.key == K_ESCAPE:
            pygame.quit()
            filename = input("filename\n> ")
            with open(filename, "wb") as f:
                pickle.dump(TAS, f)
            quit()
        if e.type == KEYDOWN:
            if e.key == K_RETURN:
                p.advance_frame(bouncer(EVENTS))
                STATES.append(get_state())
                TAS.append(EVENTS)
                EVENTS = []
            if e.key == K_BACKSPACE:
                set_state(STATES.pop())
                EVENTS = TAS.pop()
                p.adjust_scroller()
                SCREEN.blit(p.get_screen(), (0, 0))
                SCREEN.blit(p.get_HUD(), (0, 0))
            if e.key == K_PERIOD: flush()
            if e.key == K_COMMA: flush(100)
            if e.key in keymap:
                idx = -1
                for i, evnt in enumerate(EVENTS):
                    if evnt.key == e.key:
                        idx = i
                        break
                if idx == -1: EVENTS.append(Event(KEYDOWN, e.key))
                else:
                    if EVENTS[idx].type == KEYDOWN: EVENTS[idx].type = KEYUP
                    else: EVENTS.pop(idx)

    BTNS = {
        "LEFT": False,
        "RIGHT": False,
        "UP": False,
        "DOWN": False,
        "SPACE": False,
    }
    for evnt in EVENTS:
        BTNS[keymap[evnt.key]] = evnt.type
    SCREEN.blit(get_tas_menu(), (0, H-16))
    pygame.display.update()
    
