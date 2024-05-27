# wordsearch
## Too lazy to solve cereal box wordsearch puzzles....
- Wordsearch builder and solver


### Command Line

#### Builder

> ./builder --size [num cols] --words [location of word list text file] --save [optional. save results to file]

#### Solver

> ./solver --board [location of board text file] --words [location of word list text file] --save [optional. save results to file]

### Builder Class

```
from wordsearch import wordsearch

b = wordfinder.Board(col_size_num)
b.load_words(word_list.txt)
b.populate()
b.show_board()
b.show_word_list()
b.show_answer()'
b.save()
```

### Solver Class

```
from wordsearch import wordsearch

b = wordfinder.WordFinder(board.txt, word_list.txt)
b.find_list()
b.show_answer()
b.save()
```
