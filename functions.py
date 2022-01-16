# -*- coding: utf-8 -*-
import os
import pygame
import sqlite3

#______Для возвращения требуемой картинки в виде объекта pygame
def load_image(name, catalog, colorkey=None):
    fullname = os.path.join(catalog, name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()    
    return image

#Возвращение из БД фигур и информацию о них, отобранных по критериям
def get_figures(level='all', purpose='all', type_of_figure='all', color='all', coords='all', size='all', full_or_empty='all'):
    con = sqlite3.connect('design_for_game.db')
    cur = con.cursor()

    string = f'level="{level}" purpose="{purpose}" type_of_figure="{type_of_figure}" color="{color}" coords="{coords}" size="{size}" full_or_empty="{full_or_empty}"'
    string_for_search = ''
    for elem in string.split():
        if elem.split('=')[-1][1:-1] != 'all':
            string_for_search += ' AND ' + elem
    if string_for_search != '':
        string_for_search = ' WHERE' + string_for_search[4:]
    result = cur.execute(f"SELECT purpose, type_of_figure, color, coords, size, full_or_empty FROM figures {string_for_search}").fetchall()
    if result:
        return [elem for elem in result]
    return []


#Возвращение из БД информацию о изображениях, отобранных по критериям
def get_images(level='all', purpose='all', name_image='all', color='all', coords='all'):
    con = sqlite3.connect('design_for_game.db')
    cur = con.cursor()
    string = f'level="{level}" purpose="{purpose}" name_image="{name_image}" color="{color}" coords="{coords}"'
    string_for_search = ''
    for elem in string.split():
        if elem.split('=')[-1][1:-1] != 'all':
            string_for_search += ' AND ' + elem
    if string_for_search != '':
        string_for_search = ' WHERE' + string_for_search[4:]
    result = cur.execute(f"SELECT purpose, name_image, coords FROM images {string_for_search}").fetchall()
    if result:
        return [elem for elem in result]
    return []

#Функции для проверки возможности движения Марио вправо, влево, вверх, вниз
def is_moving_right(tecstures, xx, y1, y2, step, xxx):
    for elem in sorted(tecstures, key=lambda x: x[0]):
        if elem[1] < y1 < elem[1] + elem[-1] or elem[1] < y2 < elem[1] + elem[-1] or y1 < elem[1] < y2 or y1 < elem[1] + elem[-1] < y2:
            if xx + step >= elem[0] and xx <= elem[0]:
                return False, elem[0] - xxx
    return True, xx + step - xxx

def is_moving_left(tecstures, xx, y1, y2, step):
    for elem in sorted(tecstures, key=lambda x: -x[0]):
        if elem[1] < y1 < elem[1] + elem[-1] or elem[1] < y2 < elem[1] + elem[-1] or y1 < elem[1] < y2 or y1 < elem[1] + elem[-1] < y2:
            if xx - step <= elem[0] + elem[2] and xx >= elem[0] + elem[2]:
                return False, elem[0] + elem[2]
    return True, xx - step
    
def on_ground_bottom(tecstures, x1, x2, y1, y2, y0, v0y, ay, t, sy, stepty):
    t += stepty
    for elem in sorted(tecstures, key=lambda x: -x[1]):
        tx1, tx2, ty1, ty2 = elem[0], elem[0] + elem[2], elem[1], elem[1] + elem[-1]
        if tx1 < x1 < tx2 or tx1 < x2 < tx2 or x1 < tx1 < x2 or x1 < tx2 < x2:
            if ty1 <= y0 + sy + v0y * t + ay * t**2 / 2 and ty2 > y1:
                return True, ty1 - sy
    return False, None

def on_ground_top(tecstures, x1, x2, y1, y2, y0, v0y, ay, t, stepty):
    t += stepty
    for elem in sorted(tecstures, key=lambda x: -x[1]):
        tx1, tx2, ty1, ty2 = elem[0], elem[0] + elem[2], elem[1], elem[1] + elem[-1]
        if tx1 < x1 < tx2 or tx1 < x2 < tx2 or x1 < tx1 < x2 or x1 < tx2 < x2:
            if ty2 >= y0 + v0y * t + ay * t**2 / 2 and y2 >= ty2:
                return True, ty2
    return False, None