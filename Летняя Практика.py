import pygame
from time import sleep
from random import randint, shuffle

im = pygame.image.load
pygame.display.set_icon(im("icon.png"))

bg_cards = im(r"bg_cards.png")
hide_card = im(r"hide_card.png")
open_card = im(r"open_card.png")

cards = [im(r"cards\c1.png"), im(r"cards\c2.png"), im(r"cards\c3.png"), im(r"cards\cw.png"), im(r"cards\dr.png"),
         im(r"cards\d.png"), im(r"cards\dg1.png"), im(r"cards\dg2.png"), im(r"cards\f1.png"), im(r"cards\f2.png"),
         im(r"cards\g.png"), im(r"cards\k.png"), im(r"cards\p.png"), im(r"cards\pp.png"), im(r"cards\pg.png"),
         im(r"cards\s.png"), im(r"cards\sw.png"), im(r"cards\t.png"), im(r"cards\t4.png"), im(r"cards\w.png")]

score1, score2, player, hod = 0, 0, 0, 0
first_card = None
gen = True
second_card = 1
firstxy, secondxy, already_cards, card_for_lvl = [], [], [], []

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("СМОТРИ И ЗАПОМИНАЙ")
pygame.display.init()
display = pygame.display.set_mode((1024, 768))


def print_text(message, x, y, font_color=(0, 0, 0), font_type="shrift.ttf", font_size=30):
    if ("оба" in message) or ("победил" in message) or ('Счёт' in message) or ('Ничья' in message):
        font_type = pygame.font.Font(font_type, 40)
    else:
        font_type = pygame.font.Font(font_type, font_size)
    match message:
        case '12 карточек':
            text = font_type.render(message, True, (0, 255, 0))
        case '16 карточек':
            text = font_type.render(message, True, (32, 178, 170))
        case '20 карточек':
            text = font_type.render(message, True, (255, 255, 0))
        case '24 карточки':
            text = font_type.render(message, True, (0, 0, 255))
        case '30 карточек':
            text = font_type.render(message, True, (103, 184, 238))
        case '1 игрок':
            text = font_type.render(message, True, (255, 100, 100))
        case '2 игрока':
            text = font_type.render(message, True, (0, 0, 128))
        case 'Ничья!':
            text = font_type.render(message, True, (127, 255, 0))
        case "оба":
            text = font_type.render(message, True, (219, 18, 0))
        case "Начать игру":
            text = font_type.render(message, True, (218, 112, 214))
        case _:
            text = font_type.render(message, True, font_color)
    if "Счёт игрока1: " in message:
        text = font_type.render(message, True, (2, 8, 250))
    if "Счёт игрока2: " in message:
        text = font_type.render(message, True, (250, 83, 0))
    if "Вы победили!" in message:
        text = font_type.render(message, True, (220, 20, 60))
    if "победил" in message:
        text = font_type.render(message, True, (32, 178, 170))
    if "Вы оба набрали" in message:
        text = font_type.render(message, True, (219, 18, 0))
    display.blit(text, (x, y))


class Button:
    def __init__(self, width, height, inactivecolor, activecolor):
        self.width = width
        self.height = height
        self.inactivecolor = inactivecolor
        self.activecolor = activecolor

    def draw(self, x, y, message, action=None):
        if (x < pygame.mouse.get_pos()[0] < x + self.width) and (y < pygame.mouse.get_pos()[1] < y + self.height):
            pygame.draw.ellipse(display, self.activecolor, (x, y, self.width, self.height))
            if pygame.mouse.get_pressed()[0] == 1:
                pygame.mixer.Sound.play(pygame.mixer.Sound("button.mp3"))
                pygame.time.delay(300)
                if action in [1, 2, 3, 4, 5]:
                    generation(action)
                if action == 10:
                    level(1)
                if action == 20:
                    level(2)
                elif action is not None:
                    action()
        else:
            pygame.draw.ellipse(display, self.inactivecolor, (x, y, self.width, self.height))
        if action == players:
            print_text(message, x + 10, y + 30)
        elif action in [1, 2, 3, 4, 5]:
            print_text(message, x + 13, y + 36)
        else:
            print_text(message, x + 10, y + 30)


class Cardsbutton:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self, x, y, card_pic, action=None):
        global first_card, second_card, firstxy, secondxy, already_cards, score1, score2, hod
        if (x < pygame.mouse.get_pos()[0] < x + self.width) and (y < pygame.mouse.get_pos()[1] < y + self.height):
            if pygame.mouse.get_pressed()[0] == 1:
                pygame.mixer.Sound.play(pygame.mixer.Sound("button.mp3"))
                pygame.time.delay(300)
                display.blit(open_card, (x + 4, y + 4))
                display.blit(card_pic, (x, y))
                display.blit(bg_cards, (x - 10, y - 10))
                pygame.display.update()
                if first_card is None:
                    first_card = card_pic
                    firstxy = [x, y]
                    second_card = 1
                else:
                    hod += 1
                    second_card = card_pic
                    secondxy = [x, y]
                    if firstxy == secondxy:
                        display.blit(hide_card, (firstxy[0], firstxy[1]))
                        display.blit(bg_cards, (firstxy[0] - 10, firstxy[1] - 10))
                        first_card = None
                    if action is not None and first_card == second_card and (firstxy != secondxy):
                        already_cards.append(card_pic)
                        if player == 1:
                            score1 += 1
                        if player == 2:
                            if hod % 2 == 1:
                                score1 += 1
                            if hod % 2 == 0:
                                score2 += 1
                        pygame.mixer.Sound.play(pygame.mixer.Sound("twocardsopen.mp3"))
                        action(card_pic, firstxy, secondxy)
                    if first_card != second_card and second_card != 1 and len(secondxy) == 2:
                        sleep(0.5)
                        if card_pic not in already_cards:
                            if player == 1:
                                score1 -= 1
                            if player == 2:
                                if hod % 2 == 1:
                                    score1 -= 1
                                if hod % 2 == 0:
                                    score2 -= 1
                            display.blit(hide_card, (firstxy[0], firstxy[1]))
                            display.blit(bg_cards, (firstxy[0] - 10, firstxy[1] - 10))
                            display.blit(hide_card, (secondxy[0], secondxy[1]))
                            display.blit(bg_cards, (secondxy[0] - 10, secondxy[1] - 10))
                            update_display()
                    update_display()
                    first_card = None


def two_cards(card_pic, first_coor, second_coor):
    global already_cards
    already_cards.append(card_pic)
    display.blit(card_pic, (first_coor[0], first_coor[1]))
    display.blit(bg_cards, (first_coor[0] - 10, first_coor[1] - 10))
    display.blit(card_pic, (second_coor[0], second_coor[1]))
    display.blit(bg_cards, (second_coor[0] - 10, second_coor[1] - 10))
    update_display()


def set_cards(x, y, i):
    display.blit(open_card, (x, y))
    display.blit(card_for_lvl[i], (x, y))
    display.blit(bg_cards, (x - 10, y - 10))


def game_stop():
    global gen
    gen = False
    pygame.mixer.Sound.play(pygame.mixer.Sound("win.mp3"))
    sleep(2)
    if player == 1:
        win_one()
    else:
        win_two()
    startgame()


def hide_cards(x, y):
    display.blit(hide_card, (x, y))
    display.blit(bg_cards, (x - 10, y - 10))


def fill_card_for_lvl(length):
    global card_for_lvl
    while len(card_for_lvl) != length:
        el = randint(0, 19)
        if cards[el] not in card_for_lvl:
            card_for_lvl.append(cards[el])
    card_for_lvl *= 2
    shuffle(card_for_lvl)


def generation(hard):
    global already_cards, card_for_lvl, gen
    first_vxod = True
    gen = True
    display.blit(im("bg.jpg"), (0, 0))
    already_cards, card_for_lvl = [], []
    i = 0
    if hard == 1:
        fill_card_for_lvl(6)
        for x in [70, 320, 570, 820]:
            for y in [70, 320, 570]:
                set_cards(x, y, i)
                i += 1
        while gen:
            check_to_exit()
            i = 0
            for x in [70, 320, 570, 820]:
                for y in [70, 320, 570]:
                    if card_for_lvl[i] not in already_cards:
                        Cardsbutton(140, 140).draw(x, y, card_for_lvl[i], two_cards)
                    i += 1
            update_display()
            if first_vxod:
                sleep(3)
                for x in [70, 320, 570, 820]:
                    for y in [70, 320, 570]:
                        hide_cards(x, y)
            first_vxod = False
            if len(already_cards) == 12:
                game_stop()
    if hard == 2:
        fill_card_for_lvl(8)
        for x in [70, 320, 570, 820]:
            for y in [20, 220, 420, 620]:
                set_cards(x, y, i)
                i += 1
        while gen:
            check_to_exit()
            i = 0
            for x in [70, 320, 570, 820]:
                for y in [20, 220, 420, 620]:
                    if card_for_lvl[i] not in already_cards:
                        Cardsbutton(140, 140).draw(x, y, card_for_lvl[i], two_cards)
                    i += 1
            update_display()
            if first_vxod:
                sleep(6)
                for x in [70, 320, 570, 820]:
                    for y in [20, 220, 420, 620]:
                        hide_cards(x, y)
            first_vxod = False
            if len(already_cards) == 16:
                game_stop()
    if hard == 3:
        fill_card_for_lvl(10)
        for x in [40, 240, 440, 640, 840]:
            for y in [20, 220, 420, 620]:
                set_cards(x, y, i)
                i += 1
        while gen:
            check_to_exit()
            i = 0
            for x in [40, 240, 440, 640, 840]:
                for y in [20, 220, 420, 620]:
                    if card_for_lvl[i] not in already_cards:
                        Cardsbutton(140, 140).draw(x, y, card_for_lvl[i], two_cards)
                    i += 1
            update_display()
            if first_vxod:
                sleep(9)
                for x in [40, 240, 440, 640, 840]:
                    for y in [20, 220, 420, 620]:
                        hide_cards(x, y)
            first_vxod = False
            if len(already_cards) == 20:
                game_stop()
    if hard == 4:
        fill_card_for_lvl(12)
        for x in [20, 190, 360, 530, 700, 870]:
            for y in [20, 220, 420, 620]:
                set_cards(x, y, i)
                i += 1
        while gen:
            check_to_exit()
            i = 0
            for x in [20, 190, 360, 530, 700, 870]:
                for y in [20, 220, 420, 620]:
                    if card_for_lvl[i] not in already_cards:
                        Cardsbutton(140, 140).draw(x, y, card_for_lvl[i], two_cards)
                    i += 1
            update_display()
            if first_vxod:
                sleep(12)
                for x in [20, 190, 360, 530, 700, 870]:
                    for y in [20, 220, 420, 620]:
                        hide_cards(x, y)
            first_vxod = False
            if len(already_cards) == 24:
                game_stop()
    if hard == 5:
        fill_card_for_lvl(15)
        for x in [20, 190, 360, 530, 700, 870]:
            for y in [20, 170, 320, 470, 620]:
                set_cards(x, y, i)
                i += 1
        while gen:
            check_to_exit()
            i = 0
            for x in [20, 190, 360, 530, 700, 870]:
                for y in [20, 170, 320, 470, 620]:
                    if card_for_lvl[i] not in already_cards:
                        Cardsbutton(140, 140).draw(x, y, card_for_lvl[i], two_cards)
                    i += 1
            update_display()
            if first_vxod:
                sleep(15)
                for x in [20, 190, 360, 530, 700, 870]:
                    for y in [20, 170, 320, 470, 620]:
                        hide_cards(x, y)
            first_vxod = False
            if len(already_cards) == 30:
                game_stop()


def check_to_exit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


def update_display():
    pygame.display.update()
    pygame.time.Clock().tick(60)


def level(count_of_players):
    global player
    player = count_of_players
    display.blit(im("bg.jpg"), (0, 0))
    print_text("Выберите сложность", 220, 40, (105, 105, 228), "shrift.ttf", 40)
    while True:
        check_to_exit()
        Button(310, 110, (221, 160, 221), (238, 130, 238)).draw(340, 120, '12 карточек', 1)
        Button(310, 110, (186, 85, 211), (255, 0, 255)).draw(340, 240, '16 карточек', 2)
        Button(310, 110, (0, 0, 139), (0, 0, 255)).draw(340, 360, '20 карточек', 3)
        Button(310, 110, (184, 134, 11), (218, 165, 32)).draw(340, 480, '24 карточки', 4)
        Button(310, 110, (244, 91, 0), (244, 41, 0)).draw(340, 600, '30 карточек', 5)
        update_display()


def win_one():
    display.blit(im("bg.jpg"), (0, 0))
    print_text("Вы победили! Ваш счёт: " + str(score1), 120, 240)
    update_display()
    sleep(5)


def win_two():
    display.blit(im("bg.jpg"), (0, 0))
    if score1 > score2:
        print_text("Игрок 1 победил!", 240, 230)
        print_text("Счёт игрока1: " + str(score1), 250, 380)
        print_text("Счёт игрока2: " + str(score2), 250, 430)
    if score1 < score2:
        print_text("Игрок 2 победил!", 220, 230)
        print_text("Счёт игрока1: " + str(score1), 250, 380)
        print_text("Счёт игрока2: " + str(score2), 250, 430)
    if score1 == score2:
        print_text("Ничья!", 410, 145)
        print_text("Вы оба набрали: " + str(score1) + " очков", 140, 300)
    update_display()
    sleep(5)


def players():
    global score1, score2, hod
    hod, score1, score2 = 0, 0, 0
    display.blit(im("bg.jpg"), (0, 0))
    print_text("Выберите количество игроков", 80, 300, (255, 255, 128), "shrift.ttf", 40)
    while True:
        check_to_exit()
        Button(210, 100, (110, 210, 0), (110, 255, 0)).draw(250, 420, '1 игрок', 10)
        Button(210, 100, (210, 50, 0), (255, 50, 0)).draw(550, 420, '2 игрока', 20)
        update_display()


def startgame():
    display.blit(im("bg.jpg"), (0, 0))
    pygame.mixer.Sound("start.mp3").play()
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.load("bg_music.mp3")
    pygame.mixer.music.play(-1)
    while True:
        check_to_exit()
        Button(300, 100, (10, 10, 150), (10, 10, 250)).draw(360, 344, 'Начать игру', players)
        update_display()


startgame()

pygame.quit()
