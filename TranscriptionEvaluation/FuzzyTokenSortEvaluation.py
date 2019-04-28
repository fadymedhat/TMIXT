import numpy as np
from fuzzywuzzy import fuzz


class FuzzyTokenSortEvaluation(object):
    metric_list = []
    metric_map = {}

    def calculate(self, target_paragraph, predicted_paragraph):

        # strict comparison between characters
        document_accuracy = fuzz.token_sort_ratio(target_paragraph, predicted_paragraph)
        self.metric_list.append(document_accuracy)
        key = int(np.floor_divide(document_accuracy, 10))

        self.metric_map[key] = self.metric_map.get(key, 0) + 1
