import asyncio
import pygame
import random
import time
rows = 0
alive = True
difup = 60
score = 0
descentrate = 240
descents = 0
descenttimer = 240
tsc = 60
cooldown_tracker = 0
enemyreload = 1000
movecooldown = random.randint(1,10)*10
movedir = False
altshot = False
# Enemy AI will have a starting position and a horisontal offset
pygame.init()
pygame.font.init()
font = pygame.font.SysFont(None, 36)
clock=pygame.time.Clock()
alive = True
score = 0
descents = 0
descenttimer = 240
tsc = 60
cooldown_tracker = 0
enemyreload = 1000
movecooldown = random.randint(1,10)*10
movedir = False
altshot = False
# Enemy AI will have a starting position and a horisontal offset
enemyshots = []
player = pygame.Rect(320, 430, 32, 32)
WIDTH,HEIGHT=640,480
screen=pygame.display.set_mode((WIDTH,HEIGHT))
player_img = pygame.transform.scale(pygame.image.load("jet.png"), (32, 32)).convert_alpha()
shot_img = pygame.transform.scale(pygame.image.load("beam.png"), (2, 8)).convert_alpha()
rail_img = pygame.transform.scale(pygame.image.load("rail.png"), (32, 32)).convert_alpha()
ball_img = pygame.transform.scale(pygame.image.load("ball.png"), (8, 8)).convert_alpha()
death_img = pygame.transform.scale(pygame.image.load("DEATH.png"), (640, 480)).convert_alpha()
running=True
allenemiesbd = []
allenemies = []
enemies = []
for c in range(0,2):
    enemies = []
    for i in range(0,15):
        enemies.append([pygame.Rect(i*40+20, c*26, 32, 32), random.randint(1,10)*200])
        allenemies.append(enemies)
        allenemiesbd.append([0, 0, random.randint(1,10)*10, c+1%2 == 0])
    rows += 1
print(allenemies)
playershots = []
enemyshots = []
player = pygame.Rect(320, 430, 32, 32)
WIDTH,HEIGHT=640,480
screen=pygame.display.set_mode((WIDTH,HEIGHT))
player_img = pygame.transform.scale(pygame.image.load("jet.png"), (32, 32)).convert_alpha()
shot_img = pygame.transform.scale(pygame.image.load("beam.png"), (2, 8)).convert_alpha()
rail_img = pygame.transform.scale(pygame.image.load("rail.png"), (32, 32)).convert_alpha()
ball_img = pygame.transform.scale(pygame.image.load("ball.png"), (8, 8)).convert_alpha()
death_img = pygame.transform.scale(pygame.image.load("DEATH.png"), (640, 480)).convert_alpha()
fleetpos = 0
fleettarg = 0
running=True
enemies = []
playershots = []
def enemymove():
    global enemiesbd
    global movedir
    global movecooldown
    global fleetpos
    global fleettarg
    for enemies in allenemies:
        if allenemiesbd[allenemies.index(enemies)][0] < allenemiesbd[allenemies.index(enemies)][1] and len(enemies)>0:
            for e in enemies:
                e[0].x += 0.5
                try:
                    enemies[enemies.index(e)+1]
                except IndexError:
                    pass
                else:
                    if enemies.index(e) < len(enemies)/2 and enemies[enemies.index(e)+1][0].x - e[0].x > 40:
                        e[0].x +=1
                try:
                    enemies[enemies.index(e)-1]
                except IndexError:
                    pass
                else:
                    if enemies.index(e) > len(enemies)/2 and e[0].x - enemies[enemies.index(e)-1][0].x > 40:
                        e[0].x -=1
            allenemiesbd[allenemies.index(enemies)][0] += 1
        elif allenemiesbd[allenemies.index(enemies)][0] > allenemiesbd[allenemies.index(enemies)][1] and len(enemies)>0:
            for e in enemies:
                e[0].x -= 1
                try:
                    enemies[enemies.index(e)+1]
                except IndexError:
                    pass
                else:
                    if enemies.index(e) < len(enemies)/2 and enemies[enemies.index(e)+1][0].x - e[0].x > 40:
                        e[0].x +=1
                try:
                    enemies[enemies.index(e)-1]
                except IndexError:
                    pass
                else:
                    if enemies.index(e) > len(enemies)/2 and e[0].x - enemies[enemies.index(e)-1][0].x > 40:
                        e[0].x -=1
            allenemiesbd[allenemies.index(enemies)][0] -= 1
        elif allenemiesbd[allenemies.index(enemies)][0] == allenemiesbd[allenemies.index(enemies)][1] and len(enemies)>0:
            allenemiesbd[allenemies.index(enemies)][2] -= 1
            if allenemiesbd[allenemies.index(enemies)][2] == 0:
                if allenemiesbd[allenemies.index(enemies)][3]:
                    allenemiesbd[allenemies.index(enemies)][1] += 0-(enemies[0][0].x-10)
                    allenemiesbd[allenemies.index(enemies)][3] = False
                else:
                    allenemiesbd[allenemies.index(enemies)][1] += 600 - enemies[-1][0].x
                    allenemiesbd[allenemies.index(enemies)][3] = True
                allenemiesbd[allenemies.index(enemies)][2] += random.randint(1,10)*200
                # print(allenemiesbd[allenemies.index(enemies)][2])
def shoot():
    k=pygame.key.get_pressed()
    global altshot
    global playershots
    global cooldown_tracker
    cooldown_tracker += clock.get_time()
    if cooldown_tracker > 400:
        cooldown_tracker = 0
    if k[pygame.K_UP] and cooldown_tracker==0:
        if altshot:
            playershots.append(pygame.Rect(player.x + 20, player.y, 2, 8))
            altshot = False
        else:
            playershots.append(pygame.Rect(player.x + 10, player.y, 2, 8))
            altshot = True
def enemyshoot():
    global allenemies
    global enemyreload
    global enemyshots
    global enemies
    for enemies in allenemies:
        for e in enemies:
            e[1] = e[1]-1
            if e[1] < 0:
                enemyshots.append(pygame.Rect(e[0].x+10, e[0].y, 8, 8))
                e[1] = random.randint(1, 10)*enemyreload
def moveplayer():
    global player
    k=pygame.key.get_pressed()
    if k[pygame.K_RIGHT]:
        player.x += 5
    elif k[pygame.K_LEFT]:
        player.x += -5
def descend():
    global descents
    global allenemies
    global descenttimer
    descenttimer -= 1
    if descenttimer<1:
        for enemies in allenemies:
            for e in enemies:
                e[0].y += 1
        descenttimer = 180
        descents += 1
def addnew():
    global rows
    global descents
    global allenemies
    global allenemiesbd
    print(len(allenemies))
    for enemies in allenemies:
        if len(enemies) == 0:
            allenemiesbd.remove(allenemiesbd[allenemies.index(enemies)])
            allenemies.remove(enemies)
            rows -= 1
    if rows < 2 or (descents > 3 and rows < 4):
        enemies = []
        for i in range(0,15):
            enemies.append([pygame.Rect(i*40+20, c*26, 32, 32), random.randint(1,10)*200])
            allenemies.append(enemies)
            allenemiesbd.append([0, 0, random.randint(1,10)*10, c+1%2 == 0])
            rows +=1
        descents = 0

def pbullets():
    global screen
    global score
    global playerx
    global playery
    global enemies
    global enemyshots
    global playershots
    for b in playershots:
        b.y = b.y-5
        for enemies in allenemies:
            for e in enemies:
                if e[0].colliderect(b):
                    enemies.remove(e)
                    try: playershots.remove(b)
                    except ValueError: pass
                    score += 10 
        if b.y < 0:
            try: playershots.remove(b)
            except ValueError: pass
    for b in enemyshots:
        global alive
        global running
        b.y = b.y+5
        if b.colliderect(player):
            alive = False
            screen.fill("black")
            enemyshots.remove(b)
            screen.blit(death_img, (0, 0))
            screen.blit(font.render("Your score: " + str(score), False, "red"), (0, 0))
            pygame.display.flip()

        if b.y > 500:
            enemyshots.remove(b)
async def main():
    global running
    global screen
    global score
    global playerx
    global playery
    global enemies
    global enemyshots
    global playershots
    global enemyreload, tsc, difup, descentrate
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False
        if alive:
            enemymove()
            moveplayer()
            shoot()
            addnew()
            pbullets()
            enemyshoot()
            descend()
            screen.fill("black")
            for b in playershots:
                    screen.blit(shot_img, (b.x, b.y))
            for b in enemyshots:
                    screen.blit(ball_img, (b.x, b.y))
            for row in allenemies:
                for e in row:
                    screen.blit(rail_img, (e[0].x, e[0].y))
            screen.blit(player_img, (player.x, player.y))
            screen.blit(font.render("Score: " + str(score), False, "red"), (0, 0))

            pygame.display.flip()
            if enemyreload > 20:
                enemyreload -= 0.01
            tsc = tsc-1
            if tsc == 0:
                tsc = 60
                score +=1
            difup = difup-1
            if difup == 0:
                difup = 60
                if descentrate > 40:
                    descentrate -= 20
                if enemyreload > 200:
                    enemyreload -= 20 
            
        else:
            screen.fill("black")
            screen.blit(death_img, (0, 0))
            screen.blit(font.render("Your score: " + str(score), False, "red"), (0, 0))
            pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())

