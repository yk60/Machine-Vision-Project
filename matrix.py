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
    digit = None # String
    path = ""
    img_dict = {}
    matrix = np.zeros(shape=(0,))
    cos_similarity = np.zeros(shape=(0,))
    row_avg = []
    representative_img = None # filename(String)

    def __init__(self, path, digit):
        self.path = path
        self.digit = digit
        self.setDict()
        self.setMatrix()  
        self.setRowAverage()   
        self.setRepImg()   

    def setDict(self):
        self.img_dict = create_dictionary(self.path)
    def setMatrix(self):
        self.matrix = create_matrix(self.img_dict)
        self.cos_similarity = analysis_all(self.matrix)
    # def show_matrix(self):
    #     generate_html_table(list(self.img_dict.keys), self.cos_similarity)
    def get_matrix(self):
        return self
    def setRowAverage(self):
        self.row_avg = np.mean(self.cos_similarity, axis=1)
        self.row_avg = np.round(self.row_avg, 2)
    def setRepImg(self):
        index = np.argmax(self.row_avg)
        print(f"Index of representative image for digit {self.digit}: {index}")
        self.representative_img = list(self.img_dict.keys())[index]
        print(self.representative_img)
        

    
    

#\MNIST\trainingSample\trainingSample\0
#MNIST/trainingSample/trainingSample/0
