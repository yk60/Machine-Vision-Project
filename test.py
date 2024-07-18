# Use the model to classify the unknown image into the digit 0-9
import matplotlib.pyplot as plt
import numpy as np
from genutils import parse_cmdline
from imageutils import create_dictionary, create_matrix, show_image
from analysis import analysis_all, analysis_pair
from matrix import DigitMatrices

# compare cos similarity between test image and representative images for each digit
def test_image(digitMatrices, test_file):
    img_dict = create_dictionary(test_file)
    if not img_dict:
        print("Error: No dictionary created")
    test_img = create_matrix(img_dict)
    list = []    
    for i in range(0, 10):
        digitMatrix = digitMatrices.matrices[str(i)]
        rep_img = digitMatrix.representative_img
        rep_img = digitMatrix.img_dict[rep_img]
        cos_similarity = np.round(analysis_pair(rep_img, test_img), 2)
        list.append(cos_similarity)
        # show_image(rep_img)
        # show_image(test_img)
        print(f"cos similarity between unknown img and {i}: {cos_similarity}")
    print(f"\nResult: {max(list)}")


