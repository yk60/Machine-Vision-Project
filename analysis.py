import matplotlib.pyplot as plt
import numpy as np

# find cos similarity between all possible pairs of images
def analysis_all(matrix):
    dot_product = np.dot(matrix.T, matrix)
    # find color intensity
    norms = np.linalg.norm(matrix, axis=0)
    norms = norms.reshape(-1, 1)
    # find normalized similarity measure
    cos_similarity = dot_product / (norms @ norms.T)
    cos_similarity = np.round(cos_similarity, 3)
    return cos_similarity

# find cos similarity between two vectorized images
def analysis_pair(img1, img2):
    if img1.shape == img2.shape:
        dot_product = np.dot(img1.flatten(), img2.flatten())
        cos_similarity = dot_product / (np.linalg.norm(img1) * np.linalg.norm(img2))
        return cos_similarity