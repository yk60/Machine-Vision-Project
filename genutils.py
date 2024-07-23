import sys
from PIL import Image

default_values = {
    'imgSize': (28, 28),
}
params_dict = {}
# parse command-line params into a dictionary
def parse_cmdline(required_params, optional_params):
    params = sys.argv[1:]
    if '--help' in params:
        print(f"Enter parameters for {sys.argv[0]}:", end="(")
        # print('-test: Enter the path to the image to vectorize')
        for param in required_params:
            print(f"{param}=", end=" ")
        print(')')      
        return {}      
    
    for param in params:
        param = param.split('=')
        if not param[1] and param[0] in optional_params:
            break
        if not param[1] and param[0] in required_params:
            print(f"Error: Enter the value for {param[0]}.")
            return {}
        if param[0] == 'imgSize':
            param[1] = tuple(int(x.strip())for x in param[1].split(','))
            print(f"param 1 = {param[1]}")
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

# def main():
#     params_dict = parse_cmdline(['filePath', 'fileType'])
#     if params_dict:
#         print(params_dict)

# if __name__ == "__main__":
#     main()