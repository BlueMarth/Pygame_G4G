import os
import sys
import time
import json
from datetime import datetime
import numpy as np
from collections import deque

try:
    import pygame
except Exception:
    pygame = None


def initialize_grid(rows, cols, pattern=None):
    """Create and populate the initial grid.

    Parameters
    - rows, cols: grid size
    - pattern: one of {'random', 'glider', 'blinker', 'block'} or an iterable
      of (r, c) live-cell coordinates. If None, a random pattern is used.

    Returns
    - grid: numpy array of shape (rows, cols) with 0/1 values
    """
    grid = np.zeros((rows, cols), dtype=np.int8)

    if isinstance(pattern, str):
        p = pattern.lower()
    else:
        p = pattern

    if p is None or p == 'random':
        # ~50% live cells by default
        grid = (np.random.random((rows, cols)) < 0.5).astype(np.int8)
        return grid

    if p == 'glider':
        # classic glider
        glider = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        r0, c0 = 1, 1
        for dr, dc in glider:
            if 0 <= r0 + dr < rows and 0 <= c0 + dc < cols:
                grid[r0 + dr, c0 + dc] = 1
        return grid

    if p == 'blinker':
        r0, c0 = rows // 2, cols // 2
        if c0 - 1 >= 0 and c0 + 1 < cols:
            grid[r0, c0 - 1:c0 + 2] = 1
        return grid

    if p == 'block':
        r0, c0 = rows // 2, cols // 2
        for dr in (0, 1):
            for dc in (0, 1):
                if 0 <= r0 + dr < rows and 0 <= c0 + dc < cols:
                    grid[r0 + dr, c0 + dc] = 1
        return grid

    # If pattern is an iterable of coordinates, place them (wrap-around safe)
    try:
        for (r, c) in pattern:
            rr = int(r) % rows
            cc = int(c) % cols
            grid[rr, cc] = 1
        return grid
    except Exception:
        # fallback to random
        grid = (np.random.random((rows, cols)) < 0.2).astype(np.int8)
        return grid


def update_grid(grid):
    """Apply Conway's Game of Life rules and return the next grid state.

    Uses toroidal (wrap-around) neighbor behavior via numpy.roll.
    """
    # count neighbors by summing the 8 shifts
    neighbors = np.zeros_like(grid, dtype=np.int8)
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            neighbors += np.roll(np.roll(grid, dr, axis=0), dc, axis=1)

    # Apply rules:
    # - A live cell with 2 or 3 neighbors lives on
    # - A dead cell with exactly 3 neighbors becomes alive
    new_grid = ((neighbors == 3) | ((grid == 1) & (neighbors == 2))).astype(np.int8)
    return new_grid


def display_grid(grid, clear=True, live_char='█', dead_char=' '):
    """Render the grid to the console.

    - `clear`: if True, clears the terminal each frame.
    - `live_char` / `dead_char`: characters used for display.
    """
    if clear:
        if os.name == 'nt':
            os.system('cls')
        else:
            # ANSI clear
            sys.stdout.write('\x1b[2J\x1b[H')

    rows, cols = grid.shape
    lines = []
    for r in range(rows):
        # build each line quickly
        row = grid[r]
        line = ''.join(live_char if cell else dead_char for cell in row)
        lines.append(line)

    sys.stdout.write('\n'.join(lines) + '\n')
    sys.stdout.flush()


def draw_pygame(grid, surface, cell_size=10, live_color=(30, 200, 30), dead_color=(20, 20, 20), x_offset=0, y_offset=0, ages=None, generation=0, max_palette=20):
    """Draw the grid to a pygame surface. Live cells as `live_color`.
    Only draws live cells and clears background with `dead_color`.
    """
    rows, cols = grid.shape
    surface.fill(dead_color)
    # draw live cells
    rect = pygame.Rect(0, 0, cell_size, cell_size)
    # If ages are provided, draw using a red->purple gradient according to age buckets.
    if ages is None:
        for r in range(rows):
            for c in range(cols):
                if grid[r, c]:
                    rect.x = c * cell_size + x_offset
                    rect.y = r * cell_size + y_offset
                    surface.fill(live_color, rect)
        return

    # determine palette size: bound by max_palette and current generation (at least 3)
    palette_size = max(3, min(max_palette, max(1, generation)))
    # build a rainbow palette: red -> orange -> yellow -> green -> blue -> purple
    stops = [
        (255, 0, 0),     # red
        (255, 127, 0),   # orange
        (255, 255, 0),   # yellow
        (0, 200, 0),     # green
        (0, 80, 255),    # blue
        (160, 30, 160),  # purple
    ]

    def lerp(a, b, t):
        return int(a + (b - a) * t)

    palette = []
    if palette_size == 1:
        palette = [stops[0]]
    else:
        # map palette indices evenly across the stops
        total_segments = len(stops) - 1
        for i in range(palette_size):
            t_full = i / (palette_size - 1)
            # position along stops
            pos = t_full * total_segments
            seg = int(min(total_segments - 1, int(pos)))
            local_t = pos - seg
            a = stops[seg]
            b = stops[seg + 1]
            rch = lerp(a[0], b[0], local_t)
            gch = lerp(a[1], b[1], local_t)
            bch = lerp(a[2], b[2], local_t)
            palette.append((rch, gch, bch))

    for r in range(rows):
        for c in range(cols):
            if grid[r, c]:
                age = int(ages[r, c])
                if age <= 0:
                    idx = 0
                else:
                    idx = min(age - 1, palette_size - 1)
                color = palette[idx]
                rect.x = c * cell_size + x_offset
                rect.y = r * cell_size + y_offset
                surface.fill(color, rect)


def _save_user_states_file_path():
    return os.path.join(os.path.dirname(__file__), 'user_inputs.json')


def save_user_state(name, grid):
    """Save a grid under `name` to the user_inputs.json file.

    Grid is stored as a list of lists of ints.
    """
    path = _save_user_states_file_path()
    try:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {}
    except Exception:
        data = {}

    data[name] = grid.tolist()
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def load_user_states():
    """Return the saved states dict name -> grid list or empty dict."""
    path = _save_user_states_file_path()
    try:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        return {}
    return {}


def _auto_name():
    return datetime.now().strftime('user_%Y%m%d_%H%M%S')


def run_pygame(rows, cols, pattern=None, cell_size=16, fps=10):
    """Run an interactive Pygame window for Conway's Game of Life.

    Controls:
    - Click: toggle cell
    - Space: pause/unpause
    - R: randomize
    - C: clear
    - Up/Down: increase/decrease speed
    - Esc or window close: quit
    """
    if pygame is None:
        raise RuntimeError("pygame is required for the GUI runner. Install with 'pip install pygame'.")

    pygame.init()
    pygame.display.set_caption('Game of Life')

    # Prepare UI button layout and saved-state helpers early so event handling
    # can reference them on the very first frame.
    btn_x = 6
    btn_y = 6
    btn_w = 84
    btn_h = 26
    spacing = 6

    buttons = {
        'start': pygame.Rect(btn_x, btn_y, btn_w, btn_h),
        'pause': pygame.Rect(btn_x + (btn_w + spacing) * 1, btn_y, btn_w, btn_h),
        'random': pygame.Rect(btn_x + (btn_w + spacing) * 2, btn_y, btn_w, btn_h),
        'clear': pygame.Rect(btn_x + (btn_w + spacing) * 3, btn_y, btn_w, btn_h),
        'reset': pygame.Rect(btn_x + (btn_w + spacing) * 4, btn_y, btn_w, btn_h),
        'special': pygame.Rect(btn_x + (btn_w + spacing) * 5, btn_y, btn_w, btn_h),
        'save': pygame.Rect(btn_x + (btn_w + spacing) * 6, btn_y, btn_w, btn_h),
        'load': pygame.Rect(btn_x + (btn_w + spacing) * 7, btn_y, btn_w, btn_h),
    }

    special_open = False
    load_open = False
    special_items = ['Still Lifes', 'Oscillators', 'Spaceships']
    special_rects = []
    load_rects = []
    saved_states = load_user_states()

    # compute a top margin for UI and create the display including that margin
    panel_h = btn_h + 12
    top_margin = panel_h + 4
    width = cols * cell_size
    height = rows * cell_size + top_margin
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 20)

    grid = initialize_grid(rows, cols, pattern)
    ages = np.zeros((rows, cols), dtype=np.int16)  # per-cell age array: 0 means dead, positive integers count consecutive generations alive
    initial_age = None
    generation = 0
    paused = False
    started = False  # only advance simulation after user clicks Start
    initial_grid = None  # will hold the grid state at the moment Start is pressed
    # history of recent grid bytes for detecting steady states (period 1 or 2)
    history = deque(maxlen=3)
    history.append(grid.tobytes())
    steady_detected = False
    steady_generation = None
    steady_period = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Space toggles pause only after simulation has started
                    if started:
                        paused = not paused
                elif event.key == pygame.K_r:
                    grid = initialize_grid(rows, cols, 'random')
                    generation = 0
                    ages = np.zeros((rows, cols), dtype=np.int16)
                    history.clear()
                    history.append(grid.tobytes())
                    steady_detected = False
                    steady_generation = None
                    steady_period = None
                elif event.key == pygame.K_c:
                    grid = np.zeros((rows, cols), dtype=np.int8)
                    generation = 0
                    ages = np.zeros((rows, cols), dtype=np.int16)
                    history.clear()
                    history.append(grid.tobytes())
                    steady_detected = False
                    steady_generation = None
                    steady_period = None
                elif event.key == pygame.K_UP:
                    fps = min(120, fps + 1)
                elif event.key == pygame.K_DOWN:
                    fps = max(1, fps - 1)
                elif event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                # check buttons first
                hit_button = False
                for name, rect in buttons.items():
                    if rect.collidepoint(mx, my):
                        hit_button = True
                        if name == 'start':
                            started = True
                            paused = False
                            # remember the initial state so Reset can restore it
                            initial_grid = grid.copy()
                            initial_age = ages.copy()
                            # reset steady detection history starting from the snapshot
                            history.clear()
                            history.append(grid.tobytes())
                            steady_detected = False
                            steady_generation = None
                            steady_period = None
                        elif name == 'pause' and started:
                            paused = not paused
                        elif name == 'random':
                            grid = initialize_grid(rows, cols, 'random')
                            generation = 0
                            ages = np.zeros((rows, cols), dtype=np.int16)
                            history.clear()
                            history.append(grid.tobytes())
                            steady_detected = False
                            steady_generation = None
                            steady_period = None
                        elif name == 'clear':
                            grid = np.zeros((rows, cols), dtype=np.int8)
                            generation = 0
                            ages = np.zeros((rows, cols), dtype=np.int16)
                            history.clear()
                            history.append(grid.tobytes())
                            steady_detected = False
                            steady_generation = None
                            steady_period = None
                        elif name == 'reset':
                            # If an initial snapshot was saved when Start was pressed,
                            # restore it. Otherwise clear the grid (clear the screen).
                            if initial_grid is not None:
                                grid = initial_grid.copy()
                            else:
                                grid = np.zeros((rows, cols), dtype=np.int8)
                            generation = 0
                            # return to setup mode so user can tweak before restarting
                            started = False
                            paused = False
                            if initial_age is not None:
                                ages = initial_age.copy()
                            else:
                                ages = np.zeros((rows, cols), dtype=np.int16)
                            history.clear()
                            history.append(grid.tobytes())
                            steady_detected = False
                            steady_generation = None
                            steady_period = None
                        elif name == 'special':
                            special_open = not special_open
                            load_open = False
                        elif name == 'save':
                            # save the current grid with an automatic name
                            name = _auto_name()
                            # Save the grid; ages are not persisted in this simple format.
                            save_user_state(name, grid)
                            saved_states = load_user_states()
                        elif name == 'load':
                            load_open = not load_open
                            special_open = False
                        break

                if hit_button:
                    # consumed by button click
                    pass
                else:
                    # click on grid to toggle cell (only allow editing while not started)
                    # ignore clicks inside the top UI margin
                    if my >= top_margin:
                        c = mx // cell_size
                        r = (my - top_margin) // cell_size
                        if 0 <= r < rows and 0 <= c < cols and not started:
                            grid[r, c] = 0 if grid[r, c] else 1
                # handle clicks on special dropdown items
                if special_open:
                    for item, rect in special_rects:
                        if rect.collidepoint(mx, my):
                            # apply a representative pattern for each category
                            if item == 'Still Lifes':
                                grid = np.zeros((rows, cols), dtype=np.int8)
                                # block at center
                                r0, c0 = rows // 2, cols // 2
                                for dr in (0, 1):
                                    for dc in (0, 1):
                                        grid[r0 + dr, c0 + dc] = 1
                                ages = np.zeros((rows, cols), dtype=np.int16)
                            elif item == 'Oscillators':
                                grid = np.zeros((rows, cols), dtype=np.int8)
                                r0, c0 = rows // 2, cols // 2
                                grid[r0 - 1:r0 + 2, c0] = 1
                                ages = np.zeros((rows, cols), dtype=np.int16)
                            elif item == 'Spaceships':
                                grid = np.zeros((rows, cols), dtype=np.int8)
                                # place a glider
                                glider = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
                                r0, c0 = rows // 4, cols // 4
                                for dr, dc in glider:
                                    grid[r0 + dr, c0 + dc] = 1
                                ages = np.zeros((rows, cols), dtype=np.int16)
                            generation = 0
                            started = False
                            paused = False
                            special_open = False
                            break

                # handle clicks on load dropdown items
                if load_open:
                    for name, rect in load_rects:
                        if rect.collidepoint(mx, my):
                            # load the saved grid
                            saved = load_user_states().get(name)
                            if saved is not None:
                                try:
                                    arr = np.array(saved, dtype=np.int8)
                                    # accept different sizes: center/crop/pad to fit
                                    r0 = min(arr.shape[0], rows)
                                    c0 = min(arr.shape[1], cols)
                                    new_grid = np.zeros((rows, cols), dtype=np.int8)
                                    new_grid[:r0, :c0] = arr[:r0, :c0]
                                    grid = new_grid
                                    initial_grid = grid.copy()
                                    generation = 0
                                    started = False
                                    paused = False
                                    ages = np.zeros((rows, cols), dtype=np.int16)
                                    history.clear()
                                    history.append(grid.tobytes())
                                    steady_detected = False
                                    steady_generation = None
                                    steady_period = None
                                except Exception:
                                    pass
                            load_open = False
                            break
            elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
                # allow drag-to-paint while setting up (left button held)
                mx, my = event.pos
                if my >= top_margin:
                    c = mx // cell_size
                    r = (my - top_margin) // cell_size
                    if 0 <= r < rows and 0 <= c < cols and not started:
                        grid[r, c] = 1

        # end event loop

        # Only advance the simulation after the user has started it
        if started and not paused:
            new_grid = update_grid(grid)
            # update ages: births -> 1, survivals -> ages+1, deaths -> 0
            births = (new_grid == 1) & (grid == 0)
            survivals = (new_grid == 1) & (grid == 1)
            ages = np.where(births, 1, np.where(survivals, ages + 1, 0))
            grid = new_grid
            generation += 1
            # steady-state detection: compare current grid bytes to recent history
            new_b = grid.tobytes()
            if not steady_detected:
                # check period-1 (same as previous) or period-2
                if len(history) >= 1 and new_b == history[-1]:
                    steady_detected = True
                    steady_generation = generation
                    steady_period = 1
                elif len(history) >= 2 and new_b == history[-2]:
                    steady_detected = True
                    steady_generation = generation
                    steady_period = 2
            history.append(new_b)

        draw_pygame(grid, screen, cell_size=cell_size, y_offset=top_margin, ages=ages, generation=generation, max_palette=20)

        # draw UI buttons and overlay text
        # draw buttons background (semi-opaque)
        panel_h = btn_h + 12
        panel = pygame.Surface((screen.get_width(), panel_h), pygame.SRCALPHA)
        panel.fill((10, 10, 10, 120))
        screen.blit(panel, (0, 0))

        for name, rect in buttons.items():
            color = (80, 80, 80)
            if name == 'start':
                color = (30, 140, 30) if not started else (50, 100, 50)
            elif name == 'pause':
                color = (140, 120, 30) if started and paused else (80, 80, 80)
            elif name == 'random':
                color = (40, 90, 160)
            elif name == 'clear':
                color = (160, 40, 40)
            elif name == 'reset':
                color = (120, 40, 160)
            elif name == 'special':
                color = (120, 120, 40) if special_open else (80, 80, 80)
            elif name == 'save':
                color = (60, 120, 180)
            elif name == 'load':
                color = (60, 180, 120) if load_open else (80, 80, 80)
            pygame.draw.rect(screen, color, rect)
            label = name.upper()
            lbl = font.render(label, True, (240, 240, 240))
            lbl_x = rect.x + (rect.w - lbl.get_width()) // 2
            lbl_y = rect.y + (rect.h - lbl.get_height()) // 2
            screen.blit(lbl, (lbl_x, lbl_y))

        # draw special dropdown when open
        if special_open:
            special_rects = []
            menu_x = buttons['special'].x
            menu_y = buttons['special'].y + buttons['special'].h + 6
            menu_w = 160
            item_h = 24
            for i, item in enumerate(special_items):
                r = pygame.Rect(menu_x, menu_y + i * (item_h + 2), menu_w, item_h)
                pygame.draw.rect(screen, (40, 40, 40), r)
                txt = font.render(item, True, (220, 220, 220))
                screen.blit(txt, (r.x + 6, r.y + 4))
                special_rects.append((item, r))

        # draw load dropdown when open (show saved state names)
        if load_open:
            saved_states = load_user_states()
            names = list(saved_states.keys())
            load_rects = []
            menu_x = buttons['load'].x
            menu_y = buttons['load'].y + buttons['load'].h + 6
            menu_w = 220
            item_h = 22
            for i, name in enumerate(names):
                r = pygame.Rect(menu_x, menu_y + i * (item_h + 2), menu_w, item_h)
                pygame.draw.rect(screen, (40, 40, 40), r)
                txt = font.render(name, True, (220, 220, 220))
                screen.blit(txt, (r.x + 6, r.y + 3))
                load_rects.append((name, r))

        status = f"Gen: {generation}  FPS: {int(clock.get_fps())}  [{'SETUP' if not started else ('PAUSED' if paused else 'RUNNING')}]"
        if steady_detected:
            status += f"  STEADY after {steady_generation} gen (period {steady_period})"
        text_surf = font.render(status, True, (240, 240, 240))
        screen.blit(text_surf, (4, btn_y + btn_h + 4))

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    # Default to a Pygame window if pygame is available; fall back to console.
    rows, cols = 40, 80
    initial_pattern = "glider"  # Or 'random', 'blinker', 'block', or a list of coords

    if pygame is not None:
        try:
            run_pygame(rows, cols, initial_pattern, cell_size=12, fps=12)
        except Exception as e:
            print("Failed to start Pygame runner:", e)
            print("Falling back to console output.")
            grid = initialize_grid(rows, cols, initial_pattern)
            generation = 0
            try:
                while True:
                    print(f"Generation: {generation}")
                    display_grid(grid)
                    grid = update_grid(grid)
                    generation += 1
                    time.sleep(0.12)
            except KeyboardInterrupt:
                print('\nSimulation interrupted by user.')
    else:
        grid = initialize_grid(rows, cols, initial_pattern)
        generation = 0
        try:
            while True:
                print(f"Generation: {generation}")
                display_grid(grid)
                grid = update_grid(grid)
                generation += 1
                time.sleep(0.12)
        except KeyboardInterrupt:
            print('\nSimulation interrupted by user.')