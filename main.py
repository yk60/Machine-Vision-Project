# main executable used to test sample images
from genutils import parse_cmdline
from imageutils import vectorize_img
from matrix import DigitMatrix, DigitMatrices, generate_html_table
from test import test_image
import os
import time

start_time = time.time()
# build model
optional_params = ['imgSize', 'num_classes', 'classes']
required_params = ['filePath', 'testImage'] # add more
params_dict = parse_cmdline(required_params, optional_params)
if params_dict:
    dir = params_dict['filePath']
    digitMatrices = DigitMatrices()

    # train model
    for object in params_dict['classes']:
        folder = os.path.join(dir, object)
        digitMatrix = DigitMatrix(folder, object)
        digitMatrices.add_object(digitMatrix)
    # test model
    for object in params_dict['classes']:      
        testImgs = os.path.join(params_dict['testImage'], object)
        # test_image(digitMatrices, params_dict['testImage'])
        img_dict, test_img = vectorize_img(testImgs) # matrix of test imgs
        digitMatrices.project_to_subspace(img_dict, test_img, object)
    # digitMatrices.printMatrices()

    # generate_html_table(digitMatrices.matrices['3'])
   
    


else:
    print('returned an empty dictionary')

end_time = time.time()
print(f"Execution time: {end_time - start_time} seconds")
         
    
         


    