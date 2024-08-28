# Hashi Game with AI

Welcome to the Hashi Game with AI, a Python-based implementation of the traditional Hashi (bridges) puzzle, transformed into an engaging game where players compete against an advanced AI opponent.

## Overview of Hashi

In the traditional Hashi puzzle, the goal is to connect a series of islands (represented as circles with numbers) with bridges so that the number of bridges connected to each island equals the number on the island. Bridges must be straight lines, can run only horizontally or vertically, and may not cross other bridges or islands.

However, this project is not a straightforward Hashi puzzle but a gamified version where each move not only advances the state of the game but also influences the scores of both the player and the AI.

## Game Rules

1. **Building Bridges**: Players can build a bridge between two eligible islands by entering the labels of the islands separated by a space, e.g., `A B`.
2. **Setting Island Numbers**: Some islands do not initially have numbers. Players (or the AI) can assign a number (either 3 or 4) to these islands during their turn. The format for this action is `IslandLabel Number`, e.g., `C 3`.

### Scoring

- After each move, if the total number of bridges connected to an island becomes equal to its labeled number `n`, the player making the move earns `n` points and the opponent loses `n` points.
- Points from an island are awarded only once, but a single move can score points from both islands if it results in both islands satisfying their bridge conditions.

## Starting the Game

To launch the game, use the following command:

```bash
python main.py
```

You can also specify a particular map to play by providing its number as a positional argument. For example, to play on map 8:

```bash
python main.py 8
```

By default, the player starts first. However, if you prefer the AI to start, use the --start-second or -s flag:

```bash
python main.py --start-second
```

## Maps

The game maps are stored under the maps directory. Each map is a different level that you can select at the start of the game.

## Winning the Game

The game ends when all possible bridges are built or when no further actions are possible. The player with the higher score at the end of the game wins.

## Dependencies

Ensure you have Python installed on your system to run this game. No additional libraries are required for the basic functionality.
