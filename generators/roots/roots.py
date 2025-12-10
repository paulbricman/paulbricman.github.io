import random

class RootSystemGenerator:
    def __init__(self, 
                 grid_width=20,
                 grid_height=50,
                 block_size=60,
                 max_terminals=120,
                 branch_probability=0.7,
                 termination_probability=0.08,
                 vertical_line_penalty=0.9,    # Lower = more vertical lines (0.0-1.0)
                 horizontal_line_penalty=0.9,  # Lower = more horizontal lines (0.0-1.0)
                 stroke_width=8,
                 stroke_color='white',
                 padding=40):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.block_size = block_size
        self.max_terminals = max_terminals
        self.branch_probability = branch_probability
        self.termination_probability = termination_probability
        self.vertical_line_penalty = vertical_line_penalty
        self.horizontal_line_penalty = horizontal_line_penalty
        self.stroke_width = stroke_width
        self.stroke_color = stroke_color
        self.padding = padding
        
        self.grid = [[None for _ in range(grid_width)] for _ in range(grid_height)]
    
    def generate(self, seed=None):
        if seed is not None:
            random.seed(seed)
        
        self.grid = [[None for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        
        # Initial Setup
        start_x = self.grid_width // 2
        
        self.grid[0][start_x] = {'type': 'start', 'in': None, 'out': ['S']}
        self.grid[1][start_x] = {'type': 'vertical', 'in': 'N', 'out': ['S']}
        self.grid[2][start_x] = {'type': 'fork_top', 'in': 'N', 'out': ['W', 'E']}
        self.grid[2][start_x - 1] = {'type': 'horizontal', 'in': 'E', 'out': ['W']}
        self.grid[2][start_x + 1] = {'type': 'horizontal', 'in': 'W', 'out': ['E']}
        
        # Reserve targets
        self.grid[2][start_x - 2] = {'type': 'reserved'}
        self.grid[2][start_x + 2] = {'type': 'reserved'}
        
        # Active ends queue: (x, y, flow_dir, straight_count)
        active_ends = [
            (start_x - 2, 2, 'W', 0),
            (start_x + 2, 2, 'E', 0)
        ]
        
        terminal_count = 0
        
        def is_free(tx, ty):
            if tx < 0 or tx >= self.grid_width or ty >= self.grid_height:
                return False
            cell = self.grid[ty][tx]
            return cell is None or (isinstance(cell, dict) and cell.get('type') == 'reserved')

        def reserve(tx, ty):
            self.grid[ty][tx] = {'type': 'reserved'}

        while active_ends and terminal_count < self.max_terminals:
            # Random pop for organic growth
            idx = random.randint(0, len(active_ends) - 1)
            x, y, flow_dir, straight_count = active_ends.pop(idx)
            
            should_terminate = random.random() < self.termination_probability and y > 3
            force_terminate = y >= self.grid_height - 1 or terminal_count >= self.max_terminals
            
            # Probability calculation
            p_branch = self.branch_probability
            
            if flow_dir == 'W':
                target_w = x - 1
                target_s = y + 1
                can_go_w = is_free(target_w, y)
                can_go_s = is_free(x, target_s)
                rand_val = random.random()
                
                # Apply horizontal penalty (lower value = less likely to continue straight)
                p_continue_horiz = self.horizontal_line_penalty
                
                if should_terminate or force_terminate:
                    self.grid[y][x] = {'type': 'end_w', 'in': 'E', 'out': []}
                    terminal_count += 1
                # T-connector has horizontal pass-through, so apply horizontal penalty
                elif can_go_w and can_go_s and rand_val < (p_branch * p_continue_horiz):
                    self.grid[y][x] = {'type': 't_connector_w', 'in': 'E', 'out': ['W', 'S']}
                    reserve(target_w, y)
                    reserve(x, target_s)
                    active_ends.append((target_w, y, 'W', straight_count + 1))
                    active_ends.append((x, target_s, 'S', 0))
                    terminal_count += 1
                elif can_go_s and rand_val < (p_branch + 0.5): # Strongly prefer turning South
                    self.grid[y][x] = {'type': 'curve_e_s', 'in': 'E', 'out': ['S']}
                    reserve(x, target_s)
                    active_ends.append((x, target_s, 'S', 0))
                elif can_go_w and rand_val < (p_branch + 0.5 + p_continue_horiz):
                    self.grid[y][x] = {'type': 'horizontal', 'in': 'E', 'out': ['W']}
                    reserve(target_w, y)
                    active_ends.append((target_w, y, 'W', straight_count + 1))
                elif can_go_s:
                    self.grid[y][x] = {'type': 'curve_e_s', 'in': 'E', 'out': ['S']}
                    reserve(x, target_s)
                    active_ends.append((x, target_s, 'S', 0))
                elif can_go_w:
                    self.grid[y][x] = {'type': 'horizontal', 'in': 'E', 'out': ['W']}
                    reserve(target_w, y)
                    active_ends.append((target_w, y, 'W', straight_count + 1))
                else:
                    self.grid[y][x] = {'type': 'end_w', 'in': 'E', 'out': []}
                    terminal_count += 1

            elif flow_dir == 'E':
                target_e = x + 1
                target_s = y + 1
                can_go_e = is_free(target_e, y)
                can_go_s = is_free(x, target_s)
                rand_val = random.random()
                
                p_continue_horiz = self.horizontal_line_penalty
                
                if should_terminate or force_terminate:
                    self.grid[y][x] = {'type': 'end_e', 'in': 'W', 'out': []}
                    terminal_count += 1
                # T-connector has horizontal pass-through, so apply horizontal penalty
                elif can_go_e and can_go_s and rand_val < (p_branch * p_continue_horiz):
                    self.grid[y][x] = {'type': 't_connector_e', 'in': 'W', 'out': ['E', 'S']}
                    reserve(target_e, y)
                    reserve(x, target_s)
                    active_ends.append((target_e, y, 'E', straight_count + 1))
                    active_ends.append((x, target_s, 'S', 0))
                    terminal_count += 1
                elif can_go_s and rand_val < (p_branch + 0.5):
                    self.grid[y][x] = {'type': 'curve_w_s', 'in': 'W', 'out': ['S']}
                    reserve(x, target_s)
                    active_ends.append((x, target_s, 'S', 0))
                elif can_go_e and rand_val < (p_branch + 0.5 + p_continue_horiz):
                    self.grid[y][x] = {'type': 'horizontal', 'in': 'W', 'out': ['E']}
                    reserve(target_e, y)
                    active_ends.append((target_e, y, 'E', straight_count + 1))
                elif can_go_s:
                    self.grid[y][x] = {'type': 'curve_w_s', 'in': 'W', 'out': ['S']}
                    reserve(x, target_s)
                    active_ends.append((x, target_s, 'S', 0))
                elif can_go_e:
                    self.grid[y][x] = {'type': 'horizontal', 'in': 'W', 'out': ['E']}
                    reserve(target_e, y)
                    active_ends.append((target_e, y, 'E', straight_count + 1))
                else:
                    self.grid[y][x] = {'type': 'end_e', 'in': 'W', 'out': []}
                    terminal_count += 1

            elif flow_dir == 'S':
                target_s = y + 1
                target_w = x - 1
                target_e = x + 1
                can_go_s = is_free(x, target_s)
                can_go_w = is_free(target_w, y)
                can_go_e = is_free(target_e, y)
                rand_val = random.random()
                
                p_continue_vert = self.vertical_line_penalty
                
                if should_terminate or force_terminate:
                    self.grid[y][x] = {'type': 'end_n', 'in': 'N', 'out': []}
                    terminal_count += 1
                
                # Branching options
                # Fork (no vertical continuation) - not affected by vertical penalty
                elif can_go_w and can_go_e and rand_val < p_branch:
                    self.grid[y][x] = {'type': 'fork_top', 'in': 'N', 'out': ['W', 'E']}
                    reserve(target_w, y)
                    reserve(target_e, y)
                    active_ends.append((target_w, y, 'W', 0))
                    active_ends.append((target_e, y, 'E', 0))
                    terminal_count += 2
                
                # T-connectors have vertical pass-through, so apply vertical penalty
                elif can_go_w and can_go_s and rand_val < (p_branch * p_continue_vert):
                    self.grid[y][x] = {'type': 't_connector_n_w_s', 'in': 'N', 'out': ['W', 'S']}
                    reserve(target_w, y)
                    reserve(x, target_s)
                    active_ends.append((target_w, y, 'W', 0))
                    active_ends.append((x, target_s, 'S', straight_count + 1))
                    terminal_count += 1
                
                elif can_go_e and can_go_s and rand_val < (p_branch * p_continue_vert):
                    self.grid[y][x] = {'type': 't_connector_n_e_s', 'in': 'N', 'out': ['E', 'S']}
                    reserve(target_e, y)
                    reserve(x, target_s)
                    active_ends.append((target_e, y, 'E', 0))
                    active_ends.append((x, target_s, 'S', straight_count + 1))
                    terminal_count += 1
                
                # Turns (preference depends on how much we want to curve)
                elif (can_go_w or can_go_e) and rand_val < (p_branch + 0.3):
                    if can_go_w:
                        self.grid[y][x] = {'type': 'curve_n_w', 'in': 'N', 'out': ['W']}
                        reserve(target_w, y)
                        active_ends.append((target_w, y, 'W', 0))
                    else:
                        self.grid[y][x] = {'type': 'curve_n_e', 'in': 'N', 'out': ['E']}
                        reserve(target_e, y)
                        active_ends.append((target_e, y, 'E', 0))
                
                # Continue straight (controlled by vertical penalty)
                elif can_go_s and rand_val < (p_branch + 0.3 + p_continue_vert):
                    self.grid[y][x] = {'type': 'vertical', 'in': 'N', 'out': ['S']}
                    reserve(x, target_s)
                    active_ends.append((x, target_s, 'S', straight_count + 1))
                
                # Forced outcomes
                elif can_go_s:
                    self.grid[y][x] = {'type': 'vertical', 'in': 'N', 'out': ['S']}
                    reserve(x, target_s)
                    active_ends.append((x, target_s, 'S', straight_count + 1))
                
                else:
                    self.grid[y][x] = {'type': 'end_n', 'in': 'N', 'out': []}
                    terminal_count += 1
        
        # Cleanup passes
        self._fix_dangling_edges()
        self._prune_disconnected()
        
        # Verification
        self.validate_connectivity()

    def _fix_dangling_edges(self):
        """Ensure all outputs connect to a valid input. If not, downgrade to terminal."""
        opp_map = {'S': 'N', 'W': 'E', 'E': 'W', 'N': 'S'}
        
        # We might need multiple passes because fixing one might break another upstream
        # But a single pass usually suffices for trees if we go leaves-up or similar.
        # Actually, let's just do a robust single pass. If a block is bad, it becomes a terminal.
        
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                cell = self.grid[y][x]
                if not cell or cell.get('type') == 'reserved':
                    continue
                
                outputs = cell.get('out', [])
                valid_outputs = True
                
                for d in outputs:
                    nx, ny = x, y
                    if d == 'N': ny -= 1
                    elif d == 'S': ny += 1
                    elif d == 'W': nx -= 1
                    elif d == 'E': nx += 1
                    
                    # Check neighbor validity
                    neighbor_valid = False
                    if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height:
                        neighbor = self.grid[ny][nx]
                        if neighbor and neighbor.get('type') != 'reserved':
                            if neighbor.get('in') == opp_map[d]:
                                neighbor_valid = True
                    
                    if not neighbor_valid:
                        valid_outputs = False
                        break
                
                if not valid_outputs:
                    # Downgrade to terminal based on input
                    in_dir = cell.get('in')
                    if in_dir == 'N':
                        self.grid[y][x] = {'type': 'end_n', 'in': 'N', 'out': []}
                    elif in_dir == 'E':
                        self.grid[y][x] = {'type': 'end_e', 'in': 'E', 'out': []} # Input East -> End East (circle on Left) wait no
                        # Input East means flow is West. Circle should be on Right edge.
                        # My end_e logic: circle_cx = x*bs + r (Left edge).
                        # If flow is West (Input East), we are entering from Right.
                        # So we need circle on Right edge. That is end_w.
                        # Wait, let's check block_to_svg again.
                        
                        # block_to_svg:
                        # end_w: circle_cx = (x+1)*bs - r (Right Edge). Correct for Input E.
                        # end_e: circle_cx = x*bs + r (Left Edge). Correct for Input W.
                        
                        self.grid[y][x] = {'type': 'end_w', 'in': 'E', 'out': []}
                        
                    elif in_dir == 'W':
                        self.grid[y][x] = {'type': 'end_e', 'in': 'W', 'out': []}

    def _prune_disconnected(self):
        """Remove unreachable blocks starting from root."""
        visited = set()
        queue = [(self.grid_width // 2, 0)]
        visited.add((self.grid_width // 2, 0))
        
        while queue:
            cx, cy = queue.pop(0)
            cell = self.grid[cy][cx]
            if not cell: continue
            
            for out_dir in cell.get('out', []):
                nx, ny = cx, cy
                if out_dir == 'S': ny += 1
                elif out_dir == 'W': nx -= 1
                elif out_dir == 'E': nx += 1
                
                if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height:
                    if (nx, ny) not in visited and self.grid[ny][nx] and self.grid[ny][nx].get('type') != 'reserved':
                        visited.add((nx, ny))
                        queue.append((nx, ny))
        
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if (x, y) not in visited:
                    self.grid[y][x] = None

    def validate_connectivity(self):
        """Strict check: if block has 'in'='D', neighbor in direction opposite(D) must have 'out' containing 'D'."""
        errors = 0
        opp_map = {'N': 'S', 'S': 'N', 'W': 'E', 'E': 'W'}
        
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                cell = self.grid[y][x]
                if not cell: continue
                
                # Check Input Connection
                in_dir = cell.get('in')
                if in_dir: # Start block has None
                    nx, ny = x, y
                    # If input is from N, neighbor is at y-1 (North)
                    if in_dir == 'N': ny -= 1
                    elif in_dir == 'S': ny += 1
                    elif in_dir == 'W': nx -= 1
                    elif in_dir == 'E': nx += 1
                    
                    valid_input = False
                    if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height:
                        neighbor = self.grid[ny][nx]
                        # Neighbor must output to direction opposite to my input
                        # e.g. I accept from N. Neighbor is North of me. Neighbor must output S.
                        required_out = opp_map[in_dir]
                        if neighbor and required_out in neighbor.get('out', []):
                            valid_input = True
                    
                    if not valid_input:
                        print(f"Connectivity Error at ({x}, {y}): Expects input from {in_dir}, but neighbor invalid.")
                        errors += 1

                # Check Output Connections (redundant but good for verification)
                for out_dir in cell.get('out', []):
                    nx, ny = x, y
                    if out_dir == 'N': ny -= 1
                    elif out_dir == 'S': ny += 1
                    elif out_dir == 'W': nx -= 1
                    elif out_dir == 'E': nx += 1
                    
                    valid_output = False
                    if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height:
                        neighbor = self.grid[ny][nx]
                        required_in = opp_map[out_dir]
                        if neighbor and neighbor.get('in') == required_in:
                            valid_output = True
                    
                    if not valid_output:
                        print(f"Connectivity Error at ({x}, {y}): Outputs to {out_dir}, but neighbor doesn't accept.")
                        errors += 1
        
        if errors > 0:
            print(f"Validation FAILED: {errors} connectivity errors found.")

    def block_to_svg(self, block_data, x, y):
        if not block_data or block_data.get('type') == 'reserved':
            return ''
        
        block_type = block_data['type']
        paths = []
        cx = x * self.block_size + self.block_size / 2
        cy = y * self.block_size + self.block_size / 2
        r = self.block_size * 0.25  # Smaller circles
        segment_len = self.block_size * 0.15  # Tiny connecting segment
        
        # Terminal circles: centered with tiny segment to input edge
        if block_type == 'end_n':
            # Input from top, segment from top edge to circle
            top_y = y * self.block_size
            paths.append(f'<line x1="{cx}" y1="{top_y}" x2="{cx}" y2="{cy - r}" stroke="{self.stroke_color}" stroke-width="{self.stroke_width}"/>')
            paths.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{self.stroke_color}" stroke-width="{self.stroke_width}"/>')
        elif block_type == 'end_w': 
            # Input from right (East), segment from right edge to circle
            right_x = (x + 1) * self.block_size
            paths.append(f'<line x1="{right_x}" y1="{cy}" x2="{cx + r}" y2="{cy}" stroke="{self.stroke_color}" stroke-width="{self.stroke_width}"/>')
            paths.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{self.stroke_color}" stroke-width="{self.stroke_width}"/>')
        elif block_type == 'end_e':
            # Input from left (West), segment from left edge to circle
            left_x = x * self.block_size
            paths.append(f'<line x1="{left_x}" y1="{cy}" x2="{cx - r}" y2="{cy}" stroke="{self.stroke_color}" stroke-width="{self.stroke_width}"/>')
            paths.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{self.stroke_color}" stroke-width="{self.stroke_width}"/>')
        elif block_type == 'start':
            # Start circle at bottom with segment going down
            bottom_y = (y + 1) * self.block_size
            paths.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{self.stroke_color}" stroke-width="{self.stroke_width}"/>')
            paths.append(f'<line x1="{cx}" y1="{cy + r}" x2="{cx}" y2="{bottom_y}" stroke="{self.stroke_color}" stroke-width="{self.stroke_width}"/>')

        elif block_type == 'vertical':
            paths.append(f'<line x1="{cx}" y1="{y * self.block_size}" x2="{cx}" y2="{(y + 1) * self.block_size}" stroke="{self.stroke_color}" stroke-width="{self.stroke_width}"/>')
        elif block_type == 'horizontal':
            paths.append(f'<line x1="{x * self.block_size}" y1="{cy}" x2="{(x + 1) * self.block_size}" y2="{cy}" stroke="{self.stroke_color}" stroke-width="{self.stroke_width}"/>')
        
        elif block_type == 't_connector_w':
            paths.append(f'<line x1="{x * self.block_size}" y1="{cy}" x2="{(x + 1) * self.block_size}" y2="{cy}" stroke="{self.stroke_color}" stroke-width="{self.stroke_width}"/>')
            right_x = (x + 1) * self.block_size
            bottom_y = (y + 1) * self.block_size
            paths.append(f'<path d="M {right_x} {cy} Q {cx} {cy} {cx} {bottom_y}" fill="none" stroke="{self.stroke_color}" stroke-width="{self.stroke_width}"/>')

        elif block_type == 't_connector_e':
            paths.append(f'<line x1="{x * self.block_size}" y1="{cy}" x2="{(x + 1) * self.block_size}" y2="{cy}" stroke="{self.stroke_color}" stroke-width="{self.stroke_width}"/>')
            left_x = x * self.block_size
            bottom_y = (y + 1) * self.block_size
            paths.append(f'<path d="M {left_x} {cy} Q {cx} {cy} {cx} {bottom_y}" fill="none" stroke="{self.stroke_color}" stroke-width="{self.stroke_width}"/>')
        
        elif block_type == 't_connector_n_w_s': 
            top_y = y * self.block_size
            bottom_y = (y + 1) * self.block_size
            left_x = x * self.block_size
            paths.append(f'<line x1="{cx}" y1="{top_y}" x2="{cx}" y2="{bottom_y}" stroke="{self.stroke_color}" stroke-width="{self.stroke_width}"/>')
            paths.append(f'<path d="M {cx} {top_y} Q {cx} {cy} {left_x} {cy}" fill="none" stroke="{self.stroke_color}" stroke-width="{self.stroke_width}"/>')

        elif block_type == 't_connector_n_e_s':
            top_y = y * self.block_size
            bottom_y = (y + 1) * self.block_size
            right_x = (x + 1) * self.block_size
            paths.append(f'<line x1="{cx}" y1="{top_y}" x2="{cx}" y2="{bottom_y}" stroke="{self.stroke_color}" stroke-width="{self.stroke_width}"/>')
            paths.append(f'<path d="M {cx} {top_y} Q {cx} {cy} {right_x} {cy}" fill="none" stroke="{self.stroke_color}" stroke-width="{self.stroke_width}"/>')

        elif block_type == 'curve_e_s':
            paths.append(f'<path d="M {(x + 1) * self.block_size} {cy} Q {cx} {cy} {cx} {(y + 1) * self.block_size}" fill="none" stroke="{self.stroke_color}" stroke-width="{self.stroke_width}"/>')
        elif block_type == 'curve_w_s':
            paths.append(f'<path d="M {x * self.block_size} {cy} Q {cx} {cy} {cx} {(y + 1) * self.block_size}" fill="none" stroke="{self.stroke_color}" stroke-width="{self.stroke_width}"/>')
        elif block_type == 'curve_n_w':
            paths.append(f'<path d="M {cx} {y * self.block_size} Q {cx} {cy} {x * self.block_size} {cy}" fill="none" stroke="{self.stroke_color}" stroke-width="{self.stroke_width}"/>')
        elif block_type == 'curve_n_e':
            paths.append(f'<path d="M {cx} {y * self.block_size} Q {cx} {cy} {(x + 1) * self.block_size} {cy}" fill="none" stroke="{self.stroke_color}" stroke-width="{self.stroke_width}"/>')
        
        elif block_type == 'fork_top':
            top_x, top_y = cx, y * self.block_size
            left_x, left_y = x * self.block_size, cy
            right_x, right_y = (x + 1) * self.block_size, cy
            paths.append(f'<path d="M {top_x} {top_y} Q {cx} {cy} {left_x} {left_y}" fill="none" stroke="{self.stroke_color}" stroke-width="{self.stroke_width}"/>')
            paths.append(f'<path d="M {top_x} {top_y} Q {cx} {cy} {right_x} {right_y}" fill="none" stroke="{self.stroke_color}" stroke-width="{self.stroke_width}"/>')
        
        return '\n'.join(paths)
    
    def to_svg(self, background='transparent'):
        min_x, max_x = self.grid_width, 0
        min_y, max_y = self.grid_height, 0
        has_content = False
        
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                cell = self.grid[y][x]
                if cell and cell.get('type') != 'reserved':
                    min_x = min(min_x, x)
                    max_x = max(max_x, x)
                    min_y = min(min_y, y)
                    max_y = max(max_y, y)
                    has_content = True
        
        if not has_content:
            if background == 'transparent':
                return f'<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"></svg>'
            return f'<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><rect width="100" height="100" fill="{background}"/></svg>'

        offset_x = min_x * self.block_size
        offset_y = min_y * self.block_size
        content_width = (max_x - min_x + 1) * self.block_size
        content_height = (max_y - min_y + 1) * self.block_size
        
        width = content_width + 2 * self.padding
        height = content_height + 2 * self.padding
        
        svg_parts = [f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">']
        if background != 'transparent':
            svg_parts.append(f'<rect width="{width}" height="{height}" fill="{background}"/>')
        svg_parts.append(f'<g transform="translate({self.padding - offset_x}, {self.padding - offset_y})">')
        
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                svg = self.block_to_svg(self.grid[y][x], x, y)
                if svg:
                    svg_parts.append(svg)
        
        svg_parts.append('</g>')
        svg_parts.append('</svg>')
        return '\n'.join(svg_parts)


if __name__ == '__main__':
    print("Generating 1000 candidates and selecting top 20 by balanced spread (median distance - imbalance + 0.25×terminals)...")
    
    candidates = []
    
    for i in range(10000):
        gen = RootSystemGenerator()
        gen.generate(seed=i)
        
        # Find root position (start block at center top)
        root_x, root_y = gen.grid_width // 2, 0
        
        # Find all terminal positions
        terminals = []
        for y in range(gen.grid_height):
            for x in range(gen.grid_width):
                cell = gen.grid[y][x]
                if cell and cell.get('type', '').startswith('end'):
                    terminals.append((x, y))
        
        # Calculate Euclidean distances from root to each terminal
        if terminals:
            distances = [
                ((x - root_x)**2 + (y - root_y)**2)**0.5 
                for x, y in terminals
            ]
            distances.sort()
            # Calculate median
            n = len(distances)
            if n % 2 == 0:
                median_distance = (distances[n//2 - 1] + distances[n//2]) / 2
            else:
                median_distance = distances[n//2]
            
            # Calculate imbalance: standard deviation of terminal x-positions from the root
            # This measures how evenly terminals are distributed left/right of the root
            horizontal_variance = sum((x - root_x)**2 for x, y in terminals) / len(terminals)
            horizontal_imbalance = horizontal_variance ** 0.5  # Standard deviation
            
        else:
            median_distance = 0
            horizontal_imbalance = 0
        
        # Score: median distance - imbalance penalty + terminal bonus (favor spread, balance, complexity)
        terminal_bonus = 0.25 * len(terminals)
        score = median_distance - horizontal_imbalance + terminal_bonus
        
        svg = gen.to_svg()
        candidates.append((i, score, median_distance, horizontal_imbalance, len(terminals), svg))
    
    # Sort by score (descending) and take top 20
    candidates.sort(key=lambda x: x[1], reverse=True)
    top_20 = candidates[:50]
    
    print("\nTop 20 root systems by score (median distance - imbalance + 0.25×terminals):")
    for rank, (seed, score, median_dist, imbalance, term_count, svg) in enumerate(top_20, 1):
        filename = f'root_system_{rank-1}.svg'
        with open(filename, 'w') as f:
            f.write(svg)
        print(f"  #{rank}: seed={seed}, score={score:.2f} (median={median_dist:.2f}, imbalance={imbalance:.2f}), terminals={term_count}, saved as {filename}")
    
    print("\n✓ Saved top 20 root systems with best balance of spread, distribution, and complexity.")
