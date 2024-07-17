import numpy as np
from imageutils import create_dictionary, create_matrix
from analysis import analysis_all
class DigitMatrices:
    matrices = {}
    def __init__(self):
        None
    def add_object(self, DigitMatrix):
        self.matrices[DigitMatrix.digit] = DigitMatrix
    def printMatrices(self):
        for matrix in self.matrices:
            print(f"Digit: {matrix.digit}")
            print(f"{matrix.cos_similarity}\n\n\n")

class DigitMatrix:
    digit = None
    path = ""
    img_dict = {}
    matrix = np.zeros(shape=(0,))
    cos_similarity = np.zeros(shape=(0,))

    def __init__(self, path, digit):
        self.path = path
        self.digit = digit
        self.setDict()
        self.setMatrix()        

    def setDict(self):
        self.img_dict = create_dictionary(self.path)
    # returns the cos similarity matrix
    def setMatrix(self):
        self.matrix = create_matrix(self.img_dict)
        # print(f"matrix: {matrix}")
        self.cos_similarity = analysis_all(self.matrix)
        # print(self.cos_similarity)
    # def show_matrix(self):
    #     generate_html_table(list(self.img_dict.keys), self.cos_similarity)
    def get_matrix(self):
        return self

    
    

#\MNIST\trainingSample\trainingSample\0
#MNIST/trainingSample/trainingSample/0
