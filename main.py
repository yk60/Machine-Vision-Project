# main executable used to test sample images
from genutils import parse_cmdline
from table import generate_html_table
from matrix import DigitMatrix, DigitMatrices
import os


required_params = ['filePath'] # add more
params_dict = parse_cmdline(required_params)
if params_dict:
    # print(params_dict)
    dir = params_dict['filePath']
    digitMatrices = DigitMatrices()
    for subdir in os.listdir(dir):
         folder = os.path.join(dir, subdir)
         obj = DigitMatrix(folder, subdir)
         digitMatrices.add_object(obj)
    digitMatrices.printMatrices()

# file names, cos similarity
    # generate_html_table(list(dict.keys()), cos_similarity)

    