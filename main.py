import time
import pyautogui as ag
import mouse
from PIL import ImageGrab
from collections import Counter

# Constants
tilesX = 23
tilesY = 15

# !!!
# ADJUST THESE VALUES BASED ON HARDWARE AND LAG
clickDelay = 0.04
startDelay = 0.40
# !!!

# To get your own coordinates, uncomment lines 21-28 and comment lines 31-32.
# Then run the program once and replace my coordinates with yours.
# Then, recomment lines 21-28 and uncomment lines 31-32.

# input("Move mouse to top left of the most top-left tile in the game board (including empty). ")
# print(ag.position())
# left, top = ag.position()
# print(left, top)
# input("Move mouse to bottom right of the most bottom-right tile ")
# print(ag.position())
# right, bottom = ag.position()
# print(right, bottom)

#Defines game coordinates
left, top = 123, 241
right, bottom = 1168, 924

windowWidth = right - left
windowHeight = bottom - top
tileWidth = windowWidth / tilesX
tileHeight = windowHeight / tilesY
ag.PAUSE = clickDelay

# Defines a dictionary of possible colors with their respective names and RGB values.
color_dict = {
    (247, 247, 247): "Empty",
    (237, 237, 237): "Empty",
    (64, 217, 66): "Green",
    (209, 125, 211): "Magenta",
    (195, 197, 197): "Gray",
    (209, 125, 39): "Brown",
    (123, 211, 211): "Cyan",
    (60, 138, 255): "Blue",
    (253, 159, 255): "Pink",
    (210, 212, 126): "Tan",
    (253, 162, 21): "Orange",
    (253, 114, 114): "Red"
}

# Mouse click wrapper for the Mouse library.
def click_mouse (x, y):
    mouse.move(x, y, absolute = True)
    mouse.click(button = 'left')

# Calculates the Euclidean distance between the input color and each possible color in the dictionary.
def closest_color(rgb_tuple):
    closest_distance = float('inf')
    closest_color_name = "Unknown"
    for color, name in color_dict.items():
        distance = sum([(a - b) ** 2 for a, b in zip(rgb_tuple, color)])
        if distance < closest_distance:
            closest_distance = distance
            closest_color_name = name
    return closest_color_name

# Captures the screen and gets color values of tiles.
def set_colors(colors_list):
    # img = ag.screenshot()
    img = ImageGrab.grab()
    for y in range(tilesY):
        for x in range(tilesX):
            colors_list[y][x] = closest_color(img.getpixel((tiles[y][x][0], tiles[y][x][1])))

def check_neighbors(color_array, current_space):
    # Defining coordinate and color variables that will be used.
    x, y = current_space
    norX = easX = souX = wesX = x
    norY = easY = souY = wesY = y
    north = east = south = west = "Edge"

    # Expands outwards until reaching the edge. Identifies all neighboring tiles and defines their color and coordinates.
    if y != 0:
        distance = 1  # distance from current space
        while distance <= y:
            if color_array[y-distance][x] == "Empty":
                distance += 1
                continue
            else:
                north = color_array[y-distance][x]
                norX, norY = x, y-distance
                break
    if x != tilesX-1:
        distance = 1
        while distance < (tilesX-x):
            if color_array[y][x+distance] == "Empty":
                distance += 1
                continue
            else:
                east = color_array[y][x+distance]
                easX, easY = x+distance, y
                break
    if y != tilesY-1:
        distance = 1
        while distance < (tilesY-y):
            if color_array[y+distance][x] == "Empty":
                distance += 1
                continue
            else:
                south = color_array[y+distance][x]
                souX, souY = x, y+distance
                break
    if x != 0:
        distance = 1
        while distance <= x:
            if color_array[y][x-distance] == "Empty":
                distance += 1
                continue
            else:
                west = color_array[y][x-distance]
                wesX, wesY = x-distance, y
                break

    # Creates list of neighbor tile colors and their count.
    neighbors = [north, south, east, west]
    edgecount = neighbors.count("Edge")
    color_counts = Counter(item for item in neighbors if item != "Edge")

    # Removes tile from valid tiles list if all four neighbor tiles are edge pieces.
    if edgecount > 2:
        valid_tiles.remove(current_space)

    # Returns true if there is an eligible pairing (or two), eliminates neighbor pairs that are not edge pieces.
    for count in color_counts.values():
        if count == 2 or count == 4:
            if color_counts[north] in [2, 4] and north != "Edge":
                colors[norY][norX] = "Empty"
            if color_counts[east] in [2, 4] and east != "Edge":
                colors[easY][easX] = "Empty"
            if color_counts[south] in [2, 4] and south != "Edge":
                colors[souY][souX] = "Empty"
            if color_counts[west] in [2, 4] and west != "Edge":
                colors[wesY][wesX] = "Empty"
            return True
    return False

if __name__ == '__main__':
    # Creates coordinate references for tile positions.
    tiles = [[0]*tilesX for _ in range(tilesY)]
    for y in range(tilesY):
        for x in range(tilesX):
            tiles[y][x] = ((left + (x*tileWidth) + (tileWidth/2)), (top + (y*tileHeight) + (tileHeight/2)))

    # Creates a list of all possible tile coordinates. These will later be removed to prevent having to check inelligible tiles where all four neighbors are edge pieces.
    valid_tiles = []
    for y in range(tilesY):
        for x in range(tilesX):
            valid_tiles.append((x, y))
    # Spiral coordinates for testing, just comment lines 160-163 and uncomment 165.
    # valid_tiles = [(15, 7), (14, 7), (13, 7), (12, 7), (11, 7), (10, 7), (9, 7), (8, 7), (7, 7), (6, 7), (6, 8), (7, 8), (8, 8), (9, 8), (10, 8), (11, 8), (12, 8), (13, 8), (14, 8), (15, 8), (16, 8), (16, 7), (16, 6), (15, 6), (14, 6), (13, 6), (12, 6), (11, 6), (10, 6), (9, 6), (8, 6), (7, 6), (6, 6), (5, 6), (5, 7), (5, 8), (5, 9), (6, 9), (7, 9), (8, 9), (9, 9), (10, 9), (11, 9), (12, 9), (13, 9), (14, 9), (15, 9), (16, 9), (17, 9), (17, 8), (17, 7), (17, 6), (17, 5), (16, 5), (15, 5), (14, 5), (13, 5), (12, 5), (11, 5), (10, 5), (9, 5), (8, 5), (7, 5), (6, 5), (5, 5), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (5, 10), (6, 10), (7, 10), (8, 10), (9, 10), (10, 10), (11, 10), (12, 10), (13, 10), (14, 10), (15, 10), (16, 10), (17, 10), (18, 10), (18, 9), (18, 8), (18, 7), (18, 6), (18, 5), (18, 4), (17, 4), (16, 4), (15, 4), (14, 4), (13, 4), (12, 4), (11, 4), (10, 4), (9, 4), (8, 4), (7, 4), (6, 4), (5, 4), (4, 4), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (3, 11), (4, 11), (5, 11), (6, 11), (7, 11), (8, 11), (9, 11), (10, 11), (11, 11), (12, 11), (13, 11), (14, 11), (15, 11), (16, 11), (17, 11), (18, 11), (19, 11), (19, 10), (19, 9), (19, 8), (19, 7), (19, 6), (19, 5), (19, 4), (19, 3), (18, 3), (17, 3), (16, 3), (15, 3), (14, 3), (13, 3), (12, 3), (11, 3), (10, 3), (9, 3), (8, 3), (7, 3), (6, 3), (5, 3), (4, 3), (3, 3), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (2, 11), (2, 12), (3, 12), (4, 12), (5, 12), (6, 12), (7, 12), (8, 12), (9, 12), (10, 12), (11, 12), (12, 12), (13, 12), (14, 12), (15, 12), (16, 12), (17, 12), (18, 12), (19, 12), (20, 12), (20, 11), (20, 10), (20, 9), (20, 8), (20, 7), (20, 6), (20, 5), (20, 4), (20, 3), (20, 2), (19, 2), (18, 2), (17, 2), (16, 2), (15, 2), (14, 2), (13, 2), (12, 2), (11, 2), (10, 2), (9, 2), (8, 2), (7, 2), (6, 2), (5, 2), (4, 2), (3, 2), (2, 2), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13), (2, 13), (3, 13), (4, 13), (5, 13), (6, 13), (7, 13), (8, 13), (9, 13), (10, 13), (11, 13), (12, 13), (13, 13), (14, 13), (15, 13), (16, 13), (17, 13), (18, 13), (19, 13), (20, 13), (21, 13), (21, 12), (21, 11), (21, 10), (21, 9), (21, 8), (21, 7), (21, 6), (21, 5), (21, 4), (21, 3), (21, 2), (21, 1), (20, 1), (19, 1), (18, 1), (17, 1), (16, 1), (15, 1), (14, 1), (13, 1), (12, 1), (11, 1), (10, 1), (9, 1), (8, 1), (7, 1), (6, 1), (5, 1), (4, 1), (3, 1), (2, 1), (1, 1), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11), (0, 12), (0, 13), (0, 14), (1, 14), (2, 14), (3, 14), (4, 14), (5, 14), (6, 14), (7, 14), (8, 14), (9, 14), (10, 14), (11, 14), (12, 14), (13, 14), (14, 14), (15, 14), (16, 14), (17, 14), (18, 14), (19, 14), (20, 14), (21, 14), (22, 14), (22, 13), (22, 12), (22, 11), (22, 10), (22, 9), (22, 8), (22, 7), (22, 6), (22, 5), (22, 4), (22, 3), (22, 2), (22, 1), (22, 0), (21, 0), (20, 0), (19, 0), (18, 0), (17, 0), (16, 0), (15, 0), (14, 0), (13, 0), (12, 0), (11, 0), (10, 0), (9, 0), (8, 0), (7, 0), (6, 0), (5, 0), (4, 0), (3, 0), (2, 0), (1, 0), (0, 0)]

    # Starts the game from main menu.
    input("Ensure you are seeing the main menu and 'Play' is visible. Then hit enter.")
    # ag.click(left+(windowWidth/2), top+(windowHeight*0.55))
    click_mouse(left+(windowWidth/2), top+(windowHeight*0.55))
    time.sleep(startDelay)

    # Initialize color array.
    colors = [[0] * tilesX for _ in range(tilesY)]
    set_colors(colors)

    # Main play loop.
    while True:
        for valid_tile in valid_tiles:
            x, y = valid_tile
            if colors[y][x] == "Empty":
                if check_neighbors(colors, (x, y)):
                    # ag.click(tiles[y][x])
                    xCor, yCor = tiles[y][x]
                    click_mouse(xCor, yCor)
                    time.sleep(clickDelay)
