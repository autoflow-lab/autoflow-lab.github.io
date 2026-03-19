from PIL import Image, ImageDraw, ImageFont
import math

size = 512
img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Background circle (ocean blue gradient-ish)
draw.ellipse([0, 0, size, size], fill=(30, 120, 200, 255))

# Body (red-orange oval)
bx, by = size//2, size//2 + 30
draw.ellipse([bx-110, by-70, bx+110, by+70], fill=(220, 60, 30))

# Eyes (white + black)
for ex in [bx-50, bx+50]:
    draw.ellipse([ex-22, by-110, ex+22, by-66], fill=(255,255,255))
    draw.ellipse([ex-12, by-103, ex+12, by-73], fill=(20,20,20))
    # shine
    draw.ellipse([ex+2, by-100, ex+10, by-92], fill=(255,255,255))

# Smile
draw.arc([bx-35, by-75, bx+35, by-45], start=10, end=170, fill=(20,20,20), width=5)

# Claws left
draw.ellipse([bx-210, by-30, bx-130, by+40], fill=(200, 50, 20))
draw.ellipse([bx-215, by-60, bx-155, by-10], fill=(200, 50, 20))
draw.ellipse([bx-175, by-10, bx-120, by+50], fill=(200, 50, 20))

# Claws right
draw.ellipse([bx+130, by-30, bx+210, by+40], fill=(200, 50, 20))
draw.ellipse([bx+155, by-60, bx+215, by-10], fill=(200, 50, 20))
draw.ellipse([bx+120, by-10, bx+175, by+50], fill=(200, 50, 20))

# Legs (3 each side)
for i in range(3):
    angle_l = 120 + i * 20
    angle_r = 60 - i * 20
    lx = bx - 110 + 10*i
    rx = bx + 110 - 10*i
    ly = by - 20 + i * 25
    ry = by - 20 + i * 25
    draw.line([lx, ly, lx-60, ly+60], fill=(200,50,20), width=8)
    draw.line([rx, ry, rx+60, ry+60], fill=(200,50,20), width=8)

img.save("/home/node/.openclaw/workspace/scripts/crab.png")
print("Bild gespeichert!")
