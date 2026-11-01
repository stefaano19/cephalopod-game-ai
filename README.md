# Cephalopod Game

A Python implementation of a two-player Cephalopod-style board game, with a Tkinter GUI and several interchangeable move-selection strategies.

## Requirements and launch

- Python 3
- Tkinter (included with many Python distributions; some Linux installations package it separately)

From the repository root, run:

```bash
python3 CephalopodGame.py
```

The GUI prompts for a mode (human vs. human, human vs. AI, or AI vs. AI) and the first player. Human-vs-AI mode also asks which side is human. An AI move has a three-second timeout; if it expires, the game chooses a random legal move.

## Rules implemented

- The default board is 5×5. Blue moves first by default.
- A turn places a piece in an empty square. A normal placement has value 1.
- The engine examines the orthogonally adjacent occupied squares. If any subset of at least two adjacent pieces sums to between 2 and 6, each valid subset is offered as a capture move: the placed piece has the subset's sum as its value, and the selected pieces are removed. A normal placement is offered only when there are no valid capture subsets.
- The game ends when the board is full. The utility function is defined from Blue's perspective: it returns 1 when Blue occupies more squares than Red, and −1 otherwise (including a tie).

The GUI lets a human select a capture subset, review previous and subsequent positions, and step through or automatically play AI-vs-AI games.

## Strategies and AI

The strategy interface is `playerStrategy(game, state)`, which returns a move shaped like `((row, column), value, captured_positions)`.

The GUI currently assigns `playerBruniBruscoRomeo.playerStrategy` to Blue and `playerGemini.playerStrategy` to Red. Both use depth-limited alpha-beta search with a cutoff depth of 4 and hand-written position evaluators. Their evaluation code includes terms for piece values, center control, capture potential, and vulnerability. These are classical game-tree search and heuristic strategies, not machine-learning models.

Other included strategies are:

- `playerChat`: depth-limited alpha-beta search with a hand-written evaluator (cutoff depth 4).
- `playerEuristica0`: alpha-beta search with an evaluator that currently returns a constant zero (cutoff depth 5).
- `playerExampleRandom.py`: chooses a random legal move.

There is no tournament runner, benchmark report, or automated agent evaluation in the repository. AI-vs-AI play in the GUI is for observation, not a reproducible performance benchmark.

## Repository layout

| Path | Purpose |
| --- | --- |
| `CephalopodGame.py` | Game rules, board state, Tkinter UI, and game loop |
| `playerBruniBruscoRomeo/` | Blue strategy and alpha-beta search/evaluation code |
| `playerGemini/` | Red strategy and alpha-beta search/evaluation code |
| `playerChat/` | Additional alpha-beta strategy and evaluation code |
| `playerEuristica0/` | Additional alpha-beta strategy and evaluation code |
| `playerExampleRandom.py` | Random-move example strategy |

## Limitations

- Search is depth-limited and depends on hand-authored heuristics. There is no training pipeline, learned model, or measured playing-strength claim.
- Some heuristic helpers do not match the game's `"Blue"`/`"Red"` player labels or placement-based capture rules, so their scores are not validated strategic evaluations.
- The game utility treats a tie as a loss for Blue, while the AI-vs-AI completion dialog reports equal piece counts as a draw.
- No automated tests or reproducible benchmark procedure are included.

## Authorship and license

The repository does not include explicit authorship or license documentation. Confirm attribution and licensing before redistributing or presenting the project publicly.
