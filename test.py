import time
def inBounds(a1,a2,b1,b2):
    if a1 < b2 or a2 > b1:
        return True
    else:
        return False
def detect_collision(met_pos, player_pos, player_dim, met_dim): #shane
    px = player_pos[0]
    py = player_pos[1]
    mx = met_pos[0]
    my = met_pos[1]
    mb = met_dim
    pb = player_dim
    if my + mb > py:
        if inBounds(px, px + pb, mx, mx + mb):
            return True
        else:
            return False
    else:
        return False

while True:
    a = detect_collision([5,5],[5,10],1,1)
    print(a)
    time.sleep(0.1)