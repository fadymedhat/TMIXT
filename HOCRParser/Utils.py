import math
import numpy as np
from scipy import spatial
from sklearn.metrics.pairwise import cosine_similarity


def cosine_similarity_custom( x, y):
    print(' x=', len(x), ' y=', len(y))
    if len(x) != 600:
        # for item in x,y:
        #     y[item]=y[item].encode("utf-8")
        #     x[item]=x[item].encode("utf-8")
        print(x, ' ', y)
    numerator = sum(a * b for a, b in zip(x, y))
    denominator = square_rooted(x) * square_rooted(y)
    return numerator / float(denominator)

def square_rooted( x):
        return round(math.sqrt(sum([a * a for a in x])), 3)

def cosine_similarity_sklearn(x, y):
    """

    :param x:
    :param y:
    :return:
    """

    result = cosine_similarity(np.array(x).reshape(1, -1), np.array(y).reshape(1, -1))
    return result[0][0]



def cosine_similarity_scipy( x, y):


    result = 1 - spatial.distance.cosine(x, y)
    return result


def softmax(x):
    e = np.exp(x - np.max(x))
    s = np.sum(e)
    return e / s