#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sChecker.spell_checker as spell
import readline
import Tokenizer as tkr
class color:
    END = '\033[0m'
    COW = '\033[0;33m'
    MIW = '\033[0;91m'

while True:
    try:
        _input = input("You >> ")
        c_list = []

        #_word = input("Enter the word >> ")
        _list = tkr.tokenize(_input)

        for _word in _list:
            #word = spell.words(_word)
            c_word = spell.correct(_word)
            c_list.append(c_word)
            
        for i in range(len(c_list)-1):
            print('\t'+color.MIW+_list[i]+color.END+' -> '+color.COW+c_list[i]+color.END)

        print('')


        #if (_word == c_word):
            #print("Correct Word : "+color.COW+c_word+color.END)
        #else:
            #print("Did you mean : "+color.COW+c_word+color.END+" ?? instead of "+color.MIW+_word+color.END)

    except KeyboardInterrupt:
        break

    except:
        print('Unexpected Error Occured')

