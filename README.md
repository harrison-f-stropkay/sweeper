# Sweeper
 
`Field` is the parent class of both `Minefield` and `Gamefield`. `Minesweeper` combines `Minefield` and `Gamefield` to emulate the game mechanics of first-release Minesweeper, including initial guess bomb replacement to the first eligible northwest tile.

An `outside_edge` is the collection of neighboring hidden tiles that borders a region of flipped tiles. Overlapping `outside_edges` are combined into a single `outside_edge`. An `inside_edge` is the collection of flipped tiles that forms the inside perimeter of a flipped region. 

In linear time, `Sweeper` first finds all tiles guaranteed to be bomb or non-bomb by assessing the neighbors of all `inside_edge` tiles. If none are found, it then recursively backtracks through each `outside_edge` to discover all possible bomb configurations. `Sweeper` uses that information efficiently (instead of storing all of these configurations, it simply keeps a tally of the number of times each tile is configured as a bomb) to find the bomb probability of each `outside_edge` tile. It then finds the expected number of bombs in all of the `outside_edges` to calculate bomb probabilities for the remaining hidden tiles. This algorithm runs in exponential time, which is the best we can do for now because [Minesweeper has been shown to be NP-Complete](http://www.minesweeper.info/articles/MinesweeperIsNPComplete.pdf). 

`Sweeper` wins roughly 90% of games on beginner difficulty, 70% on intermediate, and 30% on expert. 30% might seem low, but a quick back-of-the-envelope analysis showed that the average expert game contains about 4.62 probabilistic moves, 0.32 of which are performed with 50% confidence (meaning that a sixth of all games are lost because of unavoidable 50-50 guesses). Also, the results for each game difficulty are quite close to those yielded by the strategy in [this paper](https://minesweepergame.com/math/algorithmic-approaches-to-playing-minesweeper-2015.pdf).

One future improvement could be to stop outside edge recursion when a guaranteed tile is discovered. This would forfeit the advantage of finding multiple guaranteed tiles in a single function call, but in many conditions, it would halt the recursion's exponential growth. To do so, `Sweeper` should find outside edge tiles with DFS (to ensure that later recursion descends through neighboring tiles in order) and assess outside edges with BFS (to exhaust all configurations for each tile as quickly as possible). 

To run `Sweeper`, simply run `driver.py`. The `play` function in MinesweeperCLI returns the truth value of whether the game was won, so you can turn on `autoplay` to test `Sweeper`'s performance over multiple games, if you'd like. In the first example below, we use `Sweeper` to help win a beginner-level game (we enter no guess to let `Sweeper` guess for us). In the second, we see `Sweeper` take on an expert-level game.  


https://user-images.githubusercontent.com/109109392/220002674-638d86df-3bee-4486-9566-a011c6854500.mov


https://user-images.githubusercontent.com/109109392/220002693-5a138559-75c2-485f-a0aa-6d70894940cb.mp4

