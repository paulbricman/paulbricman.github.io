import random
import math


class StreamsGenerator:
    def __init__(self,
                 width=700,
                 height=280,
                 num_lines=40,
                 steps=250,
                 step_size=3.5,
                 noise_scale=0.0035,
                 stroke_width=1.2,
                 stroke_color='white',
                 background='transparent',
                 padding=0):
        self.width = width
        self.height = height
        self.num_lines = num_lines
        self.steps = steps
        self.step_size = step_size
        self.noise_scale = noise_scale
        self.stroke_width = stroke_width
        self.stroke_color = stroke_color
        self.background = background
        self.padding = padding
        self.streamlines = []
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

    def _octave_noise(self, x, y, octaves=3, persistence=0.5):
        total = 0
        frequency = 1
        amplitude = 1
        max_value = 0
        for _ in range(octaves):
            total += self._noise(x * frequency, y * frequency) * amplitude
            max_value += amplitude
            amplitude *= persistence
            frequency *= 2
        return total / max_value

    def _flow_angle(self, x, y):
        n = self._octave_noise(x * self.noise_scale, y * self.noise_scale)
        return n * math.pi * 4

    def _trace(self, sx, sy):
        points = []
        x, y = sx, sy
        margin = 20
        for _ in range(self.steps):
            if x < -margin or x > self.width + margin:
                break
            if y < -margin or y > self.height + margin:
                break
            points.append((x, y))
            angle = self._flow_angle(x, y)
            x += math.cos(angle) * self.step_size
            y += math.sin(angle) * self.step_size
        return points

    def generate(self, seed=None):
        self._init_permutation(seed if seed is not None else 0)
        self.streamlines = []

        cols = 32
        rows = 22
        for row in range(rows):
            for col in range(cols):
                jx = random.uniform(-0.2, 0.2) * (self.width / cols)
                jy = random.uniform(-0.2, 0.2) * (self.height / rows)
                sx = (col + 0.5) / cols * self.width + jx
                sy = (row + 0.5) / rows * self.height + jy
                pts = self._trace(sx, sy)
                if len(pts) > 4:
                    self.streamlines.append(pts)

        extra = self.num_lines - len(self.streamlines)
        for _ in range(max(0, extra)):
            sx = random.uniform(0, self.width)
            sy = random.uniform(0, self.height)
            pts = self._trace(sx, sy)
            if len(pts) > 4:
                self.streamlines.append(pts)

    def _points_to_smooth_path(self, points):
        if len(points) < 2:
            return ''
        d = f'M {round(points[0][0])},{round(points[0][1])}'
        for pt in points[1:]:
            d += f' L {round(pt[0])},{round(pt[1])}'
        return d

    def to_svg(self):
        canvas_w = self.width + 2 * self.padding
        canvas_h = self.height + 2 * self.padding

        parts = [f'<svg width="{canvas_w}" height="{canvas_h}" xmlns="http://www.w3.org/2000/svg">']
        if self.background != 'transparent':
            parts.append(f'<rect width="{canvas_w}" height="{canvas_h}" fill="{self.background}"/>')

        clip_id = 'clip_field'
        parts.append(f'<defs><clipPath id="{clip_id}"><rect x="0" y="0" width="{self.width}" height="{self.height}"/></clipPath></defs>')
        parts.append(f'<g transform="translate({self.padding},{self.padding})" clip-path="url(#{clip_id})">')

        for pts in self.streamlines:
            d = self._points_to_smooth_path(pts)
            if d:
                parts.append(f'<path d="{d}" fill="none" stroke="{self.stroke_color}" stroke-width="{self.stroke_width}" opacity="0.55"/>')

        parts.append('</g>')
        parts.append('</svg>')
        return '\n'.join(parts)


def _score(streamlines, width, height):
    if not streamlines:
        return 0
    total_len = sum(len(s) for s in streamlines)
    coverage_score = min(total_len / (width * height / 100), 1.0)
    count_score = min(len(streamlines) / 35, 1.0)
    return coverage_score * 0.6 + count_score * 0.4


if __name__ == '__main__':
    import os
    os.makedirs('outputs', exist_ok=True)

    print("Generating 50 landscape stream patterns...")
    for i in range(50):
        gen = StreamsGenerator(
            width=700,
            height=280,
            num_lines=1200,
            steps=55,
            step_size=4.5,
            noise_scale=0.0035,
            stroke_width=0.22,
        )
        gen.generate(seed=i)
        svg = gen.to_svg()
        filename = f'outputs/stream_{i}.svg'
        with open(filename, 'w') as f:
            f.write(svg)
        score = _score(gen.streamlines, 700, 280)
        print(f"  #{i}: seed={i}, lines={len(gen.streamlines)}, score={score:.3f}, saved as {filename}")

    os.makedirs('curated', exist_ok=True)
    print("\nGenerating portrait cover stream...")
    cover = StreamsGenerator(
        width=350,
        height=495,
        num_lines=1200,
        steps=55,
        step_size=4.5,
        noise_scale=0.0035,
        stroke_width=0.22,
    )
    cover.generate(seed=3)
    cover_svg = cover.to_svg()
    with open('curated/stream_cover.svg', 'w') as f:
        f.write(cover_svg)
    print("  Saved curated/stream_cover.svg")

    print("\nDone.")
