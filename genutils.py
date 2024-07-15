import sys
from PIL import Image

# parse command-line params into a dictionary
def parse_cmdline(required_params):
    dict = {}
    params = sys.argv[1:]
    if '--help' in params:
        print(f"Enter parameters for {sys.argv[0]}:", end="(")
        print('-test: Enter the path to the image to vectorize')
        for param in required_params:
            print(f"{param}=", end=" ")
        print(')')      
        return None        
    
    for param in params:
        param = param.split('=')
        if not param[1]:
            print(f"Error: Enter the value for {param[0]}.")
            return None
        dict[param[0]] = param[1]

    for param in required_params:
        if param not in dict:
            print(f"Error: Missing required parameter: {param}.")
            return None
    return dict   

# def main():
#     params_dict = parse_cmdline(['filePath', 'fileType'])
#     if params_dict:
#         print(params_dict)

# if __name__ == "__main__":
#     main()