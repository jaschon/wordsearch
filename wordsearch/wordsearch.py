#!/usr/bin/env python3

"""Wordsearch Generator and Solver"""

import random
import string
import os

class Board:
    """Wordsearch Board"""

    choices = ('h','v','dr','du','dl')
    tries = 300

    def __init__(self, size: int = 15) -> None:
        """Build boards"""
        self.missing = []
        self.word_list = []
        self._board_setup(size)

    def _build(self, wsize: int, hsize: int) -> list:
        """Build empty board"""
        return [["_" for _ in range(wsize)] for _ in range(hsize)]

    def _board_setup(self, size: int) -> None:
        """Build empty boards"""
        self.answer = self._build(size, size)
        self.board = self._build(size, size)

    def _show(self, board: list) -> str:
        """Show boards"""
        return "\n".join(" ".join(r) for r in board)

    def _show_words(self, wordlist: list) -> str:
        return "\n".join([w.title().strip() for w in wordlist])

    def _make_word_list(self, words: list) -> list:
        return [w.strip().lower() for w in words if w.strip()]

    def _add_word_list(self, word: str) -> bool:
        if word and not word in self.word_list:
            self.word_list.append(word)
            return True
        return False

    def _add_direction(self, x: int, y: int, direction: str, offset: int) -> tuple:
        match direction:
            case 'du':
                x += offset 
                y -= offset
            case 'dl':
                x -= offset
                y += offset
            case 'dr':
                x += offset
                y += offset
            case 'v':
                y += offset
            case 'h' | _:
                x += offset
        return (x,y)

    def _random_xy(self, s: str, direction: str) -> tuple:
        try:
            match direction:
                case 'du':
                    x = random.randrange(0, len(self.answer) - len(s)+1)
                    y = random.randrange(len(s)-1, len(self.answer))
                case 'dl':
                    x = random.randrange(len(s)-1, len(self.answer))
                    y = random.randrange(0, len(self.answer)-len(s)+1)
                case 'dr':
                    x = random.randrange(0, len(self.answer) - len(s)+1)
                    y = random.randrange(0, len(self.answer) - len(s)+1)
                case 'v':
                    x = random.randrange(0, len(self.answer))
                    y = random.randrange(0, len(self.answer) - len(s)+1)
                case 'h' | _:
                    x = random.randrange(0, len(self.answer) - len(s)+1)
                    y = random.randrange(0, len(self.answer))
            return (x, y, True)
        except ValueError as e:
            return (-1,-1, False)

    def fits(self, s: str, x: int, y: int, direction: str, board: list = []) -> bool:
        """Check if word will fit in position"""
        try:
            board = board if board else self.answer
            for l in s:
                if x < 0 or y < 0: return False
                if board[y][x] != "_" and board[y][x] != l.upper():
                    return False
                x, y = self._add_direction(x, y, direction, 1)
            return True
        except IndexError:
            return False

    def add_word(self, s: str, x : int, y: int, direction: str) -> bool:
        """Add word to position"""
        try:
            for l in s:
                if x < 0 or y < 0: return False
                self.answer[y][x] = l.upper()
                x, y = self._add_direction(x, y, direction, 1)
            return True
        except IndexError:
            return False

    def add(self, s:str) -> bool:
        """Try to add a word in a random direction"""
        count = 0
        if len(s) > len(self.answer): return False
        while count < self.tries:
            count += 1
            direction = random.choice(self.choices)
            try:
                x, y, status = self._random_xy(s, direction)
                if not status: return False 
                if self.fits(s, x, y, direction, self.answer):
                    return self.add_word(s, x, y, direction)
            except (IndexError, ValueError):
                return False
        return False

    def fill(self) -> None:
        """Fill blank areas with random characters"""
        for r in range(len(self.answer)):
            for c in range(len(self.answer[0])):
                if self.answer[r][c] == "_":
                    self.board[r][c] = random.choice(string.ascii_uppercase)
                else:
                    self.board[r][c] = self.answer[r][c]

    def populate(self, words: list = []) -> None:
        """Populate board with a list of words"""
        words = self.word_list if not words else words
        for word in words:
            if not self.add(word):
                self.missing.append(word)
        if self.missing:
            return False
        self.fill()
        return True

    def load_words(self, filename: str) -> bool:
        """Load a list of words from a text file and populate board"""
        try:
            with open(os.path.abspath(filename), 'r') as fs:
                self.word_list = self._make_word_list(fs.readlines())
        except OSError as e:
            print(e)
            return False
        return True

    def show_board(self) -> None:
        """Show board"""
        print(self._show(self.board))

    def show_answer(self) -> None:
        """Show answer"""
        print(self._show(self.answer))

    def show_word_list(self) -> None:
        print(self._show_words(self.word_list))

    def save(self) -> bool:
        """Save board to text file"""
        try:
            directory = os.path.expanduser("~/Desktop")
            with open(os.path.join(directory, "board.txt"), 'w') as fs:
                    fs.write(self._show(self.board))
            with open(os.path.join(directory, "answers.txt"), 'w') as fs:
                    fs.write(self._show(self.answers))
            with open(os.path.join(directory, "words.txt"), 'w') as fs:
                fs.write(self._show_words(self.word_list))
        except OSError as e:
            print(e)
            return False
        return True


class WordFinder(Board):

    def __init__(self, filename: str = "", wordlist: str = "")  -> None:
        """Wordfinder"""
        self.missing = []
        self.word_list = []
        self.answer = []
        self.board = []
        if filename and wordlist:
            self.load_board(filename)
            self.load_words(wordlist)

    def _clean_board(self, board: list) -> list:
        """Clean loaded board"""
        return [list(r.replace(" ", "").strip().upper()) for r in board if r.strip()]

    def load_board(self, filename: str) -> None:
        """Load a premade board"""
        try:
            with open(os.path.abspath(filename), 'r') as fs:
                self.board = self._clean_board(fs.readlines())
            self.answer = self._build(len(self.board[0]), len(self.board))
        except OSError as e:
            print(e)

    def find(self, word: str) -> bool:
        """Search for start of word, then check if it matches"""
        word = word.upper()
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] == word[0]:
                    for d in self.choices:
                        if self.fits(word, x, y, d, self.board):
                            return self.add_word(word, x, y, d)
        return False

    def find_list(self) -> None:
        """Search word list and find matches"""
        for word in self.word_list:
            if not self.find(word):
                self.missing.append(word)
        print(self.missing)
        return len(self.missing) == 0

if __name__ == "__main__":
    pass
