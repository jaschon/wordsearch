#!/usr/bin/env python3

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from wordsearch import wordsearch

class TestBoard:
    """Test setup"""

    @pytest.mark.parametrize("size",[20,1,100])
    def test_setup_board(self, size):
        """Test board grid size"""
        b = wordfinder.Board(size)
        assert len(b.answer) == size
        assert len(b.answer[0]) == size

    @pytest.mark.parametrize("size",[20,1,100])
    def test_setup_answer(self, size):
        """Test answer grid size"""
        b = wordfinder.Board(size)
        assert len(b.board) == size
        assert len(b.board[0]) == size

class TestFunctions:
    """Test helper functions"""

    @pytest.mark.parametrize(
    "board,string",[
        ([['a','b','c'],['d','e','f'],['g','h','i']], "a b c\nd e f\ng h i"),
        ([[],[],[]], "\n\n"),
    ])
    def test_show(self, board, string):
        b = wordfinder.Board(10)
        assert b._show(board) == string

    @pytest.mark.parametrize(
    "words,string",[
        (["lower", "MiXeD", " CAPS ", "    spaces  "], "Lower\nMixed\nCaps\nSpaces"),
        ([], ""),
    ])
    def test_show_words(self, words, string):
        b = wordfinder.Board(10)
        assert b._show_words(words) == string

    @pytest.mark.parametrize(
    "words,result",[
        (["lower", " ", "MiXeD", "   ", " CAPS ", "    spaces  "], \
                ["lower","mixed","caps","spaces"]),
        ([], []),
    ])
    def test_make_word_list(self, words, result):
        b = wordfinder.Board(10)
        assert b._make_word_list(words) == result

    @pytest.mark.parametrize(
    "add_before, word, status",[
        ([], "test", True),
        (["test"], "test", False),
        (["tester"], "test", True),
        ([], "", False),
    ])
    def test_add_word_list(self, add_before, word, status):
        b = wordfinder.Board(10)
        b.word_list = add_before
        assert b._add_word_list(word) == status

    @pytest.mark.parametrize(
    "x,y,direction,offset,xx,yy",[
        (1,1,'du',1,2,0), #du
        (1,1,'dl',1,0,2), #dl
        (1,1,'dr',1,2,2), #dr
        (1,1,'dr',2,3,3), #dr, diff offset
        (1,1,'v',1,1,2), #v
        (1,1,'h',1,2,1), #h
        (1,1,'',1,2,1), #fallback
    ])
    def test_add_direction(self, x, y, direction, offset, xx, yy):
        b = wordfinder.Board(10)
        xresult, yresult = b._add_direction(x, y, direction, offset)
        assert xresult == xx
        assert yresult == yy

    @pytest.mark.parametrize(
            "size,direction,word,fits",[
                (4,"h","test",True),
                (3,"h","test",False),
                (4,"v","test",True),
                (3,"v","test",False),
                (4,"dl","test",True),
                (3,"dl","test",False),
                (4,"dr","test",True),
                (3,"dr","test",False),
                (4,"du","test",True),
                (3,"du","test",False),
                ])
    def test_random_xy(self, size, direction, word, fits):
        b = wordfinder.Board(size)
        for i in range(80):
            x,y,status = b._random_xy(word, direction)
            assert status == fits
            assert b.fits(word, x, y, direction, b.answer) == fits

class TestFill:
    """Test random character fill"""

    def test_fill_no_words(self):
        """Test that all spots are filled"""
        b = wordfinder.Board(4)
        b.fill()
        for r in range(len(b.answer)):
            for c in range(len(b.answer[0])):
                assert b.board[r][c] != "_"

    @pytest.mark.parametrize("word", ["s", "test", "awesome", "reallylong"])
    def test_fill_word(self, word):
        """Test that word characters aren't touched"""
        b = wordfinder.Board(len(word))
        for r in range(len(word)):
            b.add_word(word, 0, r, "h")
        b.fill()
        for r in range(len(word)):
            for c in range(len(word)):
                assert b.board[r][c] == word[c].upper()


class TestWord:
    """Test word addition and fit"""

    @pytest.mark.parametrize(
    "x,y,direction,fits",
    [
        #h
        (-1,0,'h',False),
        (0,-1,'h',False),
        (0,0,'h',True),
        (0,9,'h',True),
        (0,10,'h',False),
        (6,0,'h',True),
        (7,0,'h',False),
        (10,0,'h',False),
        #v
        (0,-1,'v',False),
        (0,0,'v',True),
        (0,6,'v',True),
        (9,6,'v',True),
        (0,7,'v',False),
        (0,10,'v',False),
        #dr
        (-1,0,'dr',False),
        (0,0,'dr',True),
        (6,0,'dr',True),
        (0,6,'dr',True),
        (6,6,'dr',True),
        (6,7,'dr',False),
        (7,0,'dr',False),
        #dl
        (-1,0,'dl',False),
        (9,0,'dl',True),
        (9,6,'dl',True),
        (9,7,'dl',False),
        #du
        (-1,0,'du',False),
        (0,0,'du',False),
        (0,3,'du',True),
        (0,7,'du',True),
        (3,6,'du',True),
        (6,9,'du',True),
        (0,9,'du',True),
        (7,8,'du',False),
        (0,2,'du',False),
        (7,3,'du',False),

    ])
    def test_fits(self, x, y, direction, fits):
        """Test fits"""
        b = wordfinder.Board(10)
        assert fits == b.fits("test", x, y, direction)
        assert fits == b.add_word("test", x, y, direction)

    @pytest.mark.parametrize(
    "board, x,y,direction,fits",
    [
        ([['R','_','_','_'],['_','_','_','_'],['_','_','_','_'],['_','_','_','_']], \
                0, 0, 'h', False),
        ([['T','_','_','_'],['_','_','_','_'],['_','_','_','_'],['_','_','_','_']], \
                0, 0, 'h', True),
        ([['T','E','_','_'],['_','_','_','_'],['_','_','_','_'],['_','_','_','_']], \
                0, 0, 'h', True),
        ([['T','E','S','T'],['_','_','_','_'],['_','_','_','_'],['_','_','_','_']], \
                0, 0, 'h', True),
        ([['T','_','_','_'],['_','_','_','_'],['_','_','_','_'],['_','_','_','_']], \
                0, 0, 'v', True),
        ([['T','_','_','_'],['E','_','_','_'],['S','_','_','_'],['T','_','_','_']], \
                0, 0, 'v', True),
        ([['T','_','_','_'],['E','_','_','_'],['_','_','_','_'],['_','_','_','_']], \
                0, 0, 'v', True),
        ([['T','_','_','_'],['_','_','_','_'],['_','_','S','_'],['_','_','_','T']], \
                0, 0, 'dr', True),
        ([['T','_','_','_'],['_','R','_','_'],['_','_','S','_'],['_','_','_','_']], \
                0, 0, 'dr', False),
        ([['T','_','_','_'],['_','E','_','_'],['_','_','S','_'],['_','_','_','T']], \
                0, 0, 'dr', True),
        ([['_','_','_','T'],['_','_','_','_'],['_','_','_','_'],['_','_','_','_']], \
                3, 0, 'dl', True),
        ([['_','_','_','T'],['_','_','_','_'],['_','_','_','_'],['T','_','_','_']], \
                3, 0, 'dl', True),
        ([['_','_','_','T'],['_','_','R','_'],['_','_','_','_'],['T','_','_','_']], \
                3, 0, 'dl', False),
        ([['_','_','_','_'],['_','_','_','_'],['_','_','_','_'],['T','_','_','_']], \
                0, 3, 'du', True),
        ([['_','_','_','R'],['_','_','_','_'],['_','_','_','_'],['T','_','_','_']], \
                0, 3, 'du', False),
        ([['_','_','_','T'],['_','_','S','_'],['_','E','_','_'],['T','_','_','_']], \
                0, 3, 'du', True),
    ])
    def test_fits_letter_match(self, board, x, y, direction, fits):
        """Test fit with matching letters"""
        b = wordfinder.Board(10)
        b.answer = board
        assert fits == b.fits("test", x, y, direction)

    @pytest.mark.parametrize("words,errors,status",
    [
        (["test","time",],[],True),
        (["test","time", "orange",],["orange",],False),
    ])
    def test_populate(self, words, errors, status):
        """Test populate"""
        b = wordfinder.Board(4)
        assert b.populate(words) == status
        assert b.missing == errors

    @pytest.mark.parametrize("word,tries,status",
    [
        ("orange", 5, False),
        ("test", -1, False),
        ("test", 5, True),
    ])
    def test_add(self, word, tries, status):
        """Test add"""
        b = wordfinder.Board(4)
        b.tries = tries
        assert b.add(word) == status


class TestFinder:
    """Test word finder"""

    @pytest.mark.parametrize(
    "board, result",
    [
        ([""," A    B    c","","DEf","","","gh     i",""],\
                [["A","B","C"],["D","E","F"],["G","H","I"]]),
    ])
    def test_clean_board(self, board, result):
        """Test board cleaning"""
        b = wordfinder.WordFinder()
        assert b._clean_board(board) == result

    @pytest.mark.parametrize(
    "board, word, status",
    [
        ([['T','E','S','T'],['Q','W','E','R'],['A','S','D','F'],['Q','Z','N','C']], \
                "test", True), #h
        ([['T','R','S','T'],['E','W','E','R'],['S','S','D','F'],['T','Z','N','C']], \
                "test", True), #v
        ([['T','R','S','T'],['Y','E','E','R'],['X','S','S','F'],['M','Z','N','T']], \
                "test", True), #dr
        ([['P','R','S','T'],['Y','E','E','R'],['X','S','S','F'],['T','Z','N','I']], \
                "test", True), #dl
        ([['P','R','S','T'],['Y','E','S','R'],['X','E','S','F'],['T','Z','N','I']], \
                "test", True), #du
        ([['P','R','S','T'],['Y','E','S','R'],['X','E','S','F'],['T','Z','N','I']], \
                "blue", False), #fail
    ])
    def test_find(self, board, word, status):
        """Test find"""
        b = wordfinder.WordFinder()
        b._board_setup(4)
        b.board = board
        assert b.find(word) == status

    @pytest.mark.parametrize(
    "board, words, errors, status",
    [
        ([['T','E','S','T'],['B','L','U','E'],['T','I','M','E'],['Q','Z','N','C']], \
                ("test", "blue", "time") , [], True), #h
        ([['T','E','S','T'],['B','L','U','E'],['T','I','M','E'],['Q','Z','N','C']], \
                ("test", "orange", "blue", "time") , ["orange",], False), #h fail
        ([['T','B','S','T'],['E','L','U','I'],['S','U','M','M'],['T','E','N','E']], \
                ("test", "blue", "time") , [], True), #v
        ([['T','B','S','T'],['E','L','U','I'],['S','U','M','M'],['T','E','N','E']], \
                ("test", "blue", "time", "orange", "yell") , ["orange", "yell"], False), #v fail
    ])
    def test_find_list(self, board, words, errors, status):
        """Test find list"""
        b = wordfinder.WordFinder()
        b._board_setup(4)
        b.board = board
        b.word_list = words
        assert b.find_list() == status
        assert b.missing == errors

