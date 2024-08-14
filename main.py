# main executable for testing
from genutils import parse_cmdline, mnist_dict, imageNet_dict
from imageutils import vectorize_img
from matrix import DigitMatrix, DigitMatrices, generate_html_table, generate_failed_tests_table, get_imageNet_classes, set_labels_dict, labels_dict
import os
import time

start_time = time.time()
# build model
optional_params = ['imgSize', 'threshold_ratio']
required_params = ['dataSet', 'classes'] # add more
params_dict = parse_cmdline(required_params, optional_params)

if params_dict:    
    if params_dict['dataSet'].lower() == 'mnist':
        params_dict.update(mnist_dict)
    if params_dict['dataSet'].lower() == 'imagenet':
        params_dict.update(imageNet_dict)
        set_labels_dict()
    digitMatrices = DigitMatrices() 

    # train model
    for object in params_dict['classes']:
        paths = [os.path.join(dir, object) for dir in params_dict['filePath']]        
        digitMatrix = DigitMatrix(paths, object)
        print(f"training the model with {len(digitMatrix.img_dict)} training images of {labels_dict.get(object, object)}...")
        digitMatrices.add_object(digitMatrix)
    
    # test model
    temp = []
    for object in params_dict['classes']:      
        testImgs = os.path.join(params_dict['testImage'], object)
        print(f"\ntesting the model with {len(os.listdir(testImgs))} testing images of {labels_dict.get(object, object)}...")
        img_dict, test_img = vectorize_img(testImgs) 
        failed_tests, accuracy = digitMatrices.project_to_subspace(img_dict, test_img, object)
        temp += failed_tests
    generate_failed_tests_table(temp)
    print("finished displaying the test results to result.html")
    # generate_html_table(digitMatrices.matrices['0']) 
else:
    print('returned an empty dictionary')

end_time = time.time()
print(f"Execution time: {end_time - start_time} seconds")