import numpy as np



class LevenshteinEvaluation(object):

    metric_list = []
    metric_map = {}

    def calculate_levenshtein(self, u, v):
        prev = None
        curr = [0] + range(1, len(v) + 1)
        # Operations: (SUB, DEL, INS)
        prev_ops = None
        curr_ops = [(0, 0, i) for i in range(len(v) + 1)]
        for x in xrange(1, len(u) + 1):
            prev, curr = curr, [x] + ([None] * len(v))
            prev_ops, curr_ops = curr_ops, [(0, x, 0)] + ([None] * len(v))
            for y in xrange(1, len(v) + 1):
                delcost = prev[y] + 1
                addcost = curr[y - 1] + 1
                subcost = prev[y - 1] + int(u[x - 1] != v[y - 1])
                curr[y] = min(subcost, delcost, addcost)
                if curr[y] == subcost:
                    (n_s, n_d, n_i) = prev_ops[y - 1]
                    curr_ops[y] = (n_s + int(u[x - 1] != v[y - 1]), n_d, n_i)
                elif curr[y] == delcost:
                    (n_s, n_d, n_i) = prev_ops[y]
                    curr_ops[y] = (n_s, n_d + 1, n_i)
                else:
                    (n_s, n_d, n_i) = curr_ops[y - 1]
                    curr_ops[y] = (n_s, n_d, n_i + 1)

        n_err, (n_sub, n_del, n_ins) = curr[len(v)], curr_ops[len(v)]

        #print '%s %d %d %d %d %d %d' % (name, n_err, n_sub, n_del, n_ins, len(target_paragraph), len(predicted_paragraph))
        document_accuracy = (1 - float(n_err) / max(len(u), len(v))) * 100
        return document_accuracy


    def calculate(self, target_paragraph, predicted_paragraph):
        document_accuracy = self.calculate_levenshtein(target_paragraph, predicted_paragraph)
        self.metric_list.append(document_accuracy)
        key = int(np.floor_divide(document_accuracy, 10))
        self.metric_map[key] = self.metric_map.get(key, 0) + 1