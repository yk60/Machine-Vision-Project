# main executable used to test sample images
from genutils import parse_cmdline, mnist_dict, imageNet_dict
from imageutils import vectorize_img
from matrix import DigitMatrix, DigitMatrices, generate_html_table, generate_failed_tests_table, get_imageNet_classes, visualize_embeddings_pca, visualize_embeddings_pca_3d
from test import test_image
import os
import time

start_time = time.time()
# build model
optional_params = ['imgSize', 'num_classes', 'classes']
required_params = ['dataSet'] # add more
params_dict = parse_cmdline(required_params, optional_params)
if params_dict:
    
    if params_dict['dataSet'].lower() == 'mnist':
        params_dict.update(mnist_dict)
    if params_dict['dataSet'].lower() == 'imagenet':
        params_dict.update(imageNet_dict)
    digitMatrices = DigitMatrices() 
    # train model   
    for object in params_dict['classes']:
        paths = [os.path.join(dir, object) for dir in params_dict['filePath']]
        digitMatrix = DigitMatrix(paths, object)
        digitMatrices.add_object(digitMatrix)
    
    # test model
    temp = []
    for object in params_dict['classes']:      
        testImgs = os.path.join(params_dict['testImage'], object)
        # test_image(digitMatrices, params_dict['testImage'])
        img_dict, test_img = vectorize_img(testImgs) # matrix of test imgs
        failed_tests, accuracy = digitMatrices.project_to_subspace(img_dict, test_img, object)
        temp += failed_tests
    generate_failed_tests_table(temp)
    # digitMatrices.printMatrices()
    # visualize_embeddings_pca([matrix.embedding_matrix for matrix in digitMatrices.matrices.values()], [matrix.digit for matrix in digitMatrices.matrices.values()])
    # visualize_embeddings_pca_3d([matrix.embedding_matrix for matrix in digitMatrices.matrices.values()], [matrix.digit for matrix in digitMatrices.matrices.values()])
    # generate_html_table(digitMatrices.matrices['0'])
else:
    print('returned an empty dictionary')

end_time = time.time()
print(f"Execution time: {end_time - start_time} seconds")
get_imageNet_classes()
         
    
         


    