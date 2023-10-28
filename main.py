import pyautogui as ag
import time
from collections import Counter

#Constants
tilesX = 23
tilesY = 15

#!!!
#ADJUST THIS VALUE BASED ON HARDWARE AND LAG
ag.PAUSE = 0.04
#!!!

#To get your own coordinates, uncomment lines 18-25 and comment lines 28-29.
#Then run the program once and replace my coordinates with yours.
#Then, recomment lines 18-25 and uncomment lines 28-29

# input("Move mouse to top left of the most top-left tile in the game board (including empty). ")
# print(ag.position())
# left, top = ag.position()
# print(left, top)
# input("Move mouse to bottom right of the most bottom-right tile ")
# print(ag.position())
# right, bottom = ag.position()
# print(right, bottom)

#Defines basic coordinates
left, top = 123, 241
right, bottom = 1168, 924

windowWidth = right - left
windowHeight = bottom - top
tileWidth = windowWidth / tilesX
tileHeight = windowHeight / tilesY

#Defines a dictionary of possible colors with their respective names and RGB values.
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

#Calculates the Euclidean distance between the input color and each possible color in the dictionary.
def closest_color(rgb_tuple):
    closest_distance = float('inf')
    closest_color_name = "Unknown"
    for color, name in color_dict.items():
        distance = sum([(a - b) ** 2 for a, b in zip(rgb_tuple, color)])
        if distance < closest_distance:
            closest_distance = distance
            closest_color_name = name
    return closest_color_name

#Captures the screen and gets color values of tiles.
def set_colors(colors_list):
    img = ag.screenshot()
    for y in range(tilesY):
        for x in range(tilesX):
            colors_list[y][x] = closest_color(img.getpixel((tiles[y][x][0], tiles[y][x][1])))

def check_neighbors(color_array, current_space):
    #Defining coordinate and color variables that will be used.
    x, y = current_space
    norX = easX = souX = wesX = x
    norY = easY = souY = wesY = y
    north = east = south = west = "Edge"

    #Expands outwards until reaching the edge. Identifies all neighboring tiles and defines their color and coordinates.
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

    #Creates list of neighbor tile colors and their count.
    neighbors = [north, south, east, west]
    color_counts = Counter(item for item in neighbors if item != "Edge")

    #Removes tile from valid tiles list if all four neighbor tiles are edge pieces.
    if color_counts["Edge"] == 4:
        valid_tiles.remove((x, y))

    #Returns true if there is an eligible pairing (or two), eliminates neighbor pairs that are not edge pieces.
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
    #Creates coordinate references for tile positions.
    tiles = [[0]*tilesX for _ in range(tilesY)]
    for y in range(tilesY):
        for x in range(tilesX):
            tiles[y][x] = ((left + (x*tileWidth) + (tileWidth/2)), (top + (y*tileHeight) + (tileHeight/4)))

    #Creates a list of all possible tile coordinates. These will later be removed to prevent having to check inelligible tiles where all four neighbors are edge pieces.
    valid_tiles = []
    for y in range(tilesY):
        for x in range(tilesX):
            valid_tiles.append((x, y))

    #Starts the game from main menu.
    input("Ensure you are seeing the main menu and 'Play' is visible. Then hit enter.")
    ag.click(left+(windowWidth/2), top+(windowHeight*0.55))

    #!!!
    #ADJUST THIS VALUE BASED ON HARDWARE AND LAG
    time.sleep(0.35)
    #!!!

    # Initialize color array.
    colors = [[0] * tilesX for _ in range(tilesY)]
    set_colors(colors)

    #Main play loop.
    while True:
        for valid_tile in valid_tiles:
            x, y = valid_tile
            if colors[y][x] == "Empty":
                if check_neighbors(colors, (x, y)):
                    ag.click(tiles[y][x])
