# unit tests
import unittest
import numpy as np
import unittest
import os
from unittest.mock import patch
from genutils import parse_cmdline, params_dict, mnist_dict, imageNet_dict
from imageutils import create_dictionary, create_matrix, show_image, vectorize_img
from analysis import analysis_all, analysis_pair
from matrix import DigitMatrix, DigitMatrices

class TestModel(unittest.TestCase):
    # call once for the entire class to setup values shared across all tests
    @classmethod
    def setUpClass(testModel):
        testModel.required_params = ['dataSet']
        testModel.optional_params = ['imgSize', 'num_classes', 'classes']
        testModel.params_dict = None
        testModel.threshold_ratio = 'threshold_ratio=0.5'
        testModel.max_eigenvector = 'max_eigenvector=10'
    def setUp(self):
        self.digitMatrices = None 

    def setDataSet(self, params_dict):
        if params_dict['dataSet'].lower() == 'mnist':
            params_dict.update(mnist_dict)
        if params_dict['dataSet'].lower() == 'imagenet':
            params_dict.update(imageNet_dict)

    # receives a tuple of positional arguments
    def create_model(self, *args):
        # temporarily replace sys.argv with self.args
        with patch('sys.argv', list(args)):
            self.params_dict = parse_cmdline(self.required_params, self.optional_params)
            if not self.params_dict:
                raise ValueError("Returned an empty dictionary")
            self.setDataSet(self.params_dict)           
            digitMatrices = DigitMatrices() 

            for object in params_dict['classes']:
                paths = [os.path.join(dir, object) for dir in params_dict['filePath']]
                digitMatrix = DigitMatrix(paths, object)
                digitMatrices.add_object(digitMatrix)
            for object in params_dict['classes']:      
                testImgs = os.path.join(params_dict['testImage'], object)
                img_dict, test_img = vectorize_img(testImgs) # matrix of test imgs
                
                failed_tests, accuracy = digitMatrices.project_to_subspace(img_dict, test_img, object)
                if accuracy < 70:
                    raise AssertionError(f"Accuracy is below 70%: {accuracy}%")
            digitMatrices = None
                
    @patch('sys.argv', ['main.py', 'dataSet=MNIST', 'classes=2,3'])            
    def test_parse_cmdline_1(self):
        self.params_dict = parse_cmdline(self.required_params, self.optional_params)
        self.setDataSet(self.params_dict)
        self.assertEqual(params_dict['classes'], ['2', '3'])
        self.assertEqual(params_dict['filePath'], ['MNIST_JPG/MNIST_JPG/trainingSet'])

    def test_model_1(self):
        self.create_model('main.py', 'dataSet=MNIST', 'classes=0,1', self.threshold_ratio)

    def test_model_2(self):
        self.create_model('main.py', 'dataSet=ImageNet', 'classes=00153,00284')

    def test_model_3(self):
        self.create_model('main.py', 'dataSet=ImageNet', 'classes=00200,00282')
        
    def test_model_4(self):
        self.create_model('main.py', 'dataSet=ImageNet', 'classes=00229,00283')

# compare cos similarity between test images and representative images from each object class
# (works only for mnist)
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
            dict = {}  # rep_img: cos_similarity
            for i in range(0, 10):
                # get indices of n rep imgs for each digit
                digitMatrix = digitMatrices.matrices[str(i)]
                rep_imgs = digitMatrix.representative_img
                rep_imgs = [digitMatrix.img_dict[rep_img] for rep_img in rep_imgs]
                cos_similarity = [np.round(analysis_pair(rep_img, test_img), 3) for rep_img in rep_imgs]
                dict[i] = np.mean(cos_similarity)
                # print(f"cos similarity between unknown img and {i}: {cos_similarity}")
            max_similarity = max(dict.values())
            actual = list(dict.values()).index(max_similarity)
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

if __name__ == '__main__':
    unittest.main() 