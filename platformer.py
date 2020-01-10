"""
welcome aboard! this is my AGDQ2020 game jam
remember not to worry about

goal is to be making levels by wensday/thursday ?

vision:
 . similar architecture from SuperRedPants
 . better physics
 . bigger levels
    . collectables per level like stars in m64
        im thinking like 20 per level, with a
        'banana door' blocking levels
    . get them all in one run like banjo kazooie
 . power ups

to do list 
========== [~ started, / ongoing, x done]
------------------------ day 1 mostly drawing and thinking about architecture
[/] pixel art
[x] platforming  :)
  [x] left right
------------------------ day 2 lots of progress today
  [x] gravity
  [x] platform/hit detection
  [x] crouch
  [x] walljump
[x] platforms
   [] BONUS handle loading
[x] scrolling
[x] backgrounds
[x] mechanics  - good times had here
  [x] springs
  [x] spikes
      [x] BONUS fix spike hitbox
  [x] hats   WARNING - REALLY FUN
     [x] sombrero : hover
     [x] baseball cap : high jump
     [x] propeller beanie : fly
  [x] checkpoint flags
------------------------ day 3 enemies are looking good, editor too
  [x] enemies
     [x] skeleton
        [x] bones
     [x] zombie
     [x] snake
     [x] ghost
  [x] cheese (collectables)
[/] HUD 
[/] level editor !!!
  [x] finalize level architecture
  [~] loading levels into game
  [x] create items
     [x] platforms
     [x] spikes
     [x] springs
     [x] enemies
     [x] flags
     [x] hats
     [x] cheese
  [x] move items
  [x] delete items
  [x] saving and loading generated levels
------------------------ day 4 OFF TO THE RACES!
[/] bugfixing
   [x?] zombie wall glitch 
[x] hub world
[/] make levels
   [x] easy / tutorial level
   [x] l0
   [x] l1
   [x] l2
----------------------- day 5 
   [x] l3
   [x] l4
   [] final rush
[] cutscenes??
"""
import pygame
from pygame import Surface
from pygame.rect import Rect
from pygame.locals import *
from pygame.transform import flip, rotate

from copy import deepcopy
import sys

from data import *

pygame.init()

W, H = 960, 640
if __name__ == "__main__":
    SCREEN = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Red Pants Adventure")
    HEL32 = pygame.font.SysFont("Helvetica", 32)
    CLOCK = pygame.time.Clock()
    SCREEN.fill((255, 255, 255))
    SCREEN.blit(HEL32.render("Loading...", 0, (0, 0, 0)), (10, 10))
    pygame.display.update()
    

def load_spritesheet(filename, data, colorkey=None):
    """data should be dict with key: ((x, y), (w, h)), assumes w, h are 32, 32"""
    surf = pygame.image.load(filename).convert()
    sheet = {}
    for name in data:
        sprite = Surface(data[name][1])
        x, y = 0 - data[name][0][0], 0 - data[name][0][1]
        sprite.blit(surf, (x, y))
        sprite.set_colorkey(colorkey)
        sheet[name] = sprite
    return sheet

def isnear(pos, dim=False):
    return (abs(pos[0] - X) < W // 2 + 64 and abs(pos[1] - Y) < H // 2 + 64) or (dim and Rect(pos, (dim[0]*32, dim[1]*32)).colliderect(Rect((X - W//2, Y - H//2), (W+64, H+64))))
        
sprites = load_spritesheet("img/redpantsadventure_spritesheet.png", sheet_data, (1, 255, 1))
endcard = pygame.image.load("img/endcard.png").convert()
endcard.set_colorkey((1, 255, 1))

def get_HUD():
    surf = Surface((32*5, 32))
    surf.fill((200, 200, 200))
    surf.blit(HEL32.render("cheese: "+str(len(INV)), 0, (0, 0, 0)), (0, 0))
    return surf

def drawn_platform(dim, idx):
    surf = Surface((dim[0]*32, dim[1]*32))
    surf.fill((1, 255, 1))
    plat = "platform" + str(idx)
    for x in range(dim[0]):
        for y in range(dim[1]):
            num = ":"
            if x == 0: num += "0"
            elif x == dim[0]-1: num += "2"
            else: num += "1"
            if y == 0: num += "0"
            elif y == dim[1]-1: num += "2"
            else: num += "1"
            surf.blit(sprites[plat+num], (x*32, y*32))
    surf.set_colorkey((1, 255, 1))
    return surf

def scroll(pos): return pos[0]+SCROLLER[0], pos[1]+SCROLLER[1]
def adjust_scroller():
    SCROLLER[0] = 0 - X + (W/2) - 16
    SCROLLER[1] = 0 - Y + (H/2) - 32

def get_screen():
    global hub
    surf = pygame.Surface((W, H))
    for y in range(-1, (H//96)+1):
        for x in range(-1, (W//96)+1):
            surf.blit(sprites['background'+str(BACK)], (((x*96)+int(SCROLLER[0]/32)%96), ((y*96)+int(SCROLLER[1]/32)%96)))

    if DOOR and isnear(DOOR): surf.blit(sprites['door'+str(dframe//4)], scroll(DOOR))
    if hub:
        for i in range(len(LEVELS)):
            pygame.draw.rect(surf, (193, 145, 61 ), Rect(scroll((256+(i*256), -16)), (64, 64)))
            surf.blit(sprites['door'+str(dframe//4)], scroll((256+(i*256), 64)))
            surf.blit(HEL32.render(str(needs[i]), 0, (0, 0, 0)), scroll((256+(i*256)+16, -16)))
            surf.blit(HEL32.render(str(len(LEVELS[i]["cheese"])), 0, (100, 0, 0)), scroll((256+(i*256)+16, +16)))

    for pos, dim, idx in PLATFORMS:
        if isnear(pos, dim): surf.blit(drawn_platform(dim, idx), scroll(pos))
    for pos, hat in HATS:
        if isnear(pos): surf.blit(sprites["hat:"+hat+"0"], scroll(pos))
    for pos, d in SPIKES:
        if isnear(pos): surf.blit(rotate(sprites["spike"], d*90), scroll(pos))
    for pos in FLAGS:
        if isnear(pos): surf.blit(sprites["flag"+str(int(pos == SPAWN))], scroll(pos))
    for pos, d, spring, f in SPRINGS:
        if isnear(pos):
            if f: surf.blit(rotate(sprites["spring1"], d*90), scroll(pos))
            else: surf.blit(rotate(sprites["spring0"], d*90), scroll(pos))
    for pos, idx in CHEESE:
        if isnear(pos): surf.blit(sprites['cheese'+str(idx)], scroll(pos))
    for pos, name, d, f, c in ENEMIES:
        if isnear(pos): surf.blit(flip(sprites["enemy:"+name+str(f)], d, 0), scroll(pos))
    if DIR == 1:
        surf.blit(sprites["player:"+STATE], (X+SCROLLER[0]-7, Y+SCROLLER[1]))
        if HAT:
            if STATE == "crouch": surf.blit(sprites["hat:"+HAT+"1"], (X+SCROLLER[0]-7, Y+SCROLLER[1]+16))
            elif STATE == "squat": surf.blit(sprites["hat:"+HAT+"1"], (X+SCROLLER[0]-7, Y+SCROLLER[1]-8))
            else: surf.blit(sprites["hat:"+HAT+"1"], (X+SCROLLER[0]-7, Y+SCROLLER[1]-16))
    elif DIR == -1:
        surf.blit(flip(sprites["player:"+STATE], 1, 0), (X+SCROLLER[0]-9, Y+SCROLLER[1]))
        if HAT:
            if STATE == "crouch": surf.blit(flip(sprites["hat:"+HAT+"1"], 1, 0), (X+SCROLLER[0]-9, Y+SCROLLER[1]+16))
            elif STATE == "squat": surf.blit(flip(sprites["hat:"+HAT+"1"], 1, 0), (X+SCROLLER[0]-9, Y+SCROLLER[1]-8))
            else: surf.blit(flip(sprites["hat:"+HAT+"1"], 1, 0), (X+SCROLLER[0]-9, Y+SCROLLER[1]-16))
    return surf


def load_level(level):
    global PLATFORMS, HATS, SPIKES, SPRINGS, ENEMIES, _ENEMIES, FLAGS, CHEESE, BACK, SPAWN
    global  X, Y, x_vel, y_vel, DOOR, HAT
    PLATFORMS = level['plat']
    HATS = level['hats']
    SPIKES = level['spikes']
    SPRINGS = level['springs']
    ENEMIES = deepcopy(level['enemies'])
    _ENEMIES = deepcopy(ENEMIES)
    FLAGS = level['flags']
    CHEESE = level['cheese']
    BACK = level['back']
    SPAWN = level['door']
    DOOR = level['door']
    X, Y = SPAWN
    x_vel, y_vel = 0, 0
    HAT = None

# PLAYER CONTROL VARIABLES
SCROLLER = [0, 0]
SPAWN = 150, 450
X, Y = SPAWN
SPEED = 9
JUMP = -15
_JUMP = JUMP
x_vel = 0
y_vel = 0
friction = 1
grav = 1
STATE = "stand"
HAT = None
DIR = 1
CROUCH = 0
mov = 0
counter = 0
INV = []

ZOMBIESPEED = 6
BONESPEED = 14
SNAKESPEED = 10

PLATFORMS = []
HATS = []
SPIKES = []
SPRINGS = []
FLAGS = []
ENEMIES = []
CHEESE = []
BACK = 0
_ENEMIES = []
DOOR = (0, 0)
dframe = 0

with open("levels/hub") as f: hublvl = eval(f.read())
LEVELS = []
with open("levels/tutorial") as f: LEVELS.append(eval(f.read()))
n = 0
while True:
    try:
        with open("levels/l"+str(n)) as f:
            LEVELS.append(eval(f.read()))
    except IOError:
        break
    n += 1
with open("levels/fin") as f: LEVELS.append(eval(f.read()))
    
try:
    with open("levels/"+sys.argv[-1]) as f:
        load_level(eval(f.read()))
        hub = False
except IOError:
    load_level(hublvl)
    hub = True

while True and __name__ == "__main__":
    plats = []
    allplats = []
    for pos, dim, idx in PLATFORMS:
        allplats.append(Rect(pos, (dim[0]*32, dim[1]*32)))
        if isnear(pos, dim): plats.append(Rect(pos, (dim[0]*32, dim[1]*32)))
    # update counters/clock
    counter += 1
    dframe = (dframe + 1) % 12
    CLOCK.tick(30)
    # draw update screen
    adjust_scroller()
    SCREEN.blit(get_screen(), (0, 0))
    SCREEN.blit(get_HUD(), (0, 0))
    pygame.display.update()

    # evaluate input
    jmp = 0
    door = 0
    for e in pygame.event.get():
        if e.type == QUIT or e.type == KEYDOWN and e.key == K_ESCAPE: quit()
        if e.type == KEYDOWN:
            if e.key == K_LEFT: mov += -1
            if e.key == K_RIGHT: mov += 1
            if e.key == K_DOWN: CROUCH += 1
            if e.key == K_SPACE: jmp += 1
            if e.key == K_UP: door = True
        if e.type == KEYUP:
            if e.key == K_LEFT: mov -= -1
            if e.key == K_RIGHT: mov -= 1
            if e.key == K_DOWN: CROUCH -= 1

    # change state, update movement
    JUMP = _JUMP * 2 if HAT == "baseball" else _JUMP
    if STATE == "dmg":
        if counter < 10: continue
        STATE = "stand"
        X, Y = SPAWN
        x_vel, y_vel = 0, 0
        HAT = None
        ENEMIES = deepcopy(_ENEMIES)
    elif jmp and (STATE in ["stand", "run0", "run1", "slide", "wall"] or HAT == "propeller"):
        if HAT == "propeller": y_vel = JUMP
        if STATE == "wall":
            y_vel = JUMP
            DIR *= -1
            x_vel = max(SPEED * DIR, x_vel) if DIR > 0 else min(SPEED * DIR, x_vel)
        else:
            STATE = "squat"
            counter = 0
    elif STATE == "squat":
        if counter >= 3: y_vel = JUMP
    elif CROUCH: STATE = "crouch"
    elif mov and STATE not in ['crouch']:
        if DIR == mov: x_vel = max(SPEED * DIR, x_vel) if DIR > 0 else min(SPEED * DIR, x_vel)
        elif not x_vel or abs(x_vel) <= 3: DIR = mov
        if (x_vel > 0 and mov < 0) or (x_vel < 0 and mov > 0): STATE == "slide" 
    elif x_vel == 0: STATE = "stand"
    else: STATE = "slide"
        
    if mov and not STATE in ["run0", "run1", "crouch", "squat"]:
        if ((x_vel > 0 and mov < 0) or (x_vel < 0 and mov > 0)): STATE = "slide"
        else:
            STATE = "run0"
            counter = 0

    if STATE.startswith("run") and counter >= 5:
        STATE = "run" + str((int(STATE[-1]) + 1) % 2)
        counter = 0

    if y_vel < 0: STATE = "jump0"
    if y_vel > 0: STATE = "jump1"

    # friction and gravity
    if x_vel and not STATE.startswith("jump"): x_vel += friction if x_vel < 0 else -1
    y_vel += grav

    if STATE in ["jump1", "run0", "run1", "stand", "slide"] and HAT == "sombraro" and not CROUCH: y_vel = 0

    # animate relevent actors
    for spring in SPRINGS:
        if spring[3]: spring[3] -= 1

    # enemy logic
    remove = []
    for i in range(len(ENEMIES)):
        pos, name, d, f , c = ENEMIES[i]
        if not isnear(pos): continue
        c += 1
        if name == "bone":
            if c % 2:
                f = (f + 1) % 2
                pos = (pos[0] + BONESPEED, pos[1]) if d == 0 else (pos[0] - BONESPEED, pos[1])
            if c > 50: remove.append(i)
            
        if name == "skeleton":
            if abs(pos[0] - X) < 410:
                if f == 0: d = 0 if X > pos[0] else 1
                if c >= 8 and f == 0: f = 1
                elif c >= 30 and f == 1:
                    f = 2
                    ENEMIES.append( [pos, 'bone', d, 0, 0] )
                elif c > 40: f, c = 0, 0
            else: f, c = 0, 0

        if name == "zombie":
            if c % 4 == 0 and abs(pos[0] - X) < 512:
                hitbox = Rect((pos[0]+8, pos[1]), (32, 64))
                if d == 0: footbox = Rect((pos[0] + 32 + ZOMBIESPEED, pos[1] + 64), (10, 10)) 
                else: footbox = Rect((pos[0] - ZOMBIESPEED, pos[1]+64), (10, 10))
                
                if hitbox.collidelist(allplats) == -1:
                    d = 0 if X > pos[0] else 1
                f = (f + 1) % 2
                pos = (pos[0] + ZOMBIESPEED, pos[1]) if d == 0 else (pos[0] - ZOMBIESPEED, pos[1])
                if hitbox.collidelist(allplats) != -1 or footbox.collidelist(allplats) == -1:
                    pos = (pos[0] - ZOMBIESPEED*2, pos[1]) if d == 0 else (pos[0] + ZOMBIESPEED*2, pos[1])

        if name == "snake":
            hitbox = Rect(pos, (64, 16))
            if c % 4 == 0:
                f = (f + 1) % 2
                pos = (pos[0] + SNAKESPEED, pos[1]) if d == 0 else (pos[0] - SNAKESPEED, pos[1])
                if hitbox.collidelist(allplats) != -1:
                    d = (d + 1) % 2
                    pos = (pos[0] + SNAKESPEED*2, pos[1]) if d == 0 else (pos[0] - SNAKESPEED*2, pos[1])

        if name == "ghost":
            d = 0 if X > pos[0] else 1
            if (d == 1 and DIR == 1) or (d == 0 and DIR == -1): f = 1
            else: f = 0
            if abs(pos[0] - X) + abs(pos[1] - Y) < 800 and f == 0:
                if abs(pos[0] - X) > 30:
                    x = -1 if X < pos[0] else 1
                else: x = 0
                if abs(pos[1] - Y) > 30:
                    y = -1 if Y < pos[1] else 1
                else: y = 0
                pos = (pos[0]+x, pos[1]+y)
                
                    
        ENEMIES[i] = [pos, name, d, f, c]

    for i in remove[::-1]: ENEMIES.pop(i) 
    
    # hit detection - platforms
    hitbox = Rect((X, Y), (32, 64)) if STATE != "crouch" else Rect((X, Y+32), (32, 32))
    checklist = plats
    if hitbox.collidelist(checklist) != -1:
        STATE = "dmg"
        continue
    if x_vel:
        while hitbox.move(x_vel, 0).collidelist(checklist) != -1:
            if STATE.startswith("jump"): STATE = "wall"
            x_vel += 1 if x_vel < 0 else -1
    if y_vel:
        while hitbox.move(0, y_vel).collidelist(checklist) != -1: y_vel += 1 if y_vel < 0 else -1
    if x_vel and y_vel:
        while hitbox.move(x_vel, y_vel).collidelist(checklist) != -1:
            y_vel += 1 if y_vel < 0 else -1
            x_vel += 1 if x_vel < 0 else -1
    #                 hats
    checklist = [Rect(pos, (46, 46)) for pos, hat in HATS]
    i = hitbox.collidelist(checklist)
    if i != -1: HAT = HATS[i][1]
    #                 flags
    checklist = [Rect(pos, (46, 64)) for pos in FLAGS]
    i = hitbox.collidelist(checklist)
    if i != -1: SPAWN = FLAGS[i]
    #                 spikes and enemies
    checklist = []
    for pos, d in SPIKES:
        if not isnear(pos): continue
        if d == 0: checklist += [Rect((pos[0]+8, pos[1]), (16, 16)), Rect((pos[0], pos[1]+16), (32, 16))]
        elif d == 1: checklist += [Rect((pos[0], pos[1]+8), (16, 16)), Rect((pos[0]+16, pos[1]), (16, 32))]
        elif d == 2: checklist += [Rect((pos[0], pos[1]), (32, 16)), Rect((pos[0]+8, pos[1]+16), (16, 16))]
        elif d == 3: checklist += [Rect((pos[0], pos[1]), (16, 32)), Rect((pos[0]+16, pos[1]+8), (32, 16))]

    for pos, name, d, f, c in ENEMIES:
        if not isnear(pos): continue
        if name in ["bone", "ghost"]: checklist.append(Rect(pos, (32, 32)))
        elif name == "snake": checklist.append(Rect(pos, (64, 16)))
        else: checklist.append(Rect(pos, (32, 64)))
    i = hitbox.collidelist(checklist)
    if i != -1:
        STATE = "dmg"
        counter = 0
    #                 springs
    checklist = [Rect(pos, (48, 48)) for pos, d, s, f in SPRINGS]
    i = hitbox.collidelist(checklist)
    if i != -1:
        SPRINGS[i][3] = 10
        if SPRINGS[i][1] == 0: y_vel = 0 - SPRINGS[i][2]
        elif SPRINGS[i][1] == 2: y_vel = SPRINGS[i][2]
        elif SPRINGS[i][1] == 3:
            DIR = 1
            x_vel = SPRINGS[i][2]
        elif SPRINGS[i][1] == 1:
            DIR = -1
            x_vel = -1 * SPRINGS[i][2]
    #                 cheese
    checklist = []
    for pos, idx in CHEESE:
        if idx == 3: checklist.append(Rect(pos, (64, 64)))
        else: checklist.append(Rect(pos, (32, 32)))
    i = hitbox.collidelist(checklist)
    if i != -1:
        if not CHEESE[i][1] == 3: INV.append(CHEESE.pop(i))
        else:
            n = H
            end = True
            while end:
                CLOCK.tick(30)
                if n >= 0: n -= 10
                SCREEN.blit(get_screen(), (0, 0))
                SCREEN.blit(endcard, (0, n))
                pygame.display.update()
                for e in pygame.event.get():
                    if e.type == QUIT or e.type == KEYDOWN and e.key == K_ESCAPE: quit()
                    if e.type == KEYDOWN:
                        if e.key == K_LEFT: mov += -1
                        if e.key == K_RIGHT: mov += 1
                        if e.key == K_DOWN: CROUCH += 1
                        if e.key == K_SPACE and n <= 0:
                            end = False
                            load_level(hublvl)
                            hub=True
                    if e.type == KEYUP:
                        if e.key == K_LEFT: mov -= -1
                        if e.key == K_RIGHT: mov -= 1
                        if e.key == K_DOWN: CROUCH -= 1
    #                 door
    if hub:
        doorlist = [Rect((256+(i*256), 64), (64, 64)) for i in range(len(LEVELS))]
        di = hitbox.collidelist(doorlist)
    # enter door
    if door and (hitbox.colliderect(Rect(DOOR, (64, 64))) or (hub and di != -1 and len(INV)>=needs[di] )):
        n = 2
        if not hub: X, Y = DOOR[0] + 16, DOOR[1]
        adjust_scroller()
        STATE = "jump1"
        while n < 980:
            surf = rotate(get_screen(), n)
            SCREEN.blit(surf, ((W-surf.get_width())//2, (H - surf.get_height())//2))
            n += n // 2
            CLOCK.tick(30)
            pygame.display.update()
            for e in pygame.event.get():
                if e.type == QUIT or e.type == KEYDOWN and e.key == K_ESCAPE: quit()
                if e.type == KEYDOWN:
                    if e.key == K_LEFT: mov += -1
                    if e.key == K_RIGHT: mov += 1
                    if e.key == K_DOWN: CROUCH += 1
                if e.type == KEYUP:
                    if e.key == K_LEFT: mov -= -1
                    if e.key == K_RIGHT: mov -= 1
                    if e.key == K_DOWN: CROUCH -= 1
    
        if hub and di != -1:
            load_level(LEVELS[di])
            hub = False
        else:
            load_level(hublvl)
            hub = True
    # apply final calculated movement
    X += x_vel
    Y += y_vel
                
