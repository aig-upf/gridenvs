#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gridenvs.utils import Direction

class Key:
    arrow_left = 65361
    arrow_up = 65362
    arrow_right = 65363
    arrow_down = 65364

    keypad0 = 65456
    keypad1 = 65457
    keypad2 = 65458
    keypad3 = 65459
    keypad4 = 65460
    keypad5 = 65461
    keypad6 = 65462
    keypad7 = 65463
    keypad8 = 65464
    keypad9 = 65465

    enter = 65293
    esc = 65307
    space = 32

    @staticmethod
    def get_char_key(char):
        return ord(char)

class Controls:
    #Provides maps key->action
    Arrows = {
        Key.arrow_left: Direction.W,
        Key.arrow_right: Direction.E,
        Key.arrow_down: Direction.S,
        Key.arrow_up: Direction.N,
        Key.space: None #Noop
    }
    KeyPad = {
        Key.keypad0: None, #Noop
        Key.keypad1: Direction.SW,
        Key.keypad2: Direction.S,
        Key.keypad3: Direction.SE,
        Key.keypad4: Direction.W,
        Key.keypad5: None, #Noop
        Key.keypad6: Direction.E,
        Key.keypad7: Direction.NW,
        Key.keypad8: Direction.N,
        Key.keypad9: Direction.NE
    }
