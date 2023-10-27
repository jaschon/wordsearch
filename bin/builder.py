#!/usr/bin/env python3
"""Build Wordsearch Games"""

import argparse
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from wordfinder import wordfinder

def main(args):
    b = wordfinder.Board(args.size)
    if b.load_words(os.path.expanduser(args.words)):
        if b.populate():
            print()
            b.show_board()
            print()
            b.show_word_list()
            print()
            b.show_answer()
            print()
            if args.save:
                b.save()
        else:
            print("OOPS!, Not able to add all the words!") 
            print("\t", ", ".join(b.missing))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wordsearch Solver")
    parser.add_argument('--size', action="store", type=int, required=True, help="Board Size")
    parser.add_argument('--words', action="store", required=True, help="Word List File")
    parser.add_argument('--save', action="store_true", required=False, help="Save Results to File")
    main(parser.parse_args())
