# Musical Maze - Comprehensive API Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Installation and Setup](#installation-and-setup)
3. [Core Classes](#core-classes)
4. [Game Components](#game-components)
5. [Sound System](#sound-system)
6. [User Interface](#user-interface)
7. [File Management](#file-management)
8. [Configuration](#configuration)
9. [Usage Examples](#usage-examples)
10. [API Reference](#api-reference)

## Project Overview

Musical Maze is an educational game that combines maze solving with musical learning. Players navigate through procedurally generated mazes while learning musical melodies. The game supports both manual play and algorithmic solving using A* pathfinding.

### Key Features
- Procedurally generated mazes
- Musical feedback system
- User authentication and progress tracking
- Multiple difficulty levels
- A* algorithm demonstration
- Customizable game settings

## Installation and Setup

### Requirements
```bash
pip install -r requirements.txt
```

### Dependencies
- **pygame**: Game engine and graphics
- **pygameMenu**: Menu system
- **psonic**: Sound synthesis
- **tkinter**: User interface (included with Python)
- **Flask**: Web framework (listed in requirements)

### Running the Application
```python
# Start the application
python app.py
```

## Core Classes

### 1. Maze Class

**Purpose**: Generates and manages the maze structure using recursive backtracking.

```python
class Maze:
    def __init__(self, w=25, h=30, sx=0, sy=0)
```

#### Public Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `generate_maze()` | `x=-1, y=-1` | `None` | Generates maze using recursive backtracking |
| `get_cell()` | `x: int, y: int` | `State` | Retrieves cell at coordinates |
| `show()` | `screen: Surface` | `None` | Renders maze walls on screen |
| `not_dir()` | `dir: int` | `int` | Returns opposite direction |

#### Usage Example
```python
from classes import Maze, const

# Create a 10x10 maze
maze = Maze(10, 10)
maze.generate_maze()

# Get a specific cell
cell = maze.get_cell(5, 5)

# Render on pygame surface
maze.show(screen)
```

### 2. Activity Class

**Purpose**: Manages player movement, pathfinding, and game state.

```python
class Activity:
    def __init__(self, maze, sound)
```

#### Public Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `move()` | `dir: int` | `None` | Moves player in specified direction |
| `show()` | `screen: Surface, walls=True` | `None` | Renders player and maze |
| `astar()` | `destination: tuple` | `None` | Performs A* pathfinding |
| `get_solution()` | | `list` | Returns optimal path to goal |
| `serialize()` | | `dict` | Exports game state to dictionary |
| `get_copy()` | | `Activity` | Creates deep copy of activity |

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `x` | `int` | Current X position |
| `y` | `int` | Current Y position |
| `wrong_moves` | `int` | Count of incorrect moves |
| `moves` | `list` | History of player positions |
| `solved_path` | `list` | Optimal solution path |

#### Usage Example
```python
from classes import Activity, Maze, Sound

# Setup
maze = Maze(5, 5)
maze.generate_maze()
sound = Sound(notes, durations)
activity = Activity(maze, sound)

# Move player
activity.move(const.right)  # Move right
activity.move(const.down)   # Move down

# Get solution
solution = activity.get_solution()

# Render
activity.show(screen, walls=True)
```

### 3. Sound Class

**Purpose**: Manages musical feedback and melody playback.

```python
class Sound:
    def __init__(self, notes, dur)
```

#### Public Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `play_all()` | | `None` | Plays complete melody |
| `play_single_note()` | `note: int, dur: float, pan=0` | `None` | Plays single note |
| `get_next_note()` | | `tuple` | Returns next note and duration |
| `play_error_note()` | | `None` | Plays error sound effect |
| `play_hint()` | `pan=0` | `None` | Plays hint for next correct note |
| `play_wall_note()` | | `None` | Plays sound when hitting wall |
| `back_to_path()` | | `None` | Plays sound for returning to path |
| `play_win()` | | `None` | Plays victory sound sequence |

#### Usage Example
```python
from classes import Sound

# Setup with melody
notes = [60, 62, 64, 65, 67]  # C major scale
durations = [0.5, 0.5, 0.5, 0.5, 1.0]
sound = Sound(notes, durations)

# Play entire melody
sound.play_all()

# Play single note
sound.play_single_note(60, 0.5)  # Middle C for 0.5 seconds

# Play hint
sound.play_hint()
```

### 4. State Class

**Purpose**: Represents individual maze cells with wall information.

```python
class State:
    def __init__(self)
```

#### Public Properties

| Property | Type | Description |
|----------|------|-------------|
| `state` | `bool` | Whether cell has been visited |
| `gate` | `list[bool]` | Wall states [right, left, up, down] |
| `x` | `int` | Cell X coordinate |
| `y` | `int` | Cell Y coordinate |
| `location` | `tuple` | Pixel coordinates (x*wc, y*hc) |

## Game Components

### Main Menu System

**File**: `main.py`

#### Main Function
```python
def main_menu(current_user)
```

Creates and displays the game's main menu with options for:
- Game configuration (mode, level, walls, melody)
- Game start
- About information

#### Configuration Functions

| Function | Parameters | Description |
|----------|------------|-------------|
| `set_game_mode()` | `mode: str, **kwargs` | Sets game mode (user/a-star) |
| `set_game_level()` | `level: tuple, **kwargs` | Sets maze dimensions |
| `set_game_walls()` | `walls: bool, **kwargs` | Enables/disables wall display |
| `set_game_melody()` | `melody: int, **kwargs` | Selects melody for gameplay |

### Game Loop

**File**: `game.py`

#### Main Function
```python
def start()
```

Initializes and runs the main game loop with:
- Pygame initialization
- Event handling (keyboard, joystick)
- Game state management
- Victory condition checking

#### Utility Functions

| Function | Parameters | Returns | Description |
|----------|------------|---------|-------------|
| `solve()` | | `None` | Automatically solves maze using A* |
| `play_to_index()` | | `None` | Plays melody up to current progress |
| `play_all()` | | `None` | Plays complete melody |
| `play_hint()` | | `None` | Plays hint for next move |
| `get_melody_game()` | `index: int` | `tuple` | Returns notes and durations for melody |

## Sound System

### Melody Structure

Melodies are defined as separate Python modules in the `sounds/` directory.

#### Example: Little Jonathan
```python
# sounds/little_jonathan.py
notes = [67, 64, 64, 65, 62, 62, 60, 62, 64, 65, 67, 67, 67]
dur = [0.25, 0.25, 0.5, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5]
```

#### Adding New Melodies

1. Create a new Python file in `sounds/` directory
2. Define `notes` and `dur` lists
3. Add entry to `const.melodies_map` in `classes.py`
4. Update melody selector in `main.py`

## User Interface

### Authentication System

**File**: `app.py`

#### User Management Functions

| Function | Parameters | Returns | Description |
|----------|------------|---------|-------------|
| `create_user()` | `name, username, password, age, gender, knowledge` | `dict` | Creates user object |
| `home()` | | `None` | Shows main login/register screen |
| `registration()` | | `None` | Shows registration form |
| `login()` | | `None` | Shows login form after registration |
| `dlogin()` | | `None` | Shows direct login form |

#### Window Management
```python
def center_window(width=300, height=200)
```

Centers tkinter window on screen with specified dimensions.

### Widget System

**File**: `widgets/main.py`

The widget system provides custom UI components for the game interface.

#### Button Class
```python
class Button:
    def __init__(self, surface, **kwargs)
```

**Parameters**:
- `surface`: Pygame surface to draw on
- `text`: Button text
- `width`, `height`: Dimensions
- `bordercolor`: Border color
- `colour`: Background color
- `fontsize`: Text size
- `target`: Callback function

**Methods**:
- `place(position)`: Position button on screen
- `render()`: Draw button
- `handle_event(event)`: Process mouse clicks

#### Label Class
```python
class Label:
    def __init__(self, surface, **kwargs)
```

For displaying text with customizable styling.

#### Entry Class
```python
class Entry:
    def __init__(self, surface, **kwargs)
```

Text input field with focus management.

#### Global Widget Functions

| Function | Returns | Description |
|----------|---------|-------------|
| `render_widgets()` | `None` | Renders all active widgets |
| `handle_widgets()` | `list` | Processes widget events |

## File Management

**File**: `files_functions.py`

### Data Persistence Functions

| Function | Parameters | Returns | Description |
|----------|------------|---------|-------------|
| `save_to_json()` | `data: dict, dest: str` | `None` | Saves data to JSON file |
| `load_json()` | `src: str` | `dict/list` | Loads data from JSON file |
| `save_passwords()` | `passwords: dict` | `None` | Saves password dictionary |
| `load_passwords()` | | `dict` | Loads password dictionary |

#### Usage Example
```python
from files_functions import save_to_json, load_json

# Save user data
user_data = {"name": "John", "score": 100}
save_to_json(user_data, "users")

# Load user data
users = load_json("users")
```

### Data Storage Locations

| File | Purpose | Structure |
|------|---------|-----------|
| `DB/users.json` | User profiles | List of user objects |
| `DB/passwords.json` | Authentication | Username:password mapping |
| `DB/players_data.json` | Game statistics | List of game session data |

## Configuration

### Constants

**File**: `classes.py`

#### Color Constants
```python
const.white = (255, 255, 255)
const.black = (0, 0, 0)
const.red = (255, 0, 0)
const.green = (0, 255, 0)
const.blue = (12, 12, 200)
const.light_blue = (18, 204, 214)
```

#### Direction Constants
```python
const.right = 0
const.left = 1
const.up = 2
const.down = 3
```

#### Game Settings
```python
const.wc = 25  # Cell width
const.hc = 25  # Cell height
const.time_poll = 75  # Animation timing
```

### Global Game Data
```python
game_data = {
    "mode": "user",        # "user" or "a-star"
    "level": (5, 5),       # Maze dimensions
    "walls": True,         # Show walls
    "user": None,          # Current user
    "melody": None         # Selected melody
}
```

## Usage Examples

### Basic Game Setup
```python
import pygame
from classes import Maze, Activity, Sound, const
from sounds import little_jonathan as lj

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))

# Create game components
maze = Maze(10, 10)
maze.generate_maze()

sound = Sound(lj.notes, lj.dur)
activity = Activity(maze, sound)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                activity.move(const.right)
            elif event.key == pygame.K_LEFT:
                activity.move(const.left)
            elif event.key == pygame.K_UP:
                activity.move(const.up)
            elif event.key == pygame.K_DOWN:
                activity.move(const.down)
    
    # Render
    screen.fill(const.gray)
    activity.show(screen)
    pygame.display.flip()
```

### Creating Custom Melodies
```python
# Define melody
custom_notes = [60, 62, 64, 65, 67, 69, 71, 72]  # C major scale
custom_durations = [0.5] * 8  # Half second per note

# Create sound object
sound = Sound(custom_notes, custom_durations)

# Play melody
sound.play_all()
```

### User Authentication Flow
```python
from files_functions import save_to_json, load_passwords
from app import create_user

# Load existing data
passwords = load_passwords()

# Create new user
new_user = create_user(
    name="Alice Smith",
    username="alice",
    password="secret123",
    age=25,
    gender=2,  # Female
    knowledge=1  # Has musical knowledge
)

# Save user
save_to_json(new_user, "users")
passwords["alice"] = "secret123"
save_passwords(passwords)
```

### A* Algorithm Usage
```python
from classes import Activity, Maze, Sound

# Setup
maze = Maze(15, 15)
maze.generate_maze()
activity = Activity(maze, sound)

# Find solution
activity.astar((maze.w - 1, maze.h - 1))  # Goal: bottom-right
solution_path = activity.get_astar((0, 0), (maze.w - 1, maze.h - 1))

# Execute solution
activity.go_to(solution_path)
```

## API Reference

### Error Handling

Most functions include basic error handling:

```python
try:
    data = load_json("users")
except Exception:
    raise Exception("Some problem with reading data.")
```

### Event System

The game uses pygame's event system:

```python
# Keyboard events
keys = pygame.key.get_pressed()
if keys[pygame.K_UP]:
    activity.move(const.up)

# Joystick events
if event.type == pygame.JOYAXISMOTION:
    if event.axis == 1 and round(event.value) < 0:
        activity.move(const.up)
```

### Performance Considerations

- Maze generation complexity: O(n*m) where n,m are dimensions
- A* pathfinding complexity: O(b^d) where b is branching factor, d is depth
- Sound playback is non-blocking using psonic
- Widget rendering is optimized for small numbers of widgets

### Thread Safety

The application is primarily single-threaded. The widget system includes some threading utilities but core game logic runs on the main thread.

## Extending the Framework

### Adding New Game Modes

1. Add mode to `game_data` configuration
2. Implement mode logic in `game.py`
3. Update menu options in `main.py`

### Custom Pathfinding Algorithms

Implement alternative to A* by:
1. Adding method to `Activity` class
2. Following the same interface as `astar()`
3. Updating solution path format

### New Sound Effects

Add sound effects by:
1. Extending `Sound` class methods
2. Using psonic library functions
3. Integrating with game events

---

*This documentation covers all public APIs and components of the Musical Maze project. For implementation details, refer to the source code and inline comments.*