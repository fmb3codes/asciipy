
import ast
from PIL import Image
import numpy as np
import webcolors
import random
import string
import math

color_map = {};
colors_seen = {}
# Update directory below where input image file is located
#directory = r"ADD INPUT PATH HERE"
# Enable/modify desired ascii density below
#ascii_density = "Ñ@#W$9876543210?!abc;:+=-,._ '"
#ascii_density = "Ñ@#W$9876543210?!abc;:+=-,._            "
#ascii_density = ".:-i|=+%O#@  "
#ascii_density = " .:-i|=+%O#@  "
#ascii_density = "@#O%+=|i-:.    "
#ascii_density = "@#O%+=|i-:. "
#ascii_density = "Ñ@#W$9876543210?!abc;:+=-,._    "
#ascii_density = "@#+=|-   "
#ascii_density = "Ñ@#W$9876543210?!abc;:+=-,._           "
ascii_density = "@#O%+=|i---+-- abcd   "

ascii_density_length = len(ascii_density)

def scale(im, nR, nC):
    nR0 = len(im)     # source number of rows 
    nC0 = len(im[0])  # source number of columns 
    return [[ im[int(nR0 * r / nR)][int(nC0 * c / nC)]  
                for c in range(nC)] for r in range(nR)]
    
def createOrLoadColorsSeen():
    try:
        with open("hex_color_map.txt", 'r') as f:
            contents = f.read()
            colors_seen = ast.literal_eval(contents)
    except IOError:
        with open("hex_color_map.txt", 'w') as f:
            for r in range(256):
                for g in range(256):
                    for b in range(256):
                        populateColorName(r, g, b)
            print(colors_seen, file=f)
                
    # read file contents into color_map

def populateColorMap():
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        color_map[name] = random.choice(string.ascii_letters)

def populateColorName(r, g, b):
    search_key = str(r) + str(g) + str(b);
    
    min_colors = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - r) ** 2
        gd = (g_c - g) ** 2
        bd = (b_c - b) ** 2
        min_colors[(rd + gd + bd)] = name
    calculated_color = min_colors[min(min_colors.keys())]
    colors_seen[search_key] = calculated_color

def getPopulatedColorName(rgb_triplet):
    r = rgb_triplet[0]
    g = rgb_triplet[1]
    b = rgb_triplet[2]
    search_key = str(r) + str(g) + str(b);
    return colors_seen[search_key]
    
def get_color_name(rgb_triplet):
    r = rgb_triplet[0]
    g = rgb_triplet[1]
    b = rgb_triplet[2]
    search_key = str(r) + str(g) + str(b);
    if search_key in colors_seen:
        return colors_seen[search_key]
    
    min_colors = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - rgb_triplet[0]) ** 2
        gd = (g_c - rgb_triplet[1]) ** 2
        bd = (b_c - rgb_triplet[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    calculated_color = min_colors[min(min_colors.keys())]
    colors_seen[search_key] = calculated_color
    return calculated_color

def mapFromTo(x,a,b,c,d):
    y=(x-a)/(b-a)*(d-c)+c
    return y

def get_color_average(rgb_triplet):
    r = rgb_triplet[0]
    g = rgb_triplet[1]
    b = rgb_triplet[2]
    avg = (int(r) + int(g) + int(b)) / 3
    
    char_index = mapFromTo(avg, 0, 255, 0, ascii_density_length - 1)
    ascii_to_use = ascii_density[math.floor(char_index)]
    
    return ascii_to_use
    

def loadImage(image_file_path):
    image = Image.open(image_file_path)

    source_image = np.array(image)
    source_rows = len(source_image)
    source_cols = len(source_image[0])

    print("Source rows:%s cols:%s" % (source_rows, source_cols))
    
    return image
    
def resizeImage(image):
    scale_x = 1600
    scale_y = 1200
    max_size = (scale_x, scale_y)

    image.thumbnail(max_size, Image.LANCZOS)

def createAsciiMatrix(rows, cols):

    ascii_matrix = np.empty(shape=(rows,cols), dtype='<U10')
    
    return ascii_matrix

def populateAsciiMatrix(image_pixels, ascii_matrix, rows, cols):
    for row in range(rows):
        for col in range(cols):
            # calculated_color = get_color_name(image_pixels[row][col])
            # ascii_matrix[row][col] = color_map[calculated_color]
            calculated_character = get_color_average(image_pixels[row][col]) # calculated character based on brightness
            ascii_matrix[row][col] = calculated_character

def writeAsciiMatrixToFile(filename, matrix):
    print("Writing to file")
    with open(filename, 'w') as f:
        for row in matrix:
            for col in row:
                # print(col, end="")
                f.write("%s" % col)
            # print("\n")
            f.write("\n")
           
           
def main():
    
    # createOrLoadColorsSeen()
    
    populateColorMap()

    print("Current directory %s" % directory)
    file_name_from_user = input("Enter file name: ")
    image = loadImage(directory + file_name_from_user)

    #resizeImage(image) # uncomment to enable image resizing; set parameters of resize inside function
        
    image_pixels = np.array(image)
    
    # image_pixels = np.rot90(image_pixels, 3)

    rows = len(image_pixels)
    cols = len(image_pixels[0])
    
    print("Resized rows:%s cols:%s" % (rows, cols))

    ascii_matrix = createAsciiMatrix(rows, cols)
            
    populateAsciiMatrix(image_pixels, ascii_matrix, rows, cols)
                
    writeAsciiMatrixToFile(file_name_from_user.split(".")[0] + ".txt", ascii_matrix)
    
    
if __name__ == "__main__":
    main()
 