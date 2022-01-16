# -*- coding: utf-8 -*-
#Импоритруем необходимые библиотеки
import sys
import pygame
from functions import *
from classes import *

#_______Для отображения заставки
def start():
    all_sprites = pygame.sprite.Group()
    #Ставится заставка после запуска программы и значок с надписью "Играть"
    zastavka = Sprites('Заставка.jpg', (0, 0), 'images')
    znak_for_igrat = Sprites('Значок играть.jpg', (384, 600), 'images')
    all_sprites.add(zastavka, znak_for_igrat)
    all_sprites.draw(screen)
    #pygame.draw.rect(screen, (0, 0, 0), ((20, 20), (20, 20)))
    pygame.display.flip()
    flag = True
    #Пока не нажата кнопка "Играть" или Крестик на окне
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                flag = False
                break
            #Если нажата кнопка Играть(А других вариантов и нет!)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if click_in_rect(znak_for_igrat.rect, event.pos):
                    run = False
                    break
    if flag:
        menu()
    else:
        pygame.quit()

#_______Для отображения меню
def menu():
    screen.fill((0, 0, 0))
    all_sprites = pygame.sprite.Group()
    zastavka = Sprites('Заставка.jpg', (0, 0), 'images', '1', all_sprites)
    back = Sprites('Выйти.bmp', (420, 500), 'images', '1', all_sprites)
    levelss = Sprites('levels.bmp', (420, 340), 'images', '1', all_sprites)
    instruct = Sprites('instruct.bmp', (420, 200), 'images', '1', all_sprites)
    all_sprites.draw(screen)
    pygame.display.flip()
    flag_back = False
    flag_levels = False
    flag_instruction = False
    run = True
    while run:
        for event in pygame.event.get():
            #Нажата кнопка
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Выйти
                if click_in_rect(back.rect, event.pos):
                    run = False
                    flag_back = True
                #Инструкция
                if click_in_rect(instruct.rect, event.pos):
                    run = False
                    flag_instruction = True
                #Уровни
                elif click_in_rect(levelss.rect, event.pos):
                    flag_levels = True
                    run = False
                    
    if flag_back:
        pygame.quit()
    elif flag_levels:
        levels()
    elif flag_instruction:
        instruction()

#Для отображения уровней
def levels():
    spisok_levels = None
    with open('levels.txt') as x:
        #Список об информации каждого уровня(имя уровня, его состояние, имя изображения иконки этого уровня)
        spisok_levels = x.read().strip('\n').split('\n')
    level = None
    screen.fill((0, 0, 0))
    all_sprites = pygame.sprite.Group()
    zastavka = Sprites('Заставка.jpg', (0, 0), 'images', '1', all_sprites)
    back = Sprites('back.png', (1050, 550), 'images', '1', all_sprites)
    posx = 130
    posy = 80
    stepx, stepy = 330, 230 
    elem_in_x = 3
    for index, elem in enumerate(spisok_levels):
        if index % elem_in_x == 0 and index != 0:
            posy += stepy
            posx = posx - elem_in_x * stepx
        level_image = Sprites(elem.split(';')[-1], (posx, posy), 'images', elem.split(';')[1], all_sprites)
        posx += stepx
    all_sprites.draw(screen)
    flag = True
    run = True
    while run:
        for event in pygame.event.get():
            #Нажата кнопка
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Назад
                if click_in_rect(back.rect, event.pos):
                    run = False
                    flag = False
                else:
                    #Если пользователь кликнул по уровню и тот оказался разблокированным
                    for index, elem in enumerate(all_sprites):
                        if click_in_rect(elem.rect, event.pos) and index > 1:
                            if spisok_levels[index - 2].split(';')[1] == '1':
                                level = spisok_levels[index - 2].split(';')[0]
                                run = False
        pygame.display.flip()
    if flag:
        load_level()
        game(level)
    else: menu()
    
#После загрузки уровня Появляется сама игра
def game(level):
    tecsture_sprites = pygame.sprite.Group()
    fon_sprites = pygame.sprite.Group()
    for_mario_group = pygame.sprite.Group()  
                
    screen = pygame.display.set_mode((1200, 720))
    mario = Mario(20, 40, for_mario_group)
    spisok = get_images(level) + get_figures(level)
    spisok1 = list(filter(lambda x: x[0] == 'tecsture', spisok))
    spisok2 = list(filter(lambda x: x[0] == 'fon', spisok))
    finish = None
    for elem in spisok1:
        Tecstures(elem, tecsture_sprites)
        
    for elem in spisok2:   
        finish = Fon(elem, fon_sprites)

    for elem in fon_sprites:
        if finish.rect.x < elem.rect.x:
            finish = elem
    
    #Для обновы медленнее
    updating = 0
    
    clock = pygame.time.Clock()
    pygame.display.set_caption('Десант')
    
    #Флаги, которые влияют на процесс игры
    level_pass = False
    level_miss = False
    exit = False
    retry = False
    pause = False
    
    #Группа для отрисовки значков
    signs_sprites = pygame.sprite.Group()
    #Кнопки, на которые можно нажать во время игры
    retrying = Sprites('retry.png', (1100, 20), 'for_game_images', '1', signs_sprites)
    exiting = Sprites('exit.png', (1100, 120), 'for_game_images', '1', signs_sprites)
    pause_or_cont = Sprites('pause.png', (20, 20), 'for_game_images', '1', signs_sprites)
    spisok_tecstur = [sprite.rect for sprite in tecsture_sprites]
    #Для описания движения Марио
    x, y, sx, sy = mario.rect
    step = 2
    y0, v0y, ty, ay, stepty = y, 0, 0, 25, 0.05
    #Начало игрового цикла
    while level_pass is False and level_miss is False and exit is False and retry is False:
        screen.fill((255, 34, 25))
        #Отрисовка фона
        fon_sprites.draw(screen)
        #Отрисовка текстур
        tecsture_sprites.draw(screen)
        #Отрисовка Марио
        for_mario_group.draw(screen)
        #Отрисовка значков
        signs_sprites.draw(screen)
        slovar_nagatiy = pygame.key.get_pressed()
        #Была нажата кнопка стоп/продолжить
        for event in pygame.event.get():
            #Если пользователь нажал на SHIFT или на значок пауза/продолжить
            if (event.type == pygame.KEYDOWN and event.key == 1073742049) or\
               (event.type == pygame.MOUSEBUTTONDOWN and click_in_rect(pause_or_cont.rect, event.pos)):
                    if pause:
                        pause = False
                        pause_or_cont.image = load_image('pause.png', 'for_game_images')
                    else:
                        pause_or_cont.image = load_image('continue.png', 'for_game_images')
                        pause = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #
                if click_in_rect(retrying.rect, event.pos):
                    if dialog('Вы действительно хотите начать сначала?'): retry = True
                elif click_in_rect(exiting.rect, event.pos):
                    if dialog('Вы действительно хотите выйти?'): exit = True
                    
        #Перезапуск игры?
        if slovar_nagatiy[pygame.K_TAB]:
            if dialog('Вы действительно хотите начать сначала?'): retry = True
        #Выход из игры?
        if slovar_nagatiy[pygame.K_ESCAPE]:
            if dialog('Вы действительно хотите выйти?'): exit = True      
                
        #если игра не на паузе
        if not pause:
            
            #______Блок для задания движения Марио по оси OX________
            if slovar_nagatiy[pygame.K_LEFT]:
                if updating == 0:
                    mario.update('left')
                flag_l, x = is_moving_left(spisok_tecstur, x, y, y + sy, step)
            if slovar_nagatiy[pygame.K_RIGHT]:
                if updating == 0:
                    mario.update('right')
                flag_r, x = is_moving_right(spisok_tecstur, x + sx, y, y + sy, step, sx)
            
            #______Блок для задания движения Марио по оси OY________
            flag_b, yy = on_ground_bottom(spisok_tecstur, x, x + sx, y, y + sy, y0, v0y, ay, ty, sy, stepty)
            flag_top, yyy = on_ground_top(spisok_tecstur, x, x + sx, y, y + sy, y0, v0y, ay, ty, stepty)
            if flag_b:
                y = yy
                ty = 0
                y0 = y
                v0y = 0
                if slovar_nagatiy[pygame.K_UP] or slovar_nagatiy[pygame.K_SPACE]:
                    v0y = -75
            elif flag_top:
                y = yyy
                ty = 0
                y0 = y
                v0y = 0
            else:
                y = y0 + v0y * ty + ay * ty**2 / 2
                ty += stepty
            
            #Это для того, чтобы Камера с Марио могла перемещаться, когда он дойдет до середины окна, только вперед
            if x - 600 > 0 and x + 600 < finish.rect.x + 200:
                x -= step
                for sprite in fon_sprites:
                    sprite.rect.x = sprite.rect.x - step
                for sprite in tecsture_sprites:
                    sprite.rect.x = sprite.rect.x - step
            
            #Чтобы Марио мог идти только вперед        
            if x < 0:
                x = 0
                
            #Если Марио упал в бездну
            if y > 720:
                level_miss = True
                
            #Если Марио дошел до финиша
            if pygame.sprite.collide_mask(mario, finish):
                level_pass = True
            
            #Вставка координат Марио
            mario.setPos((x, y))
            updating += 1
            updating %= 8            
        pygame.display.flip()
        clock.tick(100)
        
    if exit:
        load_level()
        menu()
    elif retry:
        load_level()
        game(level)
    elif level_miss:
        level_missed(level)
    elif level_pass:
        level_passed(level)
        

def level_passed_or_missed_zastavka(message):
    font = pygame.font.Font(None, 80)
    string_rendered = font.render(message, 1, (255, 0, 255))
    intro_rect = string_rendered.get_rect()
    intro_rect.y = 330
    intro_rect.x = 400
    clock = pygame.time.Clock()
    step = 0
    while step < 20:
        clock.tick(10)
        #Рисуем закрывающийся занавес
        pygame.draw.rect(screen, (0, 255, 255), (step * 30, 0, 30, 720))
        pygame.draw.rect(screen, (0, 255, 255), (1200 - (step + 1) * 30, 0, 30, 720))
        #Вставляем кусок текста в прямоугольнике
        screen.blit(string_rendered, intro_rect)
        #Обновляем экран
        pygame.display.flip()
        step += 1

def level_missed(level):
    level_passed_or_missed_zastavka('GAME OVER')
    all_sprites = pygame.sprite.Group()
    #for_level_passed_images
    missed = Sprites('missed.bmp', (0, 0), 'for_level_missed_and_level_passed_images', '1', all_sprites)
    in_menu = Sprites('in_menu.bmp', (166, 500), 'for_level_missed_and_level_passed_images', '1', all_sprites)
    again = Sprites('again.bmp', (700, 500), 'for_level_missed_and_level_passed_images', '1', all_sprites)    
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    run = True
    exit_in_menu = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if click_in_rect(in_menu.rect, event.pos):
                    exit_in_menu = True
                    run = False
                    break
                elif click_in_rect(again.rect, event.pos):
                    run = False
                    break
                
    load_level()
    if exit_in_menu: menu()
    else: game(level)
        
    
def level_passed(level):
    level2 = None
    level_passed_or_missed_zastavka('CONGRATULATION')
    all_sprites = pygame.sprite.Group()
    #for_level_passed_images
    passed = Sprites('passed.bmp', (0, 0), 'for_level_missed_and_level_passed_images', '1', all_sprites)
    in_menu = Sprites('in_menu.bmp', (63, 500), 'for_level_missed_and_level_passed_images', '1', all_sprites)
    again = Sprites('again.bmp', (803, 500), 'for_level_missed_and_level_passed_images', '1', all_sprites)
    if level != 'level_5':
        spisok_levels = None
        next_level = Sprites('nextlevel.bmp', (460, 500), 'for_level_missed_and_level_passed_images', '1', all_sprites)
        #Разблокировываем следующий уровень
        with open('levels.txt', 'r') as x:
            #Список об информации каждого уровня(имя уровня, его состояние, имя изображения иконки этого уровня)
            spisok_levels = x.read().split('\n')
        with open('levels.txt', 'w') as y:
            for index, elem in enumerate(spisok_levels):
                if level in elem:
                    level2 = spisok_levels[index + 1][:spisok_levels[index + 1].index(';')]
                    spisok_levels[index + 1] = spisok_levels[index + 1].replace(';0;', ';1;')
                    break
            for elem in spisok_levels:
                print(elem, file=y)
                                      
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    run = True
    exit_in_menu = False
    nextlevel = False
    again_pass = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if level != 'level_5':
                    if click_in_rect(next_level.rect, event.pos):
                        nextlevel = True
                        run = False
                if click_in_rect(in_menu.rect, event.pos):
                    exit_in_menu = True
                    run = False
                if click_in_rect(again.rect, event.pos):
                    run = False
                    again_pass = True
                
    load_level()               
    if exit_in_menu:
        menu()
    elif again_pass:
        game(level)
    elif nextlevel:
        game(level2)
         

def load_level():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 80)
    line = 'Загрузка'
    string_rendered = font.render(line, 1, (255, 0, 0))
    intro_rect = string_rendered.get_rect()
    intro_rect.y = 330
    intro_rect.x = 400
    clock = pygame.time.Clock()
    step = 1
    #Рамка прогрузки
    pygame.draw.rect(screen, (0, 255, 0), (250, 450, 600, 80), 10)
    #Вставляем кусок текста в прямоугольнике
    screen.blit(string_rendered, intro_rect)
    while step < 20:
        clock.tick(10)
        step += 1
        #Рисуется процесс загрузки
        pygame.draw.rect(screen, (255, 0, 0), (200 + step * 30, 460, 30, 60))
        #Обновляем экран
        pygame.display.flip()
        
    
def instruction():
    all_sprites = pygame.sprite.Group()
    screen.fill((0, 255, 0))
    fon = Sprites('left_arrow.png', (-70, 120), 'for_instruction_images', '1', all_sprites)
    moving_left = Sprites('left_arrow.png', (-70, 120), 'for_instruction_images', '1', all_sprites)
    moving_right = Sprites('right_arrow.png', (0, 120), 'for_instruction_images', '1', all_sprites)
    moving_up = Sprites('up_arrow.png', (70, 120), 'for_instruction_images', '1', all_sprites)
    moving_up2 = Sprites('space.png', (220, 120), 'for_instruction_images', '1', all_sprites)
    shift = Sprites('Shift.png', (20, 240), 'for_instruction_images', '1', all_sprites)
    tab = Sprites('tab.png', (0, 360), 'for_instruction_images', '1', all_sprites)
    escape = Sprites('esc.png', (20, 480), 'for_instruction_images', '1', all_sprites)
    back = Sprites('back.png', (1050, 550), 'for_instruction_images', '1', all_sprites)
    font = pygame.font.Font(None, 30)
    spisok_strok = [('- Управление игроком влево/вправо/прыжок/прыжок', (500, 150)), ('  - Пауза/Продолжить', (250, 275)), \
                    ('  - Начать заново', (120, 395)), ('  - В меню', (110, 505)), ('Управление в игре', (500, 20))]
    lol = 50
    for line in spisok_strok:
        string_rendered = font.render(line[0], 1, (0, 0, 0))
        intro_rect = string_rendered.get_rect()
        intro_rect.x = line[-1][0]
        intro_rect.y = line[-1][-1]
        lol += 50
        #Вставляем кусок текста в прямоугольнике
        screen.blit(string_rendered, intro_rect)
    run = True
    all_sprites.draw(screen)
    pygame.display.flip()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if click_in_rect(back.rect, event.pos):
                    run = False
    menu()

#Функция для диалогового окна
def dialog(message):
    all_sprites = pygame.sprite.Group()
    yes = Sprites('yes.bmp', (440, 310), 'images', '1', all_sprites)
    no = Sprites('no.bmp', (700, 310), 'images', '1', all_sprites)
    font = pygame.font.Font(None, 25)
    string_rendered = font.render(message, 1, (0, 0, 0))
    intro_rect = string_rendered.get_rect()
    intro_rect.x, intro_rect.y = 420, 280
    pygame.draw.rect(screen, (0, 255, 0), (400, 260, 400, 100))
    #Вставляем кусок текста в прямоугольнике
    screen.blit(string_rendered, intro_rect)
    run = True
    exit = False
    all_sprites.draw(screen)
    pygame.display.flip()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if click_in_rect(yes.rect, event.pos):
                    run = False
                    exit = True
                elif click_in_rect(no.rect, event.pos):
                    run = False
    if exit:
        return True
    else:
        return False
    
    
#Функция, которая проверяет событие нажатия кнопки мыши в области прямоугольника
def click_in_rect(rect, pos):
    x1, y1, x2, y2 = rect
    x_pos, y_pos = pos
    if x1 < x_pos < x1 + x2 and y1 < y_pos < y1 + y2:
        return True
    return False
    
    
#Инициализайия pygame
pygame.init()
size = 1200, 720
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Марио')
start()