# py-sudoku

A sudoku solver implemented in Python.

(This program requires the *numpy* numeric library.)

How to run the program
----------------------

```
python sudoku.py
```

Available commands
------------------

- `set [row] [column] [value]`: Set the value in row *[row]*, column *[column]* to *[value]*. (All values are in range [1, 9].)
- `unset [row] [column]`: Set the value in row *[row]*, column *[column]* to unknown. (All values are in range [1, 9].)
- `clear`: Removes all values from the Sudoku grid.
- `foo`: Loads a pre-filled Sudoku grid that is very hard to solve. (For testing the algorithm.)
- `solve`: Solve the Sudoku grid.
- `exit`: Exit the program and return to the operating system shell.

