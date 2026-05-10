#!/usr/bin/env python3
"""
Simple icon generator that creates basic PNG files without external dependencies
Uses only standard library
"""

import base64
import os

# Simple PNG images encoded as base64
# These are minimal 16x16, 48x48, and 128x128 px icons

# 16x16 blue square with white arrow
ICON_16 = base64.b64decode(
    'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAAdgAAAHYBTnsmCAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAFGSURBVDiNpZM/S8NQFMXPvY+kJTUYnFyK4CYodDGDxUHcnPwEfoC+gB/Az+Dq4CI4uAiCm4ODg0sdRBEpOLiUxqG0aZI3XIdSQ1v/4MCDO/yee+8590H4R0QEAGBmZGYAQEQ+AACIiAjAzBARRITPQkQQEZgZzIyIiNAcRASllBIR5JwrwHsCnHMiIsg5V/wAEZEiAjN7IuIDACilmBkRcQFgAQAzQ0R8ABCRaVmWZQCAUgoAsG3bM03TtCzbsm0bcM4BAJRSNy/3pmmqpmkq0FsAAOecaprGAgARmSql1vddp+t6H8CZMWYaEVFKKWZGQH9EhJl7AJpmHYZh0TSNAYAPADVjzJRSip1zpud5PsMweFk+QFVVURiGZhAE7wB87YxRvufFe73+aL/nj7TWZ0mSXD8/lS/1+vJCa302GU8+vgCMm2uJf01oDgAAAABJRU5ErkJggg=='
)

# 48x48 blue circle with white arrow
ICON_48 = base64.b64decode(
    'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAAdgAAAHYBTnsmCAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAQBSURBVGiB7ZlLaBNRFIa/mSSxSdPEF75QxUoRXPigFBd1oRtFcOXChW5cuHAhuhEXggtBEAQXPqrUhQtRXKgLQRBEBLWIihpfYH2gVVtrrU2aNMlkXEySmUnSNCYzmcL8EJjMnXvuuf+dc+69M3NAo9FoNBqNRqPRaDQazX+JaHUCn59/IYqKSJLEQGfkZNWcc+cm08k+w6zr9/sQQpBIJBgZGaG7u5sPHz7Q1dVFb28vfr+fYDBIOBwmGo3S09PD4OAgU1NTxONx+vr62NjYYHJykq2tLWKxGMFgEMuyiMViWJaF0+lkfX2dYDBIKBRienqacDhMJBJhdnYW0zSJRqMsLCywvLyMZVkYhsHy8jKRSCTt8Wb8o7IM/sP797x79865srLS3N7eNru7u8033d3db1+9ehXv7e01P378aH769Mm8ffu2+ezZM3N5edn8/Pmz+fTpU/Pjx4/m6uqq+fHjR/PVq1fmq1evzMePH5svX740Hz58aL5588Z8/vy5+erVK/PBgwfmvXv3zDt37ph37941Hz16ZJ49e9b09/ebgUDA/PDhg3nr1i3zxo0b5s2bN82nT5+mPN7MZL0VfTBw/cbt69enKioqGmtra4/HYrFm0zRpa2vj5MmTAAwPD+NyuWhsbOT8+fMATE5O0tHRwdGjR5menqarq4uuri5mZmaoqamhrKyMwcFB6uvrKSsrY3R0lAMHDlBZWcnExASHDh2ivLyc8fFx2tvb8fl8jI2N0d7eTklJCaOjo3R0dFBcXMzIyAhdXV0UFRUxNDREX18fwWCQgYEBAgEBLKQ83syqH/3zj/HCQ4ecwLYQoktEjorIERFpFZEWEWkWkUYRqRORGhGpEpEKESkXkTIRKRERr4h4RMQtIoUisldE8kUkT0RyRSRHRLJFJEtEMkUkQ0TSfrdDRNJEJFVEUkTEISIyp99lbFciknbpEPt+1aeycLmI+ffv93wBfAe+7mhgV9XtaiFj5n+s70IzDV0ATXkzYvLzXP+AlByNAJZQqRiQDXiyEsiIBTwFPXV1xbsN4F9A2G8rAOAH/gLj2QmQImvLnT4h6gCx2xcvlgB/gE/AFFCSrfJJOV0OwAv8EZHXwCTwGPgADANfspV+p2xRNpKfWAJMAuPAGPAb+AW8t///Y5u4tJQdB1wCXAKMAb+BMWAEGLb//wWMZqu8TYYjX+UkgBewgBHgOzAEDNr/f8lWeZsMk9+RI0C+iOSJSI6IZIlIpv1XICJuEXGJiFNEHCKSKiIpIuIQEalMYBp/lxS+A7bZzrb1f76fW8pqNBqNRqPRaDQajUaj0Wg0Go1Go9FoNBqNRqPRaDQajUaj0Wg0Go1Go9FoNBrN/8Q/2y/Q/MpQr+0AAAAASUVORK5CYII='
)

# 128x128 blue circle with white arrow
ICON_128 = base64.b64decode(
    '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'
)

def create_icons():
    """Create icon files from base64 data"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    icons = [
        ('icon16.png', ICON_16),
        ('icon48.png', ICON_48),
        ('icon128.png', ICON_128)
    ]
    
    print("Creating browser extension icons...")
    print()
    
    for filename, data in icons:
        filepath = os.path.join(script_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(data)
        print(f"✓ Created {filename}")
    
    print()
    print("Icons created successfully!")
    print()
    print("These are basic placeholder icons.")
    print("For better quality icons, you can:")
    print("  1. Use ImageMagick: ./generate-icons.sh")
    print("  2. Create custom icons with a graphics editor")
    print("  3. Use icon generation services online")

if __name__ == '__main__':
    create_icons()
