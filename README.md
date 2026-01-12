# Snake Game

A classic Snake game built with PyGame and OpenGL featuring three difficulty modes.

## Features

- **3 Game Modes:**
  - **Original Mode** (Grey snake): Standard difficulty with constant speed
  - **Hard Mode** (Blue snake): Progressive difficulty - speed increases with score
  - **Fast Mode** (Green snake): Constant fast speed

## Controls

### Menu
- **Arrow Keys (Left/Right)**: Switch between game modes
- **Space**: Start the selected game

### In-Game
- **Arrow Keys**: Control snake direction
  - Up: Move up
  - Down: Move down
  - Left: Move left
  - Right: Move right

## Requirements

- Python 3.x
- pygame
- PyOpenGL
- PyOpenGL-accelerate (optional, for better performance)

## Installation

```bash
pip install pygame PyOpenGL PyOpenGL-accelerate
```

## How to Play

1. Run `python main.py`
2. Use left/right arrow keys to select a game mode
3. Press Space to start
4. Control the snake with arrow keys
5. Eat red apples to grow and score points
6. Avoid hitting walls or your own body

## Game Modes Details

### Original Mode (Grey Snake)
- Speed: 150ms per frame (constant)
- Best for beginners

### Hard Mode (Blue Snake)
- Starting speed: 150ms per frame
- Speed increases by 2ms per apple eaten
- Maximum speed: 50ms per frame (after 50 points)
- Most challenging mode

### Fast Mode (Green Snake)
- Speed: 70ms per frame (constant)
- Fast-paced gameplay

## Project Structure

- `main.py`: Main game controller and menu system
- `game_base.py`: Shared Snake and Apple classes
- `game_1_original.py`: Original mode configuration
- `game_2_hard.py`: Hard mode configuration
- `game_3_fast.py`: Fast mode configuration
- `general_games.py`: Shared utilities (drawing, constants)

## Recent Improvements

### Bug Fixes
- Fixed critical IndexError in `random.randint()` calls
- Fixed body growth bug in `add_body()` method (LEFT/RIGHT directions were modifying Y instead of X)
- Removed unnecessary `draw_snake()` call from `__init__`
- Fixed double space in conditional statement

### Code Quality
- Eliminated code duplication by creating shared base classes
- Replaced global `g_points` variable with proper OOP score tracking
- Optimized apple position generation (list comprehension instead of repeated rebuilding)
- Added proper window title
- Improved quit handling with `sys.exit()`
- Consolidated game mode selection
- Improved comments and documentation
- Preview snake colors now match actual game colors

### Architecture
- Created `game_base.py` with reusable `Snake` and `Apple` classes
- Each game mode now simply configures colors instead of duplicating logic
- Cleaner separation of concerns

## License

This is a personal project for educational purposes.

