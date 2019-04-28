import numpy as np



class LevenshteinNLTKEvaluation(object):

    metric_list = []
    metric_map = {}


    def calculate(self, target_paragraph, predicted_paragraph):

        from nltk.metrics.distance import (edit_distance, binary_distance,
                                           jaccard_distance, masi_distance,
                                           interval_distance, custom_distance,
                                           presence, fractional_presence)
        document_accuracy = edit_distance(target_paragraph, predicted_paragraph)
        document_accuracy=(1-document_accuracy)*100
        self.metric_list.append(document_accuracy)
        key = int(np.floor_divide(document_accuracy, 10))
        self.metric_map[key] = self.metric_map.get(key, 0) + 1