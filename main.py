#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sChecker.spell_checker as spell
import readline

class color:
    END = '\033[0m'
    COW = '\033[0;33m'
    MIW = '\033[0;91m'


while True:
    try:
        _word = input("Enter the word >> ")
        word = spell.words(_word)
        c_word = spell.correct(_word)
        if (_word == c_word):
            print("Correct Word : "+color.COW+c_word+color.END)
        else:
            print("Did you mean : "+color.COW+c_word+color.END+" ?? instead of "+color.MIW+_word+color.END)

    except KeyboardInterrupt:
        break
