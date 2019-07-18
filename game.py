import pygame
from random import *
import time


class Enemy:
    x = 0
    y = 0
    v_x = 0
    v_y = 0

    def __init__(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos
        self.v_x = (450 - x_pos) / randint(int(600 / (pow(score, 0.05) + 1)), int(1200 / (pow(score, 0.05) + 1)))
        self.v_y = (450 - y_pos) / randint(int(600 / (pow(score, 0.05) + 1)), int(1200 / (pow(score, 0.05) + 1)))

    def mov(self):
        self.x += self.v_x
        self.y += self.v_y


def start_game():
    global window, clock
    global db_image, player_image, enemy_image
    global font, big_font

    pygame.init()
    window = pygame.display.set_mode((900, 900))
    pygame.display.set_caption('체험! DDoS의 현장!')
    clock = pygame.time.Clock()

    db_image = pygame.image.load("database.png")
    player_image = pygame.image.load("player.png")
    enemy_image = pygame.image.load("enemy.png")

    font = pygame.font.Font("NanumGothic.ttf", 24)
    big_font = pygame.font.Font("NanumGothic.ttf", 100)


def print_img(a, b, img):
    window.blit(img, (a, b))


def print_enemy():
    global enemy_image
    global enemy_array

    for enemy in enemy_array:
        print_img(enemy.x, enemy.y, enemy_image)


def run_game():
    global window, clock, timer
    global db_image, player_image
    global font
    global enemy_array
    global score

    p_x = 450
    p_y = 100
    speed = 10
    life = 100
    score = 0
    limit = 20
    timer = 0
    temp = 0

    enemy_array = []

    while True:
        press = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    return True
        if press[pygame.K_LEFT]:
            p_x -= int(speed)
        if press[pygame.K_RIGHT]:
            p_x += int(speed)
        if press[pygame.K_UP]:
            p_y -= int(speed)
        if press[pygame.K_DOWN]:
            p_y += int(speed)
        if press[pygame.K_k]:
            life = 0

        if pow(400 - p_x, 2) + pow(400 - p_y, 2) <= 22500:
            if press[pygame.K_LEFT]:
                p_x += int(speed * 1.5)
            if press[pygame.K_RIGHT]:
                p_x -= int(speed + 1.5)
            if press[pygame.K_UP]:
                p_y += int(speed + 1.5)
            if press[pygame.K_DOWN]:
                p_y -= int(speed + 1.5)

        if p_x < 0:
            speed -= 0.5
            p_x = 0
        elif p_x > 800:
            speed -= 0.5
            p_x = 800
        if p_y < 0:
            speed -= 0.5
            p_y = 0
        elif p_y > 800:
            speed -= 0.5
            p_y = 800

        if (timer % 60) == 0:
            timer = 0
            if len(enemy_array) < int(limit):
                while True:
                    e_x = randint(-60, 910)
                    e_y = randint(-60, 910)
                    if e_x <= 200 or e_x >= 700 or e_y <= 200 or e_y >= 700:
                        break
                enemy = Enemy(e_x, e_y)
                enemy_array.append(enemy)
        else:
            timer += 1

        for enemy in enemy_array:
            enemy.mov()
            temp = pow(425 - enemy.x, 2) + pow(425 - enemy.y, 2)
            if temp <= 15625:
                del enemy_array[enemy_array.index(enemy)]
                life -= 1
            elif pow(p_x - enemy.x + 25, 2) + pow(p_y - enemy.y + 25, 2) <= pow(125, 2):
                score += int((211600 - temp) * 0.00001 + pow(enemy.v_x * enemy.v_x + enemy.v_y * enemy.v_y, 0.5))
                speed += 0.02
                limit += 0.05
                del enemy_array[enemy_array.index(enemy)]

        window.fill((0, 0, 0))
        print_img(313, 333, db_image)
        print_img(p_x, p_y, player_image)
        print_enemy()
        pygame.draw.rect(window, (255, 255, 255), (360, 425, 180, 50))
        pygame.draw.rect(window, (255, 127, 127), (360, 425, int(1.8 * life), 50))
        text = font.render(str(life) + "/100", True, (0, 0, 0))
        window.blit(text, (400, 438))
        score_t = font.render("Score : " + str(score), True, (255, 255, 255))
        window.blit(score_t, (10, 10))

        if life <= 0:
            window.fill((0, 0, 0))
            text = big_font.render("Game Over", True, (255, 255, 255))
            window.blit(text, (200, 300))
            score_f = font.render("Final Score : " + str(score), True, (255, 255, 255))
            message = font.render("After 5 secs, Game will restart!", True, (255, 255, 255))
            window.blit(score_f, (380, 450))
            window.blit(message, (280, 500))

        pygame.display.flip()
        clock.tick(60)

        if life <= 0:
            time.sleep(5.0)
            return False


if __name__ == "__main__":
    start_game()
    while True:
        if run_game():
            break

    pygame.quit()
    quit()
