from PIL import Image, ImageDraw

data = '''25 31 32 36 37 40 43 44 45 46 47 55 56 57 58 59 61 69 98 106 120 129 138 139 140 143 144
25 30 35 43 59 61 68 69 97 98 106 120 128 129 137 141 145
0 1 3 7 8 9 13 14 15 19 20 21 24 25 26 29 30 31 35 39 40 43 44 45 46 58 61 62 63 64 69 74 75 76 77 86 87 88 89 91 93 94 98 103 104 105 106 115 116 117 120 121 122 123 127 129 132 134 135 141 145
0 2 4 6 10 12 16 18 25 30 35 40 47 57 61 65 69 73 85 89 91 92 98 102 106 114 120 124 126 129 132 133 140 145
0 2 4 6 10 12 13 14 15 16 18 25 30 34 35 40 47 57 61 65 69 74 75 76 85 89 91 98 102 106 114 120 124 126 127 128 129 130 132 139 145 146
0 2 4 6 10 12 18 25 30 35 40 43 47 56 61 65 69 77 86 87 88 89 91 98 102 106 114 120 124 129 132 145
0 2 4 7 8 9 13 14 15 19 20 21 26 27 30 35 39 40 41 44 45 46 56 61 65 68 69 70 73 74 75 76 89 91 97 98 99 103 104 105 106 115 116 117 120 124 129 132 139 145
35 85 89 145
36 37 49 50 51 52 53 79 80 81 82 83 86 87 88 108 109 110 111 112 143 144'''

rows = [set(map(int, line.split())) for line in data.splitlines()]
width = max(max(row) for row in rows) + 1
scale = 12
im = Image.new('RGB', (width * scale, len(rows) * scale), 'white')
draw = ImageDraw.Draw(im)
for y, row in enumerate(rows):
    for x in row:
        draw.rectangle((x*scale, y*scale, (x+1)*scale-1, (y+1)*scale-1), fill='black')
im.save('pixel_flag.png')

# Three sections retain the original order and make small characters easier to read.
out = Image.new('RGB', (1000, 650), 'white')
od = ImageDraw.Draw(out)
for section, (start, end) in enumerate([(0, 49), (49, 98), (98, 147)]):
    top = 30 + section * 205
    od.text((20, top), f'x = {start}..{end-1} (day 1 at top)', fill='black')
    for y, row in enumerate(rows):
        for x in range(start, end):
            left = 20 + (x-start)*19
            yy = top+25+y*19
            od.rectangle((left, yy, left+18, yy+18), fill='black' if x in row else 'white', outline='#dddddd')
out.save('pixel_grid.png')
print('Rendered', width, 'columns and', len(rows), 'rows')
