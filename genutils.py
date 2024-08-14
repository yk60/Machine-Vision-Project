import sys

mnist_dict = {
    # path to the training images of a smaller mnist dataset
    # 'filePath': ['MNIST/trainingSample/trainingSample'], 
    'filePath': ['MNIST_JPG/MNIST_JPG/trainingSet'],
    'testImage': 'MNIST_JPG/MNIST_JPG/testingSet'
}
imageNet_dict = {
    'filePath': ['ImageNet/ImageNet-10k-0', 'ImageNet/ImageNet-10k-2'],
    'testImage': 'ImageNet/TestSet'
}
default_values = {
    'imgSize': '28,28',
    'threshold_ratio': 0.01
}
params_dict = {}
# parse command-line parameters and save them into a dictionary
def parse_cmdline(required_params, optional_params):
    params = sys.argv[1:]
    if not params or'--help' in params:
        print("Select a dataset MNIST/ImageNet and 2 or more object classes. Press enter to skip entering the optional parameter.\n")
        for param in required_params:
            value = None
            while not value:
                value = input(f"Enter value for {param}: ")            
            params_dict[param] = value
        for param in optional_params:
            value = input(f"Enter value for {param}: ")
            if value:
                params_dict[param] = value
            else:
                params_dict[param] = default_values[param]  
                print(f"assigned default value for {param}, {default_values[param]}")   
    else:
        for param in params:
            if '=' in param:
                key, value = param.split('=')
                params_dict[key] = value
            else:
                print(f"Warning: Missing the value for {param}")
            

    for param in required_params:
        if param not in params_dict:
            print(f"Error: Missing required parameter: {param}.")
            return {}
    for param in optional_params:
        if param not in params_dict:
            params_dict[param] = default_values[param]  
            print(f"assigned default value for {param}, {default_values[param]}")
    validate_input(params_dict)
            
    print(f"Input: {params_dict}\n")
    return params_dict 

# validate each parameter and convert them into the accepted format
def validate_input(params_dict):
    for key, value in params_dict.items():         
        if key == 'dataSet' and value.lower() != 'mnist' and value.lower() != 'imagenet':
            print(f"Enter a valid dataset name")
            break
        if key == 'imgSize':
            value = tuple(int(x.strip())for x in value.split(','))
        if key == 'num_classes':
            num_classes = int(value)
            if num_classes < 2 or num_classes > 10:
                print(f"Error: Enter a valid number for num_classes")
                continue
        if key == 'classes':
            value = [x.strip() for x in value.split(',')]
        if key == 'threshold_ratio':
            value = float(value)
        if key == 'max_eigenvector':
            value = int(value)
        params_dict[key] = value