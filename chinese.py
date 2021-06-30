from typing import List, Dict
import random
import io
import tkinter
from tkinter import *

FONT_SIZE = 160

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


def test(char_file: str, word_file: str, char_label: StringVar):
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
                char_label.set(chars[ran_char[index]])
                print(chars[ran_char[index]])
                i = input()
                print(words[ran_char[index]])
            else:
                # random word
                print(words[ran_word[index]])
                i = input()
                print(chars[ran_word[index]])
            index += 1


def review_individual(char: Dict, char_label: StringVar):
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
            char_label.set(chars[ran_char[index]].character)
            print(chars[ran_char[index]].character)
            # i = input()
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


def get_chars(char: Dict):
    chars = []
    for x in char:
        for y in char[x]:
            chars.append(y)
    return chars


def gui_individual(chars: List[Character]):
    root = tkinter.Tk()
    root.geometry(str(int(1.5*FONT_SIZE))+'x'+str(int(1.5*FONT_SIZE)))
    i = tkinter.IntVar(value = 0)
    ran_char = random_list(0, len(chars))
    text = tkinter.StringVar(value="")
    char_label = Label(root,textvariable=text, font = ("KaiTi", FONT_SIZE))
    next = Button(root, text = "next",
                  command = lambda:[text.set(chars[ran_char[i.get()]].character),
                                    print(chars[ran_char[i.get()]].character),
                                    print(chars[ran_char[i.get()]].pinyin),
                                    i.set(i.get() + 1)])
    char_label.pack()
    next.pack()
    root.mainloop()


if __name__ == '__main__':
    gui_individual(get_chars(open_file('characters.txt', 'words.txt',0)))
    # test('characters.txt', 'words.txt', text)

