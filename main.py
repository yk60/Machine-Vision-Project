# main executable used to test sample images
from genutils import parse_cmdline
from imageutils import create_dictionary, create_matrix
from analysis import analysis_all
from table import generate_html_table

required_params = ['filePath'] # add more
params_dict = parse_cmdline(required_params)
if params_dict:
    # print(params_dict)
    path = params_dict['filePath']
    dict = create_dictionary(path)
    matrix = create_matrix(dict)
    # print(f"matrix: {matrix}")

    cos_similarity = analysis_all(matrix)
    generate_html_table(list(dict.keys()), cos_similarity)

    