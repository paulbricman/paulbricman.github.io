#!/usr/bin/env python3

import os
import subprocess
from pathlib import Path

TARGET_COLOR = "#228B22"

curated_dir = Path("curated")
output_dir = Path("rasterized")
temp_dir = Path("temp_colored")

output_dir.mkdir(exist_ok=True)
temp_dir.mkdir(exist_ok=True)

svg_files = sorted(curated_dir.glob("lattice_*.svg"))

if not svg_files:
    print("No SVG files found in curated/ directory")
    exit(1)

try:
    subprocess.run(["rsvg-convert", "--version"], capture_output=True, check=True)
except (FileNotFoundError, subprocess.CalledProcessError):
    print("Error: rsvg-convert not found. Install with: brew install librsvg")
    exit(1)

print(f"Rasterizing {len(svg_files)} SVG files at 300 DPI with color {TARGET_COLOR}...")

for svg_path in svg_files:
    with open(svg_path, 'r') as f:
        svg_content = f.read()
    
    svg_content = svg_content.replace('stroke="white"', f'stroke="{TARGET_COLOR}"')
    svg_content = svg_content.replace('fill="white"', f'fill="{TARGET_COLOR}"')
    svg_content = svg_content.replace('stroke="White"', f'stroke="{TARGET_COLOR}"')
    svg_content = svg_content.replace('fill="White"', f'fill="{TARGET_COLOR}"')
    svg_content = svg_content.replace('stroke="#fff"', f'stroke="{TARGET_COLOR}"')
    svg_content = svg_content.replace('fill="#fff"', f'fill="{TARGET_COLOR}"')
    svg_content = svg_content.replace('stroke="#ffffff"', f'stroke="{TARGET_COLOR}"')
    svg_content = svg_content.replace('fill="#ffffff"', f'fill="{TARGET_COLOR}"')
    svg_content = svg_content.replace('stroke="#FFF"', f'stroke="{TARGET_COLOR}"')
    svg_content = svg_content.replace('fill="#FFF"', f'fill="{TARGET_COLOR}"')
    svg_content = svg_content.replace('stroke="#FFFFFF"', f'stroke="{TARGET_COLOR}"')
    svg_content = svg_content.replace('fill="#FFFFFF"', f'fill="{TARGET_COLOR}"')
    
    temp_svg_path = temp_dir / svg_path.name
    with open(temp_svg_path, 'w') as f:
        f.write(svg_content)
    
    png_path = output_dir / svg_path.with_suffix('.png').name
    
    try:
        subprocess.run([
            "rsvg-convert",
            "-d", "300",
            "-p", "300",
            "-o", str(png_path),
            str(temp_svg_path)
        ], check=True, capture_output=True, text=True)
        
        print(f"  ✓ Rasterized {svg_path.name} -> {png_path.name}")
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Failed to rasterize {svg_path.name}")
        print(f"    stdout: {e.stdout}")
        print(f"    stderr: {e.stderr}")

import shutil
shutil.rmtree(temp_dir)

print(f"\n✓ Successfully rasterized {len(svg_files)} SVG files to {output_dir}/ with color {TARGET_COLOR}")



