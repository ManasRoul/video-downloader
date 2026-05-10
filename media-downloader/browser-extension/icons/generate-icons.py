#!/usr/bin/env python3
"""
Icon generator script - Creates placeholder PNG icons if ImageMagick is not available
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, output_file):
    """Create a simple download icon"""
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Colors
    bg_color = (33, 150, 243, 255)  # Blue
    fg_color = (255, 255, 255, 255)  # White
    accent_color = (255, 87, 34, 255)  # Orange-red
    
    # Draw background circle
    margin = size // 10
    draw.ellipse(
        [margin, margin, size - margin, size - margin],
        fill=bg_color
    )
    
    # Draw download arrow
    center_x = size // 2
    arrow_width = size // 10
    arrow_top = size // 4
    arrow_bottom = size * 5 // 8
    
    # Arrow shaft
    draw.rectangle(
        [center_x - arrow_width // 2, arrow_top, 
         center_x + arrow_width // 2, arrow_bottom],
        fill=fg_color
    )
    
    # Arrow head
    arrow_head_width = size // 3
    arrow_points = [
        (center_x, arrow_bottom + size // 8),  # tip
        (center_x - arrow_head_width // 2, arrow_bottom),  # left
        (center_x + arrow_head_width // 2, arrow_bottom),  # right
    ]
    draw.polygon(arrow_points, fill=fg_color)
    
    # Draw base line
    base_y = size * 7 // 8
    draw.rectangle(
        [size // 4, base_y - size // 20,
         size * 3 // 4, base_y + size // 20],
        fill=fg_color
    )
    
    # Draw small play button indicator
    play_size = size // 4
    play_x = size * 3 // 4
    play_y = size // 4
    draw.ellipse(
        [play_x - play_size // 2, play_y - play_size // 2,
         play_x + play_size // 2, play_y + play_size // 2],
        fill=accent_color
    )
    
    # Play triangle
    play_offset = play_size // 4
    play_triangle = [
        (play_x - play_offset // 2, play_y - play_offset),
        (play_x - play_offset // 2, play_y + play_offset),
        (play_x + play_offset, play_y)
    ]
    draw.polygon(play_triangle, fill=fg_color)
    
    # Save
    img.save(output_file, 'PNG')
    print(f"Created {output_file}")

def main():
    """Generate all icon sizes"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("Generating PNG icons...")
    print("(Using Python/Pillow as fallback)")
    print()
    
    try:
        create_icon(16, os.path.join(script_dir, 'icon16.png'))
        create_icon(48, os.path.join(script_dir, 'icon48.png'))
        create_icon(128, os.path.join(script_dir, 'icon128.png'))
        print()
        print("✓ Icons generated successfully!")
    except Exception as e:
        print(f"Error: {e}")
        print()
        print("Please install Pillow: pip3 install Pillow")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
