import random
import math

class FieldGenerator:
    def __init__(self,
                 width=80,
                 height=40,
                 scale=0.1,
                 octaves=3,
                 persistence=0.5,
                 threshold=0.5,
                 char_size=12,
                 stroke_color='white',
                 background='transparent',
                 padding=40):
        self.width = width
        self.height = height
        self.scale = scale
        self.octaves = octaves
        self.persistence = persistence
        self.threshold = threshold
        self.char_size = char_size
        self.stroke_color = stroke_color
        self.background = background
        self.padding = padding
        self.field = []
        self.permutation = []
    
    def _init_permutation(self, seed):
        random.seed(seed)
        p = list(range(256))
        random.shuffle(p)
        self.permutation = p + p
    
    def _fade(self, t):
        return t * t * t * (t * (t * 6 - 15) + 10)
    
    def _lerp(self, t, a, b):
        return a + t * (b - a)
    
    def _grad(self, hash_val, x, y):
        h = hash_val & 3
        u = x if h < 2 else y
        v = y if h < 2 else x
        return (u if (h & 1) == 0 else -u) + (v if (h & 2) == 0 else -v)
    
    def _noise(self, x, y):
        X = int(math.floor(x)) & 255
        Y = int(math.floor(y)) & 255
        
        x -= math.floor(x)
        y -= math.floor(y)
        
        u = self._fade(x)
        v = self._fade(y)
        
        A = self.permutation[X] + Y
        B = self.permutation[X + 1] + Y
        
        return self._lerp(v,
            self._lerp(u, self._grad(self.permutation[A], x, y),
                         self._grad(self.permutation[B], x - 1, y)),
            self._lerp(u, self._grad(self.permutation[A + 1], x, y - 1),
                         self._grad(self.permutation[B + 1], x - 1, y - 1)))
    
    def _octave_noise(self, x, y):
        total = 0
        frequency = 1
        amplitude = 1
        max_value = 0
        
        for _ in range(self.octaves):
            total += self._noise(x * frequency, y * frequency) * amplitude
            max_value += amplitude
            amplitude *= self.persistence
            frequency *= 2
        
        return total / max_value
    
    def generate(self, seed=None):
        if seed is not None:
            self._init_permutation(seed)
        else:
            self._init_permutation(0)
        
        self.field = []
        
        for y in range(self.height):
            row = []
            for x in range(self.width):
                noise_val = self._octave_noise(x * self.scale, y * self.scale)
                noise_val = (noise_val + 1) / 2
                
                char = '1' if noise_val > self.threshold else '0'
                row.append(char)
            self.field.append(row)
    
    def to_svg(self):
        char_width = self.char_size * 0.6
        canvas_width = self.width * char_width
        canvas_height = self.height * self.char_size
        
        svg_parts = [f'<svg width="{canvas_width}" height="{canvas_height}" xmlns="http://www.w3.org/2000/svg">']
        if self.background != 'transparent':
            svg_parts.append(f'<rect width="{canvas_width}" height="{canvas_height}" fill="{self.background}"/>')
        
        svg_parts.append('<g>')
        svg_parts.append(f'<style>text {{ font-family: "Consolas", "Lucida Console", "DejaVu Sans Mono", monospace; font-size: {self.char_size}px; fill: {self.stroke_color}; font-weight: 900; letter-spacing: 0.05em; }}</style>')
        
        for y, row in enumerate(self.field):
            text = ''.join(row)
            y_pos = (y + 1) * self.char_size
            svg_parts.append(f'<text x="0" y="{y_pos}">{text}</text>')
        
        svg_parts.append('</g>')
        svg_parts.append('</svg>')
        return '\n'.join(svg_parts)


if __name__ == '__main__':
    print("Generating 50 field patterns...")
    
    import os
    os.makedirs('outputs', exist_ok=True)
    
    for i in range(50):
        gen = FieldGenerator(
            width=100,
            height=25,
            scale=0.08,
            octaves=3,
            persistence=0.5,
            threshold=0.5,
            char_size=12
        )
        gen.generate(seed=i)
        
        svg = gen.to_svg()
        
        filename = f'outputs/field_{i}.svg'
        with open(filename, 'w') as f:
            f.write(svg)
        
        print(f"  #{i+1}: seed={i}, saved as {filename}")
    
    print("\n✓ Generated 50 field patterns.")

