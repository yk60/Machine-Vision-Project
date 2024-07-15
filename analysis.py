import matplotlib.pyplot as plt
import numpy as np
from imageutils import show_image

def analysis_all(matrix):
    # find similarity between images
    dot_product = np.dot(matrix.T, matrix)
    # find color intensity
    norms = np.linalg.norm(matrix, axis=0)
    norms = norms.reshape(-1, 1)
    # find normalized similarity measure
    cos_similarity = dot_product / (norms @ norms.T)
    cos_similarity = np.round(cos_similarity, 2)
    # print(f"cos_similarity:\n {cos_similarity}")
    return cos_similarity

# find similarities between two images
def analysis_pair(matrix):
    dot_product = []
    matrix = matrix.T
    if matrix.shape[0] % 2 == 0:
        for i in range (0, matrix.shape[0], 2):
            dot_product.append(np.dot(matrix[i], matrix[i+1]))
        dot_product = np.round(dot_product, 2)
        print(f"Dot product: {dot_product}")
    return None

  