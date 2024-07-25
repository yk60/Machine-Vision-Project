import numpy as np
import os
from imageutils import vectorize_img
from genutils import params_dict
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

    # project cols of y onto the subspaces of each digit (0-9) then find the subspace with the max projection
    def project_to_subspace(self, img_dict, y):
        num_tests = tests_passed = tests_failed = 0
        if y.shape[1] > 1:
            i = 0
            num_tests = tests_passed = tests_failed = 0
            test_files = list(img_dict.keys())
            for col in np.hsplit(y, y.shape[1]):
                test_file = os.path.join(params_dict['testImage'], test_files[i])
                U_matrices = [matrix.U for matrix in self.matrices.values()] # get subspaces for each digitMatrix object
                projections = [np.dot(U.T, col) for U in U_matrices] # project y onto the subspaces
                actual = np.argmax([np.linalg.norm(proj) for proj in projections]) # get the max length of projection
                expected = os.path.basename(os.path.dirname(test_file))
                # insertion order in img_dict = order of imgs tested         
                if(str(actual) == str(expected)):
                    tests_passed += 1
                else:
                    tests_failed += 1
                    print(f"({test_files[i]:<13}) Result: {actual} Expected: {expected}")
                i += 1
                num_tests += 1
            print(f"Num tests passed: {tests_passed}")
            print(f"Num tests failed: {tests_failed}")
            print(f"Accuracy: {(tests_passed / num_tests) * 100}%")

class DigitMatrix:
    digit = None # String
    path = ""
    img_dict = {}
    matrix = np.zeros(shape=(0,))
    cos_similarity = np.zeros(shape=(0,))
    row_avg = []
    representative_img = None # filename(String)
    U = None
    S = None
    VT = None

    def __init__(self, path, digit):
        self.path = path
        self.digit = digit
        self.vectorize_image()
        self.setRowAverage()   
        self.setRepImg()   
        self.apply_SVD()

    def vectorize_image(self):
        self.img_dict, self.matrix = vectorize_img(self.path)
        self.cos_similarity = analysis_all(self.matrix)

    # def show_matrix(self):
    #     generate_html_table(list(self.img_dict.keys), self.cos_similarity)
    def setRowAverage(self):
        self.row_avg = np.mean(self.cos_similarity, axis=1)
        self.row_avg = np.round(self.row_avg, 3)
    def setRepImg(self):
        index = np.argmax(self.row_avg)
        indices = np.argsort(self.row_avg)[::-1]
        indices = indices[:3]
        # print(f"Index of representative image for digit {self.digit}: {index}")
        self.representative_img = [list(self.img_dict.keys())[index] for index in indices]
        # print(f"({self.representative_img})")
    '''
    A = UΣV^T
    orthonormal col matrix(rotation) * diagonal matrix(stretch) * orthonormal col matrix(rotation)
    U = subspace spanned by the cols of matrix A
    '''
    # decompose the matrix into 3 simpler matrices to find pattern within the data 
    def apply_SVD(self):
        U, S, VT = np.linalg.svd(self.matrix, full_matrices=False)
        self.U = U
        self.S = S
        self.VT = VT
        return U, S, VT    

def generate_html_table(DigitMatrix):
    imgs = (list(DigitMatrix.img_dict.keys()))
    html_content = "<table><thead></thead><tbody>"
    # Iterate through cosine similarity matrix to populate table rows

    html_content += "<tr>"
    html_content += "<td>""</td>"
    for img in imgs:
        html_content += f'<td><img src="{DigitMatrix.path}/{img}" alt="Image"></td>'
    html_content += f'<td>Row Average</td>'
    html_content += "</tr>"
    i = 0
    for row in DigitMatrix.cos_similarity:
        html_content += "<tr>"
        html_content += f'<th scope="row"><img src="{DigitMatrix.path}/{imgs[i]}" alt="Image"></th>\n'
        for entry in row:
            html_content += f"<td>{entry}</td>"
        html_content += f"<td>{DigitMatrix.row_avg[i]}</td>"
        html_content += "</tr>"
        i+=1
            
    # Closing HTML structure
    html_content += "</tbody></table>"

    # insert html_content(table) into placeholders in index.html
    with open('index.html', 'r') as html_file:
        index_html_content = html_file.read()
    start_marker = "<!-- Start of table -->"
    end_marker = "<!-- End of table -->"

    start_content = index_html_content.split(start_marker)[0] + start_marker
    end_content = end_marker + index_html_content.split(end_marker)[1]
    updated_html_content = start_content + html_content + end_content


    with open('index.html', 'w') as html_file:
        html_file.write(updated_html_content)
