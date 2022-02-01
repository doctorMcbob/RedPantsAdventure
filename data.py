from pygame.locals import *

sheet_data = {
    "player:stand": ((0, 0), (48, 64)),
    "player:run0": ((48, 0), (48, 64)),
    "player:run1": ((96, 0), (48, 64)),
    "player:squat": ((144, 0), (48, 64)),
    "player:jump0": ((192, 0), (48, 64)),
    "player:jump1": ((240, 0), (48, 64)),
    "player:dmg": ((288, 0), (48, 64)),
    "player:wall": ((336, 0), (48, 64)),
    "player:slide": ((384, 0), (48, 64)),
    "player:crouch": ((432, 0), (48, 64)),
    "hat:sombraro0": ((416, 96), (48, 48)),
    "hat:sombraro1": ((416, 144), (48, 48)),
    "hat:baseball0": ((384, 192), (48, 48)),
    "hat:baseball1": ((432, 192), (48, 48)),
    "hat:propeller0": ((288, 192), (48, 48)),
    "hat:propeller1": ((336, 192), (48, 48)),
    "enemy:skeleton0": ((0, 448), (48, 64)),
    "enemy:skeleton1": ((48, 448), (48, 64)),
    "enemy:skeleton2": ((96, 448), (48, 64)),
    "enemy:bone0": ((144, 448), (32, 32)),
    "enemy:bone1": ((144, 480), (32, 32)),
    "enemy:zombie0": ((176, 448), (48, 64)),
    "enemy:zombie1": ((224, 448), (48, 64)),
    "enemy:snake0": ((272, 448), (64, 16)),
    "enemy:snake1": ((272, 464), (64, 16)),
    "enemy:ghost0": ((272, 480), (32, 32)),
    "enemy:ghost1": ((304, 480), (32, 32)),
    "cheese0": ((288, 64), (32, 32)),
    "cheese1": ((288, 96), (32, 32)),
    "cheese2": ((288, 128), (32, 32)),
    "cheese3": ((336, 448), (64, 64)),
    "spring0": ((320, 64), (48, 48)),
    "spring1": ((368, 64), (48, 48)),
    "spike": ((416, 64), (32, 32)),
    "flag0": ((320, 112), (46, 64)),
    "flag1": ((368, 112), (46, 64)),
    "door0": ((288, 240), (64, 64)),
    "door1": ((352, 240), (64, 64)),
    "door2": ((416, 240), (64, 64)),
    "lock": ((416, 448), (32, 32)),
}

for n in range(5): sheet_data["background" + str(n)] = ((n*96, 352), (96, 96))

for n in range(9):
    name = 'platform'+str(n)
    x_ = (n % 3) * 96
    y_ = ((n // 3) * 96) + 64
    for y in range(3):
        for x in range(3):
            sheet_data[name+":"+str(x)+str(y)] = ((x_+(x*32), y_+(y*32)), (32, 32))

submenu_data = {
    "plat": ['pos', 'dim', "idx"],
    "hats": ['pos', 'name'],
    'spikes': ['pos', 'direction'],
    'springs': ['pos', 'direction', 'strength', 'frame [do not touch]'],
    'flags': ['pos'],
    'enemies': ['pos', 'name', 'direction', 'frame [do not touch]', 'counter [do not touch]'],
    'cheese': ['pos', 'idx']
}

alphabet_keys = {
    K_a: "a",
    K_b: "b",
    K_c: "c",
    K_d: "d",
    K_e: "e",
    K_f: "f",
    K_g: "g",
    K_h: "h",
    K_i: "i",
    K_j: "j",
    K_k: "k",
    K_l: "l",
    K_m: "m",
    K_n: "n",
    K_o: "o",
    K_p: "p",
    K_q: "q",
    K_r: "r",
    K_s: "s",
    K_t: "t",
    K_u: "u",
    K_v: "v",
    K_w: "w",
    K_x: "x",
    K_y: "y",
    K_z: "z",
    K_SPACE: " ",
    K_0: "0",
    K_1: "1",
    K_2: "2",
    K_3: "3",
    K_4: "4",
    K_5: "5",
    K_6: "6",
    K_7: "7",
    K_8: "8",
    K_9: "9",
}

needs = [0, 2, 6, 15, 20, 26, 38]
