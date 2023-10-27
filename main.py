import pyautogui as ag
import time

# constants
tilesX = 23
tilesY = 15


def closest_color(rgb_tuple):
    # Define a dictionary of possible colors with their respective names and RGB values.
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

    # Calculate the Euclidean distance between the input color and each possible color in the dictionary.
    closest_distance = float('inf')
    closest_color_name = "Unknown"
    for color, name in color_dict.items():
        distance = sum([(a - b) ** 2 for a, b in zip(rgb_tuple, color)])
        if distance < closest_distance:
            closest_distance = distance
            closest_color_name = name

    return closest_color_name


def set_colors(colors_list):
    # get color values of all tiles.
    start = time.time()
    img = ag.screenshot()
    for i in range(tilesY):
        for j in range(tilesX):
            colors_list[i][j] = closest_color(img.getpixel((tiles[i][j][0], tiles[i][j][1])))
    end = time.time()
    time_spent = end - start
    print("Set Colors Array in (" + str(time_spent) + ") secs.")


# def check_neighbors(color_array, current_space):
#     x, y = current_space
#     neighbors = []
#
#     # Define the directions for the neighbors
#     directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
#
#     for dx, dy in directions:
#         new_x, new_y = x + dx, y + dy
#         if 0 <= new_x < len(color_array) and 0 <= new_y < len(color_array[0]) and color_array[new_x][new_y] != "Empty":
#             neighbors.append(color_array[new_x][new_y])
#
#     # Count the occurrences of each color
#     color_count = {}
#     for color in neighbors:
#         color_count[color] = color_count.get(color, 0) + 1
#
#     if any(count > 2 for count in color_count.values()):
#         print(neighbors)
#
#     # Return True if more than 2 neighbors have the same color
#     return any(count > 2 for count in color_count.values())


def check_neighbors(grid, indices):
    x, y = indices
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    matching_count = 0
    empty_count = 0
    target_color = None

    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        while 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]):
            if grid[new_x][new_y] == "Empty":
                empty_count += 1
                new_x, new_y = new_x + dx, new_y + dy
            else:
                if target_color is None:
                    target_color = grid[new_x][new_y]
                elif grid[new_x][new_y] == target_color:
                    matching_count += 1
                break

    return matching_count + empty_count > 2


if __name__ == '__main__':
    # get screen size
    screenWidth, screenHeight = ag.size()

    # get coordinates of opposite corners of ColorTiles window.
    print("Screen Size:", screenWidth, "x", screenHeight)
    print("Start the game and follow instructions below.")
    input("Move mouse to top left of the most top-left tile in the game board (including empty). ")
    left, top = ag.position()
    input("Move mouse to bottom right of the most bottom-right tile ")
    right, bottom = ag.position()

    # calculate game window size and tile sizes
    windowWidth = right - left
    windowHeight = bottom - top
    tileWidth = windowWidth / tilesX
    tileHeight = windowHeight / tilesY

    # create coordinate reference for tile positions
    tiles = [[0]*tilesX for _ in range(tilesY)]
    for i in range(tilesY):
        for j in range(tilesX):
            tiles[i][j] = ((left + (j*tileWidth) + (tileWidth/2)), (top + (i*tileHeight) + (tileHeight/4)))

    # start game by clicking play again and then play
    input("Ensure you are seeing the 'Play Again' button and hit enter")
    ag.moveTo(left+(windowWidth/2), top+(windowHeight*0.75), 1)
    ag.click()
    ag.moveTo(left+(windowWidth/2), top+(windowHeight*0.55), 0.1)
    ag.click()
    time.sleep(1)

    # initialize color array
    colors = [[0] * tilesX for _ in range(tilesY)]

    # main play loop
    while True:
        set_colors(colors)
        for i in range(tilesY):
            for j in range(tilesX):
                if colors[i][j] == "Empty":
                    if check_neighbors(colors, (j, i)):
                        ag.moveTo(tiles[i][j])
                        ag.click()
                        time.sleep(0.5)
                        set_colors(colors)

    # uncomment to debug color array setting.
    # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in colors]))


