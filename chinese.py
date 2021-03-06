from tkinter import messagebox
from typing import List, Dict, Tuple
from tkinter import *
import random
import tkinter
import io
import json

FONT_SIZE = 160
FILE = "data.json"

class Character:
    _character: str
    _pinyin: str
    count: int
    incorrect: int

    def __init__(self, char: str, pinyin: str) -> None:
        self.character = char
        self.pinyin = pinyin
        self.count = 0
        self.incorrect = 0

    def __eq__(self, other):
        if (self.character == other.character and
                self.pinyin == other.pinyin):
            return True
        return False

    def get_chars(self):
        return self.character

    def get_str(self):
        return self.pinyin

    def wrong(self):
        self.incorrect += 1
        self.count += 1

    def correct(self):
        self.count += 1


class Word:
    characters: List[Character]

    def __init__(self, characters: List[Character]) -> None:
        self.characters = characters

    def add_character(self, character: Character):
        self.characters.append(character)

    def __repr__(self):
        s = ""
        for x in self.characters:
            s += x.get_str() + " "
        return s[:-1]

    def get_chars(self):
        s = ""
        for x in self.characters:
            s += x.get_chars()
        return s

    def get_str(self):
        s = ""
        for x in self.characters:
            s += x.get_str() + " "
        return s[:-1]

    def wrong(self):
        for x in self.characters:
            x.wrong()

    def correct(self):
        for x in self.characters:
            x.correct()


def load_data(file_name: str) -> Dict[str, List[Character]]:
    return {}


def close(root: Tk, chars: List, file_name: str,):

    with open(file_name, "w") as outfile:
        for x in chars:
            if type(x) == Word:
                for y in x.characters:
                    c = {"character": y.get_chars(),
                         "pinyin": y.get_str(),
                         "incorrect": y.incorrect,
                         "count": y.count}
                    json.dump(c, outfile)
            else:
                c = {"character": x.get_chars(),
                     "pinyin": x.get_str(),
                     "incorrect": x.incorrect,
                     "count": x.count}
                json.dump(c, outfile)
    print("exit")
    root.destroy()


def open_file(char_file: str, word_file: str, start: int, end: int) -> \
        Tuple[Dict[str, List[Character]], List[Word]]:
    char_d = load_data(FILE)
    word_l = []
    with io.open(char_file,'r', encoding='utf-8') as cf, io.open(word_file, 'r', encoding='utf-8') as wf:
        chars = cf.readlines()[0].split()
        words = wf.readlines()[0].lower().split(",")
        for x in range(start, min(end, len(chars))):
            word = words[x].split()
            word_l.append(Word([]))
            for y in range(len(chars[x])):
                c = Character(chars[x][y], word[y])
                if c.pinyin in char_d:
                    _add_to_dict(char_d, c)
                    for z in char_d[word[y]]:
                        if z == c:
                            word_l[x-start].add_character(z)
                else:
                    char_d[c.pinyin] = [c]
                    word_l[x-start].add_character(c)
    return char_d, word_l


def _add_to_dict(d: Dict, c: Character) -> None:
    if c.pinyin in d:
        add = True
        for z in d[c.pinyin]:
            if c == z:
                add = False
        if add:
            d[c.pinyin].append(c)


def random_list(start: int, end: int) -> List[int]:
    rand_l = []
    for x in range(start, end):
        rand_l.append(x)
    # random.shuffle(rand_l)
    return rand_l


def get_chars(char: Dict):
    chars = []
    for x in char:
        for y in char[x]:
            chars.append(y)
    return chars


def next(i: IntVar, amount: int ,max_val: int) -> None:
    if i.get() + amount > max_val:
        i.set(0)
    elif i.get() + amount < 0:
        i.set(max_val)
    else:
        i.set(i.get() + amount)


def update_text(c_text: StringVar, p_text: StringVar, show_c: IntVar,
                show_p: IntVar, char: Character) -> None:
    if show_c.get():
        c_text.set(char.get_chars())
    else:
        c_text.set("")
    if show_p.get():
        p_text.set(char.get_str())
    else:
        p_text.set("")
    if show_c.get() and show_p.get():
        print(char.get_chars(), char.get_str())


def review_words(chars: List) -> None:
    root = tkinter.Tk()
    root.geometry(str(int(5.2*FONT_SIZE))+'x'+str(int(2.1*FONT_SIZE)))
    button_frame = Frame(root)
    rand_l = random_list(0, len(chars))
    index = tkinter.IntVar(value=0)
    c_text = tkinter.StringVar(value="")
    p_text = tkinter.StringVar(value="")
    show_c = tkinter.IntVar(value=1)
    show_p = tkinter.IntVar(value=1)
    update_text(c_text, p_text, show_c, show_p, chars[rand_l[index.get()]])
    char_label = Label(root,textvariable=c_text, font=("KaiTi", FONT_SIZE))
    pinyin_label = Label(root,textvariable=p_text, font=("Calibri", int(FONT_SIZE/4)))
    back_b = Button(button_frame,text='Back', command=lambda:[
        next(index, -1, len(chars)-1),
        update_text(c_text, p_text, show_c, show_p, chars[rand_l[index.get()]])
    ])
    next_b = Button(button_frame,text='Next', command=lambda:[
        next(index, 1, len(chars)-1),
        update_text(c_text, p_text, show_c, show_p, chars[rand_l[index.get()]]),
    ])
    incorrect_b = Button(button_frame,text='Incorrect', command=lambda:[
        chars[rand_l[index.get()]].wrong(),
        next(index, -1, len(chars)-1),
        update_text(c_text, p_text, show_c, show_p, chars[rand_l[index.get()]])
    ])
    correct_b = Button(button_frame,text='Correct', command=lambda:[
        chars[rand_l[index.get()]].correct(),
        next(index, -1, len(chars)-1),
        update_text(c_text, p_text, show_c, show_p, chars[rand_l[index.get()]])
    ])
    exit_b = Button(button_frame,text='Exit', command=lambda:[
        close(root, chars, FILE)])
    show_char = Checkbutton(button_frame, text='Show Characters', variable=show_c,
            command=lambda:[update_text(c_text, p_text, show_c, show_p,
                                        chars[rand_l[index.get()]])])
    show_str = Checkbutton(button_frame, text='Show PinYin', variable=show_p,
            command=lambda:[update_text(c_text, p_text, show_c, show_p,
                                        chars[rand_l[index.get()]])])
    char_label.pack()
    pinyin_label.pack()
    back_b.pack(side=LEFT)
    next_b.pack(side=LEFT)
    incorrect_b.pack(side=LEFT)
    correct_b.pack(side=LEFT)
    show_char.pack(side=LEFT)
    show_str.pack(side=LEFT)
    exit_b.pack(side=LEFT)
    button_frame.pack(side=BOTTOM)
    root.mainloop()


if __name__ == '__main__':
    c, w = open_file('characters.txt', 'words.txt',0, 250)
    review_words(w)
    # review_words(get_chars(c))

