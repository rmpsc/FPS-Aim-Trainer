import pygame
import sys
import random
import math


class Crosshair(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.gunshot = pygame.mixer.Sound('sounds/fox_laser.wav')
        self.gunshot.set_volume(.15)

    def shoot(self):
        global score
        global can_shoot
        global total_shots
        global shots_hit

        if can_shoot:
            self.gunshot.play()
            total_shots += 1
            if pygame.sprite.spritecollide(crosshair, target_group, True, pygame.sprite.collide_circle_ratio(.55)):
                shots_hit += 1
                score += 1
                add_target()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()


class Target(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        # self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]


# adds new target when one is shot
def add_target():
    new_target = Target('target_red3.png', random.randrange(200, width - 200), random.randrange(100, height - 150))
    # ensures targets don't overlap
    while pygame.sprite.spritecollide(new_target, target_group, False):
        new_target = Target('target_red3.png', random.randrange(200, width - 200), random.randrange(100, height - 100))

    target_group.add(new_target)


# updates high score
def update_high_score(s, hs):
    if s > hs:
        hs = s
        new_record.play()
    else:
        complete.play()
    return hs


def display_score(game_state):
    if game_state == 'in_progress':
        pts_surface = val_font_sm.render('PTS', True, (255, 255, 255))
        pts_rect = pts_surface.get_rect(center=(450, 55))
        screen.blit(pts_surface, pts_rect)

        score_surface = val_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(500, 50))
        screen.blit(score_surface, score_rect)

        percent_surface = impact_font.render('%', True, (255, 255, 255))
        percent_rect = percent_surface.get_rect(center=(1145, 50))
        screen.blit(percent_surface, percent_rect)

        if total_shots > 0:
            accuracy_surface = val_font.render(f'{str(math.trunc(float(shots_hit / total_shots) * 100))}', True, (255, 255, 255))
            accuracy_rect = accuracy_surface.get_rect(center=(1100, 50))
            screen.blit(accuracy_surface, accuracy_rect)
        else:
            default_acc = val_font.render(str(0), True, (255, 255, 255))
            default_acc_rect = default_acc.get_rect(center=(1100, 50))
            screen.blit(default_acc, default_acc_rect)

    if game_state == 'game_over':
        # (text, antialiasing, color, bg)
        score_surface = val_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(550, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = val_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = score_surface.get_rect(center=(1000, 100))
        screen.blit(high_score_surface, high_score_rect)

        begin_surface = val_font.render('space to begin', True, (255, 255, 255))
        begin_rect = begin_surface.get_rect(center=(795, 550))
        screen.blit(begin_surface, begin_rect)


def round_countdown():
    countdown_surface = val_font.render(str(int(countdown)), True, (255, 255, 255))
    countdown_rect = countdown_surface.get_rect(center=(800, 300))
    if .994 < countdown < 1:
        print("go")
        print(countdown)
        go.play()
    if countdown < 1:
        return
    screen.blit(countdown_surface, countdown_rect)


def round_timer():
    timer_surface = val_font.render(str(int(timer)), True, (255, 255, 255))
    timer_rect = timer_surface.get_rect(center=(800, 50))
    if timer < 1:
        return

    timer_dec_surface = val_font.render('<            >', True, (255, 255, 255))
    timer_dec_rect = timer_dec_surface.get_rect(center=(800, 50))

    screen.blit(timer_dec_surface, timer_dec_rect)
    screen.blit(timer_surface, timer_rect)


pygame.init()
clock = pygame.time.Clock()
width, height = 1600, 900
screen = pygame.display.set_mode((width, height))
val_font = pygame.font.Font('Valorant Font.ttf', 40)
val_font_sm = pygame.font.Font('Valorant Font.ttf', 20)
impact_font = pygame.font.SysFont('arialblack', 20)
print(pygame.font.get_fonts())


# Game Variables
# background = pygame.image.load('backgrounds/jett_bg.png').convert()
# background = pygame.image.load('backgrounds/wide-jett.jpg').convert()
background = pygame.image.load('backgrounds/val.png').convert()
background = pygame.transform.scale(background, (width, height))

pygame.mouse.set_visible(False)
game_active = False
game_start = False
can_shoot = False

countdown = 4
timer = 31
score = 0
high_score = 0
total_shots = 0
shots_hit = 0

round_time = 0

# Crosshair
# note: sprites must be in a group to be drawn
crosshair = Crosshair('crosshair_white_small.png')
crosshair_group = pygame.sprite.Group()
crosshair_group.add(crosshair)

# Target
target_group = pygame.sprite.Group()  # makes a new sprite group

# Sounds
go = pygame.mixer.Sound('sounds/go!.wav')
go.set_volume(.5)
new_record = pygame.mixer.Sound('sounds/new_record.wav')
new_record.set_volume(.5)
complete = pygame.mixer.Sound('sounds/complete.wav')
complete.set_volume(.5)
mission_complete = pygame.mixer.Sound('sounds/fox_mission.wav')
mission_complete.set_volume(.5)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # quits when player closes game
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            crosshair.shoot()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_active = not game_active
                if game_active:
                    for i in range(3):
                        add_target()
                    score = 0
                    round_start_time = pygame.time.get_ticks()

    screen.blit(background, (0, 0))

    if game_active:
        round_time = pygame.time.get_ticks() - round_start_time
        countdown -= .00638

        target_group.draw(screen)
        crosshair_group.draw(screen)
        crosshair_group.update()  # updates all in group at once
        round_countdown()
        display_score('in_progress')

        if round_time >= 3000:
            can_shoot = True
            timer -= .00638
            round_timer()
        if 2996 < round_time <= 3003:
            print(round_time)
        if round_time >= 33000:
            game_active = False
            # must keep in if statement or new record sound will continuously play
            high_score = update_high_score(score, high_score)

    else:
        can_shoot = False
        countdown = 4
        timer = 31
        total_shots = 0
        shots_hit = 0
        target_group.empty()
        display_score('game_over')

    pygame.display.flip()
    clock.tick(165)
