import numpy as np
import os
from imageutils import vectorize_img
from genutils import params_dict
from analysis import analysis_all

labels_dict = {}
class DigitMatrices:
    def __init__(self):
        self.matrices = {}
    def add_object(self, DigitMatrix):
        self.matrices[DigitMatrix.digit] = DigitMatrix
    def printMatrices(self):
        for digit, matrix in self.matrices.items():
            print(f"Class object: {matrix.digit}")
            print(f"Num training images: {len(matrix.img_dict)}")
    def getClassName(self, predicted, actual):
        predicted = labels_dict.get(predicted, predicted)
        actual = labels_dict.get(actual, actual)
        return predicted, actual
    # choose W that minimizes the error between AW and y
    def project_to_subspace(self, img_dict, y, object):
        num_tests = tests_passed = tests_failed = 0
        failed_tests = []
        if y.shape[1] > 1:
            i = 0
            num_tests = tests_passed = tests_failed = 0
            test_files = list(img_dict.keys())
            for col in np.hsplit(y, y.shape[1]):
                test_file = os.path.join(params_dict['testImage'], object, test_files[i])
                # project test images(col) onto the subspaces spanned by the training images (cols of A) instead of directly projecting to U
                projections = [np.dot(matrix.embedding_matrix, col) for matrix in self.matrices.values()] # = W 

                index = np.argmax([np.linalg.norm(proj) for proj in projections]) # get the index of max projection
                predicted = list(self.matrices.keys())[index]
                actual = os.path.basename(os.path.dirname(test_file))
                if params_dict['dataSet'].lower() == 'imagenet':
                    predicted, actual = self.getClassName(predicted, actual)                
                if(str(predicted) == str(actual)):
                    tests_passed += 1
                else:
                    tests_failed += 1
                    failed_tests.append([test_file, predicted, actual])
                i += 1
                num_tests += 1
            accuracy = np.round((tests_passed / num_tests) * 100, 2)
            print(f"Selected classes: {[matrix.digit for matrix in self.matrices.values()]} Class: {actual}")
            print(f"Num tests passed: {tests_passed}")
            print(f"Num tests failed: {tests_failed}")
            print(f"Accuracy: {accuracy}%\n")
            return failed_tests, accuracy
class DigitMatrix:
    digit = None # String
    paths = [] # list of paths to training/testing images
    img_dict = {}
    matrix = np.zeros(shape=(0,))
    cos_similarity = np.zeros(shape=(0,))
    row_avg = []
    representative_img = None # filename(String)
    U = None
    embedding_matrix = np.zeros(shape=(0,))

    def __init__(self, paths, digit):
        self.paths = paths 
        self.digit = digit
        self.vectorize_image()
        self.setRowAverage()   
        self.setRepImg()   
        self.apply_SVD(params_dict.get('threshold_ratio', 0.01), params_dict.get('max_eigenvector', None))

    def vectorize_image(self):
        combined_img_dict = {}
        combined_matrix = []
        for path in self.paths:
            img_dict, matrix = vectorize_img(path)
            combined_img_dict.update(img_dict)
            combined_matrix.append(matrix)
        self.img_dict = combined_img_dict
        self.matrix = np.hstack(combined_matrix) if combined_matrix else None
        self.cos_similarity = analysis_all(self.matrix)

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
 
    # decompose the matrix into 3 simpler matrices to reduce dimensionality and find pattern within the data 
    def apply_SVD(self, threshold_ratio, max_principal_eigenvectors):
        U, S, VT = np.linalg.svd(self.matrix, full_matrices=False)
        principle_eigenvalue = np.max(S)
        # use cutoff to find the indices of significant eigenvectors
        cutoff = threshold_ratio * principle_eigenvalue
        indices = np.where(S >= cutoff)[0]
        if max_principal_eigenvectors:
            indices = indices[:max_principal_eigenvectors]
        self.U = U[:, indices] # U = eigenvectors of subspace spanned by cols of A
        pseudoinverse = np.linalg.pinv(self.U) 
        max_principal_eigenvectors = len(indices)
        self.embedding_matrix = np.dot(self.U, pseudoinverse)  # U*UT
        
def set_labels_dict():
    dir = 'ImageNet/ImageNet1000_labels.txt'
    with open(dir, 'r') as file:
        labels_dict.update(eval(file.read()))  
    updated_dict = {f"{str(key).rjust(5, '0')}": value for key, value in labels_dict.items()}
    labels_dict.clear()
    labels_dict.update(updated_dict)

# populate the html table with cos similarity values and training images
def generate_html_table(DigitMatrix):
    imgs = (list(DigitMatrix.img_dict.keys()))
    html_content = '<table id="cos_similarity_table"><thead></thead><tbody>'

    html_content += "<tr>"
    html_content += "<td>""</td>"
    for img in imgs:
        html_content += f'<td><img src="{DigitMatrix.paths[0]}/{img}" alt="Image"></td>'
    html_content += f'<td>Row Average</td>'
    html_content += "</tr>"
    i = 0
    for row in DigitMatrix.cos_similarity:
        html_content += f'<tr><th scope="row"><img src="{DigitMatrix.paths[0]}/{imgs[i]}" alt="Image"></th>\n'
        for entry in row:
            html_content += f"<td>{entry}</td>"
        html_content += f"<td>{DigitMatrix.row_avg[i]}</td></tr>"
        i+=1            
    html_content += "</tbody></table>"
    insert_to_html('table.html', html_content, "<!-- Start of table -->", "<!-- End of table -->")

def generate_failed_tests_table(failed_tests):
    html_content = '<table id="tests_failed_table"><thead><tr><th>Image</th><th>File</th><th>Predicted class</th><th>Actual class</th></tr></thead><tbody>'
    for test_file in failed_tests:
        html_content += f'<tr><td><img src="{test_file[0]}" alt="Failed Image"></td>'
        html_content += f'<td>{os.path.basename(test_file[0])}</td><td>{test_file[1]}</td><td>{test_file[2]}</td></tr>'
    html_content += "</tbody></table>"
    insert_to_html('result.html', html_content, "<!-- Start of table -->", "<!-- End of table -->")

def get_imageNet_classes():
    dir = 'ImageNet/ImageNet1000_labels.txt'
    with open(dir, 'r') as file:
        html_content = ''
        labels_dict = eval(file.read())
        for key, value in labels_dict.items():
            html_content += f'<option value="{str(key).rjust(5, "0")}">{value}</option> \n'
            if int(key) == 500:
                break
    insert_to_html('index.html', html_content,"<!-- Start of ImageNet select -->", "<!-- End of ImageNet select -->")
       
# do template rendering, insert html content into placeholders set in html file
def insert_to_html(file, html_content, start_marker, end_marker):
    with open(file, 'r') as html_file:
        index_html_content = html_file.read()
    start_content = index_html_content.split(start_marker)[0] + start_marker
    end_content = end_marker + index_html_content.split(end_marker)[1]
    updated_html_content = start_content + html_content + end_content
    with open(file, 'w') as html_file:
        html_file.write(updated_html_content)