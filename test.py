# Use the model to classify the unknown image into the digit 0-9
import matplotlib.pyplot as plt
import numpy as np
from genutils import parse_cmdline
from imageutils import create_dictionary, create_matrix
from analysis import analysis_all

def test_image(img):
    print('start test')
    img_dict = create_dictionary(img)
    if not img_dict:
        print("Error: No dictionary returned")
    matrix = create_matrix(img_dict)
    
    # cos_similarity = analysis_all(matrix)
    # print(cos_similarity)

