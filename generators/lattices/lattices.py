import random
import math

class LatticeGenerator:
    def __init__(self,
                 grid_rows=8,
                 grid_cols=10,
                 hex_size=50,
                 line_probability=0.7,
                 stroke_width=4,
                 stroke_color='white',
                 fill_color='white',
                 background='transparent',
                 padding=40,
                 show_debug=False,
                 num_hexagons=0,
                 num_chains=0):
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.hex_size = hex_size
        self.line_probability = line_probability
        self.stroke_width = stroke_width
        self.stroke_color = stroke_color
        self.fill_color = fill_color
        self.background = background
        self.padding = padding
        self.show_debug = show_debug
        self.num_hexagons = num_hexagons
        self.num_chains = num_chains
        
        self.grid = {}
        self.injected_hexagons = []
    
    def _axial_to_pixel(self, q, r):
        x = self.hex_size * (math.sqrt(3) * q + math.sqrt(3)/2 * r)
        y = self.hex_size * (3/2 * r)
        return x, y
    
    def _hex_corners(self, cx, cy):
        corners = []
        for i in range(6):
            angle = math.pi / 3 * i + math.pi / 6
            x = cx + self.hex_size * math.cos(angle)
            y = cy + self.hex_size * math.sin(angle)
            corners.append((x, y))
        return corners
    
    def generate(self, seed=None):
        if seed is not None:
            random.seed(seed)
        
        self.grid = {}
        
        q_range = self.grid_cols
        r_range = self.grid_rows
        
        for r in range(-r_range//2, r_range//2 + 1):
            r_offset = r // 2
            q_start = -q_range//2 - r_offset
            q_end = q_range//2 - r_offset
            for q in range(q_start, q_end + 1):
                orientation = random.randint(0, 5)
                self.grid[(q, r)] = orientation
        
        all_cells = list(self.grid.keys())
        
        self.injected_hexagons = []
        used_cells = set()
        
        for _ in range(self.num_hexagons):
            attempts = 0
            while attempts < 50 and all_cells:
                center = random.choice(all_cells)
                center_q, center_r = center
                
                hexagon_cells = [
                    (center_q, center_r - 1),
                    (center_q + 1, center_r - 1),
                    (center_q + 1, center_r),
                    (center_q, center_r + 1),
                    (center_q - 1, center_r + 1),
                    (center_q - 1, center_r)
                ]
                
                if center in self.grid and all(cell in self.grid and cell not in used_cells for cell in hexagon_cells):
                    self._inject_hexagon(center_q, center_r)
                    self.injected_hexagons.append(center)
                    used_cells.update(hexagon_cells)
                    used_cells.add(center)
                    del self.grid[center]
                    break
                
                attempts += 1
        
        for _ in range(self.num_chains):
            if all_cells:
                start = random.choice(all_cells)
                chain_length = random.randint(3, 8)
                self._inject_chain(start[0], start[1], chain_length)
    
    def _get_neighbors(self, q, r):
        directions = [
            (1, 0), (1, -1), (0, -1),
            (-1, 0), (-1, 1), (0, 1)
        ]
        neighbors = []
        for dq, dr in directions:
            neighbor = (q + dq, r + dr)
            if neighbor in self.grid:
                neighbors.append(neighbor)
        return neighbors
    
    def _get_shared_edge(self, cell1, cell2):
        q1, r1 = cell1
        q2, r2 = cell2
        
        dq = q2 - q1
        dr = r2 - r1
        
        edge_map = {
            (1, 0): [(0, 2), (5, 3)],
            (1, -1): [(4, 2), (5, 1)],
            (0, -1): [(3, 1), (4, 0)],
            (-1, 0): [(2, 0), (3, 5)],
            (-1, 1): [(1, 5), (2, 4)],
            (0, 1): [(0, 4), (1, 3)]
        }
        
        return edge_map.get((dq, dr))
    
    def _are_connected(self, cell1, cell2):
        orientation1 = self.grid.get(cell1)
        orientation2 = self.grid.get(cell2)
        
        shared_corners = self._get_shared_edge(cell1, cell2)
        if shared_corners is None:
            return False
        
        edge1_corners = {orientation1, (orientation1 + 1) % 6}
        edge2_corners = {orientation2, (orientation2 + 1) % 6}
        
        for c1_corner, c2_corner in shared_corners:
            if c1_corner in edge1_corners and c2_corner in edge2_corners:
                return True
        
        return False
    
    def _inject_hexagon(self, center_q, center_r):
        hexagon_cells = [
            (center_q, center_r - 1),
            (center_q + 1, center_r - 1),
            (center_q + 1, center_r),
            (center_q, center_r + 1),
            (center_q - 1, center_r + 1),
            (center_q - 1, center_r)
        ]
        
        orientations = [0, 1, 2, 3, 4, 5]
        
        for cell, orientation in zip(hexagon_cells, orientations):
            if cell in self.grid:
                self.grid[cell] = orientation
    
    def _inject_chain(self, start_q, start_r, length):
        directions = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
        
        current = (start_q, start_r)
        path = [current]
        
        for _ in range(length - 1):
            valid_neighbors = []
            for i, (dq, dr) in enumerate(directions):
                neighbor = (current[0] + dq, current[1] + dr)
                if neighbor in self.grid and neighbor not in path:
                    valid_neighbors.append((neighbor, i))
            
            if not valid_neighbors:
                break
            
            next_cell, direction = random.choice(valid_neighbors)
            path.append(next_cell)
            current = next_cell
        
        if len(path) >= 2:
            for i in range(len(path) - 1):
                cell1 = path[i]
                cell2 = path[i + 1]
                
                dq = cell2[0] - cell1[0]
                dr = cell2[1] - cell1[1]
                
                direction_map = {
                    (1, 0): 0,
                    (1, -1): 5,
                    (0, -1): 4,
                    (-1, 0): 3,
                    (-1, 1): 2,
                    (0, 1): 1
                }
                
                if (dq, dr) in direction_map:
                    self.grid[cell1] = direction_map[(dq, dr)]
            
            last_dq = path[-1][0] - path[-2][0]
            last_dr = path[-1][1] - path[-2][1]
            reverse_direction_map = {
                (1, 0): 3,
                (1, -1): 2,
                (0, -1): 1,
                (-1, 0): 0,
                (-1, 1): 5,
                (0, 1): 4
            }
            if (last_dq, last_dr) in reverse_direction_map:
                self.grid[path[-1]] = reverse_direction_map[(last_dq, last_dr)]
    
    def _find_connected_components(self):
        visited = set()
        components = []
        
        for cell in self.grid:
            if cell in visited:
                continue
            
            component = set()
            queue = [cell]
            
            while queue:
                current = queue.pop(0)
                if current in visited:
                    continue
                
                visited.add(current)
                component.add(current)
                
                neighbors = self._get_neighbors(current[0], current[1])
                for neighbor in neighbors:
                    if neighbor not in visited and self._are_connected(current, neighbor):
                        queue.append(neighbor)
            
            components.append(component)
        
        return components
    
    def _has_dangling_edges(self, component):
        corner_usage = {}
        
        for q, r in component:
            orientation = self.grid[(q, r)]
            cx, cy = self._axial_to_pixel(q, r)
            corners = self._hex_corners(cx, cy)
            
            c1 = corners[orientation]
            c2 = corners[(orientation + 1) % 6]
            
            c1_key = (round(c1[0], 2), round(c1[1], 2))
            c2_key = (round(c2[0], 2), round(c2[1], 2))
            
            corner_usage[c1_key] = corner_usage.get(c1_key, 0) + 1
            corner_usage[c2_key] = corner_usage.get(c2_key, 0) + 1
        
        for count in corner_usage.values():
            if count == 1:
                return True
        
        return False
    
    def _is_hexagon(self, component):
        if len(component) != 6:
            return False
        
        if self._has_dangling_edges(component):
            return False
        
        corner_usage = {}
        for q, r in component:
            orientation = self.grid[(q, r)]
            cx, cy = self._axial_to_pixel(q, r)
            corners = self._hex_corners(cx, cy)
            
            c1 = corners[orientation]
            c2 = corners[(orientation + 1) % 6]
            
            c1_key = (round(c1[0], 2), round(c1[1], 2))
            c2_key = (round(c2[0], 2), round(c2[1], 2))
            
            corner_usage[c1_key] = corner_usage.get(c1_key, 0) + 1
            corner_usage[c2_key] = corner_usage.get(c2_key, 0) + 1
        
        if len(corner_usage) != 6:
            return False
        
        for count in corner_usage.values():
            if count != 2:
                return False
        
        return True
    
    def to_svg(self):
        min_x = min_y = float('inf')
        max_x = max_y = float('-inf')
        
        for q, r in self.grid:
            cx, cy = self._axial_to_pixel(q, r)
            min_x = min(min_x, cx - self.hex_size)
            max_x = max(max_x, cx + self.hex_size)
            min_y = min(min_y, cy - self.hex_size)
            max_y = max(max_y, cy + self.hex_size)
        
        width = max_x - min_x
        height = max_y - min_y
        offset_x = -min_x
        offset_y = -min_y
        
        canvas_width = width + 2 * self.padding
        canvas_height = height + 2 * self.padding
        
        svg_parts = [f'<svg width="{canvas_width}" height="{canvas_height}" xmlns="http://www.w3.org/2000/svg">']
        if self.background != 'transparent':
            svg_parts.append(f'<rect width="{canvas_width}" height="{canvas_height}" fill="{self.background}"/>')
        svg_parts.append(f'<g transform="translate({self.padding + offset_x}, {self.padding + offset_y})">')
        
        # Always draw pale hexagon grid outlines
        for q, r in self.grid:
            cx, cy = self._axial_to_pixel(q, r)
            corners = self._hex_corners(cx, cy)
            
            hex_path = 'M ' + ' L '.join([f'{x},{y}' for x, y in corners]) + ' Z'
            svg_parts.append(f'<path d="{hex_path}" fill="none" stroke="#d0d0d0" stroke-width="1" opacity="0.4"/>')
        
        # Draw perpendicular lines from center to edge midpoint (pale, below main segments)
        dot_radius = self.stroke_width * 0.3
        pale_color = "#d0d0d0"
        
        for (q, r), orientation in self.grid.items():
            cx, cy = self._axial_to_pixel(q, r)
            corners = self._hex_corners(cx, cy)
            
            p1 = corners[orientation]
            p2 = corners[(orientation + 1) % 6]
            edge_midpoint = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
            
            # Perpendicular line (pale)
            svg_parts.append(f'<line x1="{cx}" y1="{cy}" x2="{edge_midpoint[0]}" y2="{edge_midpoint[1]}" stroke="{pale_color}" stroke-width="1" opacity="0.4"/>')
            
            # Pale dots at both ends
            svg_parts.append(f'<circle cx="{cx}" cy="{cy}" r="{dot_radius}" fill="{pale_color}" opacity="0.4"/>')
            svg_parts.append(f'<circle cx="{edge_midpoint[0]}" cy="{edge_midpoint[1]}" r="{dot_radius}" fill="{pale_color}" opacity="0.4"/>')
        
        # Count corner usage to find intersection points
        corner_usage = {}
        corner_positions = {}
        
        for (q, r), orientation in self.grid.items():
            cx, cy = self._axial_to_pixel(q, r)
            corners = self._hex_corners(cx, cy)
            
            p1 = corners[orientation]
            p2 = corners[(orientation + 1) % 6]
            
            c1_key = (round(p1[0], 2), round(p1[1], 2))
            c2_key = (round(p2[0], 2), round(p2[1], 2))
            
            corner_usage[c1_key] = corner_usage.get(c1_key, 0) + 1
            corner_usage[c2_key] = corner_usage.get(c2_key, 0) + 1
            corner_positions[c1_key] = p1
            corner_positions[c2_key] = p2
        
        # Draw all segments as hollow capsules
        
        for (q, r), orientation in self.grid.items():
            cx, cy = self._axial_to_pixel(q, r)
            corners = self._hex_corners(cx, cy)
            
            p1 = corners[orientation]
            p2 = corners[(orientation + 1) % 6]
            
            # Edge capsule
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            length = math.sqrt(dx*dx + dy*dy)
            ux = dx / length
            uy = dy / length
            
            cap_radius = self.stroke_width / 2
            border_width = max(1.5, self.stroke_width / 8)
            
            perp_x = -uy
            perp_y = ux
            
            half_width = self.stroke_width / 2
            
            corner1 = (p1[0] + perp_x * half_width, p1[1] + perp_y * half_width)
            corner2 = (p1[0] - perp_x * half_width, p1[1] - perp_y * half_width)
            corner3 = (p2[0] - perp_x * half_width, p2[1] - perp_y * half_width)
            corner4 = (p2[0] + perp_x * half_width, p2[1] + perp_y * half_width)
            
            path = f'M {corner1[0]},{corner1[1]} A {cap_radius},{cap_radius} 0 0,1 {corner2[0]},{corner2[1]} L {corner3[0]},{corner3[1]} A {cap_radius},{cap_radius} 0 0,1 {corner4[0]},{corner4[1]} Z'
            
            svg_parts.append(f'<path d="{path}" fill="none" stroke="{self.stroke_color}" stroke-width="{border_width}"/>')
        
        # Draw white dots at intersection points (2 or 3 segments)
        dot_radius = self.stroke_width * 0.3
        for corner_key, count in corner_usage.items():
            if count >= 2:
                pos = corner_positions[corner_key]
                svg_parts.append(f'<circle cx="{pos[0]}" cy="{pos[1]}" r="{dot_radius}" fill="white"/>')
        
        svg_parts.append('</g>')
        svg_parts.append('</svg>')
        return '\n'.join(svg_parts)
    
    def validate_connectivity(self):
        errors = 0
        checked = set()
        
        for cell in self.grid:
            
            neighbors = self._get_neighbors(cell[0], cell[1])
            
            for neighbor in neighbors:
                if neighbor not in self.grid:
                    continue
                
                pair = tuple(sorted([cell, neighbor]))
                if pair in checked:
                    continue
                checked.add(pair)
                
                shared_edges = self._get_shared_edge(cell, neighbor)
                if shared_edges is None:
                    print(f"Error: No shared edge found between {cell} and {neighbor}")
                    errors += 1
                    continue
                
                cx1, cy1 = self._axial_to_pixel(cell[0], cell[1])
                corners1 = self._hex_corners(cx1, cy1)
                
                cx2, cy2 = self._axial_to_pixel(neighbor[0], neighbor[1])
                corners2 = self._hex_corners(cx2, cy2)
                
                for edge1, edge2 in shared_edges:
                    p1 = corners1[edge1]
                    p2 = corners2[edge2]
                    
                    dist = math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
                    if dist > 0.1:
                        print(f"Error: Corners {edge1} of {cell} and {edge2} of {neighbor} don't match: distance={dist:.3f}")
                        print(f"  {cell} corner {edge1}: {p1}")
                        print(f"  {neighbor} corner {edge2}: {p2}")
                        errors += 1
        
        if errors > 0:
            print(f"Validation FAILED: {errors} connectivity errors found.")
        else:
            print(f"Validation PASSED: All connections are valid.")
        
        return errors == 0
    
    def calculate_connectivity_score(self):
        components = self._find_connected_components()
        
        if not components:
            return 0
        
        total_cells = len(self.grid)
        if total_cells == 0:
            return 0
        
        hexagons = [c for c in components if self._is_hexagon(c)]
        large_closed = [c for c in components if len(c) > 6 and not self._has_dangling_edges(c)]
        
        hexagon_count = len(hexagons)
        hexagon_cells = sum(len(c) for c in hexagons)
        large_closed_cells = sum(len(c) for c in large_closed)
        
        total_connected = hexagon_cells + large_closed_cells
        
        if total_connected == 0:
            return 0
        
        hexagon_bonus = hexagon_count * 10
        connectivity_ratio = total_connected / total_cells
        
        score = connectivity_ratio * 100 + hexagon_bonus
        
        return score


if __name__ == '__main__':
    print("Generating 50 lattices with long-tailed hexagon distribution...")
    
    import os
    os.makedirs('outputs', exist_ok=True)
    
    for i in range(50):
        random.seed(i * 1000)
        
        # Long-tailed distribution: slightly more hexagons, still favor lower counts
        rand_val = random.random()
        if rand_val < 0.25:
            num_hexagons = 0
        elif rand_val < 0.55:
            num_hexagons = 1
        elif rand_val < 0.75:
            num_hexagons = 2
        elif rand_val < 0.9:
            num_hexagons = 3
        else:
            num_hexagons = 4
        
        num_chains = random.randint(0, 2)
        
        gen = LatticeGenerator(
            grid_rows=12,
            grid_cols=15,
            hex_size=50,
            stroke_width=16,
            show_debug=False,
            num_hexagons=num_hexagons,
            num_chains=num_chains
        )
        gen.generate(seed=i)
        
        svg = gen.to_svg()
        
        components = gen._find_connected_components()
        hexagons = [c for c in components if gen._is_hexagon(c)]
        large_closed = [c for c in components if len(c) > 6 and not gen._has_dangling_edges(c)]
        
        hexagon_count = len(hexagons)
        total_connected = sum(len(c) for c in hexagons) + sum(len(c) for c in large_closed)
        
        filename = f'outputs/lattice_{i}.svg'
        with open(filename, 'w') as f:
            f.write(svg)
        
        print(f"  #{i+1}: seed={i}, hexagons={hexagon_count}, connected_cells={total_connected}, saved as {filename}")
    
    print("\n✓ Generated 50 lattices directly.")



