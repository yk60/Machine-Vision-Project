import sys
from PIL import Image
mnist_dict = {
    'filePath': ['MNIST_JPG/MNIST_JPG/trainingSet'],
    'testImage': 'MNIST_JPG/MNIST_JPG/testingSet'
}
imageNet_dict = {
    'filePath': ['ImageNet/ImageNet-10k-0', 'ImageNet/ImageNet-10k-2'],
    'testImage': 'ImageNet/TestSet'
}
default_values = {
    'imgSize': (28, 28),
    'num_classes': 2,
    'classes': ['0', '1']    
}
params_dict = {}
# parse command-line params into a dictionary
def parse_cmdline(required_params, optional_params):
    params = sys.argv[1:]
    if '--help' in params:
        print("Select a dataset [MNIST] or [ImageNet] and class objects")
        print(f"Enter parameters for {sys.argv[0]}:", end="")
        for param in required_params:
            print(f"{param}", end=" ")
        print('\n')
        return {}      
    
    for param in params:
        param = param.split('=')
        if param[0] and not param[1]:
            print(f"Error: Enter the value for {param[0]}.")
            return {}            
        if param[0] == 'dataSet' and param[1].lower() != 'mnist' and param[1].lower() != 'imagenet':
            print(f"Enter a valid dataset name")
            break
        if param[0] == 'imgSize':
            param[1] = tuple(int(x.strip())for x in param[1].split(','))
        if param[0] == 'num_classes':
            num_classes = int(param[1])
            if num_classes < 2 or num_classes > 10:
                print(f"Error: Enter a valid number for num_classes")
                continue
        if param[0] == 'classes':
           param[1] = [x.strip() for x in param[1].split(',')]
        if param[0] == 'threshold_ratio':
            param[1] = float(param[1])
        if param[0] == 'max_eigenvector':
            param[1] = int(param[1])
        params_dict[param[0]] = param[1]

    for param in required_params:
        if param not in params_dict:
            print(f"Error: Missing required parameter: {param}.")
            return {}
    for param, default_value in default_values.items():
        if param not in params_dict:
            params_dict[param] = default_value
            print(f"assigned default value for {param}")
    return params_dict   