<h1>Search: Hua Rong Dao</h1>

The puzzle board is four spaces wide and five spaces tall.
We will consider the variants of this puzzle with ten pieces. 
There are four kinds of pieces:

One 2x2 piece.
Five 1x2 pieces. Each 1x2 piece is either placed horizontally or vertically. 
Four 1x1 pieces.
Once we place the ten pieces on the board, two empty spaces should remain.

The goal is to move the pieces until the 2x2 piece is above the bottom opening (i.e. helping Cao Cao escape through the Hua Rong Dao/Pass). You may move each piece horizontally or vertically only, into an available space. You are not allowed to rotate any piece or move it diagonally.

There are many other initial configurations for this puzzle. Check out this Chinese Wikipedia page Links to an external site. for 32 initial configurations. The link below each configuration opens another page where you can play the puzzle and see the solution.

Counting Moves: The consecutive moves are counted separately.
 
Two Heuristic Functions for A* Search
If we need to implement A* search to find an optimal solution, we need to provide it with an admissible heuristic function.

Using the most naive heuristic, we implemented the Manhattan distance heuristic, the simplest admissible heuristic function for this problem. Suppose that we relax the problem such that the pieces can overlap. Given this relaxation, we can solve the puzzle by moving the 2x2 piece over the other pieces towards the goal.

Next, we propose another advanced heuristic function that is admissible but dominates the Manhattan distance heuristic. Implement this heuristic function. Explain why this heuristic function is admissible and dominates the Manhattan distance heuristic.

Two files:

hrd.py the Python program and advanced.pdf contains a description of the advanced heuristic function.

    python3 hrd.py  <input file>  <DFS output file>  <A* output file>
    
The command specifies one plain text input file and the two plain text output files containing the solutions found by DFS and A* for the puzzle.

For example, if we run the following command for puzzle, specified in a file called puzzle.txt:

    python3 hrd.py puzzle.txt puzzle_sol_dfs.txt puzzle_sol_astar.txt
    
The DFS solution will be found in puzzle_sol_dfs.txt and the A* solution will be found in puzzle_sol_astar.txt

Input Format
The input to the program is a plain text file that stores an initial Hua Rong Dao puzzle configuration. See below for an example of the input file content. It contains 20 digits arranged in 5 rows and 4 digits per row, representing the initial configuration of the puzzle. The empty squares are denoted by 0. The single pieces are denoted by 7. The 2x2 piece is denoted by 1. The 5 1x2 pieces are denoted by one of {2, 3, 4, 5, 6}, but the numbers are assigned at random.

2113
2113
4665
4775
7007
 
Output Format
The two output files should store the DFS and A* solution for the input file provided.

See below for an example of the content of the output file. On the first line, print the cost of the solution. Next, print the sequence of states from the initial configuration to a goal state. Two consecutive states are separated by an empty line. The empty squares are denoted by 0. The single pieces are denoted by 4. The 2x2 piece is denoted by 1. The horizontal 1x2 pieces are denoted by 2. The vertical 1x2 pieces are denoted by 3.  Due to limited space, only the beginning of the output file is shown below. 

Make sure that your output files match this format exactly. 

Cost of the solution: 116
3113
3113
3223
3443
4004

3113
3113
3223
3443
0404

3113
3113
3223
3443
0440
