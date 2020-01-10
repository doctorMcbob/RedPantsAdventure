"""
level editor

starting fresh
"""
import pygame
from pygame import Surface
from pygame.locals import *

import sys

from data import *

pygame.init()
W, H = 960, 640
SCREEN = pygame.display.set_mode((W, H))
pygame.display.set_caption("~~ Level Editor ~~")
HEL32 = pygame.font.SysFont("Helvetica", 32)
HEL16 = pygame.font.SysFont("Helvetica", 16)

from platformer import *
import platformer as p
from data import *
p.hub = False
_X, _Y = None, None

LEVEL = {
    "door": (0, 0),
    "plat": [],
    "hats": [],
    "spikes": [],
    "springs": [],
    "flags": [],
    "enemies": [],
    "cheese": [],
    "back": 0,
}
load_level(LEVEL)

def save(filename):
    with open("levels/"+filename, "w+") as f:
        f.write(repr(LEVEL))

def load(filename):
    global LEVEL
    try:
        with open("levels/"+filename, "r") as f:
            LEVEL=eval(f.read())
    except IOError:
        print("file load error")

"""
door:    (x, y)
plat:    [(x, y), (w, h), i]
hats:    [(x, y), name]
spikes:  [(x, y), d]
spring:  [(x, y), d, strength, 0]
flags:   (x, y)
enemies: [(x, y), name, d, 0, 0]
cheese:  [(x, y), i]
back:    i
"""

def make_plat():
    global _X, _Y
    if _X is not None and _Y is not None:
        LEVEL['plat'].append([(min(p.X, _X), min(p.Y, _Y)), ((abs(p.X - _X)//32)+1, (abs(p.Y - _Y)//32)+1), 0])
        _X, _Y = None, None
    else: _X, _Y = p.X, p.Y

def make_hat(): LEVEL['hats'].append([(p.X, p.Y), 'baseball'])
def make_spike(): LEVEL['spikes'].append([(p.X, p.Y), 0])
def make_spring(): LEVEL['springs'].append([(p.X, p.Y+16), 0, 20, 0])
def make_flag(): LEVEL['flags'].append((p.X, p.Y))
def make_enemy():
    LEVEL['enemies'].append([(p.X, p.Y), "zombie", 0, 0, 0])
def make_cheese(): LEVEL['cheese'].append([(p.X, p.Y), 0])

keymap = {
    K_p: make_plat,
    K_h: make_hat,
    K_s: make_spike,
    K_w: make_spring,
    K_f: make_flag,
    K_e: make_enemy,
    K_c: make_cheese,
}

def get_submenu(item, what, idx):
    data = submenu_data[what] + ["MOVE", "DELETE"]
    surf = Surface((64*5, 64*5))
    surf.fill((200, 200, 200))
    pygame.draw.rect(surf, (100, 255, 100), Rect((0, 16+(idx*32)), (64*5, 16)))
    for i in range(len(item)):
        surf.blit(HEL16.render(data[i] + " | " + str(item[i]), 0, (0, 0, 0)), (16, 16+(i*32)))
    surf.blit(HEL16.render("MOVE", 0, (0, 0, 0)), (16, 16+len(item)*32))
    surf.blit(HEL16.render("DELETE", 0, (0, 0, 0)), (16, 16+(len(item)+1)*32))
    return surf

def get_text(pos):
    text = ""
    surf = Surface((64 * 5, 32))
    while True:
        for e in pygame.event.get():
            if e.type == QUIT or e.type == KEYDOWN and e.key == K_ESCAPE: quit()
            if e.type == KEYDOWN:
                if e.key in alphabet_keys: text += alphabet_keys[e.key]
                if e.key == K_BACKSPACE: text = text[:-1]
                if e.key == K_RETURN: return text
        surf.fill((255, 255, 255))
        surf.blit(HEL16.render(text, 0, (0, 0, 0)), (0, 0))
        SCREEN.blit(surf, pos)
        pygame.display.update()

try:
    load(sys.argv[-1])
except IOError:
    pass


while True and __name__ == "__main__":
    adjust_scroller()
    SCREEN.blit(get_screen(), (0, 0))
    if _X and _Y: SCREEN.blit(HEL32.render("C", 0, (0, 0, 0)), scroll((_X, _Y)))
    pygame.display.update()

    sub = None
    item = None
    what = None
    for e in pygame.event.get():
        if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE): quit()
        if e.type == KEYDOWN:
            if e.key == K_LEFT: p.X -= 32
            if e.key == K_RIGHT: p.X += 32
            if e.key == K_UP: p.Y -= 32
            if e.key == K_DOWN: p.Y += 32

            if e.key in keymap: keymap[e.key]()
            if e.key == K_SPACE: sub = (p.X, p.Y)
            if e.key == K_BACKSPACE: save(get_text((0, 0)))

    if sub:
        for key in LEVEL:
            if key in ['door', 'back']: continue
            if item is not None and what is not None: break
            for thing in LEVEL[key]:
                if key == 'door': continue
                if key == 'plat': rect = Rect(thing[0], (thing[1][0]*32, thing[1][1]*32))
                elif key == 'spring': rect = Rect(thing[0], (48, 48))
                elif key == 'flags': rect = Rect(thing, (32, 64))
                else: rect = Rect(thing[0], (32, 32))
                if rect.colliderect(Rect((p.X, p.Y), (32, 32))):
                    item = thing
                    what = key
                    break
    i = 0
    while item:
        SCREEN.blit(get_submenu(item, what, i), (100, 100))
        pygame.display.update()

        mov = False
        for e in pygame.event.get():
            if e.type == QUIT or e.type == KEYDOWN and e.key == K_ESCAPE: quit()
            if e.type == KEYDOWN:
                if e.key == K_UP: i = ((i - 1) % (len(item)+2))
                if e.key == K_DOWN: i = ((i + 1) % (len(item)+2))
                if i < len(item) and e.key == K_LEFT and type(item[i]) == int: item[i] -= 1
                if i < len(item) and e.key == K_RIGHT and type(item[i]) == int: item[i] += 1
                if e.key == K_SPACE:
                    if i < len(item):
                        if type(item[i]) in [str, int]:
                            item[i] = get_text((100, 500))
                            try: item[i] = int(item[i])
                            except ValueError: continue
                    if i == len(item): mov = True
                    if i == len(item) + 1:
                        LEVEL[what].remove(item)
                        item = False
                if e.key == K_RETURN: item = False
                
                
        while mov:
            adjust_scroller()
            SCREEN.blit(get_screen(), (0, 0))
            if _X and _Y: SCREEN.blit(HEL32.render("C", 0, (0, 0, 0)), scroll((_X, _Y)))
            pygame.display.update()
            for e in pygame.event.get():
                if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE): quit()
                if e.type == KEYDOWN:
                    if e.key == K_LEFT: p.X -= 32
                    if e.key == K_RIGHT: p.X += 32
                    if e.key == K_UP: p.Y -= 32
                    if e.key == K_DOWN: p.Y += 32
                    if e.key == K_SPACE: mov = False
                if type(item) == tuple: item = (p.X, p.Y)
                else:
                    item[0] = (p.X, p.Y)
                    if what == "springs":
                        if item[1] == 0: item[0] = (p.X, p.Y+16)
                        if item[1] == 1: item[0] = (p.X-16, p.Y)

            
    x, y = p.X, p.Y
    load_level(LEVEL)
    p.X, p.Y = x, y
