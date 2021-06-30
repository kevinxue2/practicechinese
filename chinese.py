from typing import List, Dict
import random
import io
import tkinter
from tkinter import *


class Character:
    character: str
    pinyin: str

    def __init__(self, char: str, pinyin: str) -> None:
        self.character = char
        self.pinyin = pinyin

    def __eq__(self, other):
        if (self.character == other.character and
                self.pinyin == other.pinyin):
            return True
        return False


class Word:
    characters: List[Character]

    def __init__(self, characters: List[Character]) -> None:
        self.characters = characters

    def __str__(self):
        s = ""
        for x in self.characters:
            s += x.pinyin + " "
        return s[:-1]


def open_file(char_file: str, word_file: str, start: int):
    char_d = {}
    with io.open(char_file,'r', encoding='utf-8') as cf, io.open(word_file, 'r', encoding='utf-8') as wf:
        chars = cf.readlines()[0].split()
        words = wf.readlines()[0].lower().split(",")
        for x in range(start, len(chars)):
            word = words[x].split()
            for y in range(len(chars[x])):
                c = Character(chars[x][y], word[y])
                if c.pinyin in char_d:
                    _add_to_dict(char_d, c)
                else:
                    char_d[c.pinyin] = [c]
    return char_d


def _add_to_dict(d: Dict, c: Character) -> None:
    if c.pinyin in d:
        add = True
        for z in d[c.pinyin]:
            if c == z:
                add = False
        if add:
            d[c.pinyin].append(c)


def test(char_file: str, word_file: str):
    run = True
    with io.open(char_file,'r', encoding='utf-8') as cf, io.open(word_file, 'r', encoding='utf-8') as wf:
        chars = cf.readlines()[0].split()
        words = wf.readlines()[0].split(",")
        start = 0

        n = len(chars)
        ran_char = random_list(start, n)
        ran_word = random_list(start, n)
        index = 0
        print(n)
        while run and index < n-start:
            rand = 0
            if rand:
                # random character
                print(chars[ran_char[index]])
                i = input()
                print(words[ran_char[index]])
            else:
                # random word
                print(words[ran_word[index]])
                i = input()
                print(chars[ran_word[index]])
            index += 1


def review_individual(char: Dict):
    run = True
    chars = []
    for x in char:
        for y in char[x]:
            chars.append(y)
    n = len(chars)
    ran_char = random_list(0, n)
    ran_word = random_list(0, n)
    index = 0
    while run and index < n:
        rand = 1
        if rand:
            # random character
            print(chars[ran_char[index]].character)
            i = input()
            print(chars[ran_char[index]].pinyin)

        else:
            # random word
            print(chars[ran_word[index]].pinyin)
            i = input()
            print(chars[ran_word[index]].character)
        index += 1


def random_list(start: int, end: int) -> list:
    l = []
    for x in range(start, end):
        l.append(x)
    random.shuffle(l)
    return l

# def run_gui():
#     print('r')
#     root = tkinter.Tk()
#     next = Button(root, text = "hello")
#     next.pack()
#     root.mainloop()


if __name__ == '__main__':
    # run_gui()
    review_individual(open_file('characters.txt', 'words.txt',0))
    # test('characters.txt', 'words.txt')
