# main executable used to test sample images
from genutils import parse_cmdline
from matrix import DigitMatrix, DigitMatrices, generate_html_table
from test import test_image
import os

# build model
required_params = ['filePath'] # add more
params_dict = parse_cmdline(required_params)
if params_dict:
    dir = params_dict['filePath']
    digitMatrices = DigitMatrices()
    for subdir in os.listdir(dir):
         folder = os.path.join(dir, subdir)
         obj = DigitMatrix(folder, subdir)
         digitMatrices.add_object(obj)
    # digitMatrices.printMatrices()


    # if not digitMatrices.matrices['1']:
    #      print('matrix not found')
    # generate_html_table(digitMatrices.matrices['2'])
    # classify unknown image
    if params_dict['testImage']:
        test_image(digitMatrices, params_dict['testImage'])
         
    
         


    