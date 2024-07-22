# Use the model to classify the unknown image into the digit 0-9
import matplotlib.pyplot as plt
import numpy as np
import os
from imageutils import create_dictionary, create_matrix, show_image
from analysis import analysis_all, analysis_pair
from matrix import DigitMatrices


# compare cos similarity between test image and representative images for each digit
def test_image(digitMatrices, test_files):
    num_tests = tests_passed = tests_failed = 0
    if os.path.isdir(test_files):
        for test_file in os.listdir(test_files):
            test_file = os.path.join(test_files, test_file)
            img_dict = create_dictionary(test_file)
            if not img_dict:
                print("Error: No dictionary created")
                return 1
            test_img = create_matrix(img_dict)
            dict = {}    
            for i in range(0, 10):
                digitMatrix = digitMatrices.matrices[str(i)]
                rep_img = digitMatrix.representative_img
                rep_img = digitMatrix.img_dict[rep_img]
                cos_similarity = np.round(analysis_pair(rep_img, test_img), 2)
                dict[i] = cos_similarity
                # show_image(rep_img)
                # show_image(test_img)
                # print(f"cos similarity between unknown img and {i}: {cos_similarity}")
            max_similarity = max(dict.values())
            actual = list(dict.values()).index(max_similarity)
            # get the dir path containing test_file and extract the name of the last dir
            expected = os.path.basename(os.path.dirname(test_file))
            if(str(actual) == str(expected)):
                tests_passed += 1
            else:
                tests_failed += 1
                print(f"({os.path.basename(test_file):<13}) Actual: {actual} Expected: {expected}")
            num_tests += 1
        print(f"Num tests passed: {tests_passed}")
        print(f"Num tests failed: {tests_failed}")
        print(f"Accuracy: {(tests_passed / num_tests) * 100}%")
    else:
        print("Invalid test directory")



