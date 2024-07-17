import numpy as np
import os
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
# from matrix import DigitMatrix, DigitMatrices

# load an image file into a 2D numpy array of gray pixel values
def process_image(dir, file):
    path = os.path.join(dir, file)
    image = Image.open(path).resize((28, 28)) #optional parameter
    np.set_printoptions(threshold=np.inf, linewidth=np.inf)
    image = ImageOps.grayscale(image)
    arr = np.array(image) / 255.0
    arr = vectorize_array(np.round(arr, 2))   
    return arr

# vectorize the 2D array into a single column vector (n x 1)
def vectorize_array(arr):
    return arr.reshape(-1, 1)

def create_dict_helper(dir, file, img_dict):
    if file.lower().endswith('.jpg'):
        img_dict[file] = process_image(dir, file)
    else:
        print(f"Failed to vectorize the image: {file}")

# load a directory of JPEG image files into a dict mapping : filename -> vectorized image.
def create_dictionary(dir):
    img_dict = {}
    try:
        # if dir is a full path to an image
        if os.path.isfile(dir):
            file = os.path.basename(dir)
            create_dict_helper(os.path.dirname(dir), file, img_dict) 
            return img_dict  
        
        for file in os.listdir(dir):
            create_dict_helper(dir, file, img_dict)         
        return img_dict
    except FileNotFoundError:
        print('FileNotFoundError')

# -combine the vectorized images into a matrix (2D NumPy array), where every vectorized image is a column.
def create_matrix(img_dict):
    if img_dict:
        matrix = np.column_stack(list(img_dict.values()))
        # print('Matrix shape:', matrix.shape)
        return matrix
    return None

def show_image(img_arr):
    plt.imshow(img_arr, cmap='gray') 
    plt.show() 

def main():
    dir = 'images/'
    img_dict = create_dictionary(dir)
    matrix = create_matrix(img_dict)
  
if __name__ == "__main__":
    main()